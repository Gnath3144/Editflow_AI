# ⚙️ Codealytica YouTube Publisher: Configuration Guide

This document describes all configuration settings in `config/settings.json`, API quotas, privacy controls, and playlist bindings.

---

## Configuration File: `config/settings.json`

```json
{
  "app_name": "Codealytica YouTube Publisher",
  "version": "1.0.0",
  "default_channel_id": "UClHA7HX1h5eWwgfVjt8wb5A",
  "default_playlist_id": "PLIkXO9w8SPGg",
  "default_playlist_title": "Generative AI with Ollama: From Fundamentals to Hands-On Practice | Codealytica",
  "default_video_privacy": "private",
  "default_playlist_privacy": "unlisted",
  "default_category_id": "27",
  "chunk_size_bytes": 8388608,
  "max_retries": 5,
  "base_backoff_seconds": 2.0,
  "max_backoff_seconds": 60.0,
  "source_directory": "D:\\Codealytica\\Enhanced_Videos\\AIML_Day01\\YOUTUBE_UPLOAD_READY_CORRECTED",
  "database_path": "data/publisher.db"
}
```

### Parameter Reference

| Key | Default | Description |
|---|---|---|
| `default_channel_id` | `UClHA7HX1h5eWwgfVjt8wb5A` | **Strict Security Check:** If the authenticated OAuth session belongs to any other channel, uploading is halted immediately. |
| `default_playlist_id` | `PLIkXO9w8SPGg` | Target YouTube playlist ID. Reused automatically to avoid duplicate playlists. |
| `default_video_privacy` | `private` | **Codealytica Policy:** Videos are always uploaded as `private` initially. |
| `default_playlist_privacy` | `unlisted` | Playlist is accessible via direct link for course students. |
| `default_category_id` | `27` | YouTube Category `27` = **Education** (`28` = Science & Technology). |
| `chunk_size_bytes` | `8388608` | Resumable upload chunk size (`8 MB`). Optimal for modern broadband connections. |
| `max_retries` | `5` | Maximum retry attempts for transient network drops (500, 503, connection reset). |
| `base_backoff_seconds` | `2.0` | Initial exponential backoff delay. |
| `source_directory` | `...` | Default folder scanned for lesson packages. |

---

## YouTube API Quota Management

YouTube Data API v3 allocates a default project quota of **10,000 units per calendar day** (resets at midnight Pacific Time / 1:30 PM IST).

### Quota Cost Breakdown:
- **`videos.insert` (Video Upload):** `1,600 units` per video
- **`thumbnails.set` (Custom Thumbnail):** `50 units`
- **`captions.insert` (Closed Captions):** `50 units`
- **`playlistItems.insert` (Add to Playlist):** `50 units`
- **Total per video:** `~1,750 units`

### Day 01 Batch Requirement:
- 6 Lesson Videos × 1,600 = **9,600 units**
- Supporting metadata = **~600 units**
- **Total:** ~10,200 units.
> 💡 **Recommendation:** If quota threshold is reached during Lesson 06, the SQLite upload ledger records exactly which videos succeeded. The publisher resumes seamlessly tomorrow without re-uploading completed lessons!
