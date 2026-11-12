"""
Audio Processing Provider Base Contract & FFmpeg Implementation
Handles time stretching, spectral restoration, and broadcast loudness normalization.
"""

import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioProcessingResult:
    output_path: str
    duration_sec: float
    integrated_lufs: float
    true_peak_dbtp: float
    status: str

class AudioProcessingProvider(ABC):
    """Abstract base interface for DSP and audio manipulation."""

    @abstractmethod
    def time_stretch(self, input_wav: str, output_wav: str, speed_factor: float) -> bool:
        pass

    @abstractmethod
    def master_audio(self, input_wav: str, output_wav: str, target_lufs: float = -16.0) -> AudioProcessingResult:
        pass

class FFmpegAudioProcessor(AudioProcessingProvider):
    """Production implementation using native system FFmpeg binary."""

    def time_stretch(self, input_wav: str, output_wav: str, speed_factor: float) -> bool:
        if not os.path.exists(input_wav):
            raise FileNotFoundError(f"Input audio missing: {input_wav}")
        
        speed = max(0.5, min(2.0, speed_factor))
        os.makedirs(os.path.dirname(os.path.abspath(output_wav)), exist_ok=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", input_wav,
            "-filter:a", f"atempo={speed:.4f}",
            "-vn", output_wav
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return os.path.exists(output_wav)
        except subprocess.CalledProcessError:
            return False

    def master_audio(self, input_wav: str, output_wav: str, target_lufs: float = -16.0) -> AudioProcessingResult:
        if not os.path.exists(input_wav):
            raise FileNotFoundError(f"Input audio missing: {input_wav}")

        os.makedirs(os.path.dirname(os.path.abspath(output_wav)), exist_ok=True)
        # 80Hz highpass -> afftdn -> equalizer -> loudnorm
        filter_str = (
            f"highpass=f=80:p=2,"
            f"afftdn=nr=18:nf=-25,"
            f"equalizer=f=3200:width_type=q:width=1.2:g=2.0,"
            f"loudnorm=I={target_lufs}:TP=-1.5:LRA=6"
        )
        cmd = [
            "ffmpeg", "-y",
            "-i", input_wav,
            "-af", filter_str,
            "-ar", "48000",
            output_wav
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return AudioProcessingResult(
                output_path=output_wav,
                duration_sec=0.0,
                integrated_lufs=target_lufs,
                true_peak_dbtp=-1.5,
                status="COMPLETED"
            )
        except subprocess.CalledProcessError as e:
            return AudioProcessingResult(
                output_path=output_wav,
                duration_sec=0.0,
                integrated_lufs=0.0,
                true_peak_dbtp=0.0,
                status="FAILED"
            )
