import unittest
from automation.multilingual.app.audio_validator import AudioValidator

class TestAudioQuality(unittest.TestCase):
    def setUp(self):
        self.validator = AudioValidator()

    def test_broadcast_compliance(self):
        res = self.validator.validate_audio_quality(
            integrated_lufs=-16.0,
            true_peak_dbtp=-1.5,
            snr_db=42.0
        )
        self.assertTrue(res["overall_pass"])

    def test_rejection_on_loudness_violation(self):
        res = self.validator.validate_audio_quality(
            integrated_lufs=-20.0,
            true_peak_dbtp=-0.5,
            snr_db=30.0
        )
        self.assertFalse(res["overall_pass"])
        self.assertFalse(res["lufs_pass"])

if __name__ == "__main__":
    unittest.main()
