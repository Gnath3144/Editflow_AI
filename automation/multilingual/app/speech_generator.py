"""TTS speech generation with provider integration."""
from typing import Optional
from ..providers.tts_base import TTSProvider, TTSResult, MockTTSProvider
from .voice_profile_manager import VoiceProfileManager

class SpeechGenerator:
    def __init__(self, provider: Optional[TTSProvider] = None):
        self.provider = provider or MockTTSProvider()
        self.voice_mgr = VoiceProfileManager()

    def synthesize(self, text: str, locale: str, output_path: str) -> TTSResult:
        voice_info = self.voice_mgr.get_voice_for_locale(locale)
        voice_id = voice_info.get("provider_voice_id") if voice_info else None
        return self.provider.generate_speech(text, locale, output_path, voice_id=voice_id)
