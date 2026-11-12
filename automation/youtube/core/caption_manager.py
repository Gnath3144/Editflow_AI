"""
Caption and Subtitle Management Module for YouTube Data API v3.
Validates subtitle files (.srt, .vtt) and uploads them to published YouTube videos.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple
from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload

from core.retry_manager import RetryManager

logger = logging.getLogger(__name__)


class CaptionManager:
    """Handles closed-caption / subtitle upload for videos."""

    def __init__(self, youtube_service: Resource, retry_manager: Optional[RetryManager] = None):
        self.youtube = youtube_service
        self.retry_manager = retry_manager or RetryManager()

    @staticmethod
    def validate_subtitle(subtitle_path: str) -> Tuple[bool, str]:
        """Validates that subtitle file exists, is non-empty, and has correct extension."""
        p = Path(subtitle_path)
        if not p.exists():
            return False, f"Subtitle file does not exist: {subtitle_path}"

        if p.suffix.lower() not in [".srt", ".vtt"]:
            return False, f"Invalid subtitle format '{p.suffix}'. Must be .srt or .vtt."

        if p.stat().st_size == 0:
            return False, "Subtitle file is empty (0 bytes)."

        return True, "Subtitle is valid."

    def upload_caption(
        self,
        video_id: str,
        subtitle_path: str,
        language: str = "en",
        name: str = "English",
        is_draft: bool = False
    ) -> Tuple[bool, str]:
        """Uploads closed caption track to YouTube video."""
        valid, msg = self.validate_subtitle(subtitle_path)
        if not valid:
            return False, msg

        body = {
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": name,
                "isDraft": is_draft
            }
        }

        def _upload():
            media = MediaFileUpload(subtitle_path, mimetype="*/*", resumable=False)
            req = self.youtube.captions().insert(
                part="snippet",
                body=body,
                media_body=media
            )
            return req.execute()

        try:
            res = self.retry_manager.execute_with_retry(_upload, f"Upload Subtitles for {video_id}")
            caption_id = res.get("id")
            logger.info("Successfully uploaded subtitles for video %s (Caption ID: %s)", video_id, caption_id)
            return True, f"Subtitles uploaded successfully (ID: {caption_id})."
        except Exception as e:
            logger.error("Failed to upload captions for %s: %s", video_id, e)
            return False, f"Caption upload failed: {str(e)}"
