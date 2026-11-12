"""
Autonomous CLI Publisher for Codealytica YouTube Publisher.
Executes end-to-end publishing pipeline: Video -> Thumbnail -> Captions -> Playlist
with real-time CLI progress, transfer speed, and ETA calculation.
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.authentication import AuthManager
from core.channel_manager import ChannelManager
from core.playlist_manager import PlaylistManager
from core.report_generator import ReportGenerator
from core.retry_manager import QuotaExceededError
from core.upload_engine import UploadEngine
from core.video_scanner import VideoScanner
from database.database import DatabaseManager
from database.models import JobStatus, UploadJob, VideoMetadata

SOURCE_DIR = r"D:\Codealytica\Enhanced_Videos\AIML_Day01\YOUTUBE_UPLOAD_READY_CORRECTED"
TARGET_CHANNEL_ID = "UClHA7HX1h5eWwgfVjt8wb5A"
TARGET_PLAYLIST_ID = "PLIkXO9w8SPGg"
TARGET_PLAYLIST_TITLE = "Generative AI with Ollama: From Fundamentals to Hands-On Practice | Codealytica"


def progress_bar_str(pct: float, width: int = 35) -> str:
    filled = int(width * (pct / 100.0))
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct:5.1f}%"


def main():
    print("\n" + "=" * 70)
    print("🎬  CODEALYTICA YOUTUBE PUBLISHER - CLI ENGINE")
    print("    Prepare Once. Upload Automatically. Publish Confidently.")
    print("=" * 70 + "\n")

    # 1. Initialize Database
    db = DatabaseManager()

    # 2. Authenticate
    auth = AuthManager()
    creds = auth.load_cached_credentials()
    if not creds or not creds.valid:
        print("❌ Error: Valid OAuth credentials not found in token.json.")
        sys.exit(1)

    service = auth.get_youtube_service()
    if not service:
        print("❌ Error: Unable to build YouTube API service.")
        sys.exit(1)

    # 3. Channel Verification
    print("🔍 [1/4] Verifying Channel Identity...")
    cm = ChannelManager(service, expected_channel_id=TARGET_CHANNEL_ID)
    ok, info, msg = cm.fetch_primary_channel()
    if not ok or not info:
        print(f"❌ Security Block: {msg}")
        sys.exit(1)

    print(f"✅ Verified Channel: {info.channel_title} (ID: {info.channel_id})")
    db.record_channel(info.channel_id, info.channel_title, info.custom_url)

    # 4. Playlist Verification
    print("\n📋 [2/4] Verifying Target Playlist...")
    pm = PlaylistManager(service)
    pl = pm.get_playlist_by_id(TARGET_PLAYLIST_ID)
    if not pl:
        print(f"❌ Target playlist {TARGET_PLAYLIST_ID} not found.")
        sys.exit(1)

    print(f"✅ Target Playlist: {pl.get('snippet', {}).get('title')} ({TARGET_PLAYLIST_ID}) [UNLISTED]")

    # 5. Scan Video Assets
    print(f"\n📂 [3/4] Scanning Video Lessons from: {SOURCE_DIR}...")
    scanner = VideoScanner(SOURCE_DIR)
    videos = scanner.scan_lessons()
    if not videos:
        print("❌ No valid lesson packages discovered.")
        sys.exit(1)

    print(f"✅ Discovered {len(videos)} approved lessons to publish in sequential order.\n")

    # 6. Initialize Upload Engine
    engine = UploadEngine(
        youtube_service=service,
        channel_id=TARGET_CHANNEL_ID,
        db_manager=db
    )

    jobs = [
        UploadJob(
            job_id=f"job_lesson_{v.lesson_number:02d}_{int(time.time())}",
            video_metadata=v,
            playlist_id=TARGET_PLAYLIST_ID,
            total_bytes=v.file_size_bytes
        )
        for v in videos
    ]

    # 7. Execute Publishing Queue
    print("=" * 70)
    print("🚀 [4/4] EXECUTING SEQUENTIAL PUBLISHING QUEUE (VIDEOS: PRIVATE)")
    print("=" * 70)

    completed_jobs = []

    for idx, job in enumerate(jobs, start=1):
        meta = job.video_metadata
        mb = meta.file_size_bytes / (1024 * 1024)
        print(f"\n──────────────────────────────────────────────────────────────────────")
        print(f"▶️  LESSON {meta.lesson_number:02d} / {len(jobs):02d}: {meta.title}")
        print(f"    File: {meta.video_file} ({mb:.2f} MB)")
        print(f"    Privacy: PRIVATE | Playlist: UNLISTED")
        print(f"──────────────────────────────────────────────────────────────────────")

        def _cli_progress(j: UploadJob, pct: float, speed_bps: float, eta_seconds: float):
            speed_mb = speed_bps / (1024 * 1024)
            mins = int(eta_seconds // 60)
            secs = int(eta_seconds % 60)
            eta_str = f"{mins:02d}:{secs:02d}" if eta_seconds > 0 else "--:--"
            bar = progress_bar_str(pct)
            sys.stdout.write(f"\r    {bar} | Speed: {speed_mb:4.2f} MB/s | ETA: {eta_str}")
            sys.stdout.flush()

        def _cli_log(msg: str):
            # Print stage logs cleanly
            if "Uploading custom thumbnail" in msg or "Uploading subtitle" in msg or "Adding video to playlist" in msg:
                print(f"\n    📦 {msg}")
            elif "Video published with ID" in msg:
                print(f"\n    🎉 {msg}")

        try:
            success = engine.process_upload_job(
                job,
                progress_callback=_cli_progress,
                log_callback=_cli_log
            )
            print() # newline after progress bar
            if success:
                print(f"    ✅ Status: COMPLETED | YouTube Link: {job.youtube_video_url}")
                completed_jobs.append(job)
            else:
                print(f"    ⚠️ Status: {job.status.value.upper()} | Error: {job.error_message}")
        except QuotaExceededError as qe:
            print(f"\n\n🛑 QUOTA EXHAUSTED: {qe}")
            print("    The upload ledger has safely recorded all progress.")
            print("    Run this command again tomorrow to resume remaining videos.")
            break
        except Exception as e:
            print(f"\n\n❌ Unexpected Error on Lesson {meta.lesson_number:02d}: {e}")

    # 8. Post-Publishing Reports
    print("\n" + "=" * 70)
    print("📊 GENERATING PUBLISHING AUDIT REPORTS")
    print("=" * 70)

    report_md = str(PROJECT_ROOT / "YOUTUBE_UPLOAD_REPORT.md")
    report_csv = str(PROJECT_ROOT / "YOUTUBE_UPLOAD_REPORT.csv")

    ReportGenerator.generate_markdown_report(
        completed_jobs,
        channel_name=info.channel_title,
        channel_id=TARGET_CHANNEL_ID,
        playlist_title=TARGET_PLAYLIST_TITLE,
        playlist_id=TARGET_PLAYLIST_ID,
        output_path=report_md
    )
    ReportGenerator.generate_csv_report(completed_jobs, report_csv)

    print(f"✅ Markdown Audit Report: {report_md}")
    print(f"✅ CSV Export Ledger:     {report_csv}")
    print("\n🎉 ALL TASKS COMPLETE!\n")


if __name__ == "__main__":
    main()
