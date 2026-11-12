"""
Codealytica YouTube Publisher
Desktop Application & Automation Engine Entry Point.

Tagline: Prepare Once. Upload Automatically. Publish Confidently.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("CodealyticaPublisher")

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.json"


def load_settings() -> dict:
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("Could not read settings.json: %s", e)
    return {}


def run_cli_scan(folder_path: str) -> None:
    from core.video_scanner import VideoScanner
    from core.validation import PreFlightValidator

    print(f"\n🔍 Scanning Video Assets in: {folder_path}\n" + "=" * 60)
    scanner = VideoScanner(folder_path)
    videos = scanner.scan_lessons()

    if not videos:
        print("❌ No valid lesson videos found in directory.")
        return

    print(f"✅ Discovered {len(videos)} approved lessons:")
    for v in videos:
        mb = v.file_size_bytes / (1024 * 1024)
        print(f"  [{v.lesson_number:02d}] {v.title}")
        print(f"       File: {v.video_file} ({mb:.2f} MB)")
        print(f"       Thumbnail: {v.thumbnail_file or 'None'} | Subtitles: {v.subtitle_file or 'None'}")
        print(f"       SHA256: {v.file_hash_sha256[:16]}...")
    print("=" * 60)


def run_cli_dry_run(folder_path: str) -> None:
    from core.video_scanner import VideoScanner
    from core.validation import PreFlightValidator
    from database.database import DatabaseManager

    print(f"\n🧪 Executing Pre-Flight Dry-Run Validation on: {folder_path}\n" + "=" * 60)
    scanner = VideoScanner(folder_path)
    videos = scanner.scan_lessons()
    db = DatabaseManager()
    validator = PreFlightValidator(db)
    reports = validator.validate_batch(videos)

    all_passed = True
    for v, rep in zip(videos, reports):
        status = "PASSED" if rep.is_valid else "FAILED"
        print(f"  Lesson {v.lesson_number:02d}: [{status}] - {v.title}")
        if rep.errors:
            all_passed = False
            for err in rep.errors:
                print(f"    ❌ ERROR: {err}")
        if rep.warnings:
            for w in rep.warnings:
                print(f"    ⚠️ WARNING: {w}")

    print("=" * 60)
    if all_passed:
        print(f"🎉 100% PRE-FLIGHT VALIDATION PASSED for {len(videos)} videos!")
        print("   All assets and metadata satisfy YouTube Data API v3 requirements.\n")
    else:
        print("❌ Some validation checks failed. Please address errors before publishing.\n")


def run_gui(default_folder: str) -> None:
    try:
        from PySide6.QtWidgets import QApplication
        from database.database import DatabaseManager
        from ui.main_window import MainWindow

        app = QApplication(sys.argv)
        app.setApplicationName("Codealytica YouTube Publisher")
        app.setOrganizationName("Codealytica")

        db = DatabaseManager()
        window = MainWindow(db_manager=db, default_folder=default_folder)
        window.show()

        sys.exit(app.exec())
    except ImportError as e:
        logger.error(
            "PySide6 is not installed in current Python environment (%s). "
            "Run 'pip install PySide6' or run with CLI mode: 'python app.py --dry-run'", e
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Codealytica YouTube Publisher: Automated YouTube Publishing Platform"
    )
    parser.add_argument(
        "--folder",
        type=str,
        default=None,
        help="Path to folder containing lesson videos"
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan and list video assets without opening GUI"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute pre-flight metadata and file constraint checks"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in command-line mode without GUI"
    )

    args = parser.parse_args()
    settings = load_settings()

    target_folder = (
        args.folder
        or settings.get("source_directory")
        or r"D:\Codealytica\Enhanced_Videos\AIML_Day01\YOUTUBE_UPLOAD_READY_CORRECTED"
    )

    if args.scan:
        run_cli_scan(target_folder)
    elif args.dry_run:
        run_cli_dry_run(target_folder)
    elif args.cli:
        print(f"Codealytica YouTube Publisher CLI Mode (Folder: {target_folder})")
        run_cli_dry_run(target_folder)
    else:
        run_gui(target_folder)


if __name__ == "__main__":
    main()
