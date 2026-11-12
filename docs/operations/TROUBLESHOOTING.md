# Operations & Runtime Troubleshooting Guide

This guide details resolutions for common runtime errors, environmental issues, and operational roadblocks encountered during video post-production.

---

## 1. Environment & Dependency Issues

### Problem: `Program 'pip.exe' failed to run: An Application Control policy has blocked this file.`
- **Cause:** Windows AppLocker or Application Control policy restricting direct execution of unsigned virtual environment binaries.
- **Resolution:**
  - Avoid invoking `pip.exe` directly.
  - Use `python.exe -m pip ...` or copy pre-built `site-packages` using robocopy from a verified development cache.

### Problem: `DeprecationWarning: Please import 'binary_dilation' from the 'scipy.ndimage' namespace`
- **Cause:** Upstream `resemblyzer` package importing deprecated scipy modules.
- **Resolution:**
  - This is a non-blocking warning. Editflow AI's `automation/editorial/core/speaker_diarizer.py` patches runtime STFT execution safely.

---

## 2. Audio Processing & Mastering Issues

### Problem: `LoudnessComplianceError: Master audio loudness violates broadcast specification.`
- **Cause:** Audio segment dynamic range is unusually wide, causing single-pass filtergraph to deviate outside -16.0 ± 1.0 LUFS.
- **Resolution:**
  - Re-run with aggressive compression: check `automation/editorial/configuration/audio_quality_rules.json` and adjust the compressor threshold from `-24dB` to `-28dB`.
  - Ensure background noise gating is not cutting into quiet vocal tails.

### Problem: FFmpeg error: `Filtergraph parsing failed`
- **Cause:** Unescaped special characters or path spaces in complex filter arguments.
- **Resolution:**
  - Always use `PathManager` and ensure paths in `-filter_complex` use forward slashes (`/`) without Windows backslashes (`\`).

---

## 3. Multilingual Localisation Issues

### Problem: `TimingDriftError: Target audio exceeds 200 ms synchronization threshold.`
- **Cause:** The target translated text is substantially longer than the original English sentence, exceeding the 1.30x WSOLA speed limit.
- **Resolution:**
  - Enable concise translation mode in `automation/multilingual/config/translation_rules.json`.
  - Add abbreviation rules or increase the inter-segment gap borrow threshold.

---

## 4. YouTube Publishing Issues

### Problem: `HttpError 403: The user has exceeded the number of videos they may upload.`
- **Cause:** Daily YouTube channel upload quota reached.
- **Resolution:**
  - Wait 24 hours for Google YouTube API quota reset.
  - Editflow AI saves upload progress in `data/job_state/` allowing seamless resumption.
