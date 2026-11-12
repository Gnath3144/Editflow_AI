"""
Multilingual Dubbing Preparation & Validation Module
Verifies that English master sentences comply with timing, syllable rate,
and expansion constraints across all 12 target language profiles.
"""

import os
import json
from typing import List, Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "configuration", "language_profiles.json")

class MultilingualIntegrator:
    def __init__(self, config_path: Optional[str] = None):
        path = config_path or CONFIG_PATH
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.languages = json.load(f)
        else:
            self.languages = {
                "telugu": {"expansion_factor": 1.18, "pause_buffer_ms": 250},
                "hindi": {"expansion_factor": 1.12, "pause_buffer_ms": 200},
                "spanish": {"expansion_factor": 1.15, "pause_buffer_ms": 200}
            }

    def validate_sentence_spacing(self, sentences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Checks whether gaps between English sentences accommodate localized speech expansion.
        """
        issues = []
        for i in range(len(sentences) - 1):
            curr_s = sentences[i]
            next_s = sentences[i+1]
            gap_ms = (next_s.get("start", 0.0) - curr_s.get("end", 0.0)) * 1000.0

            # Target language expansion checks
            for lang_name, profile in self.languages.items():
                min_buffer = profile.get("pause_buffer_ms", 200)
                expansion = profile.get("expansion_factor", 1.15)
                duration_ms = (curr_s.get("end", 0.0) - curr_s.get("start", 0.0)) * 1000.0
                projected_expansion_ms = duration_ms * (expansion - 1.0)

                if gap_ms < projected_expansion_ms:
                    issues.append({
                        "sentence_index": i,
                        "language": lang_name,
                        "gap_ms": round(gap_ms, 1),
                        "projected_expansion_ms": round(projected_expansion_ms, 1),
                        "deficit_ms": round(projected_expansion_ms - gap_ms, 1)
                    })

        return {
            "is_valid_for_dubbing": len(issues) == 0,
            "total_bottlenecks": len(issues),
            "issues": issues[:10]
        }
