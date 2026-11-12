# 🎬 Codealytica YouTube Publisher

> **"Prepare Once. Upload Automatically. Publish Confidently."**

A production-ready desktop automation application and publishing engine for Windows 11. Designed to automate YouTube video publishing using the official **YouTube Data API v3** with OAuth 2.0 Desktop flow, eliminating fragile browser UI automation.

---

## 🌟 Key Capabilities

- **100% Official YouTube Data API v3**: Completely eliminates browser clicking, Chrome/Edge automation hurdles, and DOM fragility.
- **Atomic Multi-Stage Publishing Pipeline**:
  1. **Resumable Chunked Video Upload** (`8 MB` chunks with real-time transfer speed and ETA).
  2. **Custom 1080p Thumbnail Application** (`thumbnails.set` with < 2MB auto-validation).
  3. **Closed Captions & Subtitles** (`captions.insert` with `.srt` sync).
  4. **Automated Playlist Organization** (`playlistItems.insert` in exact lesson order).
- **Strict Channel Identity Guard**: Mandatory verification against Channel ID `UClHA7HX1h5eWwgfVjt8wb5A` (Codealytica) before any publishing operation is permitted.
- **Privacy First**: Strict default `PRIVATE` status for all video uploads and `UNLISTED` for course playlists.
- **SQLite Ledger & Idempotency**: Computes SHA-256 file hashes to prevent accidental duplicate uploads and save daily API quota.
- **Dual Interface**:
  - Modern Dark-Themed **PySide6 Desktop GUI** (JetBrains / VS Code aesthetic).
  - Headless **CLI Engine** (`--scan`, `--dry-run`, `--cli`).

---

## 📁 Project Architecture

```
D:\Codealytica\YouTube_Publisher\
├── config/
│   ├── settings.json                 # Global configurations & channel/playlist mappings
│   ├── DAY01_UPLOAD_MANIFEST.json    # Pre-computed 6-lesson manifest with metadata
│   ├── client_secret.json.example    # OAuth 2.0 template file
│   └── token.json                    # Cached OAuth refresh token (gitignored)
├── database/
│   ├── __init__.py
│   ├── models.py                     # VideoMetadata, PlaylistMetadata, UploadJob
│   └── database.py                   # SQLite upload ledger & SHA-256 duplicate detection
├── core/
│   ├── __init__.py
│   ├── authentication.py             # Google OAuth 2.0 Desktop InstalledAppFlow
│   ├── channel_manager.py            # Channel verification & security checks
│   ├── video_scanner.py              # Directory asset discovery (MP4, PNG, SRT, MD)
│   ├── metadata_manager.py           # Markdown parser & description/chapter builder
│   ├── upload_engine.py              # Resumable chunked uploader & pipeline orchestrator
│   ├── thumbnail_manager.py          # Custom thumbnail setter & validator
│   ├── caption_manager.py            # Closed captions (.srt) uploader
│   ├── playlist_manager.py           # Playlist lookup, creation & item sequence
│   ├── retry_manager.py              # Exponential backoff & quota error categorization
│   ├── validation.py                 # Pre-flight constraint validator
│   └── report_generator.py           # Post-publish Markdown and CSV report generator
├── ui/
│   ├── styles.py                     # Modern dark-theme QSS stylesheet
│   ├── dashboard.py                  # Metrics cards, channel badge & recent ledger
│   ├── authentication_page.py        # Client secret selection & OAuth authorization
│   ├── folder_page.py                # Video directory scanner table
│   ├── review_page.py                # Metadata inspector & Dry-Run validator
│   └── main_window.py                # Main window & sidebar navigation
├── scripts/
│   ├── setup.ps1                     # One-click environment installer (.venv + deps)
│   ├── launch.ps1                    # One-click desktop launcher
│   ├── build.ps1                     # PyInstaller standalone executable compiler
│   └── generate_manifest.py          # Manifest generator utility
├── tests/
│   └── test_publisher.py             # 100% passing unit tests
├── app.py                            # Main application entry point (GUI + CLI)
├── requirements.txt                  # Python dependencies
├── SETUP_GUIDE.md                    # Detailed Google Cloud OAuth setup guide
├── CONFIGURATION_GUIDE.md            # Settings and quota reference
├── UPLOAD_WORKFLOW.md                # Publishing procedure walkthrough
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Install Environment
Run PowerShell as standard user:
```powershell
cd "D:\Codealytica\YouTube_Publisher"
.\scripts\setup.ps1
```

### 2. Configure Google Cloud OAuth Credentials
1. Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) to enable **YouTube Data API v3** in Google Cloud Console.
2. Download the Desktop OAuth Client JSON and save it as:
   ```
   D:\Codealytica\YouTube_Publisher\config\client_secret.json
   ```

### 3. Run Pre-Flight Dry Run
Verify all Day 01 assets and metadata without consuming quota:
```powershell
.\.venv\Scripts\python.exe app.py --dry-run
```

### 4. Launch Desktop GUI
```powershell
.\scripts\launch.ps1
```

---

## 🎯 Day 01 Publishing Overview

- **Source Folder:** `D:\Codealytica\Enhanced_Videos\AIML_Day01\YOUTUBE_UPLOAD_READY_CORRECTED`
- **Target Channel:** `UClHA7HX1h5eWwgfVjt8wb5A` (`Codealytica`)
- **Target Playlist:** `PLIkXO9w8SPGg` (`Generative AI with Ollama: From Fundamentals to Hands-On Practice | Codealytica`)
- **Videos in Order:**
  1. `Install Local AI on Windows in 3 Minutes with Ollama | Zero Cloud Cost Setup`
  2. `Google Gemma 2B Architecture & Parameters Explained | Local LLM Deep Dive`
  3. `Run Local LLMs on an 8GB RAM Laptop | Qwen 2.5 0.5B Setup Guide`
  4. `Local AI Benchmark & Windows Task Manager GPU Monitoring | Live LLM Test`
  5. `Small vs Large AI Models: The Star Analogy Explained | Model Sizing Guide`
  6. `Generative AI vs Traditional AI Explained + 3 Golden Rules | Day 01 Finale`

---

## 🔒 Security & Privacy Commitments
- **Zero Browser Automation:** Pure official API via Google OAuth 2.0.
- **Strict Privacy:** Videos default to `PRIVATE`; playlist is `UNLISTED`.
- **No Asset Alteration:** Original MP4s, PNGs, and SRTs are strictly read-only.
- **Never Commit Secrets:** OAuth tokens and `client_secret*.json` are strictly `.gitignore`d.
