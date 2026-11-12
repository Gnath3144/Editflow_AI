"""
Transcription Worker Implementation
"""
from core.logging.logger import get_logger

logger = get_logger("editflow.workers.transcription_worker")

class TranscriptionWorker:
    def __init__(self):
        self.name = "transcription_worker"

    def run(self, job_data: dict) -> dict:
        logger.info(f"Running worker transcription_worker...")
        return {"status": "COMPLETED", "worker": self.name}
