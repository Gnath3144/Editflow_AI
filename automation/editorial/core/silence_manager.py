"""
Pause, Hesitation & Silence Manager
Categorizes pauses and silences into:
- Micro-pause (< 0.3s): Preserved unchanged
- Natural conversational pause (0.3s - 0.8s): Preserved
- Pedagogical pause (0.8s - 1.5s): Preserved / capped
- Hesitation silence (1.5s - 3.0s): Shortened to 0.40s
- Dead air (> 3.0s): Cut or shortened to 0.50s
Ensures safety lead-in/lead-out buffers and micro-fades.
"""

import os
import json
from typing import List, Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "configuration", "silence_rules.json")

class SilenceManager:
    def __init__(self, config_path: Optional[str] = None):
        path = config_path or CONFIG_PATH
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "micro_pause": {"max_duration_sec": 0.30},
                "natural_pause": {"min_duration_sec": 0.30, "max_duration_sec": 0.80},
                "pedagogical_pause": {"min_duration_sec": 0.80, "max_duration_sec": 1.50, "max_allowed_static_sec": 1.20},
                "hesitation_silence": {"min_duration_sec": 1.50, "max_duration_sec": 3.00, "target_shortened_sec": 0.40},
                "dead_air": {"min_duration_sec": 3.00, "target_shortened_sec": 0.50}
            }

    def classify_pause(self, duration: float, has_screen_activity: bool = False) -> Dict[str, Any]:
        if duration <= 0.30:
            return {"category": "MICRO_PAUSE", "action": "DO_NOT_TOUCH", "target_duration": duration}
        elif duration <= 0.80:
            return {"category": "NATURAL_PAUSE", "action": "PRESERVE", "target_duration": duration}
        elif duration <= 1.50:
            if has_screen_activity:
                return {"category": "PEDAGOGICAL_PAUSE_ACTIVE", "action": "PRESERVE", "target_duration": duration}
            else:
                capped = min(duration, self.config.get("pedagogical_pause", {}).get("max_allowed_static_sec", 1.20))
                return {"category": "PEDAGOGICAL_PAUSE_STATIC", "action": "PRESERVE_OR_CAP", "target_duration": capped}
        elif duration <= 3.00:
            target = self.config.get("hesitation_silence", {}).get("target_shortened_sec", 0.40)
            return {"category": "HESITATION_SILENCE", "action": "SHORTEN", "target_duration": target}
        else:
            target = self.config.get("dead_air", {}).get("target_shortened_sec", 0.50)
            return {"category": "DEAD_AIR", "action": "SHORTEN", "target_duration": target}

    def process_silence_gaps(self, speech_segments: List[Dict[str, Any]], total_duration: float) -> List[Dict[str, Any]]:
        """
        Takes speech segments [{start, end, ...}], finds gaps between them,
        and generates edit decisions for trimming long pauses.
        """
        decisions = []
        if not speech_segments:
            if total_duration > 3.0:
                decisions.append({
                    "decision_id": "DEC-SIL-00000",
                    "start_time": 0.0,
                    "end_time": round(total_duration, 3),
                    "duration": round(total_duration, 3),
                    "action": "REMOVE",
                    "category": "Total Dead Air",
                    "confidence": 0.99,
                    "rule_reference": "PAUSE_AND_SILENCE_POLICY:SEC_1",
                    "semantic_impact": "Completely remove unvoiced recording.",
                    "crossfade_ms": 0.0
                })
            return decisions

        # Check gap before first speech segment
        first_start = speech_segments[0].get("start", 0.0)
        if first_start > 2.0:
            decisions.append({
                "decision_id": "DEC-SIL-HEAD",
                "start_time": 0.0,
                "end_time": round(max(0.0, first_start - 0.30), 3),
                "duration": round(max(0.0, first_start - 0.30), 3),
                "action": "REMOVE",
                "category": "Pre-Speech Lead-in Dead Air",
                "confidence": 0.98,
                "rule_reference": "PAUSE_AND_SILENCE_POLICY:SEC_1",
                "semantic_impact": "Remove dead air preceding first instruction.",
                "crossfade_ms": 10.0
            })

        # Inter-segment gaps
        for i in range(len(speech_segments) - 1):
            curr_end = speech_segments[i].get("end", 0.0)
            next_start = speech_segments[i+1].get("start", 0.0)
            gap = next_start - curr_end

            if gap > 1.50:
                classification = self.classify_pause(gap)
                if classification["action"] == "SHORTEN":
                    target_pause = classification["target_duration"]
                    cut_start = curr_end + (target_pause / 2.0)
                    cut_end = next_start - (target_pause / 2.0)
                    if cut_end > cut_start + 0.1:
                        decisions.append({
                            "decision_id": f"DEC-SIL-{i:05d}",
                            "start_time": round(cut_start, 3),
                            "end_time": round(cut_end, 3),
                            "duration": round(cut_end - cut_start, 3),
                            "action": "SHORTEN",
                            "category": classification["category"],
                            "confidence": 0.92,
                            "rule_reference": "PAUSE_AND_SILENCE_POLICY:SEC_1",
                            "semantic_impact": f"Trim pause of {gap:.2f}s down to {target_pause:.2f}s natural cadence.",
                            "crossfade_ms": 12.0
                        })

        # Check gap after last segment
        last_end = speech_segments[-1].get("end", total_duration)
        if total_duration - last_end > 2.0:
            decisions.append({
                "decision_id": "DEC-SIL-TAIL",
                "start_time": round(last_end + 0.50, 3),
                "end_time": round(total_duration, 3),
                "duration": round(total_duration - (last_end + 0.50), 3),
                "action": "REMOVE",
                "category": "Post-Speech Lead-out Dead Air",
                "confidence": 0.98,
                "rule_reference": "PAUSE_AND_SILENCE_POLICY:SEC_1",
                "semantic_impact": "Remove trailing dead air at end of session.",
                "crossfade_ms": 10.0
            })

        return decisions
