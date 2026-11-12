"""
Text-to-Speech (TTS) Provider Abstract Base Contract
Supports Azure Speech, ElevenLabs, Google Cloud TTS, AWS Polly, and offline mocks.
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class TTSResult:
    audio_path: Optional[str]
    duration_sec: float
    sample_rate: int
    provider: str
    voice_id: str
    status: str  # COMPLETED, NOT_CONFIGURED, FAILED
    error_message: Optional[str] = None

class TTSProvider(ABC):
    """Abstract base interface for speech synthesis."""

    @abstractmethod
    def generate_speech(self, text: str, target_lang: str, output_path: str, voice_id: Optional[str] = None) -> TTSResult:
        """Generates speech audio file from text."""
        pass

    @abstractmethod
    def estimate_duration(self, text: str, target_lang: str) -> float:
        """Estimates spoken duration in seconds before synthesis."""
        pass

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Checks if required API keys / client libraries exist."""
        pass

class MockTTSProvider(TTSProvider):
    """Mock provider for unit tests without network calls."""

    def generate_speech(self, text: str, target_lang: str, output_path: str, voice_id: Optional[str] = None) -> TTSResult:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        # Create a small valid silent WAV header or placeholder file
        with open(output_path, "wb") as f:
            f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00")
        
        duration = self.estimate_duration(text, target_lang)
        return TTSResult(
            audio_path=output_path,
            duration_sec=duration,
            sample_rate=16000,
            provider="MockTTSProvider",
            voice_id=voice_id or f"{target_lang}-MockVoice",
            status="COMPLETED"
        )

    def estimate_duration(self, text: str, target_lang: str) -> float:
        word_count = len(text.split())
        return max(0.5, round(word_count * 0.35, 2))

    def validate_credentials(self) -> bool:
        return True
