"""
Job Manager & State Persistence
Tracks lifecycle of video post-production tasks (editorial, multilingual, mastering, publishing).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from ..filesystem.paths import PathManager

class JobManager:
    def __init__(self, path_manager: Optional[PathManager] = None):
        self.paths = path_manager or PathManager()
        self.state_dir = self.paths.get_job_state_dir()

    def create_job(self, job_id: str, job_type: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        job_data = {
            "job_id": job_id,
            "job_type": job_type,
            "status": "INITIALIZED",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "checkpoints": []
        }
        self.save_job(job_data)
        return job_data

    def save_job(self, job_data: Dict[str, Any]):
        job_id = job_data["job_id"]
        job_data["updated_at"] = datetime.utcnow().isoformat()
        p = self.state_dir / f"{job_id}.json"
        with open(p, "w", encoding="utf-8") as f:
            json.dump(job_data, f, indent=2)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        p = self.state_dir / f"{job_id}.json"
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
