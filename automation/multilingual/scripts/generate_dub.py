"""
CLI entrypoint to generate localized dubbing packages.
Usage:
  python -m automation.multilingual.scripts.generate_dub --video-id VIDEO_ID --language ta-IN [--output-dir DIR]
"""

import os
import sys
import json
import argparse

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from automation.multilingual.app.localisation_orchestrator import LocalisationOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Generate Multilingual Dubbing Package")
    parser.add_argument("--video-id", required=True, help="Target YouTube Video ID")
    parser.add_argument("--language", "--locale", dest="language", required=True, help="Target Locale (e.g. ta-IN, te-IN, hi-IN)")
    parser.add_argument("--transcript", help="Path to source transcript JSON")
    parser.add_argument("--output-dir", default=None, help="Output directory for dubbing artifacts")
    parser.add_argument("--dry-run", action="store_true", help="Simulate generation without writing audio")
    args = parser.parse_args()

    out_dir = args.output_dir or os.path.join(r"D:\Codealytica\Enhanced_Videos\Multilingual", args.video_id, args.language)
    print(f"[*] Generating Localised Dub for Video: {args.video_id} -> Language: {args.language}")
    print(f"[*] Output Directory: {out_dir}")

    transcript_data = {"segments": []}
    if args.transcript and os.path.exists(args.transcript):
        with open(args.transcript, "r", encoding="utf-8") as f:
            transcript_data = json.load(f)
    else:
        transcript_data = {
            "segments": [
                {"start_time": 0.0, "end_time": 4.5, "text": "Welcome to the Codealytica Generative AI and LLM masterclass."},
                {"start_time": 5.0, "end_time": 9.2, "text": "In this lesson we define our Pydantic BaseModel and run Ollama."}
            ]
        }

    orchestrator = LocalisationOrchestrator(output_dir=out_dir)
    manifest = orchestrator.process_video_language(args.video_id, transcript_data, args.language)
    print(f"[+] Dubbing generation complete. Manifest created:")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
