"""
Central Path Management Module
Resolves all project directories using pathlib.Path and cleanly handles Windows paths with spaces.
"""

import os
from pathlib import Path
from typing import Union

class PathManager:
    def __init__(self, root_override: Union[str, Path, None] = None):
        if root_override:
            self.root = Path(root_override).resolve()
        else:
            # Resolves D:\Codealytica\Editflow AI
            self.root = Path(__file__).resolve().parents[2]

        # Workspace Directories
        self.config_dir = self.root / "config"
        self.automation_dir = self.root / "automation"
        self.workers_dir = self.root / "workers"
        self.tools_dir = self.root / "tools"
        self.workflows_dir = self.root / "workflows"
        self.projects_dir = self.root / "projects"
        self.media_dir = self.root / "media"
        self.output_dir = self.root / "output"
        self.data_dir = self.root / "data"
        self.logs_dir = self.root / "logs"
        self.tests_dir = self.root / "tests"
        self.scripts_dir = self.root / "scripts"
        self.docs_dir = self.root / "docs"

        # External Data & Legacy Source Preservation
        self.raw_recordings_root = Path(r"D:\Codealytica")
        self.enhanced_videos_root = Path(r"D:\Codealytica\Enhanced_Videos")
        self.legacy_postproduction_root = Path(r"D:\Codealytica\Video_PostProduction")
        self.legacy_publisher_root = Path(r"D:\Codealytica\YouTube_Publisher")

        self.ensure_workspace_directories()

    def ensure_workspace_directories(self):
        for d in [self.config_dir, self.media_dir, self.output_dir, self.data_dir, self.logs_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def safe_path(self, path: Union[str, Path]) -> str:
        """Returns normalized string path properly escaped for Windows subprocess calls."""
        p = Path(path).resolve()
        return str(p)

    def get_job_state_dir(self) -> Path:
        p = self.data_dir / "job_state"
        p.mkdir(parents=True, exist_ok=True)
        return p

    def get_manifests_dir(self) -> Path:
        p = self.data_dir / "manifests"
        p.mkdir(parents=True, exist_ok=True)
        return p

    def get_logs_dir(self) -> Path:
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        return self.logs_dir
