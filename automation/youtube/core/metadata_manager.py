"""
Metadata Parser and Manager for YouTube Uploads.
Parses structured Markdown metadata files, extracts video titles, descriptions,
chapter timestamps, tags, hashtags, and formats clean descriptions suitable for YouTube.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from database.models import Chapter, VideoMetadata, VideoPrivacyStatus

logger = logging.getLogger(__name__)


class MetadataManager:
    """Parses and formats metadata from Markdown files and JSON manifests."""

    @staticmethod
    def parse_metadata_file(metadata_path: str) -> Dict[str, any]:
        """Parses a _METADATA.md file into structured fields."""
        p = Path(metadata_path)
        if not p.exists():
            return {}

        with open(p, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        data: Dict[str, any] = {
            "title": "",
            "description": "",
            "chapters": [],
            "tags": [],
            "hashtags": [],
            "raw_content": content,
        }

        # 1. High precision extractor for "## 1. Suggested YouTube Video Title"
        title_block = re.search(
            r"##\s*1\.\s*Suggested YouTube Video Title\s*```(?:text)?\s*([^\n\r]+?)\s*```",
            content,
            re.DOTALL | re.IGNORECASE
        )
        if title_block:
            data["title"] = title_block.group(1).strip()
        else:
            # Fallback patterns
            title_patterns = [
                r"\*\*Title\*\*:\s*([^\n\r]+)",
                r"Title:\s*([^\n\r]+)",
                r"^#\s+([^\n\r]+)",
            ]
            for pat in title_patterns:
                m = re.search(pat, content, re.MULTILINE | re.IGNORECASE)
                if m:
                    extracted = m.group(1).strip().strip('"\'*`')
                    if extracted and not extracted.lower().startswith("youtube upload metadata"):
                        data["title"] = extracted
                        break

        # Clean title length (YouTube limit is 100 characters)
        if len(data["title"]) > 100:
            data["title"] = data["title"][:97] + "..."

        # 2. High precision extractor for "## 2. YouTube Video Description"
        desc_block = re.search(
            r"##\s*2\.\s*YouTube Video Description\s*```(?:text)?\s*(.*?)\s*```",
            content,
            re.DOTALL | re.IGNORECASE
        )
        if desc_block:
            data["description"] = desc_block.group(1).strip()
        else:
            desc_match = re.search(
                r"(?:##\s*Description|\*\*Description\*\*|Description:)(.*?)(?:##\s*(?:Chapters|Timestamps|Tags)|$)",
                content,
                re.DOTALL | re.IGNORECASE
            )
            if desc_match:
                data["description"] = desc_match.group(1).strip()
            else:
                data["description"] = content.strip()

        # 3. Extract Chapters / Timestamps from either description or full content
        chapter_regex = re.compile(
            r"(?:^|\n)\s*\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\s*[-–:]?\s*([^\n\r]+)"
        )
        chapters: List[Dict[str, str]] = []
        for match in chapter_regex.finditer(data["description"]):
            ts = match.group(1).strip()
            if len(ts) == 4 and ts[1] == ":":
                ts = "0" + ts
            ch_title = match.group(2).strip().strip("-–* ")
            if ch_title and not any(c["timestamp"] == ts for c in chapters):
                chapters.append({"timestamp": ts, "title": ch_title})
        data["chapters"] = chapters

        # 4. Extract Tags and Hashtags
        hashtags = re.findall(r"#(\w+)", data["description"])
        extracted_tags: List[str] = []
        for ht in hashtags:
            if ht not in extracted_tags and len(ht) <= 50:
                extracted_tags.append(ht)

        tags_match = re.search(r"(?:Tags|\*\*Tags\*\*):\s*([^\n\r]+)", content, re.IGNORECASE)
        if tags_match:
            raw_tags = tags_match.group(1).split(",")
            for t in raw_tags:
                clean_tag = t.strip().strip('"\'`#')
                if clean_tag and len(clean_tag) <= 50 and clean_tag not in extracted_tags:
                    extracted_tags.append(clean_tag)

        # Truncate tags within 480 chars total
        final_tags: List[str] = []
        current_len = 0
        for tag in extracted_tags:
            if current_len + len(tag) + 1 <= 480:
                final_tags.append(tag)
                current_len += len(tag) + 1
        data["tags"] = final_tags

        # Clean forbidden YouTube HTML characters (< and >)
        data["title"] = data["title"].replace("<", "[").replace(">", "]")
        data["description"] = data["description"].replace("<", "[").replace(">", "]")
        return data

    @staticmethod
    def build_youtube_description(
        summary_text: str,
        chapters: List[Dict[str, str]],
        links: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        series_title: str = "Generative AI with Ollama: From Fundamentals to Hands-On Practice"
    ) -> str:
        """Assembles a clean, professional YouTube description."""
        # If summary_text already has the complete structured description from the text block, use it directly!
        if "TIMESTAMPS / CHAPTERS" in summary_text or "====================" in summary_text:
            if len(summary_text) > 5000:
                return summary_text[:4990] + "..."
            return summary_text

        parts: List[str] = []
        if summary_text:
            parts.append(summary_text.strip())

        parts.append("\n" + "=" * 40)
        parts.append(f"🎓 Course: {series_title}")
        parts.append("Organization: Codealytica")
        parts.append("=" * 40)

        if chapters:
            parts.append("\n📌 CHAPTERS & TIMESTAMPS:")
            for ch in chapters:
                parts.append(f"{ch['timestamp']} - {ch['title']}")

        if links:
            parts.append("\n🔗 IMPORTANT RESOURCES & LINKS:")
            for link in links:
                parts.append(f"• {link}")

        parts.append("\n💡 Stay connected with Codealytica for more deep-dive AI engineering tutorials!")
        parts.append("Subscribe to never miss an update.\n")

        if tags:
            top_hashtags = " ".join([f"#{t.replace(' ', '')}" for t in tags[:5]])
            parts.append(top_hashtags)

        full_desc = "\n".join(parts)
        if len(full_desc) > 5000:
            full_desc = full_desc[:4990] + "..."

        return full_desc
