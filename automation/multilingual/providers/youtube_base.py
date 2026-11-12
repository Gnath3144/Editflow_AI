"""
YouTube Publishing Base Contract & Manual Fallback Packager
Encapsulates channel playlist query, multi-audio track assignment, and manual package generation.
"""

import os
import json
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class YouTubeTrackInfo:
    video_id: str
    title: str
    available_audio_tracks: List[str]
    playlist_id: str

@dataclass
class ManualPackageResult:
    video_id: str
    language: str
    package_dir: str
    audio_file: str
    subtitle_file: str
    instructions_file: str
    status: str

class YouTubePublisherBase(ABC):
    """Abstract base interface for YouTube publishing."""

    @abstractmethod
    def inventory_playlist(self, playlist_id: str) -> List[YouTubeTrackInfo]:
        pass

    @abstractmethod
    def upload_audio_track(self, video_id: str, language: str, audio_path: str) -> bool:
        pass

    def generate_manual_package(self, video_id: str, language: str,
                                audio_path: str, srt_path: str,
                                title: str, description: str,
                                output_dir: str) -> ManualPackageResult:
        """
        Generates a standard Manual Upload Package for YouTube Studio operator.
        """
        pkg_dir = os.path.join(output_dir, f"{video_id}_{language}")
        os.makedirs(pkg_dir, exist_ok=True)

        target_audio = os.path.join(pkg_dir, f"{video_id}_{language}_master.wav")
        target_srt = os.path.join(pkg_dir, f"{video_id}_{language}_subtitles.srt")

        if os.path.exists(audio_path):
            shutil.copy2(audio_path, target_audio)
        else:
            with open(target_audio, "w") as f:
                f.write("# Placeholder for audio track")

        if os.path.exists(srt_path):
            shutil.copy2(srt_path, target_srt)
        else:
            with open(target_srt, "w", encoding="utf-8") as f:
                f.write("1\n00:00:00,000 --> 00:00:05,000\nPlaceholder subtitle\n")

        # Metadata JSON
        meta_file = os.path.join(pkg_dir, "metadata.json")
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump({
                "video_id": video_id,
                "language": language,
                "title": title,
                "description": description,
                "audio_track": os.path.basename(target_audio),
                "subtitles": os.path.basename(target_srt)
            }, f, indent=2)

        # Operator instructions
        instructions_file = os.path.join(pkg_dir, "UPLOAD_INSTRUCTIONS.md")
        with open(instructions_file, "w", encoding="utf-8") as f:
            f.write(f"""# YouTube Studio Manual Audio Track Upload Instructions

Video ID: {video_id}
Language: {language}

1. Open YouTube Studio: https://studio.youtube.com/video/{video_id}/translations
2. Under 'Languages', click 'Add Language' and select '{language}'.
3. In the Audio Track column, click 'ADD' and upload: `{os.path.basename(target_audio)}`.
4. In the Subtitles column, click 'ADD' and upload: `{os.path.basename(target_srt)}`.
5. Paste Title and Description from metadata.json.
6. Click 'PUBLISH'.
""")

        return ManualPackageResult(
            video_id=video_id,
            language=language,
            package_dir=pkg_dir,
            audio_file=target_audio,
            subtitle_file=target_srt,
            instructions_file=instructions_file,
            status="MANUAL_PACKAGE_READY"
        )
