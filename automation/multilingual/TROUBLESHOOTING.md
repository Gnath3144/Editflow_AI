# Troubleshooting & Operational Recovery

---

## 1. Common Issues & Resolutions

### Problem: `ProviderNotConfiguredException`
- **Cause:** Cloud API key environment variable is not set.
- **Solution:** Verify `AZURE_SPEECH_KEY`, `OPENAI_API_KEY`, etc. in your system environment or run scripts in mock/dry-run mode.

### Problem: Audio Drift / Speech Overlap
- **Cause:** Localized translation exceeded target video pause window.
- **Solution:** Inspect `segment_timing_validator.py` log; enable adaptive pacing or tighten translation verbosity.
