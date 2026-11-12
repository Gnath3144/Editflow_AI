# Provider Implementation Guide

This directory defines the abstract contracts for external cloud and native processing services.

---

## 1. Provider Structure

- **`translation_base.py`**: Base class `TranslationProvider`.
- **`tts_base.py`**: Base class `TTSProvider`.
- **`audio_processing_base.py`**: Base class `AudioProcessingProvider` + `FFmpegAudioProcessor`.
- **`youtube_base.py`**: Base class `YouTubePublisherBase` + `generate_manual_package`.

---

## 2. Implementing a New Cloud Provider

To add a new provider (e.g. ElevenLabs TTS):
1. Subclass `TTSProvider`.
2. Implement `generate_speech`, `estimate_duration`, and `validate_credentials`.
3. Check `os.getenv("ELEVENLABS_API_KEY")`. If missing, return `TTSResult(status="NOT_CONFIGURED")`.
4. Register the new provider class in `__init__.py`.
