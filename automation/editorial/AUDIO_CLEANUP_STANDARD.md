# Audio Cleanup and Mastering Standard
## Broadcast-Grade Acoustic Processing Specification

---

## 1. Audio Processing Pipeline

All mastered lessons must undergo strict sequential DSP processing via FFmpeg / SoX:

```
Raw Audio Input (48 kHz / 44.1 kHz, Stereo/Mono)
     │
     ▼
[Step 1: Highpass Filter]  ── 80 Hz, 18 dB/octave (Eliminates HVAC rumble, mic desk thumps)
     │
     ▼
[Step 2: Spectral Denoise] ── Dynamic thresholding (-20 dB to -25 dB stationary noise reduction)
     │
     ▼
[Step 3: Surgical EQ]      ── Notch filter resonant frequencies (typically 250 Hz - 450 Hz)
     │
     ▼
[Step 4: Vocal Presence]   ── Broad gentle peak (+2.5 dB @ 3.2 kHz, Q=1.2) for speech crispness
     │
     ▼
[Step 5: Dynamic Control]  ── 2.5:1 ratio, attack 15ms, release 120ms, threshold -18 dBFS
     │
     ▼
[Step 6: Loudness Normalization] ── ITU-R BS.1770-4: Target -16.0 LUFS, Max True Peak -1.5 dBTP
     │
     ▼
Final Broadcast Master (48 kHz, 24-bit PCM / 320 kbps AAC)
```

---

## 2. Hard Acoustic Constraints

- **Integrated Loudness:** `-16.0 LUFS` (Permissible tolerance: `±0.5 LUFS`).
- **Maximum True Peak:** `-1.5 dBTP` (Prevents inter-sample clipping upon YouTube AAC transcoding).
- **Loudness Range (LRA):** Must not exceed `6.0 LU` across any single master lesson.
- **Signal-to-Noise Ratio (SNR):** Master audio must achieve `≥ 38 dB SNR`.
- **Phase Alignment:** Dual mono centered; phase correlation `r ≥ 0.95`.\n