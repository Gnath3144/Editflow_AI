"""Syllable and mora rate measurement."""
import re

class SpeechRateAnalyzer:
    def count_syllables_english(self, text: str) -> int:
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        total = 0
        for w in words:
            # Count vowel groups
            vowels = len(re.findall(r"[aeiouy]+", w))
            if w.endswith("e") and not w.endswith("le") and len(w) > 2:
                vowels = max(1, vowels - 1)
            total += max(1, vowels)
        return total

    def calculate_rate(self, text: str, duration_sec: float, language: str = "en") -> float:
        if duration_sec <= 0:
            return 0.0
        syllables = self.count_syllables_english(text)
        return round(syllables / duration_sec, 2)
