import asyncio
import json
import websockets
import base64
import threading
import numpy as np
import sounddevice as sd
import keyboard  # For push-to-talk
from pydub import AudioSegment
import io

# WebSocket URL
WS_URL = "ws://localhost:8000/ws/convo"

# Expected sample rate and audio format
SAMPLE_RATE = 24000  
CHANNELS = 1
CHUNK_LENGTH_S = 0.05  # 50ms chunk size
BYTES_PER_SAMPLE = 2

# Audio control flags
allow_audio_playback = True  # Flag to allow/disallow playback
push_to_talk_key = "space"  # Change this key for PTT activation

# PCM16 Audio Processing
def decode_pcm16(audio_base64):
    """Decodes base64 PCM16 audio into raw PCM16 bytes."""
    try:
        audio_bytes = base64.b64decode(audio_base64)
        return np.frombuffer(audio_bytes, dtype=np.int16).tobytes()
    except Exception as e:
        print(f"❌ Error decoding PCM16 audio: {e}")
        return None

class AudioPlayerAsync:
    """Handles real-time audio playback using sounddevice."""
    
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.stream = sd.OutputStream(
            callback=self.callback,
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=np.int16,
            blocksize=int(CHUNK_LENGTH_S * SAMPLE_RATE),
        )
        self.playing = False

    def callback(self, outdata, frames, time, status):  
        if not allow_audio_playback:
            outdata.fill(0)  # Silence output if playback is disabled
            return

        with self.lock:
            data = np.empty(0, dtype=np.int16)

            while len(data) < frames and len(self.queue) > 0:
                item = self.queue.pop(0)
                frames_needed = frames - len(data)
                data = np.concatenate((data, item[:frames_needed]))
                if len(item) > frames_needed:
                    self.queue.insert(0, item[frames_needed:])

            if len(data) < frames:
                data = np.concatenate((data, np.zeros(frames - len(data), dtype=np.int16)))

        outdata[:] = data.reshape(-1, 1)

    def add_data(self, data: bytes):
        """Add PCM16 data to queue for playback."""
        with self.lock:
            np_data = np.frombuffer(data, dtype=np.int16)
            self.queue.append(np_data)
            if not self.playing:
                self.start()

    def start(self):
        """Start playback."""
        self.playing = True
        self.stream.start()

    def stop(self):
        """Stop playback and clear queue."""
        self.playing = False
        self.stream.stop()
        with self.lock:
            self.queue = []

    def clear_queue(self):
        """Clears all queued audio."""
        with self.lock:
            self.queue = []

    def terminate(self):
        """Terminate stream."""
        self.stream.close()

# Instantiate the audio player
audio_player = AudioPlayerAsync()

async def send_microphone_audio(ws):
    """Captures microphone audio and sends it to the WebSocket when PTT key is held."""
    print(f"🎤 Push-to-Talk enabled: Hold **{push_to_talk_key.upper()}** to speak...")
    
    read_size = int(SAMPLE_RATE * 0.1)  # 20ms buffer
    stream = sd.InputStream(channels=CHANNELS, samplerate=SAMPLE_RATE, dtype="int16")
    
    while True:
        if keyboard.is_pressed(push_to_talk_key):  # PTT active
            stream.start()
            print("🎙️ Recording... (Release key to stop)")

            while keyboard.is_pressed(push_to_talk_key):
                if stream.read_available < read_size:
                    await asyncio.sleep(0)
                    continue

                data, _ = stream.read(read_size)
                encoded_audio = base64.b64encode(data).decode("utf-8")
                await ws.send(json.dumps({"audio_bytes": encoded_audio}))

            print("🛑 Stopped recording.")

            stream.stop()

        await asyncio.sleep(0.1)  # Prevents CPU overload

async def websocket_client():
    """Handles WebSocket connection and real-time communication."""
    global allow_audio_playback

    try:
        async with websockets.connect(WS_URL) as ws:
            print("✅ Connected to Proxy WebSocket!")

            # Start microphone audio streaming (Push-to-Talk mode)
            asyncio.create_task(send_microphone_audio(ws))

            while True:
                try:
                    while True:
                        message = await ws.recv()

                        try:
                            response_json = json.loads(message)

                            # Handle speech.started (Stop and clear audio)
                            if response_json.get("type") == "speech.started":
                                print("🔇 Speech started: Stopping audio playback.")
                                allow_audio_playback = False
                                audio_player.clear_queue()

                            # Handle speech.ended (Resume playback)
                            elif response_json.get("type") == "speech.ended":
                                print("🔊 Speech ended: Allowing audio playback.")
                                allow_audio_playback = True

                            # Handle text transcript
                            elif response_json.get("type") == "response.audio_transcript.delta":
                                delta_text = response_json["delta"]
                                print(f"📝 Transcript: {delta_text}")

                            # Handle audio playback
                            elif response_json.get("type") == "response.audio.delta":
                                try:
                                    audio_bytes = decode_pcm16(response_json["delta"])
                                    if audio_bytes:
                                        print(f"🔊 Queued audio chunk of {len(audio_bytes)} bytes")
                                        audio_player.add_data(audio_bytes)
                                except Exception as e:
                                    print(f"❌ Error processing audio: {e}")

                            # Handle other messages
                            else:
                                print(f"ℹ️ Received JSON response: {response_json}")

                        except Exception as e:
                            print("❌ Error while parsing response:", e)                        

                except websockets.exceptions.ConnectionClosedOK:
                    print("🔌 WebSocket closed normally.")
                    break
                except websockets.exceptions.ConnectionClosedError as e:
                    print(f"❌ Unexpected WebSocket close: {e}")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
                    break

    except Exception as e:
        print(f"❌ Failed to connect to WebSocket: {e}")


# Run the WebSocket client
asyncio.run(websocket_client())

# Stop the audio playback gracefully
audio_player.terminate()
