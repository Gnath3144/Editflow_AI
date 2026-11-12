import unittest
from automation.multilingual.app.audio_timing_aligner import AudioTimingAligner
from automation.multilingual.app.segment_timing_validator import SegmentTimingValidator

class TestAudioAlignment(unittest.TestCase):
    def setUp(self):
        self.aligner = AudioTimingAligner()
        self.validator = SegmentTimingValidator(max_drift_ms=200.0)

    def test_alignment_and_drift_detection(self):
        segments = [
            {"start_time": 0.0, "end_time": 3.0},
            {"start_time": 3.1, "end_time": 6.0}
        ]
        aligned = self.aligner.align_segments(segments, total_duration=10.0)
        val = self.validator.validate_timings(aligned)
        self.assertTrue(val["is_valid"])

    def test_overlap_violation_flagged(self):
        bad_segments = [
            {"aligned_start": 0.0, "aligned_end": 4.5},
            {"aligned_start": 4.0, "aligned_end": 8.0}
        ]
        val = self.validator.validate_timings(bad_segments)
        self.assertFalse(val["is_valid"])
        self.assertEqual(val["violations_count"], 1)

if __name__ == "__main__":
    unittest.main()
