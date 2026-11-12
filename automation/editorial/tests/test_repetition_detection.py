import unittest
from automation.editorial.core.repetition_engine import RepetitionEngine

class TestRepetitionDetection(unittest.TestCase):
    def setUp(self):
        self.engine = RepetitionEngine()

    def test_single_word_stutter(self):
        words = [
            {"word": "in", "start": 1.0, "end": 1.2},
            {"word": "in", "start": 1.3, "end": 1.5},
            {"word": "the", "start": 1.6, "end": 1.8},
            {"word": "terminal", "start": 1.9, "end": 2.4}
        ]
        decisions = self.engine.detect_exact_repetitions(words)
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["category"], "Exact Word Stutter")
        self.assertEqual(decisions[0]["action"], "REMOVE")
        self.assertEqual(decisions[0]["start_time"], 1.0)
        self.assertEqual(decisions[0]["end_time"], 1.2)

    def test_two_word_phrase_stutter(self):
        words = [
            {"word": "we", "start": 2.0, "end": 2.2},
            {"word": "will", "start": 2.25, "end": 2.45},
            {"word": "we", "start": 2.6, "end": 2.8},
            {"word": "will", "start": 2.85, "end": 3.05},
            {"word": "execute", "start": 3.1, "end": 3.5}
        ]
        decisions = self.engine.detect_exact_repetitions(words)
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["category"], "Exact Phrase Stutter")
        self.assertEqual(decisions[0]["start_time"], 2.0)
        self.assertEqual(decisions[0]["end_time"], 2.45)

    def test_false_start_detection(self):
        sentences = [
            {"text": "we need to-", "start": 5.0, "end": 5.8},
            {"text": "we need to make sure python is installed", "start": 6.1, "end": 8.5}
        ]
        decisions = self.engine.detect_false_starts(sentences)
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["category"], "False Start Sentence Stumble")
        self.assertEqual(decisions[0]["action"], "REMOVE")

if __name__ == "__main__":
    unittest.main()
