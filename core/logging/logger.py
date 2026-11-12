"""
Structured Central Logging
Writes logs to logs/editflow.log and console with standard formatting.
"""

import logging
import sys
from pathlib import Path
from ..filesystem.paths import PathManager

_LOGGER_INSTANCE = None

def get_logger(name: str = "editflow") -> logging.Logger:
    global _LOGGER_INSTANCE
    if _LOGGER_INSTANCE is not None:
        return _LOGGER_INSTANCE

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    paths = PathManager()
    log_file = paths.get_logs_dir() / "editflow.log"

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    _LOGGER_INSTANCE = logger
    return logger
