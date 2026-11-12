"""
Automated Quality Control Validation Module
Executes 4-tier acceptance tests on mastered lessons:
1. Acoustic & Loudness QC
2. Speaker Purity QC
3. Semantic & Editorial QC
4. Technical & Video Encoding QC
"""

import os
import json
from typing import Dict, Any, Optional

class QualityValidator:
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.join(os.path.dirname(__file__), "..", "configuration")

    def validate_lesson(self,
                        lesson_title: str,
                        integrated_lufs: float,
                        true_peak_dbtp: float,
                        snr_db: float,
                        instructor_purity_pct: float,
                        word_truncation_count: int,
                        filler_removal_rate: float,
                        video_codec: str,
                        frame_rate: float,
                        resolution: str) -> Dict[str, Any]:
        """
        Runs comprehensive QC evaluation against published standards.
        """
        acoustic_pass = (-16.5 <= integrated_lufs <= -15.5) and (true_peak_dbtp <= -1.5) and (snr_db >= 38.0)
        speaker_pass = (instructor_purity_pct >= 95.0)
        semantic_pass = (word_truncation_count == 0) and (filler_removal_rate >= 0.90)
        technical_pass = ("nvenc" in video_codec.lower() or "264" in video_codec.lower()) and (abs(frame_rate - 30.0) < 0.1) and (resolution == "1920x1080")

        overall_pass = acoustic_pass and speaker_pass and semantic_pass and technical_pass

        return {
            "target_lesson": lesson_title,
            "overall_pass": overall_pass,
            "acoustic_qc": {
                "pass": acoustic_pass,
                "integrated_lufs": integrated_lufs,
                "true_peak_dbtp": true_peak_dbtp,
                "snr_db": snr_db
            },
            "speaker_qc": {
                "pass": speaker_pass,
                "instructor_purity_pct": instructor_purity_pct
            },
            "semantic_qc": {
                "pass": semantic_pass,
                "word_truncation_count": word_truncation_count,
                "filler_removal_rate": filler_removal_rate
            },
            "technical_qc": {
                "pass": technical_pass,
                "video_codec": video_codec,
                "frame_rate": frame_rate,
                "resolution": resolution
            }
        }
