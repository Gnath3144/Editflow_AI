"""Core engine package initialization with resilient imports."""

try:
    from core.authentication import AuthManager, YOUTUBE_SCOPES
    from core.caption_manager import CaptionManager
    from core.channel_manager import ChannelManager
    from core.playlist_manager import PlaylistManager
    from core.retry_manager import QuotaExceededError, RetryManager
    from core.thumbnail_manager import ThumbnailManager
    from core.upload_engine import UploadEngine
except ImportError:
    AuthManager = None
    YOUTUBE_SCOPES = []
    CaptionManager = None
    ChannelManager = None
    PlaylistManager = None
    QuotaExceededError = Exception
    RetryManager = None
    ThumbnailManager = None
    UploadEngine = None

from core.metadata_manager import MetadataManager
from core.report_generator import ReportGenerator
from core.validation import PreFlightValidator, ValidationReport
from core.video_scanner import VideoScanner

__all__ = [
    "AuthManager",
    "CaptionManager",
    "ChannelManager",
    "MetadataManager",
    "PlaylistManager",
    "QuotaExceededError",
    "ReportGenerator",
    "RetryManager",
    "ThumbnailManager",
    "UploadEngine",
    "PreFlightValidator",
    "ValidationReport",
    "VideoScanner",
    "YOUTUBE_SCOPES",
]
