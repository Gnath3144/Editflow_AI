import unittest
import os
import tempfile
from automation.multilingual.app.subtitle_generator import SubtitleGenerator
from automation.multilingual.app.multilingual_comprehension_validator import MultilingualComprehensionValidator

class TestSubtitles(unittest.TestCase):
    def setUp(self):
        self.generator = SubtitleGenerator()
        self.validator = MultilingualComprehensionValidator(max_cpl=17)

    def test_srt_generation(self):
        segments = [
            {"start_time": 0.0, "end_time": 3.5, "translated_text": "வணக்கம், பாடம் ஒன்றுக்கு வரவேற்கிறோம்."}
        ]
        with tempfile.NamedTemporaryFile(suffix=".srt", delete=False) as f:
            temp_path = f.name
        try:
            self.generator.generate_srt(segments, temp_path)
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("00:00:00,000 --> 00:00:03,500", content)
            self.assertIn("வணக்கம்", content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
