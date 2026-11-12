# Contributing to QMM AutoEdit

Thanks for your interest in improving AutoEdit. This is a small, single-file
project by design — please keep contributions in that spirit.

## Development Setup

```bash
git clone https://github.com/Gnath3144/Editflow_AI.git
cd autoedit
./setup.sh
```

That installs the optional `faster-whisper` dependency and confirms `ffmpeg`/`ffprobe`
are on your `PATH`. There is no build step — `autoedit.py` runs directly:

```bash
python autoedit.py RAW.mp4
```

## Project Philosophy

- **One file, zero required dependencies.** `autoedit.py` is pure stdlib +
  `subprocess` calls to `ffmpeg`/`ffprobe`. `faster-whisper` is the only optional
  dependency and must stay optional — if it's missing, the tool should still run
  (silence-cut + reframe) and skip captions gracefully, never crash or silently no-op.
- **No GPU requirement.** Every change must keep the tool runnable CPU-only.
- **Keep it hackable.** Favor small, readable functions over abstractions. A new
  contributor should be able to read top-to-bottom and understand the whole pipeline.

## Branch / PR Workflow

1. Fork the repo and create a feature branch from `main`.
2. Make your change. Keep the diff focused — one concern per PR.
3. Test your change manually against a real video file for at least one mode
   (`short`, `longform`, `clean`) before opening a PR. There is no automated test
   suite yet; describe your manual test steps in the PR description.
4. Open a PR with a clear description of *why* the change is needed, not just *what*
   changed.

## Code Style

- Follow the existing style in `autoedit.py`: type-annotated function signatures,
  `@dataclass(frozen=True)` for simple value objects, small focused functions.
- Match PEP 8 conventions. No new dependencies unless clearly justified — this tool's
  value proposition is "just FFmpeg + one optional pip package."
- Keep functions small and single-purpose; the file is organized in clearly commented
  sections (ffmpeg helpers, silence detection, best-clip finder, transcription,
  render, orchestration, CLI) — add new code to the matching section.

## Reporting Issues

Please use the issue templates under `.github/ISSUE_TEMPLATE/`. Include:

- Your OS, Python version, and `ffmpeg -version` output
- The exact command you ran
- Whether `faster-whisper` is installed
- The full error output or unexpected behavior

## Using Claude Code

This repo ships a `CLAUDE.md` with the full architecture and command reference.
If you're using Claude Code to contribute, it will pick this up automatically —
start a session with `claude` in the repo root.
