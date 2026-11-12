import unittest
from automation.editorial.core.silence_manager import SilenceManager

class TestPauseDetection(unittest.TestCase):
    def setUp(self):
        self.manager = SilenceManager()

    def test_micro_pause_untouched(self):
        res = self.manager.classify_pause(0.20)
        self.assertEqual(res["category"], "MICRO_PAUSE")
        self.assertEqual(res["action"], "DO_NOT_TOUCH")

    def test_natural_pause_preserved(self):
        res = self.manager.classify_pause(0.55)
        self.assertEqual(res["category"], "NATURAL_PAUSE")
        self.assertEqual(res["action"], "PRESERVE")

    def test_hesitation_shortened(self):
        res = self.manager.classify_pause(2.20)
        self.assertEqual(res["category"], "HESITATION_SILENCE")
        self.assertEqual(res["action"], "SHORTEN")
        self.assertEqual(res["target_duration"], 0.40)

    def test_dead_air_shortened(self):
        res = self.manager.classify_pause(8.50)
        self.assertEqual(res["category"], "DEAD_AIR")
        self.assertEqual(res["action"], "SHORTEN")
        self.assertEqual(res["target_duration"], 0.50)

    def test_process_silence_gaps_head_and_inter(self):
        segments = [
            {"start": 10.0, "end": 15.0},
            {"start": 18.0, "end": 22.0}
        ]
        decisions = self.manager.process_silence_gaps(segments, total_duration=25.0)
        # Should detect lead-in dead air (0 to ~9.7) and inter-gap (15 to 18 = 3.0s)
        self.assertGreaterEqual(len(decisions), 2)
        head_dec = decisions[0]
        self.assertEqual(head_dec["category"], "Pre-Speech Lead-in Dead Air")
        self.assertEqual(head_dec["action"], "REMOVE")

if __name__ == "__main__":
    unittest.main()
