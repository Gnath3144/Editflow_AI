"""Synchronized multilingual SRT and VTT subtitle generator."""
from typing import List, Dict, Any

class SubtitleGenerator:
    def _format_timestamp(self, seconds: float) -> str:
        ms = int((seconds % 1) * 1000)
        total_sec = int(seconds)
        hrs = total_sec // 3600
        mins = (total_sec % 3600) // 60
        secs = total_sec % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

    def generate_srt(self, segments: List[Dict[str, Any]], output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            for i, s in enumerate(segments, 1):
                start = self._format_timestamp(s.get("start_time", 0.0))
                end = self._format_timestamp(s.get("end_time", 0.0))
                text = s.get("translated_text", s.get("text", "")).strip()
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
