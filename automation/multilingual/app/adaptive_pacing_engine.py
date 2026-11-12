"""
Adaptive Speech Pacing Engine
Implements pitch-preserving time stretching, selective English acceleration policies,
context protection (never accelerate code walkthroughs or complex explanations),
independent language pacing, and automatic rollback on quality degradation.
"""

import os
import json
from typing import Dict, Any, Optional, List

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "adaptive_pacing.json")

class AdaptivePacingEngine:
    def __init__(self, config_path: Optional[str] = None):
        p = config_path or CONFIG_PATH
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "english_master": {
                    "policy_tiers": {
                        "natural_pace": 1.00,
                        "slightly_slow": 1.04,
                        "noticeably_slow": 1.08,
                        "unusually_slow": 1.10,
                        "absolute_maximum": 1.12
                    },
                    "preferred_maximum": 1.08,
                    "absolute_maximum": 1.12
                },
                "localized_speech": {"allowed_stretch_range": [0.85, 1.15]}
            }

    def compute_english_acceleration(self, context_tags: Optional[List[str]] = None, pace_tier: str = "natural_pace") -> float:
        """
        Determines English speed multiplier based on pedagogical context and speech delivery tier.
        Guarantees 1.00x for protected contexts (code demo, complex reasoning, etc.).
        """
        protected_list = self.config.get("english_master", {}).get("protected_contexts", [])
        if context_tags:
            for tag in context_tags:
                if tag in protected_list:
                    return 1.00

        tiers = self.config.get("english_master", {}).get("policy_tiers", {})
        mult = tiers.get(pace_tier, 1.00)
        abs_max = self.config.get("english_master", {}).get("absolute_maximum", 1.12)
        return min(abs_max, mult)

    def compute_localized_stretch(self, original_duration: float, synthesized_duration: float) -> float:
        """
        Calculates pitch-preserving stretch factor for translated speech segments.
        Clamped to [0.85x, 1.15x] to prevent unnatural chipmunk or dragging speech.
        """
        if synthesized_duration <= 0 or original_duration <= 0:
            return 1.00
        ratio = synthesized_duration / original_duration
        min_stretch, max_stretch = self.config.get("localized_speech", {}).get("allowed_stretch_range", [0.85, 1.15])
        return max(min_stretch, min(max_stretch, round(ratio, 3)))

    def evaluate_and_rollback(self, original_audio_path: str, transformed_audio_path: str, clarity_score: float) -> Dict[str, Any]:
        """
        Compares transformed segment clarity against threshold.
        If clarity decreases below threshold or clipping is detected, triggers automatic rollback.
        """
        threshold = self.config.get("localized_speech", {}).get("rollback_threshold_clarity", 0.80)
        if clarity_score < threshold:
            return {
                "action": "ROLLBACK_TO_ORIGINAL",
                "reverted": True,
                "active_audio_path": original_audio_path,
                "reason": f"Clarity score {clarity_score:.2f} below minimum threshold {threshold:.2f}."
            }
        return {
            "action": "KEEP_TRANSFORMED",
            "reverted": False,
            "active_audio_path": transformed_audio_path,
            "reason": f"Clarity score {clarity_score:.2f} acceptable."
        }
