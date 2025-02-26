import base64
import logging
import numpy as np
import requests
import json
import config

import base64
import io
import numpy as np
from pydub import AudioSegment

AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"

def decode_to_mp3(audio_base64: str, 
                  input_sample_rate: int = 24000, 
                  output_sample_rate: int = 44100, 
                  channels: int = 1, 
                  bitrate: str = "128k") -> bytes:
    """
    Decodes a base64-encoded PCM16 audio string, converts it to MP3 format with
    the specified output sample rate and bitrate, and returns the MP3 bytes.
    
    Args:
        audio_base64 (str): Base64-encoded PCM16 audio.
        input_sample_rate (int): Sample rate of the incoming PCM16 audio (default: 24000 Hz).
        output_sample_rate (int): Desired MP3 sample rate (default: 88200 Hz).
        channels (int): Number of audio channels (default: 1).
        bitrate (str): MP3 bitrate (default: "128k").
    
    Returns:
        bytes: The converted MP3 audio bytes, or None if conversion fails.
    """
    try:
        # Decode the base64 PCM16 audio into raw bytes.
        raw_audio_bytes = base64.b64decode(audio_base64)
        
        # Create an AudioSegment from the raw PCM16 bytes.
        audio_segment = AudioSegment(
            data=raw_audio_bytes,
            sample_width=2,          # 16-bit PCM = 2 bytes per sample
            frame_rate=input_sample_rate,
            channels=channels
        )
        
        # Resample the audio to the desired output sample rate.
        audio_segment = audio_segment.set_frame_rate(output_sample_rate)
        
        # Export the audio segment as MP3.
        buffer = io.BytesIO()
        audio_segment.export(buffer, format="mp3", bitrate=bitrate)
        return buffer.getvalue()
    except Exception as e:
        logging.error("Conversion to MP3 failed: %s", e)
        return None

def post_audio_bytes(audio_bytes, url, headers):
    headers["Content-Type"] = "application/octet-stream"
    response = requests.post(url, headers=headers, data=audio_bytes)
    return response

def parse_blendshapes_from_json(json_response):
    blendshapes = json_response.get("blendshapes", [])
    facial_data = []

    for frame in blendshapes:
        frame_data = [float(value) for value in frame]
        facial_data.append(frame_data)

    return facial_data

def send_audio_to_neurosync(audio_bytes, use_local=True):
    try:
        # Use the local or remote URL depending on the flag
        url = config.LOCAL_URL if use_local else config.REMOTE_URL
        headers = {}
        if not use_local:
            headers["API-Key"] = config.API_KEY

        response = post_audio_bytes(audio_bytes, url, headers)
        response.raise_for_status()  
        json_response = response.json()
        return parse_blendshapes_from_json(json_response)

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None