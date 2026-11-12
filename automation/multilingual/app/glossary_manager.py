"""Terminology glossary enforcement and lookup."""
import os
import json
from typing import List, Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "terminology_glossary.json")

class GlossaryManager:
    def __init__(self, config_path: Optional[str] = None):
        p = config_path or CONFIG_PATH
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {"shielded_tokens": []}
        self.tokens = set(self.config.get("shielded_tokens", []))

    def is_protected_token(self, token: str) -> bool:
        return token in self.tokens

    def get_protected_tokens(self) -> List[str]:
        return list(self.tokens)

    def validate_preservation(self, original: str, translated: str) -> List[str]:
        """Checks if protected tokens present in original appear in translated text."""
        missing = []
        for t in self.tokens:
            if t in original and t not in translated:
                missing.append(t)
        return missing
