import unittest
from automation.multilingual.app.transcript_normalizer import TranscriptNormalizer

class TestTranslationPreservation(unittest.TestCase):
    def setUp(self):
        self.normalizer = TranscriptNormalizer()

    def test_shielding_and_unshielding_code(self):
        text = "Run `pip install pydantic` to set up your environment."
        shielded, shields = self.normalizer.shield_text(text)
        self.assertIn("[[SHIELD_0]]", shielded)
        self.assertNotIn("`pip install pydantic`", shielded)

        # Simulate translation keeping shield token
        translated_sim = f"Ejecute [[SHIELD_0]] para configurar su entorno."
        restored = self.normalizer.unshield_text(translated_sim, shields)
        self.assertIn("`pip install pydantic`", restored)

if __name__ == "__main__":
    unittest.main()
