import unittest
from automation.multilingual.app.adaptive_pacing_engine import AdaptivePacingEngine

class TestAdaptivePacing(unittest.TestCase):
    def setUp(self):
        self.engine = AdaptivePacingEngine()

    def test_protected_context_remains_unaccelerated(self):
        # Demonstrating code, introducing new terms, or explaining complex concepts must be 1.00x
        rate_code = self.engine.compute_english_acceleration(context_tags=["demonstrating_code"])
        self.assertEqual(rate_code, 1.00)

        rate_concept = self.engine.compute_english_acceleration(context_tags=["complex_technical_concept"])
        self.assertEqual(rate_concept, 1.00)

    def test_english_acceleration_tiers(self):
        rate_natural = self.engine.compute_english_acceleration(pace_tier="natural_pace")
        self.assertEqual(rate_natural, 1.00)

        rate_slow = self.engine.compute_english_acceleration(pace_tier="noticeably_slow")
        self.assertEqual(rate_slow, 1.08)

        rate_unusual = self.engine.compute_english_acceleration(pace_tier="unusually_slow")
        self.assertEqual(rate_unusual, 1.10)

        # Enforces absolute ceiling of 1.12x
        rate_max = self.engine.compute_english_acceleration(pace_tier="absolute_maximum")
        self.assertEqual(rate_max, 1.12)

    def test_localized_stretch_bounds(self):
        stretch = self.engine.compute_localized_stretch(original_duration=5.0, synthesized_duration=5.5)
        self.assertEqual(stretch, 1.1)

        # Bounds enforcement: cannot exceed 1.15
        stretch_high = self.engine.compute_localized_stretch(original_duration=5.0, synthesized_duration=10.0)
        self.assertEqual(stretch_high, 1.15)

        # Bounds enforcement: cannot drop below 0.85
        stretch_low = self.engine.compute_localized_stretch(original_duration=10.0, synthesized_duration=5.0)
        self.assertEqual(stretch_low, 0.85)

    def test_automatic_rollback_on_degradation(self):
        # If clarity is low, roll back to original
        rollback = self.engine.evaluate_and_rollback(
            original_audio_path="orig.wav",
            transformed_audio_path="stretched.wav",
            clarity_score=0.65
        )
        self.assertTrue(rollback["reverted"])
        self.assertEqual(rollback["active_audio_path"], "orig.wav")

        # If clarity is high, keep transformed
        keep = self.engine.evaluate_and_rollback(
            original_audio_path="orig.wav",
            transformed_audio_path="stretched.wav",
            clarity_score=0.92
        )
        self.assertFalse(keep["reverted"])
        self.assertEqual(keep["active_audio_path"], "stretched.wav")

if __name__ == "__main__":
    unittest.main()
