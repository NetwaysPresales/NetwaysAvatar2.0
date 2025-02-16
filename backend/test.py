import asyncio
import json
import websockets
import base64
import simpleaudio as sa
import queue
import threading

# WebSocket URL
WS_URL = "ws://localhost:8000/ws"

# Accumulate transcript text
transcript = ""

# Queue for audio chunks
audio_queue = queue.Queue()

# Expected sample rate (ensure this matches the received audio's sample rate)
EXPECTED_SAMPLE_RATE = 24000  # Common for AI-generated speech

def audio_player():
    """Continuously plays audio chunks from the queue in order."""
    while True:
        audio_bytes = audio_queue.get()  # Get the next chunk (blocks if empty)
        if audio_bytes is None:  # Stop signal
            break
        try:
            wave_obj = sa.WaveObject(audio_bytes, num_channels=1, bytes_per_sample=2, sample_rate=EXPECTED_SAMPLE_RATE)
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Ensures sequential playback
        except Exception as e:
            print(f"❌ Error playing audio: {e}")

# Start the audio playback thread
audio_thread = threading.Thread(target=audio_player, daemon=True)
audio_thread.start()

async def test_proxy():
    global transcript

    try:
        async with websockets.connect(WS_URL) as ws:
            print("✅ Connected to Proxy WebSocket!")

            while True:
                try:
                    message = await ws.recv()

                    # Try parsing the message as JSON
                    try:
                        response_json = json.loads(message)

                        # Process text delta
                        if response_json.get("type") == "text":
                            delta_text = response_json["content"]
                            transcript += delta_text
                            print(f"📝 Transcript: {transcript}")

                        # Handle unexpected JSON types
                        else:
                            print(f"ℹ️ Received JSON response: {response_json}")

                    except json.JSONDecodeError:
                        # If JSON decoding fails, assume it's an audio chunk
                        try:
                            audio_bytes = base64.b64decode(message)
                            print(f"🔊 Queued audio chunk of {len(audio_bytes)} bytes")
                            audio_queue.put(audio_bytes)  # Add to queue
                        except Exception as e:
                            print(f"❌ Error decoding audio: {e}")

                except websockets.exceptions.ConnectionClosed:
                    print("❌ WebSocket connection closed.")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
                    break
    except Exception as e:
        print(f"❌ Failed to connect to WebSocket: {e}")

# Run the test
asyncio.run(test_proxy())

# Stop the audio playback thread gracefully
audio_queue.put(None)
audio_thread.join()
