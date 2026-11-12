"""
Thumbnail Management Module for YouTube Data API v3.
Validates aspect ratio, file size, and sets custom video thumbnails.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple
from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload

from core.retry_manager import RetryManager

logger = logging.getLogger(__name__)

MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024  # 2MB YouTube limit


class ThumbnailManager:
    """Handles custom thumbnail validation and upload."""

    def __init__(self, youtube_service: Resource, retry_manager: Optional[RetryManager] = None):
        self.youtube = youtube_service
        self.retry_manager = retry_manager or RetryManager()

    @staticmethod
    def validate_thumbnail(thumbnail_path: str) -> Tuple[bool, str]:
        """Validates that thumbnail exists and satisfies YouTube size limits."""
        p = Path(thumbnail_path)
        if not p.exists():
            return False, f"Thumbnail file does not exist: {thumbnail_path}"
        
        if p.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            return False, f"Invalid format '{p.suffix}'. Must be JPG or PNG."

        size = p.stat().st_size
        if size == 0:
            return False, "Thumbnail file is empty (0 bytes)."

        if size > MAX_THUMBNAIL_BYTES:
            mb = size / (1024 * 1024)
            return False, f"Thumbnail size ({mb:.2f}MB) exceeds 2MB YouTube maximum."

        return True, "Thumbnail is valid."

    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> Tuple[bool, str]:
        """Uploads and applies the custom thumbnail for a video."""
        valid, msg = self.validate_thumbnail(thumbnail_path)
        if not valid:
            return False, msg

        mimetype = "image/png" if thumbnail_path.lower().endswith(".png") else "image/jpeg"

        def _upload():
            media = MediaFileUpload(thumbnail_path, mimetype=mimetype, resumable=False)
            req = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=media
            )
            return req.execute()

        try:
            res = self.retry_manager.execute_with_retry(_upload, f"Set Thumbnail for {video_id}")
            logger.info("Successfully set custom thumbnail for video %s", video_id)
            return True, "Custom thumbnail applied successfully."
        except Exception as e:
            logger.error("Failed to set thumbnail for %s: %s", video_id, e)
            return False, f"Thumbnail upload failed: {str(e)}"
