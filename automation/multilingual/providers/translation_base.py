"""
Translation Provider Abstract Base Contract
Supports Azure Translator, OpenAI, DeepL, Google Cloud Translate, and offline mocks.
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class TranslationResult:
    text: str
    source_lang: str
    target_lang: str
    provider: str
    status: str  # COMPLETED, NOT_CONFIGURED, FAILED
    error_message: Optional[str] = None

class TranslationProvider(ABC):
    """Abstract base interface for translation backends."""

    @abstractmethod
    def translate_text(self, text: str, target_lang: str, source_lang: str = "en") -> TranslationResult:
        """Translates a single text string into the target language."""
        pass

    @abstractmethod
    def translate_segments(self, segments: List[Dict[str, Any]], target_lang: str) -> List[TranslationResult]:
        """Translates a list of segment dictionaries."""
        pass

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Checks if provider credentials are set and valid."""
        pass

class MockTranslationProvider(TranslationProvider):
    """Mock provider for unit tests and local simulation."""

    def __init__(self, prefix: str = "[TRANSLATED]"):
        self.prefix = prefix

    def translate_text(self, text: str, target_lang: str, source_lang: str = "en") -> TranslationResult:
        return TranslationResult(
            text=f"{self.prefix} ({target_lang}) {text}",
            source_lang=source_lang,
            target_lang=target_lang,
            provider="MockTranslationProvider",
            status="COMPLETED"
        )

    def translate_segments(self, segments: List[Dict[str, Any]], target_lang: str) -> List[TranslationResult]:
        return [self.translate_text(s.get("text", ""), target_lang) for s in segments]

    def validate_credentials(self) -> bool:
        return True
