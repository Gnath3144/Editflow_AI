import unittest
from automation.editorial.core.audio_master import AudioMaster

class TestAudioMaster(unittest.TestCase):
    def setUp(self):
        self.master = AudioMaster()

    def test_ffmpeg_filtergraph_construction(self):
        filters = self.master.build_ffmpeg_filter_string()
        self.assertIn("highpass=f=80.0", filters)
        self.assertIn("afftdn", filters)
        self.assertIn("equalizer=f=3200", filters)
        self.assertIn("acompressor", filters)
        self.assertIn("loudnorm=I=-16.0:TP=-1.5", filters)

if __name__ == "__main__":
    unittest.main()
