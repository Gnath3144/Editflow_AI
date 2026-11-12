"""
Pre-Flight Validation Module for YouTube Uploads.
Ensures assets, metadata constraints, and channel requirements are strictly met
prior to invoking any YouTube API upload endpoints.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from database.database import DatabaseManager
from database.models import VideoMetadata, VideoPrivacyStatus

logger = logging.getLogger(__name__)

MAX_TITLE_CHARS = 100
MAX_DESC_CHARS = 5000
MAX_TAGS_CHARS = 500
MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024  # 2MB


@dataclass
class ValidationReport:
    video_path: str
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    is_duplicate: bool = False
    existing_video_id: Optional[str] = None


class PreFlightValidator:
    """Validates video assets and metadata before upload execution."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager

    def validate_video_metadata(self, meta: VideoMetadata, check_duplicate: bool = True) -> ValidationReport:
        """Runs pre-flight validation on a single VideoMetadata object."""
        report = ValidationReport(video_path=meta.video_path)

        # 1. Video file check
        v_path = Path(meta.video_path)
        if not v_path.exists():
            report.errors.append(f"Video file does not exist: {meta.video_path}")
            report.is_valid = False
        elif v_path.stat().st_size == 0:
            report.errors.append("Video file is empty (0 bytes).")
            report.is_valid = False

        # 2. Duplicate detection via SHA-256
        if check_duplicate and self.db and meta.file_hash_sha256:
            existing = self.db.find_completed_upload_by_hash(meta.file_hash_sha256)
            if existing:
                report.is_duplicate = True
                report.existing_video_id = existing.get("youtube_video_id")
                report.warnings.append(
                    f"Duplicate video detected! Already uploaded with YouTube ID '{report.existing_video_id}'."
                )

        # 3. Title length check
        if not meta.title or not meta.title.strip():
            report.errors.append("Video title is empty.")
            report.is_valid = False
        elif len(meta.title) > MAX_TITLE_CHARS:
            report.errors.append(
                f"Title exceeds {MAX_TITLE_CHARS} characters ({len(meta.title)} chars)."
            )
            report.is_valid = False

        # 4. Description length check
        if len(meta.description) > MAX_DESC_CHARS:
            report.errors.append(
                f"Description exceeds {MAX_DESC_CHARS} characters ({len(meta.description)} chars)."
            )
            report.is_valid = False

        # 5. Tags length check
        tags_str = ",".join(meta.tags)
        if len(tags_str) > MAX_TAGS_CHARS:
            report.warnings.append(
                f"Total tags string ({len(tags_str)} chars) exceeds recommended {MAX_TAGS_CHARS} chars."
            )

        # 6. Thumbnail check (optional but recommended)
        if meta.thumbnail_path:
            t_path = Path(meta.thumbnail_path)
            if not t_path.exists():
                report.warnings.append(f"Specified thumbnail not found: {meta.thumbnail_path}")
            elif t_path.stat().st_size > MAX_THUMBNAIL_BYTES:
                mb = t_path.stat().st_size / (1024 * 1024)
                report.errors.append(f"Thumbnail size ({mb:.2f}MB) exceeds 2MB YouTube limit.")
                report.is_valid = False
            elif t_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                report.errors.append(f"Thumbnail format '{t_path.suffix}' must be PNG or JPG.")
                report.is_valid = False
        else:
            report.warnings.append("No custom thumbnail found. YouTube will generate a default frame.")

        # 7. Subtitle check
        if meta.subtitle_path:
            s_path = Path(meta.subtitle_path)
            if not s_path.exists():
                report.warnings.append(f"Specified subtitle file not found: {meta.subtitle_path}")
            elif s_path.stat().st_size == 0:
                report.warnings.append("Subtitle file is empty (0 bytes).")
            elif s_path.suffix.lower() not in [".srt", ".vtt"]:
                report.errors.append(f"Subtitle format '{s_path.suffix}' must be .srt or .vtt.")
                report.is_valid = False

        # 8. Privacy Check
        if meta.privacy_status not in [VideoPrivacyStatus.PRIVATE, VideoPrivacyStatus.UNLISTED, VideoPrivacyStatus.PUBLIC]:
            report.errors.append(f"Invalid privacy status '{meta.privacy_status}'.")
            report.is_valid = False

        return report

    def validate_batch(self, videos: List[VideoMetadata]) -> List[ValidationReport]:
        """Validates a batch of video metadata records."""
        return [self.validate_video_metadata(v) for v in videos]
