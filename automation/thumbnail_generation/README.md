# Codealytica Automated YouTube Thumbnail Generator

A production-grade Python image composition pipeline for automated generation and QA of YouTube video thumbnails.

## Features
- **Standard YouTube Specs:** Generates exact 1280 × 720 (16:9) images under 2 MB.
- **High-CTR Visual Architecture:** Clear hierarchy, large curiosity-inducing headlines, high-contrast support badges, and authentic code/hardware telemetry crops.
- **Brand Consistency:** Codealytica branding (`CODE. ANALYZE. BUILD. GROW.`), dark tech gradient backgrounds, electric cyan accents (`#00E5FF`), and safe margin padding.
- **Quality Assurance:** Generates a 2x3 master contact sheet and a mobile-feed simulation preview (320px width) to verify small-screen readability.
- **YouTube API Integration Ready:** Integrates with YouTube Data API v3 (`thumbnails.set`) once approved.

## Directory Structure
- `generate_thumbnails.py`: Main thumbnail composition engine.
- `thumbnail_config.json`: Master JSON configuration for all 6 lessons.
- `requirements.txt`: Python package requirements (Pillow, OpenCV, NumPy).
- `output/`: Generated 1280x720 PNG thumbnails.
- `previews/`: Master contact sheet and mobile feed previews.
- `THUMBNAIL_GENERATION_REPORT.md`: Audit matrix and QA report.

## Execution
```bash
# In YouTube_Publisher virtual environment
python generate_thumbnails.py
```
