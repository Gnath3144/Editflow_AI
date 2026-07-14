#!/usr/bin/env bash
set -euo pipefail

# QMM AutoEdit — First-time setup
# Usage: ./setup.sh

echo "=== QMM AutoEdit Setup ==="

# Check prerequisites
command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || {
  echo "Error: Python 3.9+ is required (python3 or python not found on PATH)."
  exit 1
}
PY="$(command -v python3 || command -v python)"

command -v ffmpeg >/dev/null 2>&1 || {
  echo "Error: ffmpeg is required and was not found on PATH."
  echo "  macOS:   brew install ffmpeg"
  echo "  Ubuntu:  sudo apt install ffmpeg"
  echo "  Windows: winget install ffmpeg (or download from ffmpeg.org)"
  exit 1
}
command -v ffprobe >/dev/null 2>&1 || {
  echo "Error: ffprobe is required and was not found on PATH (it ships with ffmpeg)."
  exit 1
}

echo "Found: $("$PY" --version), $(ffmpeg -version | head -n1)"

# Environment
if [ -f .env.example ] && [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example — edit it only if you want a non-default caption font"
fi

# Optional dependency: faster-whisper (captions + --clip best-window scoring)
echo ""
echo "Installing optional dependency: faster-whisper (captions engine)..."
if "$PY" -m pip install --quiet faster-whisper; then
  echo "faster-whisper installed — captions are enabled."
  echo "Note: the first captioned run downloads the ~140MB 'base' Whisper model."
else
  echo "Warning: faster-whisper install failed. AutoEdit still works without it —"
  echo "         dead-air cutting and reframing run fine; captions are skipped."
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Run: python3 autoedit.py RAW.mp4"
echo "  2. Find your edited video next to the source (e.g. RAW_QMM_short.mp4)"
echo "  3. Using Claude Code? CLAUDE.md has all the context."
