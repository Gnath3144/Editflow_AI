"""
Scans manifests and generates a comprehensive Markdown and JSON progress report.
Usage:
  python -m automation.multilingual.scripts.generate_localisation_report --video-id zP0kOyucuMA
  python -m automation.multilingual.scripts.generate_localisation_report --manifest-dir DIR
"""

import os
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate Multilingual Localisation Summary Report")
    parser.add_argument("--video-id", help="Filter by specific Video ID")
    parser.add_argument("--manifest-dir", default=r"D:\Codealytica\Enhanced_Videos\Multilingual", help="Directory containing manifests")
    parser.add_argument("--out", help="Output markdown report file")
    args = parser.parse_args()

    search_dir = args.manifest_dir
    print(f"[*] Scanning manifests in: {search_dir}")
    manifests = []

    if os.path.exists(search_dir):
        for root, _, files in os.walk(search_dir):
            for fname in files:
                if fname.endswith("manifest.json"):
                    p = os.path.join(root, fname)
                    try:
                        with open(p, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if not args.video_id or data.get("video_id") == args.video_id:
                                manifests.append(data)
                    except Exception:
                        pass

    md_content = """# Codealytica Multilingual Localisation Summary Report

| Video ID | Language | Translation | Speech (TTS) | Publishing Status | Segments |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    if manifests:
        for m in manifests:
            md_content += f"| {m.get('video_id')} | {m.get('language')} | {m.get('translation_status')} | {m.get('tts_status')} | {m.get('publishing_status')} | {m.get('segments_count', 0)} |\n"
    else:
        md_content += "| None | None | None | None | No manifests found | 0 |\n"

    out_file = args.out or os.path.join(search_dir, "LOCALISATION_REPORT.md")
    os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] Localisation report generated: {out_file}")
    print(md_content)

if __name__ == "__main__":
    main()
