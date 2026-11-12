"""Translation execution with provider fallback."""
from typing import List, Dict, Any, Optional
from ..providers.translation_base import TranslationProvider, TranslationResult, MockTranslationProvider
from .transcript_normalizer import TranscriptNormalizer

class TranslationEngine:
    def __init__(self, provider: Optional[TranslationProvider] = None):
        self.provider = provider or MockTranslationProvider()
        self.normalizer = TranscriptNormalizer()

    def translate_segment(self, text: str, target_lang: str) -> TranslationResult:
        # Shield code
        shielded, shields = self.normalizer.shield_text(text)
        res = self.provider.translate_text(shielded, target_lang)
        if res.status == "COMPLETED":
            restored = self.normalizer.unshield_text(res.text, shields)
            res.text = restored
        return res

    def translate_all_segments(self, segments: List[Dict[str, Any]], target_lang: str) -> List[Dict[str, Any]]:
        translated = []
        for s in segments:
            res = self.translate_segment(s.get("text", ""), target_lang)
            translated.append({
                **s,
                "translated_text": res.text,
                "translation_status": res.status,
                "provider": res.provider
            })
        return translated
