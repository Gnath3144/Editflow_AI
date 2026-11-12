# Quality Control Standard
## Four-Dimensional Quality Acceptance Gate

Every generated lesson must pass all four quality validation tiers before rendering or publishing approval.

---

## 1. The Four Quality Tiers

### Tier 1: Acoustic & Loudness QC
- **Integrated Loudness:** `-16.0 LUFS ± 0.5 LUFS`.
- **True Peak:** `≤ -1.5 dBTP`.
- **LRA (Loudness Range):** `≤ 6.0 LU`.
- **SNR (Signal-to-Noise Ratio):** `≥ 38.0 dB`.
- **Silence at Head/Tail:** Head `0.20s - 0.40s`, Tail `0.50s - 1.00s`.

### Tier 2: Speaker Purity QC
- **Instructor Vocal Share:** `≥ 95.0%` of all voiced speech in the lesson.
- **Participant Conceptual Context:** `≤ 5.0%` of voiced speech.
- **Irrelevant Chatter / Noise:** `0.0%` permitted.

### Tier 3: Semantic & Editorial QC
- **Safety Window Compliance:** `100%` of splices buffered with ≥ 10ms micro-fades.
- **Word Truncation Rate:** `0.0%` (Zero clipped words).
- **Filler Word Elimination:** `≥ 90.0%` of Tier 1 non-semantic fillers removed.
- **Pedagogical Density:** Lesson content must maintain continuous topic focus.

### Tier 4: Technical & Video Encoding QC
- **Video Codec:** H.264 / NVENC CFR (Constant Frame Rate) 30.00 fps.
- **Resolution:** 1920 × 1080 (16:9).
- **Video Bitrate:** 4,500 kbps to 8,000 kbps (High profile, level 4.1).
- **Audio Codec:** AAC-LC 48 kHz, 320 kbps stereo.
- **Subtitle Sync:** 100% of subtitle cues aligned within ± 50ms of audio onset.\n