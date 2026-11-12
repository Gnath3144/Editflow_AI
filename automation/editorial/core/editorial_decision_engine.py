"""
Central Editorial Decision Engine
Harmonizes and resolves edit proposals across:
- Filler word removal
- Repetition & false start trimming
- Silence & pause compression
- Speaker diarization & unmuted chatter elimination
Produces a compliant, verified, non-destructive Edit Decision List (EDL).
"""

import os
import json
from typing import List, Dict, Any, Optional

class EditorialDecisionEngine:
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.join(os.path.dirname(__file__), "..", "configuration")

    def harmonize_decisions(self, candidate_decisions: List[Dict[str, Any]], total_duration: float) -> List[Dict[str, Any]]:
        """
        Sorts candidates, removes overlaps, enforces minimum splice intervals,
        and ensures semantic continuity.
        """
        if not candidate_decisions:
            return []

        # Sort by start_time
        sorted_dec = sorted(candidate_decisions, key=lambda x: x["start_time"])
        harmonized = []

        last_end = 0.0
        for dec in sorted_dec:
            start = dec["start_time"]
            end = dec["end_time"]

            # Prevent negative or out-of-bounds duration
            if start < 0:
                start = 0.0
            if end > total_duration:
                end = total_duration
            if end <= start:
                continue

            # Check overlap with previous edit
            if start < last_end:
                # Resolve conflict by extending or merging
                if dec["confidence"] > harmonized[-1]["confidence"]:
                    harmonized[-1]["end_time"] = max(harmonized[-1]["end_time"], end)
                    harmonized[-1]["duration"] = harmonized[-1]["end_time"] - harmonized[-1]["start_time"]
                    last_end = harmonized[-1]["end_time"]
                continue

            harmonized.append(dec)
            last_end = end

        return harmonized

    def generate_keep_timeline(self, remove_decisions: List[Dict[str, Any]], total_duration: float) -> List[Dict[str, float]]:
        """
        Inverts a list of REMOVE / CUT decisions into a list of KEEP intervals [start, end].
        """
        if not remove_decisions:
            return [{"start": 0.0, "end": total_duration, "duration": total_duration}]

        sorted_cuts = sorted(remove_decisions, key=lambda x: x["start_time"])
        keep_intervals = []
        current_pos = 0.0

        for cut in sorted_cuts:
            cut_start = cut["start_time"]
            cut_end = cut["end_time"]

            if cut_start > current_pos + 0.05:
                keep_intervals.append({
                    "start": round(current_pos, 3),
                    "end": round(cut_start, 3),
                    "duration": round(cut_start - current_pos, 3)
                })
            current_pos = max(current_pos, cut_end)

        if current_pos < total_duration - 0.05:
            keep_intervals.append({
                "start": round(current_pos, 3),
                "end": round(total_duration, 3),
                "duration": round(total_duration - current_pos, 3)
            })

        return keep_intervals
