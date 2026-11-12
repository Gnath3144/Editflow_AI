"""
Day 01 Manifest Generation Script.
Scans the approved production folder, parses all metadata, and produces
DAY01_UPLOAD_MANIFEST.json.
"""

import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.video_scanner import VideoScanner
from core.validation import PreFlightValidator

SOURCE_DIR = r"D:\Codealytica\Enhanced_Videos\AIML_Day01\YOUTUBE_UPLOAD_READY_CORRECTED"
TARGET_PLAYLIST_ID = "PLIkXO9w8SPGg"
TARGET_PLAYLIST_TITLE = "Generative AI with Ollama: From Fundamentals to Hands-On Practice | Codealytica"


def main():
    scanner = VideoScanner(SOURCE_DIR)
    videos = scanner.scan_lessons()
    validator = PreFlightValidator()
    reports = validator.validate_batch(videos)

    manifest_data = {
        "series_title": TARGET_PLAYLIST_TITLE,
        "playlist_id": TARGET_PLAYLIST_ID,
        "channel_id": "UClHA7HX1h5eWwgfVjt8wb5A",
        "default_privacy": "private",
        "total_lessons": len(videos),
        "lessons": []
    }

    for idx, (v, rep) in enumerate(zip(videos, reports), start=1):
        lesson_dict = v.model_dump()
        lesson_dict["validation"] = {
            "is_valid": rep.is_valid,
            "errors": rep.errors,
            "warnings": rep.warnings,
            "is_duplicate": rep.is_duplicate
        }
        manifest_data["lessons"].append(lesson_dict)

    json_str = json.dumps(manifest_data, indent=2, ensure_ascii=False)

    # Attempt to write to file
    out_file = PROJECT_ROOT / "config" / "DAY01_UPLOAD_MANIFEST.json"
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(json_str)
        sys.stderr.write(f"Manifest written to {out_file}\n")
    except PermissionError:
        sys.stderr.write("Sandboxed file write denied. Printing manifest to stdout.\n")

    print("---MANIFEST_START---")
    print(json_str)
    print("---MANIFEST_END---")


if __name__ == "__main__":
    main()
