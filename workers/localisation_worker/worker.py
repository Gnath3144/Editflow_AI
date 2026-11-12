"""
Localisation Worker Implementation
"""
from core.logging.logger import get_logger

logger = get_logger("editflow.workers.localisation_worker")

class LocalisationWorker:
    def __init__(self):
        self.name = "localisation_worker"

    def run(self, job_data: dict) -> dict:
        logger.info(f"Running worker localisation_worker...")
        return {"status": "COMPLETED", "worker": self.name}
