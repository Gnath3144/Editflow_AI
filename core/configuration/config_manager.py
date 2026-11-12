"""
Central Configuration Manager
Loads settings from .env and JSON configs across application, editorial, multilingual, and youtube.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from ..filesystem.paths import PathManager

class ConfigManager:
    def __init__(self, path_manager: Optional[PathManager] = None):
        self.paths = path_manager or PathManager()
        self.env_file = self.paths.root / ".env"
        self.env_vars: Dict[str, str] = {}
        self.load_env()

    def load_env(self):
        if self.env_file.exists():
            with open(self.env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        self.env_vars[k.strip()] = v.strip()
                        os.environ[k.strip()] = v.strip()

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.environ.get(key, self.env_vars.get(key, default))

    def load_json(self, relative_path: str) -> Dict[str, Any]:
        p = self.paths.config_dir / relative_path
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
