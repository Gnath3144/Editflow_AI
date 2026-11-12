"""
Repetition & Restart Detection Engine
Identifies:
- Exact word/phrase repetitions (stutters)
- Sentence false starts and self-corrections
- Redundant looping definitions while preserving deliberate pedagogical reinforcement
"""

import os
import json
import re
from typing import List, Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "configuration", "repetition_rules.json")

class RepetitionEngine:
    def __init__(self, config_path: Optional[str] = None):
        path = config_path or CONFIG_PATH
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "exact_repetition": {"enabled": True, "max_intervening_silence_sec": 1.5},
                "near_repetition": {"enabled": True, "similarity_threshold": 0.85, "max_window_sec": 8.0}
            }

    def _normalize(self, text: str) -> str:
        return re.sub(r"[^\w\s]", "", text).lower().strip()

    def detect_exact_repetitions(self, words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detects immediate 1-word and 2-word exact repetitions (stutters)
        e.g., 'we will we will' -> keep final 'we will'
        """
        decisions = []
        n = len(words)
        if n < 2:
            return decisions

        i = 0
        while i < n - 1:
            w1 = self._normalize(words[i].get("word", ""))
            w2 = self._normalize(words[i+1].get("word", ""))
            
            # Single word repetition
            if w1 and w1 == w2 and (words[i+1].get("start", 0) - words[i].get("end", 0)) < 1.2:
                decisions.append({
                    "decision_id": f"DEC-REP-{i:05d}",
                    "start_time": round(words[i].get("start", 0.0), 3),
                    "end_time": round(words[i].get("end", 0.0), 3),
                    "duration": round(words[i].get("end", 0.0) - words[i].get("start", 0.0), 3),
                    "action": "REMOVE",
                    "category": "Exact Word Stutter",
                    "confidence": 0.92,
                    "rule_reference": "REPETITION_REMOVAL_STANDARD:SEC_1",
                    "semantic_impact": f"Remove stuttered prefix word '{w1}'; retain clean subsequent delivery.",
                    "crossfade_ms": 12.0
                })
                i += 2
                continue

            # Two-word phrase repetition
            if i < n - 3:
                phrase1 = f"{w1} {self._normalize(words[i+1].get('word', ''))}"
                phrase2 = f"{self._normalize(words[i+2].get('word', ''))} {self._normalize(words[i+3].get('word', ''))}"
                if phrase1 and phrase1 == phrase2 and (words[i+2].get("start", 0) - words[i+1].get("end", 0)) < 1.5:
                    decisions.append({
                        "decision_id": f"DEC-REP-{i:05d}",
                        "start_time": round(words[i].get("start", 0.0), 3),
                        "end_time": round(words[i+1].get("end", 0.0), 3),
                        "duration": round(words[i+1].get("end", 0.0) - words[i].get("start", 0.0), 3),
                        "action": "REMOVE",
                        "category": "Exact Phrase Stutter",
                        "confidence": 0.90,
                        "rule_reference": "REPETITION_REMOVAL_STANDARD:SEC_1",
                        "semantic_impact": f"Remove repeated prefix phrase '{phrase1}'; retain final clean phrase.",
                        "crossfade_ms": 12.0
                    })
                    i += 4
                    continue

            i += 1
        return decisions

    def detect_false_starts(self, sentences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifies incomplete aborted sentence fragments immediately followed by a restart.
        """
        decisions = []
        for i in range(len(sentences) - 1):
            curr_s = sentences[i]
            next_s = sentences[i+1]
            text = curr_s.get("text", "").strip()
            
            # Pattern: sentence ending in trailing dash or short fragmented restart
            if text.endswith("-") or (len(text.split()) <= 3 and (next_s.get("start", 0) - curr_s.get("end", 0)) < 1.0):
                # Check if next sentence begins with similar subject
                curr_words = [self._normalize(w) for w in text.split()]
                next_words = [self._normalize(w) for w in next_s.get("text", "").split()]
                if curr_words and next_words and curr_words[0] == next_words[0]:
                    decisions.append({
                        "decision_id": f"DEC-FST-{i:05d}",
                        "start_time": round(curr_s.get("start", 0.0), 3),
                        "end_time": round(curr_s.get("end", 0.0), 3),
                        "duration": round(curr_s.get("end", 0.0) - curr_s.get("start", 0.0), 3),
                        "action": "REMOVE",
                        "category": "False Start Sentence Stumble",
                        "confidence": 0.86,
                        "rule_reference": "REPETITION_REMOVAL_STANDARD:SEC_1",
                        "semantic_impact": f"Eliminate aborted false start '{text}' in favor of completed thought.",
                        "crossfade_ms": 15.0
                    })
        return decisions
