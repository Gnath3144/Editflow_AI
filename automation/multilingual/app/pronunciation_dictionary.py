"""Phonetic and SSML pronunciation overrides."""
from typing import Dict, Any

class PronunciationDictionary:
    def __init__(self):
        self.overrides = {
            "pydantic": "pie-dan-tic",
            "pytorch": "pie-torch",
            "ffmpeg": "eff-eff-em-peg",
            "nvenc": "en-venc",
            "vram": "vee-ram"
        }

    def apply_ssml_overrides(self, text: str) -> str:
        processed = text
        for term, phonetic in self.overrides.items():
            processed = processed.replace(term, phonetic)
        return processed
