import unittest
from automation.editorial.core.quality_validator import QualityValidator

class TestQualityValidator(unittest.TestCase):
    def setUp(self):
        self.validator = QualityValidator()

    def test_approved_master_passes_all_tiers(self):
        res = self.validator.validate_lesson(
            lesson_title="Lesson 01 - The Structured Output Challenge",
            integrated_lufs=-16.0,
            true_peak_dbtp=-1.5,
            snr_db=42.0,
            instructor_purity_pct=98.5,
            word_truncation_count=0,
            filler_removal_rate=0.94,
            video_codec="h264_nvenc",
            frame_rate=30.0,
            resolution="1920x1080"
        )
        self.assertTrue(res["overall_pass"])
        self.assertTrue(res["acoustic_qc"]["pass"])
        self.assertTrue(res["speaker_qc"]["pass"])
        self.assertTrue(res["semantic_qc"]["pass"])
        self.assertTrue(res["technical_qc"]["pass"])

    def test_failed_loudness_is_rejected(self):
        res = self.validator.validate_lesson(
            lesson_title="Bad Audio Lesson",
            integrated_lufs=-22.0, # Too quiet
            true_peak_dbtp=-0.5, # Clipped peak
            snr_db=25.0,
            instructor_purity_pct=98.0,
            word_truncation_count=0,
            filler_removal_rate=0.92,
            video_codec="h264_nvenc",
            frame_rate=30.0,
            resolution="1920x1080"
        )
        self.assertFalse(res["overall_pass"])
        self.assertFalse(res["acoustic_qc"]["pass"])

if __name__ == "__main__":
    unittest.main()
