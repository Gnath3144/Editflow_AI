"""Code shielding and text preprocessing for translation."""
import re
from typing import Tuple, Dict, List

class TranscriptNormalizer:
    def __init__(self):
        self.code_block_pattern = re.compile(r"```[\s\S]*?```")
        self.inline_code_pattern = re.compile(r"`[^`]+`")
        self.url_pattern = re.compile(r"https?://[^\s]+")
        self.cli_flag_pattern = re.compile(r"\s(--?[a-zA-Z0-9_-]+)\b")

    def shield_text(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Replaces code and sensitive syntax with [[SHIELD_N]] tokens."""
        shields = {}
        counter = 0

        def replacer(match):
            nonlocal counter
            token = f"[[SHIELD_{counter}]]"
            shields[token] = match.group(0)
            counter += 1
            return token

        # Shield code blocks first
        shielded = self.code_block_pattern.sub(replacer, text)
        # Shield inline code
        shielded = self.inline_code_pattern.sub(replacer, shielded)
        # Shield URLs
        shielded = self.url_pattern.sub(replacer, shielded)
        return shielded, shields

    def unshield_text(self, text: str, shields: Dict[str, str]) -> str:
        """Restores original code tokens into translated text."""
        unshielded = text
        for token, original in shields.items():
            unshielded = unshielded.replace(token, original)
        return unshielded
