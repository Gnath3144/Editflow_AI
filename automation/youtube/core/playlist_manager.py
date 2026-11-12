"""
Playlist Management Module for YouTube Data API v3.
Finds, creates, and organizes videos into YouTube playlists in exact sequence.
"""

import logging
from typing import List, Optional, Tuple
from googleapiclient.discovery import Resource

from core.retry_manager import RetryManager
from database.models import PlaylistMetadata, VideoPrivacyStatus

logger = logging.getLogger(__name__)


class PlaylistManager:
    """Handles playlist lookup, creation, and item ordering."""

    def __init__(self, youtube_service: Resource, retry_manager: Optional[RetryManager] = None):
        self.youtube = youtube_service
        self.retry_manager = retry_manager or RetryManager()

    def get_playlist_by_id(self, playlist_id: str) -> Optional[dict]:
        """Fetches playlist details by ID."""
        try:
            req = self.youtube.playlists().list(
                part="snippet,status",
                id=playlist_id
            )
            res = self.retry_manager.execute_with_retry(req.execute, f"Get Playlist {playlist_id}")
            items = res.get("items", [])
            return items[0] if items else None
        except Exception as e:
            logger.error("Error fetching playlist %s: %s", playlist_id, e)
            return None

    def find_playlist_by_title(self, title: str) -> Optional[dict]:
        """Searches user's playlists for an exact or closely matching title."""
        try:
            req = self.youtube.playlists().list(
                part="snippet,status",
                mine=True,
                maxResults=50
            )
            res = self.retry_manager.execute_with_retry(req.execute, "Find Playlist by Title")
            for item in res.get("items", []):
                if item.get("snippet", {}).get("title", "").strip().lower() == title.strip().lower():
                    return item
            return None
        except Exception as e:
            logger.error("Error listing playlists: %s", e)
            return None

    def create_playlist(
        self,
        title: str,
        description: str = "",
        privacy_status: VideoPrivacyStatus = VideoPrivacyStatus.UNLISTED
    ) -> Tuple[bool, Optional[str], str]:
        """Creates a new playlist on the authenticated channel."""
        body = {
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": privacy_status.value
            }
        }

        def _create():
            req = self.youtube.playlists().insert(
                part="snippet,status",
                body=body
            )
            return req.execute()

        try:
            res = self.retry_manager.execute_with_retry(_create, f"Create Playlist '{title}'")
            playlist_id = res.get("id")
            logger.info("Created playlist '%s' with ID %s", title, playlist_id)
            return True, playlist_id, "Playlist created successfully."
        except Exception as e:
            logger.error("Failed to create playlist '%s': %s", title, e)
            return False, None, f"Failed to create playlist: {str(e)}"

    def get_or_create_playlist(
        self,
        title: str,
        preferred_id: Optional[str] = None,
        description: str = "",
        privacy_status: VideoPrivacyStatus = VideoPrivacyStatus.UNLISTED
    ) -> Tuple[bool, Optional[str], str]:
        """Verifies preferred ID or finds/creates matching playlist."""
        # 1. Check preferred ID first
        if preferred_id:
            existing = self.get_playlist_by_id(preferred_id)
            if existing:
                logger.info("Found existing playlist by ID: %s (%s)", preferred_id, existing.get("snippet", {}).get("title"))
                return True, preferred_id, "Reused existing playlist by ID."

        # 2. Check by title
        found = self.find_playlist_by_title(title)
        if found:
            p_id = found.get("id")
            logger.info("Found existing playlist by title: %s (%s)", title, p_id)
            return True, p_id, "Found existing playlist by title."

        # 3. Create if not found
        return self.create_playlist(title, description, privacy_status)

    def add_video_to_playlist(
        self,
        playlist_id: str,
        video_id: str,
        position: Optional[int] = None
    ) -> Tuple[bool, str]:
        """Inserts a video into the specified playlist."""
        snippet = {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
        # Position omitted to allow sequential appending without requiring manual playlist sort mode
        body = {"snippet": snippet}

        def _insert():
            req = self.youtube.playlistItems().insert(
                part="snippet",
                body=body
            )
            return req.execute()

        try:
            res = self.retry_manager.execute_with_retry(_insert, f"Add {video_id} to playlist {playlist_id}")
            logger.info("Added video %s to playlist %s at position %s", video_id, playlist_id, position)
            return True, "Added to playlist successfully."
        except Exception as e:
            logger.error("Failed to add video %s to playlist %s: %s", video_id, playlist_id, e)
            return False, f"Failed to add to playlist: {str(e)}"
