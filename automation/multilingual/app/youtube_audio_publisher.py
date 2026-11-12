"""YouTube multi-track publisher and manual package generator."""
from typing import Optional
from ..providers.youtube_base import YouTubePublisherBase, ManualPackageResult

class YouTubeAudioPublisher:
    def __init__(self, provider: Optional[YouTubePublisherBase] = None):
        self.provider = provider

    def publish_track(self, video_id: str, locale: str, audio_path: str, srt_path: str,
                      title: str, description: str, output_dir: str) -> ManualPackageResult:
        if self.provider:
            uploaded = self.provider.upload_audio_track(video_id, locale, audio_path)
            if uploaded:
                return ManualPackageResult(
                    video_id=video_id,
                    language=locale,
                    package_dir=output_dir,
                    audio_file=audio_path,
                    subtitle_file=srt_path,
                    instructions_file="",
                    status="AUTOMATED_PUBLISHED"
                )
        # Fallback to standard manual package
        from ..providers.youtube_base import YouTubePublisherBase
        class DirectPackager(YouTubePublisherBase):
            def inventory_playlist(self, pid): return []
            def upload_audio_track(self, v, l, a): return False
        packager = DirectPackager()
        return packager.generate_manual_package(video_id, locale, audio_path, srt_path, title, description, output_dir)
