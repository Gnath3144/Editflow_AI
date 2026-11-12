# Pause and Silence Management Policy
## Timing Thresholds, Micro-Fade Standards, and Pacing

---

## 1. Silence Classification Matrix

| Duration Range | Category | Context | Required Action |
| :--- | :--- | :--- | :--- |
| **0.00s – 0.30s** | Micro-pause | Normal inter-word spacing | **DO NOT TOUCH** |
| **0.30s – 0.80s** | Natural Cadence | Comma, semicolon, natural breath | **PRESERVE UNCHANGED** |
| **0.80s – 1.50s** | Pedagogical Pause | Slide reveal, complex code block | **PRESERVE** (Cap at 1.20s if static) |
| **1.50s – 3.00s** | Hesitation Silence | Searching for file, thinking | **SHORTEN to 0.40s** |
| **> 3.00s** | Dead Air / Stalled Demo | Waiting for download / open mic | **TRIM or CUT to 0.50s** |

---

## 2. Splice Micro-Fade Specification

Every splice where audio is trimmed or removed must apply an equal-power micro-fade:
- **Fade Out:** `10.0ms` Hann window curve.
- **Fade In:** `10.0ms` Hann window curve.
- This prevents transient DC-offset clicks and high-frequency pops at the waveform discontinuity.\n