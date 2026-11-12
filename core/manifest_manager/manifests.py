"""
Manifest Manager Module
Calculates cryptographic SHA-256 hashes and verifies manifest integrity across production stages.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional
from ..filesystem.paths import PathManager

class ManifestManager:
    def __init__(self, path_manager: Optional[PathManager] = None):
        self.paths = path_manager or PathManager()
        self.manifests_dir = self.paths.get_manifests_dir()

    def compute_sha256(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    def save_manifest(self, manifest_id: str, data: Dict[str, Any]) -> Path:
        out = self.manifests_dir / f"{manifest_id}.manifest.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return out

    def load_manifest(self, manifest_id: str) -> Optional[Dict[str, Any]]:
        p = self.manifests_dir / f"{manifest_id}.manifest.json"
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
