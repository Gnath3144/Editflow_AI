"""
Codealytica Multilingual Providers Package
Abstract provider contracts and implementations for Translation, TTS, DSP, and YouTube.
"""

from .translation_base import TranslationProvider, TranslationResult, MockTranslationProvider
from .tts_base import TTSProvider, TTSResult, MockTTSProvider
from .audio_processing_base import AudioProcessingProvider, AudioProcessingResult, FFmpegAudioProcessor
from .youtube_base import YouTubePublisherBase, YouTubeTrackInfo, ManualPackageResult

__all__ = [
    "TranslationProvider",
    "TranslationResult",
    "MockTranslationProvider",
    "TTSProvider",
    "TTSResult",
    "MockTTSProvider",
    "AudioProcessingProvider",
    "AudioProcessingResult",
    "FFmpegAudioProcessor",
    "YouTubePublisherBase",
    "YouTubeTrackInfo",
    "ManualPackageResult"
]
