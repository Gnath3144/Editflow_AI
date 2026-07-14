# QMM AutoEdit

**Version:** 1.0 | **Stack:** Python 3.9+ (stdlib only) + FFmpeg | **No port (CLI tool)**

## What
A free, CPU-only auto-editor. Point it at a raw video and it cuts dead air,
burns word-by-word karaoke captions, and (for Shorts) reframes to a blurred-background
9:16 canvas — an open, no-paywall alternative to paid Premiere auto-editing plugins.

## Quick Start

```bash
./setup.sh                                   # check ffmpeg, install optional captions dep
python autoedit.py RAW.mp4                   # default: short mode (9:16 + captions)
```

## Commands

```bash
# Core usage
python autoedit.py RAW.mp4                          # short (9:16, dead-air cut, captions)
python autoedit.py RAW.mp4 --mode longform          # keep source aspect + full length, tighten + caption
python autoedit.py RAW.mp4 --mode clean             # dead-air cut only, no captions (fastest)
python autoedit.py RAW.mp4 --mode short --clip 60   # auto-pick best 60s window, then Short (Opus-Clip style)
python autoedit.py RAW.mp4 --out my_edit.mp4        # custom output path
python autoedit.py RAW.mp4 --no-captions            # force captions off in any mode
python autoedit.py RAW.mp4 --captions               # force captions on (requires faster-whisper)

# No test suite, linter, or build step exists — this is a single dependency-free script.
```

There is no package manager, build step, or test runner in this repo — `autoedit.py`
is the entire project. Verify any command change against the `argparse` block at the
bottom of `autoedit.py` before documenting it elsewhere.

## Architecture

```
autoedit.py   <- the whole project (one file, ~320 lines)
LICENSE       <- MIT
.env.example  <- documents the one optional env var (AUTOEDIT_FONT)
```

Pipeline inside `autoedit.py`, run in order by `autoedit()`:
1. **(optional) best-window clip** — `find_best_window()` scores audio RMS energy per
   second via `ffmpeg astats` and keeps the highest-energy N-second span (`--clip N`, short mode only).
2. **dead-air cut** — `detect_silences()` parses `ffmpeg -af silencedetect` output;
   `keep_segments()` inverts silences into padded "loud" segments; `render_cut()`
   concatenates them with `select`/`aselect` filters.
3. **transcription (optional)** — `transcribe()` runs `faster-whisper` (model `base`,
   CPU, int8) on the *already-cut* clip so caption timing lines up post-cut. Skips
   silently with a printed notice if `faster-whisper` is not installed.
4. **captions** — `build_ass()` writes a karaoke-style `.ass` subtitle file (4-word
   groups, current word highlighted gold).
5. **reframe + burn** — `render_final()` scales/crops to 1080x1920 with a blurred
   background (short mode) or keeps source aspect (longform/clean), burns captions via
   the `ass` ffmpeg filter, and encodes with `libx264`.

## Key Files

```
autoedit.py   Single-file CLI: argparse entrypoint (main), MODES dict (short/longform/clean),
              ffmpeg/ffprobe helpers, silence detection, best-window finder, faster-whisper
              transcription, ASS caption builder, final render.
.env.example  AUTOEDIT_FONT (caption font, default "Impact") — the only configurable value.
LICENSE       MIT.
```

## Configuration

All configuration is via one optional environment variable. See `.env.example`:

| Variable | Required | Description |
|----------|----------|--------------|
| `AUTOEDIT_FONT` | No (default `Impact`) | Font name passed into the ASS caption style; libass substitutes automatically if the font isn't installed. |

No API keys, no database, no network config — the tool only shells out to local
`ffmpeg`/`ffprobe` and (optionally) loads a local `faster-whisper` model on first caption run.

## Requirements

- **FFmpeg + ffprobe on PATH** (hard requirement — the tool exits with an error without them)
- **Python 3.9+** (stdlib only, zero required pip packages)
- **Optional:** `pip install faster-whisper` — needed for captions and the `--clip` best-window
  finder's speech scoring; first run downloads the ~140MB `base` model. Without it, silence-cut
  and reframe still run; captions are skipped with a printed notice (graceful degrade, never a
  silent no-op).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
