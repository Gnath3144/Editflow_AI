"""
Deploy Generated V2 Thumbnails to YouTube for Codealytica Day 01 Lessons.

1. Inspects recovered V2 thumbnails and creates THUMBNAIL_RECOVERY_MANIFEST.json.
2. Authenticates with YouTube Data API v3 using existing Codealytica credentials.
3. Verifies channel identity (UClHA7HX1h5eWwgfVjt8wb5A).
4. Verifies current video privacy status is UNLISTED.
5. Deploys custom thumbnails via service.thumbnails().set().
6. Verifies updated thumbnail URLs and confirms privacy remains UNLISTED.
7. Updates THUMBNAIL_RECOVERY_MANIFEST.json with live deployment metadata.
"""

import datetime
import json
import logging
import os
import sys
from pathlib import Path

from PIL import Image
from googleapiclient.http import MediaFileUpload

# Ensure YouTube_Publisher core is on sys.path
BASE_DIR = Path("D:/Codealytica/YouTube_Publisher")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.authentication import AuthManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("thumbnail_deployer")

EXPECTED_CHANNEL_ID = "UClHA7HX1h5eWwgfVjt8wb5A"
GENERATOR_DIR = BASE_DIR / "Thumbnail_Generator"
OUTPUT_DIR = GENERATOR_DIR / "output_portrait_v2"
MANIFEST_PATH = GENERATOR_DIR / "THUMBNAIL_RECOVERY_MANIFEST.json"

VIDEOS = [
    {
        "lesson_num": 1,
        "video_id": "zP0kOyucuMA",
        "title": "Install Local AI on Windows in 3 Minutes with Ollama | Zero Cloud Cost Setup",
        "headline": "RUN AI LOCALLY!",
        "badge": "NO CLOUD NEEDED",
        "file_name": "Lesson_01_zP0kOyucuMA_Thumbnail_v2.png"
    },
    {
        "lesson_num": 2,
        "video_id": "x-7RglvLPVw",
        "title": "Google Gemma 2B Architecture & Parameters Explained | Local LLM Deep Dive",
        "headline": "2 BILLION PARAMETERS?!",
        "badge": "GEMMA 2B",
        "file_name": "Lesson_02_x-7RglvLPVw_Thumbnail_v2.png"
    },
    {
        "lesson_num": 3,
        "video_id": "v0Ce7IYYCvU",
        "title": "Run Local LLMs on an 8GB RAM Laptop | Qwen 2.5 0.5B Setup Guide",
        "headline": "ONLY 8GB RAM?!",
        "badge": "RUN LOCAL AI",
        "file_name": "Lesson_03_v0Ce7IYYCvU_Thumbnail_v2.png"
    },
    {
        "lesson_num": 4,
        "video_id": "bUsxJjJW0uY",
        "title": "Local AI Benchmark & Windows Task Manager GPU Monitoring | Live LLM Test",
        "headline": "WATCH YOUR GPU!",
        "badge": "LIVE AI TEST",
        "file_name": "Lesson_04_bUsxJjJW0uY_Thumbnail_v2.png"
    },
    {
        "lesson_num": 5,
        "video_id": "ThBJnBpSjkI",
        "title": "Small vs Large AI Models: The Star Analogy Explained | Model Sizing Guide",
        "headline": "SMALL vs LARGE AI",
        "badge": "WHICH ONE?",
        "file_name": "Lesson_05_ThBJnBpSjkI_Thumbnail_v2.png"
    },
    {
        "lesson_num": 6,
        "video_id": "EjkFaIYaU60",
        "title": "Generative AI vs Traditional AI Explained + 3 Golden Rules | Day 01 Finale",
        "headline": "3 GOLDEN AI RULES",
        "badge": "MUST KNOW",
        "file_name": "Lesson_06_EjkFaIYaU60_Thumbnail_v2.png"
    }
]


def inspect_and_build_manifest():
    logger.info("Inspecting local V2 thumbnail files...")
    manifest = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "channel_id": EXPECTED_CHANNEL_ID,
        "playlist_id": "PLIkXO9w8SPGg",
        "thumbnails": []
    }

    all_valid = True
    for item in VIDEOS:
        file_path = OUTPUT_DIR / item["file_name"]
        entry = {
            "lesson_num": item["lesson_num"],
            "video_id": item["video_id"],
            "title": item["title"],
            "headline": item["headline"],
            "badge": item["badge"],
            "file_name": item["file_name"],
            "file_path": str(file_path),
            "file_exists": file_path.exists(),
            "integrity_valid": False,
            "resolution": None,
            "file_size_bytes": 0,
            "file_size_mb": 0.0,
            "generation_status": "PENDING",
            "youtube_deployment_status": "PENDING",
            "deployed_urls": {},
            "deployed_at": None,
            "privacy_status": None
        }

        if file_path.exists():
            entry["file_size_bytes"] = file_path.stat().st_size
            entry["file_size_mb"] = round(entry["file_size_bytes"] / (1024 * 1024), 3)
            try:
                with Image.open(file_path) as img:
                    img.verify()
                with Image.open(file_path) as img:
                    entry["resolution"] = f"{img.width}x{img.height}"
                    if img.width == 1280 and img.height == 720 and entry["file_size_bytes"] < 2 * 1024 * 1024:
                        entry["integrity_valid"] = True
                        entry["generation_status"] = "COMPLETED"
                    else:
                        all_valid = False
            except Exception as e:
                logger.error(f"Error validating {item['file_name']}: {e}")
                all_valid = False
        else:
            all_valid = False

        manifest["thumbnails"].append(entry)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    logger.info(f"Manifest written to {MANIFEST_PATH}. All files valid: {all_valid}")
    return manifest, all_valid


def deploy_thumbnails():
    manifest, all_valid = inspect_and_build_manifest()
    if not all_valid:
        logger.error("Validation failed for one or more thumbnail files. Aborting deployment.")
        sys.exit(1)

    logger.info("Connecting to YouTube Data API...")
    auth_mgr = AuthManager()
    youtube = auth_mgr.get_youtube_service()

    # 1. Verify channel
    channel_resp = youtube.channels().list(part="snippet", mine=True).execute()
    channels = channel_resp.get("items", [])
    if not channels:
        raise RuntimeError("No authenticated channel found.")
    actual_channel_id = channels[0]["id"]
    channel_title = channels[0]["snippet"]["title"]
    logger.info(f"Authenticated as Channel: '{channel_title}' ({actual_channel_id})")

    if actual_channel_id != EXPECTED_CHANNEL_ID:
        raise ValueError(f"Channel mismatch! Expected {EXPECTED_CHANNEL_ID}, got {actual_channel_id}")

    # 2. Process each video
    for entry in manifest["thumbnails"]:
        video_id = entry["video_id"]
        file_path = entry["file_path"]
        lesson_num = entry["lesson_num"]
        logger.info(f"\n--- Processing Lesson {lesson_num} (Video ID: {video_id}) ---")

        # Verify current status
        video_resp = youtube.videos().list(part="status,snippet", id=video_id).execute()
        items = video_resp.get("items", [])
        if not items:
            logger.error(f"Video {video_id} not found on YouTube!")
            continue

        curr_privacy = items[0]["status"]["privacyStatus"]
        logger.info(f"Current Privacy Status: {curr_privacy}")
        if curr_privacy.upper() != "UNLISTED":
            logger.warning(f"Video {video_id} is currently {curr_privacy}, not UNLISTED! Will preserve state.")
        entry["privacy_status"] = curr_privacy

        # Upload thumbnail
        logger.info(f"Uploading thumbnail: {file_path}")
        media = MediaFileUpload(file_path, mimetype="image/png", resumable=True)
        set_resp = youtube.thumbnails().set(videoId=video_id, media_body=media).execute()

        # Parse response
        resp_items = set_resp.get("items", [])
        if resp_items:
            thumb_info = resp_items[0]
            entry["deployed_urls"] = {
                k: thumb_info[k].get("url") for k in thumb_info if isinstance(thumb_info[k], dict)
            }
            entry["youtube_deployment_status"] = "DEPLOYED"
            entry["deployed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            logger.info(f"SUCCESS: Thumbnail set for {video_id}!")
            for res_key, res_url in entry["deployed_urls"].items():
                logger.info(f"  [{res_key}]: {res_url}")
        else:
            logger.error(f"Thumbnail upload response missing items for {video_id}: {set_resp}")
            entry["youtube_deployment_status"] = "FAILED"

        # Double check privacy remains unchanged
        post_resp = youtube.videos().list(part="status", id=video_id).execute()
        post_privacy = post_resp["items"][0]["status"]["privacyStatus"]
        entry["privacy_status"] = post_privacy
        logger.info(f"Confirmed Privacy Status post-upload: {post_privacy}")

    # Update manifest
    manifest["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest["all_deployed"] = all(e["youtube_deployment_status"] == "DEPLOYED" for e in manifest["thumbnails"])
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    logger.info(f"\n==========================================")
    logger.info(f"ALL DEPLOYMENTS COMPLETE: {manifest['all_deployed']}")
    logger.info(f"Manifest saved to: {MANIFEST_PATH}")
    logger.info(f"==========================================")


if __name__ == "__main__":
    deploy_thumbnails()
