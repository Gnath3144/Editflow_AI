import unittest
from automation.editorial.core.editorial_decision_engine import EditorialDecisionEngine

class TestSemanticContinuity(unittest.TestCase):
    def setUp(self):
        self.engine = EditorialDecisionEngine()

    def test_harmonize_decisions_overlapping(self):
        candidates = [
            {"decision_id": "D1", "start_time": 10.0, "end_time": 12.0, "confidence": 0.80},
            {"decision_id": "D2", "start_time": 11.5, "end_time": 14.0, "confidence": 0.95}
        ]
        harmonized = self.engine.harmonize_decisions(candidates, total_duration=20.0)
        self.assertEqual(len(harmonized), 1)
        self.assertEqual(harmonized[0]["start_time"], 10.0)
        self.assertEqual(harmonized[0]["end_time"], 14.0)

    def test_generate_keep_timeline(self):
        cuts = [
            {"start_time": 0.0, "end_time": 5.0},
            {"start_time": 10.0, "end_time": 12.0}
        ]
        keeps = self.engine.generate_keep_timeline(cuts, total_duration=20.0)
        self.assertEqual(len(keeps), 2)
        self.assertEqual(keeps[0]["start"], 5.0)
        self.assertEqual(keeps[0]["end"], 10.0)
        self.assertEqual(keeps[1]["start"], 12.0)
        self.assertEqual(keeps[1]["end"], 20.0)

if __name__ == "__main__":
    unittest.main()
