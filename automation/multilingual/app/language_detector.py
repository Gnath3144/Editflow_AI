"""Language verification and profile registry."""
import os
import json
from typing import Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "languages.json")

class LanguageDetector:
    def __init__(self, config_path: Optional[str] = None):
        p = config_path or CONFIG_PATH
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                self.languages = json.load(f)
        else:
            self.languages = {}

    def is_supported(self, locale: str) -> bool:
        return locale in self.languages

    def get_profile(self, locale: str) -> Optional[Dict[str, Any]]:
        return self.languages.get(locale)

    def list_supported_locales(self) -> list:
        return list(self.languages.keys())
