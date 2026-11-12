import unittest
import os
import shutil
import tempfile
from automation.multilingual.providers.youtube_base import YouTubePublisherBase
from automation.multilingual.app.youtube_audio_publisher import YouTubeAudioPublisher

class DummyPublisher(YouTubePublisherBase):
    def inventory_playlist(self, pid): return []
    def upload_audio_track(self, v, l, a): return False  # Cannot upload directly without CMS

class TestYouTubeTrackMapping(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.publisher = DummyPublisher()
        self.audio_pub = YouTubeAudioPublisher(provider=self.publisher)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_manual_package_generation_on_unsupported_direct_upload(self):
        res = self.audio_pub.publish_track(
            video_id="zP0kOyucuMA",
            locale="ta-IN",
            audio_path="nonexistent.wav",
            srt_path="nonexistent.srt",
            title="Lesson 01 - Tamil",
            description="Tamil audio track",
            output_dir=self.test_dir
        )
        # Must gracefully fall back to MANUAL_PACKAGE_READY and never falsely claim AUTOMATED_PUBLISHED
        self.assertEqual(res.status, "MANUAL_PACKAGE_READY")
        self.assertTrue(os.path.exists(res.package_dir))
        self.assertTrue(os.path.exists(res.instructions_file))

    def test_direct_packager_metadata_and_instructions(self):
        res = self.publisher.generate_manual_package(
            video_id="x-7RglvLPVw",
            language="hi-IN",
            audio_path="dummy.wav",
            srt_path="dummy.srt",
            title="Lesson 02 - Hindi",
            description="Hindi audio track",
            output_dir=self.test_dir
        )
        self.assertEqual(res.status, "MANUAL_PACKAGE_READY")
        with open(res.instructions_file, "r", encoding="utf-8") as f:
            instr = f.read()
        self.assertIn("YouTube Studio Manual Audio Track Upload Instructions", instr)
        self.assertIn("https://studio.youtube.com/video/x-7RglvLPVw/translations", instr)

if __name__ == "__main__":
    unittest.main()
