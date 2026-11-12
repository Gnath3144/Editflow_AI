"""
Channel Management and Identity Verification Module.
Ensures that the authenticated Google session exactly matches the target YouTube channel
before any publishing or modification operations are permitted.
"""

import logging
from typing import Optional, Tuple

from googleapiclient.discovery import Resource

from database.models import ChannelInfo

logger = logging.getLogger(__name__)


class ChannelManager:
    """Manages channel verification and metadata queries."""

    def __init__(self, youtube_service: Resource, expected_channel_id: Optional[str] = None):
        self.youtube = youtube_service
        self.expected_channel_id = expected_channel_id
        self.current_channel: Optional[ChannelInfo] = None

    def fetch_primary_channel(self) -> Tuple[bool, Optional[ChannelInfo], str]:
        """Fetches the authenticated user's primary channel information."""
        if not self.youtube:
            return False, None, "YouTube service is not connected."

        try:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                mine=True
            )
            response = request.execute()

            items = response.get("items", [])
            if not items:
                return False, None, "No YouTube channel found for this Google account."

            primary = items[0]
            channel_id = primary.get("id", "")
            snippet = primary.get("snippet", {})
            stats = primary.get("statistics", {})

            thumbnails = snippet.get("thumbnails", {})
            thumb_url = thumbnails.get("default", {}).get("url") if thumbnails else None

            channel_info = ChannelInfo(
                channel_id=channel_id,
                channel_title=snippet.get("title", ""),
                custom_url=snippet.get("customUrl"),
                subscriber_count=int(stats.get("subscriberCount", 0)),
                video_count=int(stats.get("videoCount", 0)),
                thumbnail_url=thumb_url,
            )
            self.current_channel = channel_info

            # Strict security verification against expected channel ID
            if self.expected_channel_id and channel_id != self.expected_channel_id:
                msg = (
                    f"SECURITY ALERT: Channel ID mismatch! Expected '{self.expected_channel_id}', "
                    f"but authenticated channel is '{channel_id}' ('{channel_info.channel_title}'). "
                    f"Publishing blocked."
                )
                logger.critical(msg)
                return False, channel_info, msg

            logger.info("Channel verified: %s (ID: %s)", channel_info.channel_title, channel_id)
            return True, channel_info, "Channel verified successfully."

        except Exception as e:
            logger.error("Failed to query channel info: %s", e)
            return False, None, f"YouTube API error: {str(e)}"

    def verify_target_channel(self) -> Tuple[bool, str]:
        """Returns True if the authenticated session matches the expected channel."""
        success, info, msg = self.fetch_primary_channel()
        if not success:
            return False, msg
        return True, f"Verified as {info.channel_title} ({info.channel_id})"
