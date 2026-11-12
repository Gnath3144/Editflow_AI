"""
Resumable Video Upload Engine for YouTube Data API v3.
Implements chunked uploading, progress tracking, rate calculation,
and atomic pipeline orchestration (Video -> Thumbnail -> Captions -> Playlist).
"""

import logging
import os
import time
from typing import Callable, Dict, Optional, Tuple
from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload

from core.caption_manager import CaptionManager
from core.playlist_manager import PlaylistManager
from core.retry_manager import QuotaExceededError, RetryManager
from core.thumbnail_manager import ThumbnailManager
from core.validation import PreFlightValidator
from database.database import DatabaseManager
from database.models import JobStatus, UploadJob, VideoMetadata, VideoPrivacyStatus

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 8 * 1024 * 1024  # 8MB chunk size for reliable broadband uploads


class UploadEngine:
    """Orchestrates resilient, chunked YouTube publishing."""

    def __init__(
        self,
        youtube_service: Resource,
        channel_id: str,
        db_manager: DatabaseManager,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        retry_manager: Optional[RetryManager] = None
    ):
        self.youtube = youtube_service
        self.channel_id = channel_id
        self.db = db_manager
        self.chunk_size = chunk_size
        self.retry_manager = retry_manager or RetryManager()
        self.validator = PreFlightValidator(db_manager)

        self.thumbnail_manager = ThumbnailManager(self.youtube, self.retry_manager)
        self.caption_manager = CaptionManager(self.youtube, self.retry_manager)
        self.playlist_manager = PlaylistManager(self.youtube, self.retry_manager)

        self._is_cancelled = False

    def cancel(self) -> None:
        """Flags the upload engine to abort pending or in-progress operations."""
        self._is_cancelled = True
        logger.warning("UploadEngine cancellation requested.")

    def process_upload_job(
        self,
        job: UploadJob,
        progress_callback: Optional[Callable[[UploadJob, float, float, float], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """Executes the full publishing pipeline for a single upload job."""
        self._is_cancelled = False
        meta = job.video_metadata

        def log(msg: str):
            logger.info("[%s] %s", meta.video_file, msg)
            if log_callback:
                log_callback(f"[{meta.video_file}] {msg}")

        log(f"Starting publishing pipeline for: {meta.title}")

        # Ensure job is registered in database ledger
        self.db.create_upload_job(job, self.channel_id)

        # 1. Pre-flight validation
        report = self.validator.validate_video_metadata(meta, check_duplicate=True)
        if not report.is_valid:
            err_msg = "; ".join(report.errors)
            job.status = JobStatus.FAILED
            job.error_message = err_msg
            self.db.update_job_status(job.job_id, JobStatus.FAILED, error_message=err_msg)
            self.db.log_event(job.job_id, "VALIDATION_FAILED", err_msg)
            log(f"Pre-flight validation failed: {err_msg}")
            return False

        # 2. Check for duplicate upload
        video_id = None
        if report.is_duplicate and report.existing_video_id:
            log(f"Duplicate video detected in ledger. Reusing existing YouTube video ID: {report.existing_video_id}")
            video_id = report.existing_video_id
            job.youtube_video_id = video_id
            job.youtube_video_url = f"https://youtu.be/{video_id}"
            job.status = JobStatus.UPLOADED
            self.db.update_job_status(
                job.job_id,
                JobStatus.UPLOADED,
                youtube_video_id=video_id,
                youtube_url=job.youtube_video_url
            )
            self.db.log_event(job.job_id, "UPLOAD_REUSED_DUPLICATE", f"Reused {video_id}")
        else:
            # 3. Perform Video Upload
            job.status = JobStatus.UPLOADING
            self.db.update_job_status(job.job_id, JobStatus.UPLOADING)
            self.db.log_event(job.job_id, "UPLOAD_STARTED", f"Uploading {meta.video_file}")

            body = {
                "snippet": {
                    "title": meta.title,
                    "description": meta.description,
                    "tags": meta.tags,
                    "categoryId": meta.category_id,
                    "defaultLanguage": meta.language,
                    "defaultAudioLanguage": meta.language
                },
                "status": {
                    "privacyStatus": getattr(meta.privacy_status, "value", str(meta.privacy_status)),
                    "selfDeclaredMadeForKids": meta.made_for_kids
                }
            }

            media = MediaFileUpload(
                meta.video_path,
                mimetype="video/mp4",
                chunksize=self.chunk_size,
                resumable=True
            )

            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            start_time = time.time()
            last_time = start_time
            last_bytes = 0

            try:
                while response is None:
                    if self._is_cancelled:
                        job.status = JobStatus.FAILED
                        job.error_message = "Upload cancelled by user."
                        self.db.update_job_status(job.job_id, JobStatus.FAILED, error_message=job.error_message)
                        log("Upload aborted by user.")
                        return False

                    status, response = request.next_chunk()
                    now = time.time()

                    if status:
                        bytes_uploaded = status.resumable_progress
                        total_bytes = status.total_size
                        progress_pct = (bytes_uploaded / total_bytes) * 100.0 if total_bytes > 0 else 0.0

                        # Calculate instantaneous speed (bytes/sec)
                        time_delta = now - last_time
                        speed_bps = 0.0
                        if time_delta > 0:
                            speed_bps = (bytes_uploaded - last_bytes) / time_delta

                        # Estimate remaining time
                        remaining_bytes = max(0, total_bytes - bytes_uploaded)
                        eta_seconds = (remaining_bytes / speed_bps) if speed_bps > 0 else 0.0

                        last_time = now
                        last_bytes = bytes_uploaded

                        job.bytes_uploaded = bytes_uploaded
                        job.total_bytes = total_bytes
                        job.upload_progress_pct = progress_pct

                        self.db.update_job_progress(job.job_id, bytes_uploaded, total_bytes, progress_pct)

                        if progress_callback:
                            progress_callback(job, progress_pct, speed_bps, eta_seconds)

                # Upload complete
                video_id = response.get("id")
                video_url = f"https://youtu.be/{video_id}"
                job.youtube_video_id = video_id
                job.youtube_video_url = video_url
                job.status = JobStatus.UPLOADED
                self.db.update_job_status(job.job_id, JobStatus.UPLOADED, youtube_video_id=video_id, youtube_url=video_url)
                self.db.log_event(job.job_id, "UPLOAD_SUCCESS", f"Video published with ID: {video_id}")
                log(f"Video uploaded successfully! ID: {video_id} ({video_url})")

            except QuotaExceededError as qe:
                job.status = JobStatus.FAILED
                job.error_message = str(qe)
                self.db.update_job_status(job.job_id, JobStatus.FAILED, error_message=str(qe))
                self.db.log_event(job.job_id, "QUOTA_EXCEEDED", str(qe))
                log(f"CRITICAL: {qe}")
                raise qe
            except Exception as e:
                err = f"Upload failed: {str(e)}"
                job.status = JobStatus.FAILED
                job.error_message = err
                self.db.update_job_status(job.job_id, JobStatus.FAILED, error_message=err)
                self.db.log_event(job.job_id, "UPLOAD_ERROR", err)
                log(err)
                return False

        # 4. Apply Custom Thumbnail
        if meta.thumbnail_path and os.path.exists(meta.thumbnail_path):
            log(f"Uploading custom thumbnail: {meta.thumbnail_file}")
            job.thumbnail_status = "uploading"
            thumb_ok, thumb_msg = self.thumbnail_manager.set_thumbnail(video_id, meta.thumbnail_path)
            job.thumbnail_status = "completed" if thumb_ok else "failed"
            self.db.update_job_asset_status(job.job_id, thumbnail_status=job.thumbnail_status)
            log(f"Thumbnail status: {job.thumbnail_status} ({thumb_msg})")

        # 5. Upload Closed Captions / Subtitles
        if meta.subtitle_path and os.path.exists(meta.subtitle_path):
            log(f"Uploading subtitle track: {meta.subtitle_file}")
            job.caption_status = "uploading"
            cap_ok, cap_msg = self.caption_manager.upload_caption(
                video_id=video_id,
                subtitle_path=meta.subtitle_path,
                language=meta.subtitle_language
            )
            job.caption_status = "completed" if cap_ok else "failed"
            self.db.update_job_asset_status(job.job_id, caption_status=job.caption_status)
            log(f"Subtitle status: {job.caption_status} ({cap_msg})")

        # 6. Add to Playlist
        if job.playlist_id:
            log(f"Adding video to playlist: {job.playlist_id} (position {meta.lesson_number - 1})")
            job.playlist_status = "adding"
            pl_ok, pl_msg = self.playlist_manager.add_video_to_playlist(
                playlist_id=job.playlist_id,
                video_id=video_id,
                position=meta.lesson_number - 1
            )
            job.playlist_status = "completed" if pl_ok else "failed"
            self.db.update_job_asset_status(job.job_id, playlist_status=job.playlist_status)
            log(f"Playlist status: {job.playlist_status} ({pl_msg})")

        # 7. Finalize Job Status
        job.status = JobStatus.COMPLETED
        self.db.update_job_status(job.job_id, JobStatus.COMPLETED)
        self.db.log_event(job.job_id, "JOB_COMPLETED", f"Video {video_id} completely configured.")
        log(f"All publishing steps completed for: {meta.title}")
        return True
