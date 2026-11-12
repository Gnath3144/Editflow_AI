"""
Video and Asset Scanner Module.
Discovers and inspects approved video files, thumbnails, subtitle tracks,
and metadata files from local course directories.
"""

import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from database.database import compute_file_sha256
from database.models import Chapter, VideoMetadata, VideoPrivacyStatus
from core.metadata_manager import MetadataManager

logger = logging.getLogger(__name__)


class VideoScanner:
    """Scans and indexes video assets for publishing."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)

    def scan_lessons(self, privacy: VideoPrivacyStatus = VideoPrivacyStatus.PRIVATE) -> List[VideoMetadata]:
        """Scans the root directory for Lesson folders and builds VideoMetadata models."""
        if not self.root_dir.exists():
            logger.error("Scan directory does not exist: %s", self.root_dir)
            return []

        results: List[VideoMetadata] = []

        # Find all Lesson_* directories or check if root_dir itself contains media
        lesson_dirs = sorted([
            d for d in self.root_dir.iterdir()
            if d.is_dir() and re.match(r"Lesson_\d+", d.name, re.IGNORECASE)
        ])

        if not lesson_dirs:
            # Fallback: scan root_dir itself
            lesson_dirs = [self.root_dir]

        for idx, folder in enumerate(lesson_dirs, start=1):
            # Extract lesson number from folder name if available
            num_match = re.search(r"Lesson_(\d+)", folder.name, re.IGNORECASE)
            lesson_num = int(num_match.group(1)) if num_match else idx

            # Find MP4 video
            mp4_candidates = [
                f for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() == ".mp4" and not f.name.startswith("._")
            ]
            if not mp4_candidates:
                logger.warning("No MP4 video found in %s", folder)
                continue

            # Prioritize clean/master files over draft/temp
            mp4_file = sorted(mp4_candidates, key=lambda f: f.stat().st_size, reverse=True)[0]
            file_size = mp4_file.stat().st_size
            file_hash = compute_file_sha256(str(mp4_file))

            # Find Thumbnail (Prefer _Selected_Frame.png or largest png/jpg)
            thumb_file: Optional[Path] = None
            thumb_candidates = [
                f for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg"]
            ]
            for t in thumb_candidates:
                if "_Selected_Frame" in t.name or "thumbnail" in t.name.lower():
                    thumb_file = t
                    break
            if not thumb_file and thumb_candidates:
                thumb_file = thumb_candidates[0]

            # Find Subtitles (.srt or .vtt)
            sub_file: Optional[Path] = None
            sub_candidates = [
                f for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() in [".srt", ".vtt"]
            ]
            for s in sub_candidates:
                if "_Subtitles" in s.name or "subtitles" in s.name.lower():
                    sub_file = s
                    break
            if not sub_file and sub_candidates:
                sub_file = sub_candidates[0]

            # Find Metadata (_METADATA.md or README.md)
            meta_file: Optional[Path] = None
            meta_candidates = [
                f for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() == ".md"
            ]
            for m in meta_candidates:
                if "_METADATA" in m.name or "metadata" in m.name.lower():
                    meta_file = m
                    break
            if not meta_file and meta_candidates:
                meta_file = meta_candidates[0]

            # Parse metadata
            parsed: Dict[str, any] = {}
            if meta_file:
                parsed = MetadataManager.parse_metadata_file(str(meta_file))

            # Default title if missing
            title = parsed.get("title") or f"Lesson {lesson_num:02d} | {mp4_file.stem}"
            
            # Format chapters
            chapters = [
                Chapter(timestamp=c["timestamp"], title=c["title"])
                for c in parsed.get("chapters", [])
            ]

            # Formatted full description
            desc = MetadataManager.build_youtube_description(
                summary_text=parsed.get("description", ""),
                chapters=parsed.get("chapters", []),
                tags=parsed.get("tags", []),
            )

            thumb_size = thumb_file.stat().st_size if thumb_file else 0

            meta = VideoMetadata(
                lesson_number=lesson_num,
                folder_name=folder.name,
                folder_path=str(folder),
                video_file=mp4_file.name,
                video_path=str(mp4_file),
                file_size_bytes=file_size,
                file_hash_sha256=file_hash,
                title=title,
                description=desc,
                tags=parsed.get("tags", []),
                category_id="27",  # Education
                privacy_status=privacy,
                made_for_kids=False,
                language="en",
                thumbnail_file=thumb_file.name if thumb_file else None,
                thumbnail_path=str(thumb_file) if thumb_file else None,
                thumbnail_size_bytes=thumb_size,
                subtitle_file=sub_file.name if sub_file else None,
                subtitle_path=str(sub_file) if sub_file else None,
                subtitle_language="en",
                chapters=chapters,
            )
            results.append(meta)

        results.sort(key=lambda m: m.lesson_number)
        logger.info("Scanned %d valid lesson videos from %s", len(results), self.root_dir)
        return results
