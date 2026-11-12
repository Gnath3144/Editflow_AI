"""Readability and cognitive load validation for subtitles."""
from typing import List, Dict, Any

class MultilingualComprehensionValidator:
    def __init__(self, max_cpl: int = 17):
        self.max_cpl = max_cpl

    def validate_subtitles(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        violations = []
        for i, s in enumerate(segments):
            text = s.get("translated_text", "")
            duration = max(0.5, s.get("end_time", 0.0) - s.get("start_time", 0.0))
            cpl = len(text) / duration
            if cpl > self.max_cpl:
                violations.append({
                    "segment_index": i,
                    "cpl": round(cpl, 1),
                    "text": text[:30]
                })
        return {
            "is_valid": len(violations) == 0,
            "violations_count": len(violations),
            "violations": violations[:5]
        }
