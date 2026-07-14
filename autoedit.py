"""QMM AutoEdit — free, CPU-only auto-editor. Our own AutoCut/Opus-Clip.

Two jobs, one engine:
  * SHORTEN  -> raw footage into an upload-ready 9:16 Short (dead-air cut, big
    karaoke captions, blurred-bg reframe, optional auto-pick best window).
  * POLISH LONG-FORM -> keep the full 16:9 video and full length, but tighten
    dead air + filler and burn captions. Editing, not just shortening.

Runs cloud-first on a no-GPU rig. Whisper captions are OPTIONAL: if faster-whisper
is absent the silence-cut + reframe still ships (graceful degrade, never a silent no-op).

Modes:
  short     9:16, dead-air cut, captions        (add --clip 60 to auto-pick best window)
  longform  keep aspect + full length, tighten dead air/filler, captions
  clean     keep aspect, dead-air cut only, no captions (fastest tighten)

Usage:
  python autoedit.py RAW.mp4                          # short (default)
  python autoedit.py RAW.mp4 --mode longform          # polish a whole long video
  python autoedit.py RAW.mp4 --mode short --clip 60    # best 60s -> Short
  python autoedit.py RAW.mp4 --mode clean              # just remove dead air
  python autoedit.py RAW.mp4 --out my_edit.mp4
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass

# --- tunables -------------------------------------------------------------
SILENCE_DB = -30.0          # below this = "silence" (dBFS)
MIN_SILENCE = 0.45          # a gap must last this long (s) to be cut
KEEP_PAD = 0.12             # padding kept on each side of a loud segment (s)
LONG_MIN_SILENCE = 0.90     # long-form is gentler: only cut the big dead gaps
LONG_KEEP_PAD = 0.22        # and leave more breathing room
MIN_KEEP = 0.30             # drop kept segments shorter than this (s)
W, H = 1080, 1920           # 9:16 canvas
FONT_NAME = os.environ.get("AUTOEDIT_FONT", "Impact")  # any installed font; libass substitutes if absent
GOLD = "&H0046BEF0"         # ASS = &HAABBGGRR ; gold
WHITE = "&H00F0F0F0"
BLACK_BG = "&H80000000"
WHISPER_MODEL = "base"      # tiny|base|small — base is the sweet spot on CPU/7GB


# --- ffmpeg helpers -------------------------------------------------------
def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def probe_duration(path: str) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "json", path]).stdout
    return float(json.loads(out)["format"]["duration"])


def has_audio(path: str) -> bool:
    out = run(["ffprobe", "-v", "error", "-select_streams", "a",
               "-show_entries", "stream=index", "-of", "json", path]).stdout
    return bool(json.loads(out).get("streams"))


# --- silence detection & keep-list ---------------------------------------
@dataclass(frozen=True)
class Segment:
    start: float
    end: float

    @property
    def dur(self) -> float:
        return self.end - self.start


def detect_silences(path: str, min_silence: float) -> list[Segment]:
    """Parse ffmpeg silencedetect -> list of silent Segments."""
    proc = subprocess.run(
        ["ffmpeg", "-i", path, "-af",
         f"silencedetect=noise={SILENCE_DB}dB:d={min_silence}", "-f", "null", "-"],
        capture_output=True, text=True)
    silences, start = [], None
    for line in proc.stderr.splitlines():
        if "silence_start:" in line:
            start = float(line.split("silence_start:")[1].strip())
        elif "silence_end:" in line and start is not None:
            end = float(line.split("silence_end:")[1].split("|")[0].strip())
            silences.append(Segment(start, end))
            start = None
    return silences


def keep_segments(silences: list[Segment], total: float, pad: float) -> list[Segment]:
    """Invert silences into the loud parts we keep, padded and de-slivered."""
    keeps, cursor = [], 0.0
    for s in silences:
        loud_end = s.start + pad
        if loud_end - cursor >= MIN_KEEP:
            keeps.append(Segment(cursor, min(loud_end, total)))
        cursor = max(cursor, s.end - pad)
    if total - cursor >= MIN_KEEP:
        keeps.append(Segment(cursor, total))
    return keeps or [Segment(0.0, total)]


# --- best-clip finder (Opus-Clip style, audio-energy) ---------------------
def find_best_window(path: str, window: float, total: float) -> Segment:
    """Pick the `window`-second span with the highest speech energy."""
    if window >= total:
        return Segment(0.0, total)
    proc = subprocess.run(
        ["ffmpeg", "-i", path, "-af",
         "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
         "-f", "null", "-"], capture_output=True, text=True)
    times, rms, t = [], [], 0.0
    for line in proc.stderr.splitlines():
        if "pts_time:" in line:
            t = float(line.split("pts_time:")[1].strip())
        elif "RMS_level=" in line:
            val = line.split("RMS_level=")[1].strip()
            if val not in ("-inf", "inf", "nan"):
                times.append(t); rms.append(float(val))
    if not rms:
        return Segment(0.0, min(window, total))
    best_start, best_score, start = 0.0, -1e9, 0.0
    while start + window <= total:
        score = sum(r for tt, r in zip(times, rms) if start <= tt < start + window)
        if score > best_score:
            best_score, best_start = score, start
        start += 1.0
    return Segment(best_start, best_start + window)


# --- transcription (optional) --------------------------------------------
@dataclass(frozen=True)
class Word:
    start: float
    end: float
    text: str


def transcribe(path: str) -> list[Word]:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("  [captions] faster-whisper not installed -> skipping captions")
        return []
    print(f"  [captions] transcribing with whisper '{WHISPER_MODEL}' (CPU)...")
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(path, word_timestamps=True, vad_filter=True)
    words: list[Word] = []
    for seg in segments:
        for w in (seg.words or []):
            txt = w.word.strip()
            if txt:
                words.append(Word(w.start, w.end, txt))
    return words


def _ass_time(t: float) -> str:
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build_ass(words: list[Word], path: str, play_w: int, play_h: int,
              group: int = 4) -> None:
    """Karaoke-pop captions: small word groups, current word highlighted gold."""
    fs = int(play_h * 0.052)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {play_w}
PlayResY: {play_h}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Base,{FONT_NAME},{fs},{WHITE},&H00101010,{BLACK_BG},1,4,2,2,60,60,{int(play_h*0.18)},1

[Events]
Format: Layer, Start, End, Style, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for i in range(0, len(words), group):
        grp = words[i:i + group]
        for j, cur in enumerate(grp):
            seg_end = grp[j + 1].start if j + 1 < len(grp) else grp[-1].end
            parts = []
            for k, w in enumerate(grp):
                tok = w.text.upper().replace("{", "").replace("}", "").strip(", ")
                parts.append(f"{{\\c{GOLD}}}{tok}{{\\c{WHITE}}}" if k == j else tok)
            lines.append(f"Dialogue: 0,{_ass_time(cur.start)},{_ass_time(seg_end)},"
                         f"Base,,0,0,0,,{' '.join(parts)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")


# --- render ---------------------------------------------------------------
def _select_expr(keeps: list[Segment]) -> str:
    return "+".join(f"between(t,{s.start:.3f},{s.end:.3f})" for s in keeps)


def render_cut(src: str, keeps: list[Segment], out: str) -> None:
    """Concatenate the kept segments back into one continuous clip."""
    expr = _select_expr(keeps)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
         "-vf", f"select='{expr}',setpts=N/FRAME_RATE/TB",
         "-af", f"aselect='{expr}',asetpts=N/SR/TB",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", out])


def render_final(cut: str, out: str, reframe: bool, ass: str | None) -> None:
    """Reframe to 9:16 blurred-bg (or keep aspect) and burn captions."""
    if reframe:
        chain = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
                 f"crop={W}:{H},boxblur=40:2[bg];"
                 f"[0:v]scale={W}:-2:force_original_aspect_ratio=decrease[fg];"
                 f"[bg][fg]overlay=(W-w)/2:(H-h)/2[v]"]
    else:
        chain = ["[0:v]copy[v]"]
    last = "[v]"
    if ass:
        esc = ass.replace("\\", "/").replace(":", "\\:")
        chain.append(f"{last}ass='{esc}'[vo]")
        last = "[vo]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", cut,
           "-filter_complex", ";".join(chain), "-map", last]
    if has_audio(cut):
        cmd += ["-map", "0:a", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", out]
    run(cmd)


# --- modes ----------------------------------------------------------------
@dataclass(frozen=True)
class Mode:
    reframe: bool        # 9:16 blurred-bg vs keep source aspect
    captions: bool       # burn karaoke captions
    min_silence: float   # silence gap threshold
    keep_pad: float      # breathing room around kept audio


MODES = {
    "short":    Mode(reframe=True,  captions=True,  min_silence=MIN_SILENCE,      keep_pad=KEEP_PAD),
    "longform": Mode(reframe=False, captions=True,  min_silence=LONG_MIN_SILENCE, keep_pad=LONG_KEEP_PAD),
    "clean":    Mode(reframe=False, captions=False, min_silence=LONG_MIN_SILENCE, keep_pad=LONG_KEEP_PAD),
}


# --- orchestration --------------------------------------------------------
def autoedit(src: str, out: str, mode_name: str, clip: float | None,
             captions_override: bool | None) -> None:
    if not os.path.exists(src):
        sys.exit(f"ERROR: not found: {src}")
    mode = MODES[mode_name]
    want_captions = mode.captions if captions_override is None else captions_override
    audio = has_audio(src)
    total = probe_duration(src)
    print(f"QMM AutoEdit [{mode_name}]  |  {os.path.basename(src)}  "
          f"({total:.1f}s, audio={audio})")

    work = tempfile.mkdtemp(prefix="qmm_autoedit_")
    stage = src

    # 1) optional best-clip crop (short mode only)
    if clip:
        win = find_best_window(src, clip, total) if audio else Segment(0.0, min(clip, total))
        print(f"  [clip] best {clip:.0f}s window @ {win.start:.1f}-{win.end:.1f}s")
        clipped = os.path.join(work, "clip.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{win.start:.3f}", "-i", src,
             "-t", f"{win.dur:.3f}", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "20", "-pix_fmt", "yuv420p", clipped])
        stage, total = clipped, win.dur

    # 2) dead-air cut
    if audio:
        sils = detect_silences(stage, mode.min_silence)
        keeps = keep_segments(sils, total, mode.keep_pad)
        cut_dur = sum(k.dur for k in keeps)
        tighter = 100 * (1 - cut_dur / total) if total else 0
        print(f"  [cut] {len(sils)} dead gaps removed -> {cut_dur:.1f}s ({tighter:.0f}% tighter)")
        cut = os.path.join(work, "cut.mp4")
        render_cut(stage, keeps, cut)
    else:
        print("  [cut] no audio -> keeping full footage (silence-cut skipped)")
        cut = stage

    # 3) captions on the cut clip (timing already correct post-cut)
    ass = None
    if want_captions and audio:
        words = transcribe(cut)
        if words:
            play_w, play_h = (W, H) if mode.reframe else (1920, 1080)
            ass = os.path.join(work, "caps.ass")
            build_ass(words, ass, play_w, play_h)
            print(f"  [captions] {len(words)} words burned")

    # 4) reframe + burn
    render_final(cut, out, mode.reframe, ass)
    print(f"BUILT  {out}  ({probe_duration(out):.1f}s)  <- upload-ready")


def main() -> None:
    ap = argparse.ArgumentParser(description="QMM AutoEdit — free auto-editor")
    ap.add_argument("src")
    ap.add_argument("--mode", choices=list(MODES), default="short")
    ap.add_argument("--out", default=None)
    ap.add_argument("--clip", type=float, default=None,
                    help="short mode: auto-pick best N-second window first (Opus-Clip)")
    cap = ap.add_mutually_exclusive_group()
    cap.add_argument("--captions", dest="captions", action="store_true", default=None)
    cap.add_argument("--no-captions", dest="captions", action="store_false")
    a = ap.parse_args()
    suffix = {"short": "_QMM_short", "longform": "_QMM_edit", "clean": "_QMM_clean"}[a.mode]
    out = a.out or os.path.splitext(a.src)[0] + suffix + ".mp4"
    autoedit(a.src, out, a.mode, a.clip, a.captions)


if __name__ == "__main__":
    main()
