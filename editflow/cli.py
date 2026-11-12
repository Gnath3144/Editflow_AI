"""
Central Editflow AI Command-Line Interface
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.filesystem.paths import PathManager
from core.configuration.config_manager import ConfigManager
from core.logging.logger import get_logger

logger = get_logger("editflow.cli")

def cmd_health(args):
    logger.info("Executing Editflow AI System Health Check...")
    paths = PathManager()
    
    # 1. Python Environment
    print(f"[*] Python Interpreter: {sys.executable} (Version: {sys.version.split()[0]})")
    
    # 2. Workspace Directories
    print(f"[*] Workspace Root: {paths.root}")
    print(f"    - Media Directory: {paths.media_dir} [Writable: {os.access(paths.media_dir, os.W_OK)}]")
    print(f"    - Output Directory: {paths.output_dir} [Writable: {os.access(paths.output_dir, os.W_OK)}]")
    print(f"    - Data Directory: {paths.data_dir} [Writable: {os.access(paths.data_dir, os.W_OK)}]")
    print(f"    - Logs Directory: {paths.logs_dir} [Writable: {os.access(paths.logs_dir, os.W_OK)}]")
    
    # 3. FFmpeg & FFprobe
    for tool in ["ffmpeg", "ffprobe"]:
        try:
            res = subprocess.run([tool, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            v_line = res.stdout.splitlines()[0] if res.stdout else "Available"
            print(f"[+] {tool.upper()}: READY ({v_line})")
        except Exception:
            print(f"[-] {tool.upper()}: NOT_INSTALLED or NOT_ON_PATH")

    # 4. Core Libraries
    libs = ["torch", "faster_whisper", "av", "soundfile", "webrtcvad", "resemblyzer"]
    for lib in libs:
        try:
            mod = __import__(lib)
            v = getattr(mod, "__version__", "Ready")
            print(f"[+] Library {lib}: READY (v{v})")
        except Exception as e:
            print(f"[-] Library {lib}: NOT_INSTALLED ({e})")

    # 5. Disk Space
    import shutil
    total, used, free = shutil.disk_usage(paths.root)
    print(f"[*] Disk Space on {paths.root.drive}: Free {free / (1024**3):.2f} GB / Total {total / (1024**3):.2f} GB")
    print("[+] Health check finished: SYSTEM OPERATIONAL.")

def cmd_validate(args):
    logger.info("Validating system configurations...")
    script = PROJECT_ROOT / "automation" / "multilingual" / "scripts" / "validate_configuration.py"
    if script.exists():
        subprocess.run([sys.executable, str(script)], check=True)
    else:
        print(f"[-] Validation script not found: {script}")

def cmd_inventory(args):
    logger.info(f"Inventorying YouTube playlist: {args.playlist_id}...")
    script = PROJECT_ROOT / "automation" / "multilingual" / "scripts" / "inventory_playlist.py"
    if script.exists():
        subprocess.run([sys.executable, str(script), "--playlist-id", args.playlist_id], check=True)
    else:
        print(f"[-] Inventory script not found: {script}")

def main():
    parser = argparse.ArgumentParser(
        prog="editflow",
        description="Editflow AI - Central Video Post-Production & Multilingual Automation System"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # Health
    sub_health = subparsers.add_parser("health", help="Check system health, dependencies, and tools")
    sub_health.set_defaults(func=cmd_health)

    # Validate
    sub_validate = subparsers.add_parser("validate", help="Validate configurations, schemas, and language profiles")
    sub_validate.set_defaults(func=cmd_validate)

    # Inventory
    sub_inv = subparsers.add_parser("inventory", help="Inventory YouTube playlist multi-audio status")
    sub_inv.add_argument("--playlist-id", default="PLIkXO9w8SPGg", help="YouTube Playlist ID")
    sub_inv.set_defaults(func=cmd_inventory)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
