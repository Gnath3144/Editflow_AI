"""
Filler & Discourse Marker Intelligence Module
Implements 4-tier classification:
- Tier 1: Non-semantic fillers (um, uh, er, etc.) -> Target for REMOVE
- Tier 2: Optional discourse markers (basically, actually, right?, etc.) -> Contextual evaluation
- Tier 3: Meaningful expressions (for example, notice that, etc.) -> Always KEEP
- Tier 4: Uncertain fragments -> Flag for HUMAN_REVIEW
"""

import os
import json
import re
from typing import List, Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "configuration", "filler_words.json")

class FillerDetector:
    def __init__(self, config_path: Optional[str] = None):
        path = config_path or CONFIG_PATH
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "tier_1_non_semantic_fillers": {"tokens": ["um", "uh", "er", "ah", "umm", "uhh"], "min_confidence": 0.88},
                "tier_2_optional_discourse_markers": {"tokens": ["basically", "actually", "right?", "okay?", "got it?"], "max_density_per_minute": 2.0},
                "tier_3_meaningful_expressions": {"tokens": ["for example", "specifically", "notice that", "therefore"]}
            }
        
        self.t1_tokens = set(t.lower() for t in self.config.get("tier_1_non_semantic_fillers", {}).get("tokens", []))
        self.t2_tokens = set(t.lower() for t in self.config.get("tier_2_optional_discourse_markers", {}).get("tokens", []))
        self.t3_tokens = set(t.lower() for t in self.config.get("tier_3_meaningful_expressions", {}).get("tokens", []))

    def clean_text(self, text: str) -> str:
        return re.sub(r"[^\w\s]", "", text).lower().strip()

    def classify_token(self, token: str) -> Dict[str, Any]:
        cleaned = self.clean_text(token)
        if cleaned in self.t1_tokens:
            return {
                "tier": 1,
                "classification": "NON_SEMANTIC_FILLER",
                "recommended_action": "REMOVE",
                "confidence": self.config.get("tier_1_non_semantic_fillers", {}).get("min_confidence", 0.90)
            }
        elif cleaned in self.t2_tokens:
            return {
                "tier": 2,
                "classification": "OPTIONAL_DISCOURSE_MARKER",
                "recommended_action": "CONTEXTUAL_EVALUATION",
                "confidence": 0.80
            }
        elif cleaned in self.t3_tokens:
            return {
                "tier": 3,
                "classification": "MEANINGFUL_EXPRESSION",
                "recommended_action": "KEEP",
                "confidence": 0.95
            }
        else:
            return {
                "tier": 4,
                "classification": "STANDARD_SPEECH",
                "recommended_action": "KEEP",
                "confidence": 0.99
            }

    def analyze_words(self, words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyzes a sequence of word dicts (word, start, end, probability).
        Returns list of edit candidates for identified fillers.
        """
        decisions = []
        for i, w in enumerate(words):
            raw_word = w.get("word", "").strip()
            classification = self.classify_token(raw_word)
            
            if classification["classification"] == "NON_SEMANTIC_FILLER":
                start_t = w.get("start", 0.0)
                end_t = w.get("end", 0.0)
                duration = max(0.0, end_t - start_t)
                
                decisions.append({
                    "decision_id": f"DEC-FIL-{i:05d}",
                    "start_time": round(start_t, 3),
                    "end_time": round(end_t, 3),
                    "duration": round(duration, 3),
                    "action": "REMOVE",
                    "category": "Non-Semantic Verbal Filler",
                    "token": raw_word,
                    "confidence": classification["confidence"],
                    "rule_reference": "EDITING_DECISION_POLICY:SEC_1",
                    "semantic_impact": f"Eliminate non-semantic verbal filler '{raw_word}' to preserve instructional density.",
                    "crossfade_ms": 10.0
                })
        return decisions
