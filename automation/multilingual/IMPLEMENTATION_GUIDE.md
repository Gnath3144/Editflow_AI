# Developer Implementation Guide

---

## 1. Prerequisites & Environment Setup

- Python 3.10+ (Tested on Windows 11 with Python 3.12).
- FFmpeg 6.0+ on system `PATH` (with `atempo`, `highpass`, `afftdn`, and `loudnorm` filters).
- Virtual Environment:
  ```powershell
  cd D:\Codealytica\Video_PostProduction
  .\.venv\Scripts\Activate.ps1
  ```

---

## 2. Configuration Conventions

1. Copy example configuration:
   ```powershell
   Copy-Item automation/multilingual/config/youtube_config.example.json automation/multilingual/config/youtube_config.json
   ```
2. Verify all JSON configurations pass validation:
   ```powershell
   python automation/multilingual/scripts/validate_configuration.py
   ```

---

## 3. Running Unit Tests

Run the full suite of 10 automated unit tests:
```powershell
python -m unittest discover -s automation/multilingual/tests -v
```
