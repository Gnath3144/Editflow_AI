import unittest
from automation.editorial.core.filler_detector import FillerDetector

class TestFillerDetection(unittest.TestCase):
    def setUp(self):
        self.detector = FillerDetector()

    def test_tier_1_non_semantic_filler(self):
        res = self.detector.classify_token("um")
        self.assertEqual(res["tier"], 1)
        self.assertEqual(res["classification"], "NON_SEMANTIC_FILLER")
        self.assertEqual(res["recommended_action"], "REMOVE")
        self.assertGreaterEqual(res["confidence"], 0.88)

    def test_tier_2_optional_discourse_marker(self):
        res = self.detector.classify_token("basically")
        self.assertEqual(res["tier"], 2)
        self.assertEqual(res["classification"], "OPTIONAL_DISCOURSE_MARKER")

    def test_tier_3_meaningful_expression(self):
        res = self.detector.classify_token("for example")
        self.assertEqual(res["tier"], 3)
        self.assertEqual(res["classification"], "MEANINGFUL_EXPRESSION")
        self.assertEqual(res["recommended_action"], "KEEP")

    def test_standard_pedagogical_speech(self):
        res = self.detector.classify_token("pydantic")
        self.assertEqual(res["tier"], 4)
        self.assertEqual(res["classification"], "STANDARD_SPEECH")
        self.assertEqual(res["recommended_action"], "KEEP")

    def test_analyze_words_pipeline(self):
        words = [
            {"word": "Now", "start": 1.0, "end": 1.2},
            {"word": "um", "start": 1.3, "end": 1.7},
            {"word": "we", "start": 1.8, "end": 2.0},
            {"word": "install", "start": 2.1, "end": 2.5}
        ]
        decisions = self.detector.analyze_words(words)
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["action"], "REMOVE")
        self.assertEqual(decisions[0]["token"], "um")
        self.assertEqual(decisions[0]["start_time"], 1.3)
        self.assertEqual(decisions[0]["end_time"], 1.7)

if __name__ == "__main__":
    unittest.main()
