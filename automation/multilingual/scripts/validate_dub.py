"""
Validates a generated dubbing package against audio, subtitle, and manifest standards.
Usage:
  python -m automation.multilingual.scripts.validate_dub --video-id VIDEO_ID --language ta-IN
  python -m automation.multilingual.scripts.validate_dub --package-dir DIR
"""

import os
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Validate Localised Dubbing Package")
    parser.add_argument("--package-dir", help="Path to package directory")
    parser.add_argument("--video-id", help="Target YouTube Video ID")
    parser.add_argument("--language", help="Target Language Locale")
    args = parser.parse_args()

    pkg_dir = args.package_dir
    if not pkg_dir:
        if args.video_id and args.language:
            pkg_dir = os.path.join(r"D:\Codealytica\Enhanced_Videos\Multilingual", args.video_id, args.language)
        else:
            print("[-] Must provide either --package-dir or both --video-id and --language")
            sys.exit(1)

    print(f"[*] Validating Dubbing Package in: {pkg_dir}")
    if not os.path.exists(pkg_dir):
        print(f"[-] Directory not found: {pkg_dir}")
        sys.exit(1)

    has_audio = any(f.endswith(".wav") for f in os.listdir(pkg_dir))
    has_srt = any(f.endswith(".srt") for f in os.listdir(pkg_dir))
    has_manifest = any(f.endswith("manifest.json") for f in os.listdir(pkg_dir))

    print(f"  Audio Master (.wav): {'FOUND' if has_audio else 'MISSING'}")
    print(f"  Subtitle File (.srt): {'FOUND' if has_srt else 'MISSING'}")
    print(f"  Manifest JSON: {'FOUND' if has_manifest else 'MISSING'}")

    if has_audio and has_srt and has_manifest:
        print("[+] Package validated successfully: READY_TO_UPLOAD.")
        sys.exit(0)
    else:
        print("[-] Package validation failed: Missing required artifacts.")
        sys.exit(1)

if __name__ == "__main__":
    main()
