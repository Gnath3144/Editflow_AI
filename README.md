# QMM AutoEdit

A free, CPU-only auto-editor that turns raw video into upload-ready 9:16 Shorts or
polished long-form cuts — automatic dead-air removal, word-by-word karaoke captions,
and blurred-background reframe. It's an open, no-paywall alternative to paid
Premiere auto-editing plugins, built on just **FFmpeg** and **faster-whisper**.
No GPU required — runs on any machine that can run FFmpeg.

## Features

- **Dead-air removal** — detects silence with `ffmpeg silencedetect` and stitches the
  loud parts back together, tighter and cleaner.
- **Karaoke-style burned-in captions** — word-by-word highlighted subtitles via
  `faster-whisper` + a hand-built `.ass` style (fully optional, degrades gracefully).
- **Blurred-background 9:16 reframe** — turns any source aspect ratio into an
  upload-ready vertical Short.
- **Best-window auto-clip** (`--clip N`) — Opus-Clip-style: scores audio energy and
  picks the highest-energy N-second window before editing.
- **Three modes** — `short` (Shorts/Reels/TikTok), `longform` (keep full length +
  aspect, just tighten and caption), `clean` (dead-air cut only, no captions).
- **Zero required dependencies** — pure Python stdlib + subprocess calls to FFmpeg.
  `faster-whisper` is optional and only needed for captions.

## Quick Start

```bash
git clone https://github.com/respectfulnrespected59-source/qmm-autoedit.git
cd qmm-autoedit
./setup.sh
python autoedit.py RAW.mp4
```

See [CLAUDE.md](CLAUDE.md) for detailed commands and architecture.

## Prerequisites

- **FFmpeg + ffprobe** on your `PATH` (hard requirement)
- **Python 3.9+**
- **Optional:** `faster-whisper` (`pip install faster-whisper`) for captions and the
  `--clip` best-window finder. Without it, AutoEdit still cuts dead air and reframes —
  it just skips captions with a printed notice.

## Usage

```bash
python autoedit.py RAW.mp4                          # short mode (default)
python autoedit.py RAW.mp4 --mode longform          # polish a whole long video
python autoedit.py RAW.mp4 --mode short --clip 60   # auto-pick best 60s window -> Short
python autoedit.py RAW.mp4 --mode clean             # just remove dead air, no captions
python autoedit.py RAW.mp4 --out my_edit.mp4         # custom output filename
python autoedit.py RAW.mp4 --no-captions            # force captions off
```

| Mode | Aspect | Dead-air cut | Captions | Best for |
|------|--------|--------------|----------|----------|
| `short` | 9:16, blurred-bg reframe | aggressive (0.45s+ gaps) | yes | TikTok / Reels / Shorts |
| `longform` | source aspect, full length | gentle (0.9s+ gaps) | yes | polished long-form uploads |
| `clean` | source aspect, full length | gentle (0.9s+ gaps) | no | fastest tighten pass, no transcription |

## How It Works

1. **(optional) best-window clip** — scores audio RMS energy per second and keeps the
   highest-energy `--clip N` window (short mode only).
2. **Silence detection -> cut** — `ffmpeg silencedetect` finds gaps; the loud segments
   are padded and concatenated back into one continuous clip.
3. **Transcribe the cut clip** — `faster-whisper` (CPU, `base` model, int8) runs word-level
   transcription on the *already-cut* audio so caption timing lines up post-cut.
4. **Karaoke captions** — word timestamps are grouped and written to a `.ass` subtitle
   file with the current word highlighted gold.
5. **Reframe + burn** — blurred-background 9:16 scale/crop (short mode) or pass-through
   aspect (longform/clean), captions burned in via the `ass` filter, final `libx264` encode.

## Configuration

```bash
cp .env.example .env
```

The only setting is `AUTOEDIT_FONT` (default `Impact`) — the font used for burned-in
captions. There are no API keys, accounts, or network dependencies to configure.

## Performance

AutoEdit runs roughly real-time on a modern CPU (silence-cut + reframe are fast;
transcription is the slower stage). It is not instant like a GPU-accelerated tool, but
it is fully hands-free — no manual scrubbing, no timeline editing, no paid plugin.

## Using with Claude Code

This project includes a `CLAUDE.md` that gives Claude Code full context on the
pipeline and every flag.

```bash
claude    # Start Claude Code — reads CLAUDE.md automatically
```

## License

MIT — see [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

Built by **Quantum Melanin Media (QMM)** — free, no-paywall creator tooling.
