import asyncio
import json
import base64
import threading
import time
import numpy as np
import sounddevice as sd
import keyboard
import websockets
from queue import Queue

from ns_utils.livelink_utils import create_socket_connection, initialize_py_face, FaceBlendShape
from ns_utils.audio_workers import audio_queue_worker

# --------------------------------------------------------------------
# WebSocket and Audio Settings
# --------------------------------------------------------------------
WS_URL = "ws://localhost:8000/ws/convo"
SAMPLE_RATE = 24000      # OpenAI sends 24 kHz PCM16 audio
CHANNELS = 1
CHUNK_LENGTH_S = 0.05    # 50ms chunks
push_to_talk_key = "space"

# Global flag for audio playback control
allow_audio_playback = True

# --------------------------------------------------------------------
# PCM16 Decoder
# --------------------------------------------------------------------
def decode_pcm16(audio_base64: str) -> bytes:
    """
    Decode a base64-encoded PCM16 audio string into raw PCM16 bytes.
    If the decoded length is not even, trim the last byte.
    """
    try:
        audio_bytes = base64.b64decode(audio_base64)
        if len(audio_bytes) % 2 != 0:
            audio_bytes = audio_bytes[:-1]
        return np.frombuffer(audio_bytes, dtype=np.int16).tobytes()
    except Exception as e:
        print(f"❌ Error decoding PCM16 audio: {e}")
        return None

# --------------------------------------------------------------------
# Initialization of Audio Worker Components
# --------------------------------------------------------------------
# Initialize the face and socket connection.
py_face = initialize_py_face()
socket_connection = create_socket_connection()

# Create a threading.Queue for audio items.
audio_queue = Queue()

# Start the default animation thread and store it in a mutable container.
from threading import Thread
from ns_utils.animation_utils import default_animation_loop
default_animation_thread = Thread(target=default_animation_loop, args=(py_face,))
default_animation_thread.start()
default_animation_thread_container = [default_animation_thread]

# Start the audio queue worker (ensuring sequential processing).
worker_thread = Thread(
    target=audio_queue_worker, 
    args=(audio_queue, py_face, socket_connection, default_animation_thread_container)
)
worker_thread.start()

# --------------------------------------------------------------------
# Microphone Audio Sending (Push-To-Talk)
# --------------------------------------------------------------------
async def send_microphone_audio(ws):
    """Capture microphone audio and send it over the WebSocket."""
    print(f"Push-to-Talk enabled: Hold {push_to_talk_key.upper()} to speak...")
    read_size = int(SAMPLE_RATE * 0.1)  # 100ms buffer
    stream = sd.InputStream(channels=CHANNELS, samplerate=SAMPLE_RATE, dtype="int16")
    while True:
        if keyboard.is_pressed(push_to_talk_key):
            stream.start()
            print("Recording... (Release key to stop)")
            while keyboard.is_pressed(push_to_talk_key):
                if stream.read_available < read_size:
                    await asyncio.sleep(0)
                    continue
                data, _ = stream.read(read_size)
                encoded_audio = base64.b64encode(data).decode("utf-8")
                await ws.send(json.dumps({"audio_bytes": encoded_audio}))
            print("Stopped recording.")
            stream.stop()
        else:
            silent_data = np.zeros(read_size, dtype=np.int16).tobytes()
            encoded_silent_audio = base64.b64encode(silent_data).decode("utf-8")
            await ws.send(json.dumps({"audio_bytes": encoded_silent_audio}))
        await asyncio.sleep(0.1)

# --------------------------------------------------------------------
# WebSocket Client
# --------------------------------------------------------------------
async def websocket_client():
    """
    Connects to the WebSocket and processes incoming messages.
    For 'response.audio.delta.neurosync' messages, the payload must contain:
      - "audio_delta": a base64-encoded PCM16 audio string (24 kHz)
      - "blendshapes": a list of blendshape frames (each frame a list of floats)
    The client decodes the audio, computes its duration, and enqueues the item.
    """
    global allow_audio_playback
    try:
        async with websockets.connect(WS_URL) as ws:
            print("Connected to WebSocket!")
            asyncio.create_task(send_microphone_audio(ws))
            while True:
                try:
                    message = await ws.recv()
                    response_json = json.loads(message)
                    msg_type = response_json.get("type")
                    match msg_type:
                        case "input_audio_buffer.speech_started":
                            print("Speech started: Stopping audio playback.")
                            allow_audio_playback = False
                        case "input_audio_buffer.speech_stopped":
                            print("Speech ended: Allowing audio playback.")
                            allow_audio_playback = True
                        case "response.audio_transcript.delta":
                            delta_text = response_json.get("delta")
                            # Process transcript updates if needed.
                        case "response.audio.delta.neurosync":
                            # Expect payload with base64-encoded PCM16 audio and blendshape frames.
                            encoded_audio = response_json.get("audio_delta")
                            blendshapes = response_json.get("blendshapes")
                            if encoded_audio and blendshapes:
                                raw_audio = decode_pcm16(encoded_audio)
                                if raw_audio:
                                    # Compute duration for mono PCM16: (len(raw_audio)/2) / SAMPLE_RATE.
                                    duration = (len(raw_audio) / 2) / SAMPLE_RATE
                                    # Enqueue the audio and blendshape data.
                                    audio_queue.put((raw_audio, blendshapes, duration))
                                    print("Queued neurosync audio and blendshapes.")
                                else:
                                    print("Failed to decode audio.")
                            else:
                                print("Missing audio or blendshapes in payload.")
                        case "response.audio.delta":
                            # For standard audio playback (without blendshape sync)
                            encoded_audio = response_json.get("delta")
                            if encoded_audio:
                                raw_audio = decode_pcm16(encoded_audio)
                                if raw_audio:
                                    # (Optional) You could play standard audio directly here.
                                    print("Standard audio playback not handled by new worker.")
                                else:
                                    print("Failed to decode PCM16 audio.")
                        case "rate_limits.updated":
                            print("Updated rate limits:", response_json)
                        case _:
                            print(f"Received unknown message type: {msg_type}")
                except websockets.exceptions.ConnectionClosedOK:
                    print("WebSocket closed normally.")
                    break
                except websockets.exceptions.ConnectionClosedError as e:
                    print(f"Unexpected WebSocket close: {e}")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break
    except Exception as e:
        print(f"Failed to connect to WebSocket: {e}")

# --------------------------------------------------------------------
# Main Execution
# --------------------------------------------------------------------
asyncio.run(websocket_client())
