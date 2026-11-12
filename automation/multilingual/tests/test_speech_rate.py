import unittest
from automation.multilingual.app.speech_rate_analyzer import SpeechRateAnalyzer

class TestSpeechRate(unittest.TestCase):
    def setUp(self):
        self.analyzer = SpeechRateAnalyzer()

    def test_syllable_count_and_rate(self):
        text = "Hello world welcome to Python"
        syllables = self.analyzer.count_syllables_english(text)
        self.assertGreaterEqual(syllables, 5)

        rate = self.analyzer.calculate_rate(text, duration_sec=2.0)
        self.assertGreater(rate, 2.0)

if __name__ == "__main__":
    unittest.main()
