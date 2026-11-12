"""Timing drift and overlap detection."""
from typing import List, Dict, Any

class SegmentTimingValidator:
    def __init__(self, max_drift_ms: float = 200.0):
        self.max_drift_ms = max_drift_ms

    def validate_timings(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        violations = []
        for i in range(len(segments) - 1):
            curr_end = segments[i].get("aligned_end", 0.0)
            next_start = segments[i+1].get("aligned_start", 0.0)
            if curr_end > next_start + (self.max_drift_ms / 1000.0):
                violations.append({
                    "segment_index": i,
                    "curr_end": curr_end,
                    "next_start": next_start,
                    "overlap_sec": round(curr_end - next_start, 3)
                })
        return {
            "is_valid": len(violations) == 0,
            "violations_count": len(violations),
            "violations": violations
        }
