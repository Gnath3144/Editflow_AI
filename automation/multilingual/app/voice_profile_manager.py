"""Voice archetype and provider voice mapping."""
import os
import json
from typing import Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "voice_profiles.json")

class VoiceProfileManager:
    def __init__(self, config_path: Optional[str] = None):
        p = config_path or CONFIG_PATH
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {"profiles": {}}

    def get_voice_for_locale(self, locale: str) -> Optional[Dict[str, Any]]:
        return self.config.get("profiles", {}).get(locale)
