from __future__ import annotations

from collections import deque
from timecode import Timecode
from statistics import mean
from typing import List
import datetime
import struct
import random
import uuid
from enum import Enum

class FaceBlendShape(Enum):
    EyeBlinkLeft = 0
    EyeLookDownLeft = 1
    EyeLookInLeft = 2
    EyeLookOutLeft = 3
    EyeLookUpLeft = 4
    EyeSquintLeft = 5
    EyeWideLeft = 6
    EyeBlinkRight = 7
    EyeLookDownRight = 8
    EyeLookInRight = 9
    EyeLookOutRight = 10
    EyeLookUpRight = 11
    EyeSquintRight = 12
    EyeWideRight = 13
    JawForward = 14
    JawLeft = 15
    JawRight = 16
    JawOpen = 17
    MouthClose = 18
    MouthFunnel = 19
    MouthPucker = 20
    MouthLeft = 21
    MouthRight = 22
    MouthSmileLeft = 23
    MouthSmileRight = 24
    MouthFrownLeft = 25
    MouthFrownRight = 26
    MouthDimpleLeft = 27
    MouthDimpleRight = 28
    MouthStretchLeft = 29
    MouthStretchRight = 30
    MouthRollLower = 31
    MouthRollUpper = 32
    MouthShrugLower = 33
    MouthShrugUpper = 34
    MouthPressLeft = 35
    MouthPressRight = 36
    MouthLowerDownLeft = 37
    MouthLowerDownRight = 38
    MouthUpperUpLeft = 39
    MouthUpperUpRight = 40
    BrowDownLeft = 41
    BrowDownRight = 42
    BrowInnerUp = 43
    BrowOuterUpLeft = 44
    BrowOuterUpRight = 45
    CheekPuff = 46
    CheekSquintLeft = 47
    CheekSquintRight = 48
    NoseSneerLeft = 49
    NoseSneerRight = 50
    TongueOut = 51
    HeadYaw = 52
    HeadPitch = 53
    HeadRoll = 54
    LeftEyeYaw = 55
    LeftEyePitch = 56
    LeftEyeRoll = 57
    RightEyeYaw = 58
    RightEyePitch = 59
    RightEyeRoll = 60
    Angry = 61
    Disgusted = 62
    Fearful = 63
    Happy = 64
    Neutral = 65
    Sad = 66
    Surprised = 67

# Group blendshapes into sections for scaling
MOUTH_BLENDSHAPES = [
    FaceBlendShape.JawForward, FaceBlendShape.JawLeft, FaceBlendShape.JawRight, FaceBlendShape.JawOpen,
    FaceBlendShape.MouthClose, FaceBlendShape.MouthFunnel, FaceBlendShape.MouthPucker,
    FaceBlendShape.MouthLeft, FaceBlendShape.MouthRight, FaceBlendShape.MouthSmileLeft,
    FaceBlendShape.MouthSmileRight, FaceBlendShape.MouthFrownLeft, FaceBlendShape.MouthFrownRight,
    FaceBlendShape.MouthDimpleLeft, FaceBlendShape.MouthDimpleRight, FaceBlendShape.MouthStretchLeft,
    FaceBlendShape.MouthStretchRight, FaceBlendShape.MouthRollLower, FaceBlendShape.MouthRollUpper,
    FaceBlendShape.MouthShrugLower, FaceBlendShape.MouthShrugUpper, FaceBlendShape.MouthPressLeft,
    FaceBlendShape.MouthPressRight, FaceBlendShape.MouthLowerDownLeft, FaceBlendShape.MouthLowerDownRight,
    FaceBlendShape.MouthUpperUpLeft, FaceBlendShape.MouthUpperUpRight
]

EYE_BLENDSHAPES = [
    FaceBlendShape.EyeBlinkLeft, FaceBlendShape.EyeLookDownLeft, FaceBlendShape.EyeLookInLeft,
    FaceBlendShape.EyeLookOutLeft, FaceBlendShape.EyeLookUpLeft, FaceBlendShape.EyeSquintLeft,
    FaceBlendShape.EyeWideLeft, FaceBlendShape.EyeBlinkRight, FaceBlendShape.EyeLookDownRight,
    FaceBlendShape.EyeLookInRight, FaceBlendShape.EyeLookOutRight, FaceBlendShape.EyeLookUpRight,
    FaceBlendShape.EyeSquintRight, FaceBlendShape.EyeWideRight
]

EYEBROW_BLENDSHAPES = [
    FaceBlendShape.BrowDownLeft, FaceBlendShape.BrowDownRight, FaceBlendShape.BrowInnerUp,
    FaceBlendShape.BrowOuterUpLeft, FaceBlendShape.BrowOuterUpRight
]

def scale_blendshapes_by_section(blendshapes: List[float], mouth_scale: float, eye_scale: float, eyebrow_scale: float, threshold: float = 0.0) -> List[float]:
    scaled_blendshapes = []
    for i, value in enumerate(blendshapes):
        if value > threshold:
            if i in [bs.value for bs in MOUTH_BLENDSHAPES]:
                scaled_value = value * mouth_scale
            elif i in [bs.value for bs in EYE_BLENDSHAPES]:
                scaled_value = value * eye_scale
            elif i in [bs.value for bs in EYEBROW_BLENDSHAPES]:
                scaled_value = value * eyebrow_scale
            else:
                scaled_value = value  # No scaling for unclassified blendshapes

            if scaled_value > 1.0:
                scaled_value = 1.0
            scaled_blendshapes.append(max(scaled_value, 0.0))
        else:
            scaled_blendshapes.append(max(value, 0.0))
    return scaled_blendshapes

class PyLiveLinkFace:
    def __init__(self, name: str = "face1", uuid_str: str = str(uuid.uuid1()), fps: int = 60, filter_size: int = 0) -> None:
        # Ensure the uuid is properly formatted
        self.uuid = f"${uuid_str}" if not uuid_str.startswith("$") else uuid_str
        self.name = name
        self.fps = fps
        self._filter_size = filter_size
        self._version = 6

        self._scaling_factor_mouth = 1.1
        self._scaling_factor_eyes = 1.0
        self._scaling_factor_eyebrows = 0.4

        now = datetime.datetime.now()
        timcode = Timecode(self.fps, f'{now.hour}:{now.minute}:{now.second}:{now.microsecond * 0.001}')
        self._frames = timcode.frames
        self._sub_frame = 1056060032
        self._denominator = int(self.fps / 60)
        # Allocate enough space for all blendshapes as defined in the enum.
        NUM_BLENDSHAPES = len(FaceBlendShape)
        self._blend_shapes = [0.0] * NUM_BLENDSHAPES
        self._old_blend_shapes = [deque([0.0], maxlen=filter_size) for _ in range(NUM_BLENDSHAPES)]

    def encode(self) -> bytes:
        version_packed = struct.pack('<I', self._version)
        uuid_packed = self.uuid.encode('utf-8')
        name_packed = self.name.encode('utf-8')
        name_length_packed = struct.pack('!i', len(self.name))
        now = datetime.datetime.now()
        timcode = Timecode(self.fps, f'{now.hour}:{now.minute}:{now.second}:{now.microsecond * 0.001}')
        frames_packed = struct.pack("!II", timcode.frames, self._sub_frame)
        frame_rate_packed = struct.pack("!II", self.fps, self._denominator)
    
        # Scale only a subset (for example, the first 61) if necessary.
        # Here we pack the first 61 blendshapes.
        scaled_blend_shapes = scale_blendshapes_by_section(
            self._blend_shapes, 
            self._scaling_factor_mouth, 
            self._scaling_factor_eyes, 
            self._scaling_factor_eyebrows
        )
        data_packed = struct.pack('!B61f', 61, *scaled_blend_shapes[:61])
        return version_packed + uuid_packed + name_length_packed + name_packed + frames_packed + frame_rate_packed + data_packed

    def set_blendshape(self, index: FaceBlendShape, value: float, no_filter: bool = True) -> None:
        # Clamp head rotations if needed.
        if index in [FaceBlendShape.HeadYaw, FaceBlendShape.HeadPitch, FaceBlendShape.HeadRoll]:
            value = max(min(value, 0.00), -0.00)
        if no_filter:
            self._blend_shapes[index.value] = value
        else:
            self._old_blend_shapes[index.value].append(value)
            self._blend_shapes[index.value] = mean(self._old_blend_shapes[index.value])

    def set_scaling_factor_mouth(self, scaling_factor: float) -> None:
        self._scaling_factor_mouth = scaling_factor

    def set_scaling_factor_eyes(self, scaling_factor: float) -> None:
        self._scaling_factor_eyes = scaling_factor

    def set_scaling_factor_eyebrows(self, scaling_factor: float) -> None:
        self._scaling_factor_eyebrows = scaling_factor

    def random_blink_intervals(self, duration: float = 60, min_interval: float = 1.0, max_interval: float = 5.0) -> List[float]:
        intervals = []
        current_time = 0.0
        while current_time < duration:
            blink_interval = random.uniform(min_interval, max_interval)
            intervals.append(current_time + blink_interval)
            current_time += blink_interval
        return intervals
