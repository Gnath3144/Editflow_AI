"""
Google OAuth 2.0 Authentication Manager for YouTube Data API v3.
Implements the desktop client authorization flow with persistent token refresh,
token caching, and channel identity verification.
"""

import json
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

logger = logging.getLogger(__name__)

# Required scopes for YouTube uploads, metadata setting, captions, and playlist management
YOUTUBE_SCOPES: List[str] = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]


class AuthManager:
    """Manages Google OAuth 2.0 credentials and YouTube service creation."""

    def __init__(self, client_secrets_file: Optional[str] = None, token_file: Optional[str] = None):
        base_dir = Path(__file__).resolve().parent.parent
        self.config_dir = base_dir / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.client_secrets_file = client_secrets_file or str(self.config_dir / "client_secret.json")
        self.token_file = token_file or str(self.config_dir / "token.json")
        self.credentials: Optional[Credentials] = None
        self.youtube_service: Optional[Resource] = None

    def is_client_secret_configured(self) -> bool:
        """Checks if a valid client_secret.json file exists."""
        p = Path(self.client_secrets_file)
        if not p.exists() or p.stat().st_size == 0:
            return False
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                return "installed" in data or "web" in data
        except Exception:
            return False

    def load_cached_credentials(self) -> Optional[Credentials]:
        """Loads cached OAuth credentials from token.json if valid or refreshable."""
        if os.path.exists(self.token_file):
            try:
                self.credentials = Credentials.from_authorized_user_file(self.token_file, YOUTUBE_SCOPES)
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    logger.info("Cached token expired. Refreshing OAuth token...")
                    self.credentials.refresh(Request())
                    self.save_credentials()
                if self.credentials and self.credentials.valid:
                    logger.info("Successfully loaded valid OAuth credentials from cache.")
                    return self.credentials
            except Exception as e:
                logger.warning("Failed to load cached credentials: %s", e)
                self.credentials = None
        return None

    def save_credentials(self) -> None:
        """Saves authorized credentials to token.json."""
        if self.credentials:
            Path(self.token_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, "w", encoding="utf-8") as f:
                f.write(self.credentials.to_json())
            logger.info("OAuth credentials securely cached to %s", self.token_file)

    def authenticate_desktop(self, port: int = 0) -> Tuple[bool, str]:
        """Runs the OAuth 2.0 Desktop local server flow."""
        if not self.is_client_secret_configured():
            return False, f"Missing or invalid client secret file at {self.client_secrets_file}"

        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file,
                scopes=YOUTUBE_SCOPES
            )
            # Opens default browser locally on user's machine
            self.credentials = flow.run_local_server(
                port=port,
                prompt="consent",
                success_message="Authentication successful! You can close this browser tab and return to Codealytica YouTube Publisher."
            )
            self.save_credentials()
            self.get_youtube_service()
            return True, "Successfully authenticated with YouTube Data API."
        except Exception as e:
            logger.error("Authentication failed: %s", e)
            return False, f"OAuth authentication error: {str(e)}"

    def get_youtube_service(self) -> Optional[Resource]:
        """Builds or returns the YouTube API service resource."""
        if self.youtube_service is not None:
            return self.youtube_service

        if not self.credentials:
            self.load_cached_credentials()

        if self.credentials and self.credentials.valid:
            self.youtube_service = build(
                "youtube",
                "v3",
                credentials=self.credentials,
                cache_discovery=False
            )
            return self.youtube_service
        return None

    def disconnect(self) -> bool:
        """Revokes token and clears local cached credentials."""
        self.credentials = None
        self.youtube_service = None
        if os.path.exists(self.token_file):
            try:
                os.remove(self.token_file)
                logger.info("Local token cache removed.")
                return True
            except OSError as e:
                logger.error("Error removing token file: %s", e)
                return False
        return True
