# This software is licensed under a **dual-license model**
# For individuals and businesses earning **under $1M per year**, this software is licensed under the **MIT License**
# Businesses or organizations with **annual revenue of $1,000,000 or more** must obtain permission to use this software commercially.

import time
import socket
import numpy as np
import pandas as pd
from threading import Event

from ns_utils.livelink_utils import FaceBlendShape, UDP_IP, UDP_PORT

ground_truth_path = r"./ns_utils/animation/default.csv"
columns_to_drop = [
    'TongueOut', 'HeadYaw', 'HeadPitch', 'HeadRoll',
    'LeftEyeYaw', 'LeftEyePitch', 'LeftEyeRoll',
    'RightEyeYaw', 'RightEyePitch', 'RightEyeRoll'
]

def load_default_animation(csv_path):
    data = pd.read_csv(csv_path)
    data = data.drop(columns=['Timecode', 'BlendshapeCount'] + columns_to_drop)
    return data.values

default_animation_data = load_default_animation(ground_truth_path)

def blend_animation(data, blend_frames=30):

    last_frames = data[-blend_frames:]
    first_frames = data[:blend_frames]

    blended_frames = np.zeros_like(last_frames)
    for i in range(blend_frames):
        alpha = i / blend_frames  # Linear blending factor
        blended_frames[i] = (1 - alpha) * last_frames[i] + alpha * first_frames[i]

    blended_data = np.vstack([data[:-blend_frames], blended_frames])
    return blended_data

blended_animation_data = blend_animation(default_animation_data, blend_frames=30)

stop_default_animation = Event()

def default_animation_loop(py_face):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((UDP_IP, UDP_PORT))
        while not stop_default_animation.is_set():
            for frame in blended_animation_data:
                # Check before processing each frame
                if stop_default_animation.is_set():
                    break

                # Apply the frame blendshapes
                for i, value in enumerate(frame):
                    py_face.set_blendshape(FaceBlendShape(i), float(value))
                
                # Send the frame
                try:
                    s.sendall(py_face.encode())
                except Exception as e:
                    print(f"Error in default animation sending: {e}")
                
                # Instead of one long sleep, break it into short chunks
                total_sleep = 1 / 60
                sleep_interval = 0.005  # check every 5ms
                while total_sleep > 0 and not stop_default_animation.is_set():
                    time.sleep(min(sleep_interval, total_sleep))
                    total_sleep -= sleep_interval

def play_full_animation(facial_data, fps, py_face, socket_connection, blend_in_frames, blend_out_frames):
    for blend_shape_data in facial_data[blend_in_frames:-blend_out_frames]:
        apply_blendshapes(blend_shape_data, 1.0, py_face)
        socket_connection.sendall(py_face.encode())
        time.sleep(1 / fps)

def apply_blendshapes(frame_data: np.ndarray, weight: float, py_face):
    for i in range(51):  # Apply the first 51 blendshapes (no neck at the moment)
        default_value = default_animation_data[0][i]
        facial_value = frame_data[i]
        blended_value = (1 - weight) * default_value + weight * facial_value
        py_face.set_blendshape(FaceBlendShape(i), float(blended_value))
'''
    # Handle new emotion dimensions (61 to 67)
    additional_values = frame_data[61:68]
    values_str = " ".join([f"{i+61}: {value:.2f}" for i, value in enumerate(additional_values)])
    print(f"Frame Values: {values_str}")

    # Determine the emotion with the highest value
    max_emotion_index = np.argmax(additional_values)
    emotions = ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]
    print(f"Highest emotion: {emotions[max_emotion_index]} with value: {additional_values[max_emotion_index]:.2f}")'''

def blend_in(facial_data, fps, py_face, encoded_data, blend_in_frames):
    for frame_index in range(blend_in_frames):
        weight = frame_index / blend_in_frames
        apply_blendshapes(facial_data[frame_index], weight, py_face)
        encoded_data.append(py_face.encode())
        time.sleep(1 / fps)

def blend_out(facial_data, fps, py_face, encoded_data, blend_out_frames):
    total_frames = len(facial_data)
    # If blend_out_frames is greater than available frames, adjust it.
    if blend_out_frames > total_frames:
        blend_out_frames = total_frames
    for frame_index in range(blend_out_frames):
        weight = frame_index / blend_out_frames
        reverse_index = total_frames - blend_out_frames + frame_index
        apply_blendshapes(facial_data[reverse_index], 1.0 - weight, py_face)
        encoded_data.append(py_face.encode())
        time.sleep(1 / fps)