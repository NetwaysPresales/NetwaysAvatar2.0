import io
import time
import pygame
import wave
from threading import Event, Lock, Thread
from ns_utils.livelink_utils import initialize_py_face
from ns_utils.send_to_unreal import send_pre_encoded_data_to_unreal, pre_encode_facial_data
from ns_utils.animation_utils import stop_default_animation, default_animation_loop

queue_lock = Lock()

def wrap_pcm16_to_wav(raw_pcm16_bytes, sample_rate=24000, channels=1, sample_width=2):
    """
    Wrap raw PCM16 data in a WAV header.
    
    Args:
        raw_pcm16_bytes (bytes): Raw PCM16 audio data.
        sample_rate (int): Sample rate (default 24000 Hz).
        channels (int): Number of channels (default 1).
        sample_width (int): Bytes per sample (default 2 for 16-bit audio).
        
    Returns:
        bytes: A valid WAV file as bytes.
    """
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(raw_pcm16_bytes)
    buffer.seek(0)
    return buffer.read()

def play_audio_from_memory(audio_data, start_event):
    try:
        pygame.mixer.init()  # Optionally, specify a buffer size here.
        # Wrap the raw PCM16 audio in a WAV header.
        wav_audio = wrap_pcm16_to_wav(audio_data, sample_rate=24000, channels=1, sample_width=2)
        audio_file = io.BytesIO(wav_audio)
        pygame.mixer.music.load(audio_file)
        
        # Wait until the start event is triggered, then play the audio.
        start_event.wait()
        pygame.mixer.music.play()
        
        clock = pygame.time.Clock()
        # Tick the clock to allow pygame to update playback status.
        while pygame.mixer.music.get_busy():
            clock.tick(60)
    except pygame.error as e:
        print(f"Error in play_audio_from_memory: {e}")

def run_audio_animation_from_bytes(audio_bytes, generated_facial_data, duration, py_face, socket_connection, default_animation_thread_container):
    """
    Processes one audio item (audio_bytes, generated_facial_data) as follows:
      1. Stops the default animation by setting stop_default_animation and joining the current default thread.
      2. Starts two threads: one for audio playback and one for sending pre‑encoded facial data.
      3. Waits for both threads to finish.
      4. Restarts the default animation and updates the mutable container.
    """
    # Create a temporary instance for encoding blend-in/out facial data.
    encoding_face = initialize_py_face()
    encoded_facial_data = pre_encode_facial_data(generated_facial_data, encoding_face)

    with queue_lock:
        stop_default_animation.set()
        if default_animation_thread_container[0] and default_animation_thread_container[0].is_alive():
            default_animation_thread_container[0].join()

    start_event = Event()

    audio_thread = Thread(target=play_audio_from_memory, args=(audio_bytes, start_event))
    data_thread = Thread(target=send_pre_encoded_data_to_unreal, args=(encoded_facial_data, start_event, duration, socket_connection))

    audio_thread.start()
    data_thread.start()

    start_event.set()

    audio_thread.join()
    data_thread.join()

    with queue_lock:
        stop_default_animation.clear()
        default_animation_thread_container[0] = Thread(target=default_animation_loop, args=(py_face,))
        default_animation_thread_container[0].start()

def audio_queue_worker(audio_queue, py_face, socket_connection, default_animation_thread_container):
    """
    Processes audio items from audio_queue sequentially.
    Each item is a tuple (audio_bytes, facial_data) that is played back with synchronized facial animation.
    """
    while True:
        item = audio_queue.get()
        if item is None:
            break
        audio_bytes, facial_data, duration = item
        run_audio_animation_from_bytes(audio_bytes, facial_data, duration, py_face, socket_connection, default_animation_thread_container)
        audio_queue.task_done()
