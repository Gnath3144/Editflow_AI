# 🚀 Codealytica YouTube Publishing Workflow

Step-by-step walkthrough for publishing Day 01 and future video series using the **Codealytica YouTube Publisher**.

---

## Workflow Summary

```
  Local Folder (MP4, PNG, SRT, MD)
                 │
                 ▼
       [1. Scan Directory]
                 │
                 ▼
       [2. Authenticate OAuth] ──► Verified Channel: UClHA7HX1h5eWwgfVjt8wb5A
                 │
                 ▼
       [3. Pre-Flight Dry Run] ──► Validates Limits & Checks SHA-256 Ledger
                 │
                 ▼
       [4. Launch Upload Engine]
                 │
                 ├─► A. Resumable Video Chunk Upload (Private)
                 ├─► B. Custom 1080p Thumbnail Upload
                 ├─► C. Closed Captions (.srt) Upload
                 └─► D. Append to Unlisted Playlist (PLIkXO9w8SPGg)
                 │
                 ▼
    [5. Audit Report & Ledger Updated] (Markdown & CSV)
```

---

## Step 1: Place Video Assets in Standard Structure

Each lesson folder must contain:
1. Master video: `.mp4`
2. Custom thumbnail: `_Selected_Frame.png` or `.jpg` (< 2MB)
3. Subtitles: `_Subtitles.srt` or `.vtt`
4. Metadata: `_METADATA.md` with Title, Description, and Chapters

Example:
```
D:\Codealytica\Enhanced_Videos\AIML_Day01\YOUTUBE_UPLOAD_READY_CORRECTED\
├── Lesson_01\
│   ├── Day01_Lesson01_Introduction_to_Local_AI_and_Ollama.mp4
│   ├── Day01_Lesson01_Introduction_to_Local_AI_and_Ollama_Selected_Frame.png
│   ├── Day01_Lesson01_Introduction_to_Local_AI_and_Ollama.srt
│   └── Day01_Lesson01_Introduction_to_Local_AI_and_Ollama_METADATA.md
├── Lesson_02\
...
└── Lesson_06\
```

---

## Step 2: Run Pre-Flight Dry Run

Before launching uploads or consuming YouTube API quota, verify everything:
```powershell
cd "D:\Codealytica\YouTube_Publisher"
.\.venv\Scripts\python.exe app.py --dry-run
```
Output confirms:
- Title length ≤ 100 characters
- Description formatted with valid chapters
- Thumbnails ≤ 2MB
- SHA-256 deduplication check against SQLite database

---

## Step 3: Launch Desktop GUI & Authenticate

1. Start the desktop application:
   ```powershell
   .\scripts\launch.ps1
   ```
2. Navigate to the **Authentication** tab.
3. Select your `config/client_secret.json`.
4. Click **Authorize via Browser (OAuth 2.0)**.
5. In the browser popup, sign in with the Google Account owning **Codealytica**.
6. The app automatically captures the OAuth token and confirms channel `UClHA7HX1h5eWwgfVjt8wb5A`.

---

## Step 4: Publish Lessons

1. Go to **Review & Dry Run** tab.
2. Confirm the 6 lessons are listed in exact order.
3. Click **Proceed to Upload Engine 🚀**.
4. The publishing engine executes autonomously:
   - Tracks chunked progress with transfer speed and ETA.
   - Applies custom high-res thumbnail.
   - Uploads English closed captions.
   - Adds video to playlist `PLIkXO9w8SPGg` in sequential lesson order.
5. Post-publishing report is saved to `YOUTUBE_UPLOAD_REPORT.md` and `YOUTUBE_UPLOAD_REPORT.csv`.
