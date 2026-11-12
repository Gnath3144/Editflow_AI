"""Target language timing adaptation."""
import os
import json
from typing import Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "languages.json")

class LanguageSpecificPacing:
    def __init__(self, config_path: Optional[str] = None):
        p = config_path or CONFIG_PATH
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                self.languages = json.load(f)
        else:
            self.languages = {}

    def get_target_rate(self, locale: str) -> float:
        profile = self.languages.get(locale, {})
        return profile.get("voice_requirements", {}).get("target_syllable_rate", 5.0)
