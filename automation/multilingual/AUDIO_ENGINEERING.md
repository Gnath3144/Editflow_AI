# Audio Engineering & Mastering Specification

---

## 1. Acoustic Standards for Localized Tracks

Every localized voice track must adhere to strict broadcast mastering specifications:

- **Integrated Loudness:** `-16.0 LUFS` (Tolerance: `±0.5 LUFS`).
- **Maximum True Peak:** `-1.5 dBTP` (Prevents inter-sample distortion upon AAC compression).
- **Loudness Range (LRA):** `≤ 6.0 LU`.
- **Signal-to-Noise Ratio (SNR):** `≥ 38.0 dB`.
- **Sample Rate:** `48,000 Hz` (48 kHz, 16-bit or 24-bit PCM).
- **Channels:** Dual Mono / Stereo Centered.

---

## 2. Time-Stretching & Pitch Preservation

When localized speech needs expansion or compression to fit video sync:
- Time stretching is performed via FFmpeg `atempo` or Rubber Band library.
- Formant and pitch preservation is mandatory.
- Acceleration factor must remain within `[0.85x, 1.15x]`. Any segment requiring $> 1.15x$ acceleration must trigger pause insertion or sentence rephrasing instead of unnatural high-speed delivery.
