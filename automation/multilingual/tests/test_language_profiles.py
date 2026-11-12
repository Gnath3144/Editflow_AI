import unittest
from automation.multilingual.app.language_detector import LanguageDetector

class TestLanguageProfiles(unittest.TestCase):
    def setUp(self):
        self.detector = LanguageDetector()

    def test_all_12_languages_present(self):
        expected_locales = [
            "ta-IN", "te-IN", "ml-IN", "hi-IN", "ur-PK", "zh-CN",
            "ja-JP", "ko-KR", "ms-MY", "en-SG", "en-GB", "en-US"
        ]
        locales = self.detector.list_supported_locales()
        for loc in expected_locales:
            self.assertIn(loc, locales, f"Locale {loc} missing from configuration")

    def test_language_profile_structure(self):
        profile = self.detector.get_profile("ta-IN")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["display_name"], "Tamil")
        self.assertEqual(profile["native_name"], "தமிழ்")
        self.assertEqual(profile["family"], "Dravidian")
        self.assertEqual(profile["text_direction"], "ltr")
        self.assertIn("voice_requirements", profile)
        self.assertGreater(profile["voice_requirements"]["target_syllable_rate"], 0)

    def test_urdu_rtl_direction(self):
        urdu = self.detector.get_profile("ur-PK")
        self.assertIsNotNone(urdu)
        self.assertEqual(urdu["text_direction"], "rtl")
        self.assertTrue(urdu["subtitle_requirements"]["rtl_support"])

    def test_bahasa_melayu_and_singapore_english_specifications(self):
        my = self.detector.get_profile("ms-MY")
        self.assertIsNotNone(my)
        self.assertEqual(my["language_id"], "bahasa_melayu")

        sg = self.detector.get_profile("en-SG")
        self.assertIsNotNone(sg)
        self.assertEqual(sg["language_id"], "singapore_english")

if __name__ == "__main__":
    unittest.main()
