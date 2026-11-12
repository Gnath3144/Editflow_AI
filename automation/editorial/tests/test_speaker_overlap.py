import unittest
import numpy as np
from automation.editorial.core.speaker_diarizer import SpeakerDiarizer, patch_resemblyzer_stft

class TestSpeakerDiarizer(unittest.TestCase):
    def setUp(self):
        self.diarizer = SpeakerDiarizer()

    def test_patch_resemblyzer_execution(self):
        success = patch_resemblyzer_stft()
        self.assertTrue(success)

    def test_classification_fallback(self):
        dummy_slice = np.zeros(16000, dtype=np.float32)
        res = self.diarizer.classify_segment(dummy_slice, text="How do we define the Pydantic model?")
        self.assertIn("speaker_role", res)
        self.assertIn("action", res)

if __name__ == "__main__":
    unittest.main()
