# Windows Environment Setup Guide

This guide walks through the detailed setup and optimization of **Codealytica Editflow AI** on Microsoft Windows 10 and Windows 11 (64-bit).

---

## 1. System Requirements

- **Operating System:** Windows 10 64-bit (Build 19041+) or Windows 11 64-bit.
- **CPU:** Multi-core x86_64 processor (Intel Core i5/i7/i9 or AMD Ryzen 5/7/9).
- **RAM:** Minimum 16 GB (Recommended: 32 GB for concurrent video encoding and Whisper model inference).
- **Disk Space:** Minimum 50 GB free NVMe/SSD storage for media caching and rendered video outputs.

---

## 2. Installing Prerequisites

### A. Python 3.12 (64-bit)
1. Download Python 3.12.8 (64-bit) from [python.org](https://www.python.org/downloads/windows/).
2. Run the installer and ensure you check:
   - :white_check_mark: **"Add python.exe to PATH"**
   - :white_check_mark: **"Use admin privileges when installing py.exe"**
3. Verify in PowerShell:
   ```powershell
   python --version
   # Expected output: Python 3.12.8
   ```

### B. FFmpeg & FFprobe
1. Download a modern FFmpeg release build (e.g., Gyan.dev FFmpeg release full build).
2. Extract the archive to `C:\ffmpeg` so that binaries reside at `C:\ffmpeg\bin\ffmpeg.exe`.
3. Add `C:\ffmpeg\bin` to your User or System `PATH` environment variable.
4. Verify in PowerShell:
   ```powershell
   ffmpeg -version
   ffprobe -version
   ```

---

## 3. Setting Up the Virtual Environment

Open PowerShell in the Editflow AI project directory:

```powershell
cd "D:\Codealytica\Editflow AI"

# Create a clean virtual environment
python -m venv .venv

# Enable script execution if restricted
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install wheel
python -m pip install --upgrade pip setuptools wheel

# Install all project dependencies
python -m pip install -r requirements.txt
```

---

## 4. Validating the Installation

Execute the Editflow AI system health check:

```powershell
python -m editflow health
```

Expected output:
```text
[*] Python Interpreter: D:\Codealytica\Editflow AI\.venv\Scripts\python.exe
[*] Workspace Root: D:\Codealytica\Editflow AI
[+] FFMPEG: READY
[+] FFPROBE: READY
[+] Library torch: READY
[+] Library faster_whisper: READY
[+] Library av: READY
[+] Library soundfile: READY
[+] Library webrtcvad: READY
[+] Library resemblyzer: READY
[+] Health check finished: SYSTEM OPERATIONAL.
```
