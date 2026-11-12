# Developer Onboarding & Architecture Guide

Welcome to the **Codealytica Editflow AI** developer onboarding guide. This document helps new engineers quickly understand the code structure, development workflow, and core systems.

---

## 1. Architecture Fundamentals

Editflow AI is structured around decoupled, autonomous subsystems:
1. **`core/`**: Shared platform services (PathManager, ConfigManager, Structured Logger, JobManager, ManifestManager).
2. **`editflow/`**: Primary CLI interface and diagnostic tools.
3. **`automation/editorial/`**: Editorial Intelligence Engine (Diarization, Pause Compaction, Loudness Mastering).
4. **`automation/multilingual/`**: Localisation Engine (Translation, Pacing, Voice Generation, Subtitles).
5. **`automation/youtube/`**: YouTube Data API v3 publishing and metadata synchronization.
6. **`automation/thumbnail_generation/`**: Branded portrait thumbnail generator V2.
7. **`workers/`**: Background worker daemon stubs.

---

## 2. Setting Up Your Development Environment

Follow [Windows Setup](../installation/WINDOWS_SETUP.md) or [Multi-Platform Installation](../installation/INSTALLATION.md). Once installed:

```powershell
# Verify installation
python -m editflow health

# Validate configurations
python -m editflow validate

# Run test suites
python -m unittest discover -s automation/editorial/tests
python -m unittest discover -s automation/multilingual/tests
```

---

## 3. Key Development Principles

- **Deterministic Execution:** No floating timestamps or random seeds in audio or image processing; outputs must be reproducible.
- **Fail Fast & Validate:** Input arguments must be validated against JSON schemas before long-running FFmpeg or Whisper tasks are launched.
- **Log Everything:** Use `core.logging.logger.get_logger(__name__)` with appropriate log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
- **Protect Raw Media:** Source recordings in `D:\Codealytica` must never be touched, modified, or overwritten.
