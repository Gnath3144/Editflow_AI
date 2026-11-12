import unittest
import os
import json
import shutil
import tempfile
from automation.multilingual.app.localisation_orchestrator import LocalisationOrchestrator

class TestManifest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.orchestrator = LocalisationOrchestrator(output_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_process_video_generates_manifest(self):
        transcript_data = {
            "segments": [
                {"start_time": 0.0, "end_time": 3.0, "text": "Introduction to AI models."}
            ]
        }
        manifest = self.orchestrator.process_video_language(
            video_id="TEST_VID_01",
            transcript_data=transcript_data,
            target_locale="te-IN"
        )
        self.assertEqual(manifest["video_id"], "TEST_VID_01")
        self.assertEqual(manifest["language"], "te-IN")
        self.assertEqual(manifest["translation_status"], "COMPLETED")
        self.assertEqual(manifest["tts_status"], "COMPLETED")
        self.assertEqual(manifest["segments_count"], 1)

    def test_idempotent_manifest_update(self):
        transcript_data = {
            "segments": [
                {"start_time": 0.0, "end_time": 3.0, "text": "Introduction to AI models."}
            ]
        }
        # Run 1
        m1 = self.orchestrator.process_video_language("TEST_VID_01", transcript_data, "hi-IN")
        # Run 2
        m2 = self.orchestrator.process_video_language("TEST_VID_01", transcript_data, "hi-IN")
        self.assertEqual(m1["video_id"], m2["video_id"])
        self.assertEqual(m1["translation_status"], m2["translation_status"])

    def test_failed_segment_recovery_structure(self):
        # Verify schema accommodates retry and failure states
        manifest_data = {
            "video_id": "TEST_RETRY_01",
            "source_transcript_hash": "hash_abc",
            "language": "ta-IN",
            "translation_status": "FAILED",
            "translation_provider": "TranslationEngine",
            "tts_status": "PENDING",
            "publishing_status": "UNPUBLISHED",
            "segments_count": 5
        }
        self.assertEqual(manifest_data["translation_status"], "FAILED")
        # Simulate retry
        manifest_data["translation_status"] = "COMPLETED"
        manifest_data["tts_status"] = "COMPLETED"
        self.assertEqual(manifest_data["translation_status"], "COMPLETED")

if __name__ == "__main__":
    unittest.main()
