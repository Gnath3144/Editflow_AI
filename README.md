# Editflow AI
## Autonomous Video Post-Production, Editorial Intelligence & Multilingual Localization System

**Editflow AI** is the central production workspace for Codealytica's technical masterclasses and AI video pipelines.

---

## Architecture Overview

```
D:\Codealytica\Editflow AI\
├── core/                              # Central framework (paths, config, logging, jobs, manifests)
├── automation/
│   ├── editorial/                     # Permanent Editorial Intelligence Engine (clean cuts, vocal mastering)
│   ├── multilingual/                  # Phase 13 Multilingual Localization Engine (12 languages)
│   ├── video_processing/              # FFmpeg rendering, NVENC 1080p CFR 30fps, EndScreen automation
│   ├── youtube/                       # YouTube publisher, OAuth authentication, playlist manager
│   └── thumbnail_generation/          # High-CTR authentic instructor thumbnail generator
├── workers/                           # Specialized async job workers (video, audio, transcription, editorial)
├── tools/                             # Multimedia analysis and quality control tools
├── config/                            # Consolidated JSON configurations (editorial, multilingual, youtube)
├── media/                             # Local working media and cache
├── output/                            # Processed video lessons, audio masters, and YouTube packages
├── data/                              # Manifests, metadata, and job state checkpoints
├── logs/                              # Structured logs (logs/editflow.log)
├── tests/                             # Unified unit and integration test suites
└── scripts/                           # PowerShell automation and health check scripts
```

---

## Quick Start

### 1. Check System Health:
```powershell
.\.venv\Scripts\python.exe -m editflow health
```

### 2. Validate All Configurations & Schemas:
```powershell
.\.venv\Scripts\python.exe -m editflow validate
```

### 3. Inventory YouTube Playlist:
```powershell
.\.venv\Scripts\python.exe -m editflow inventory --playlist-id PLIkXO9w8SPGg
```

### 4. Run Test Suites:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s automation/multilingual/tests -v
.\.venv\Scripts\python.exe -m unittest discover -s automation/editorial/tests -v
```

---

## Key Modules Documentation
- [Editorial Intelligence Engine](automation/editorial/README.md)
- [Multilingual Localisation Engine (Phase 13)](automation/multilingual/README.md)
- [System Architecture Guide](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [Operations Manual](docs/operations/OPERATIONS_GUIDE.md)
