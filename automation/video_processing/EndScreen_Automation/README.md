# 🎬 Codealytica YouTube End Screen Automation

Automated End Screen configuration for Codealytica Day 01 lessons using Python and Playwright over Chrome/Edge CDP.

---

## Architecture & Configuration

This project automates the sequential configuration of YouTube End Screens inside the YouTube Studio Video Editor:

```
Lesson 01 (zP0kOyucuMA)  ──►  Lesson 02 (x-7RglvLPVw)
Lesson 02 (x-7RglvLPVw)  ──►  Lesson 03 (v0Ce7IYYCvU)
Lesson 03 (v0Ce7IYYCvU)  ──►  Lesson 04 (bUsxJjJW0uY)
Lesson 04 (bUsxJjJW0uY)  ──►  Lesson 05 (ThBJnBpSjkI)
Lesson 05 (ThBJnBpSjkI)  ──►  Lesson 06 (EjkFaIYaU60)
Lesson 06 (EjkFaIYaU60)  ──►  Playlist (PLIkXO9w8SPGg)
```

---

## Verified Timings (Final 20 Seconds / Outro)

| Lesson # | Video ID | Duration | Start Time | End Time | Target Type | Target ID |
|---|---|---|---|---|---|---|
| 01 | `zP0kOyucuMA` | `03:23` | `03:03` | `03:23` | Video | `x-7RglvLPVw` |
| 02 | `x-7RglvLPVw` | `03:49` | `03:29` | `03:49` | Video | `v0Ce7IYYCvU` |
| 03 | `v0Ce7IYYCvU` | `01:27` | `01:07` | `01:27` | Video | `bUsxJjJW0uY` |
| 04 | `bUsxJjJW0uY` | `03:35` | `03:15` | `03:35` | Video | `ThBJnBpSjkI` |
| 05 | `ThBJnBpSjkI` | `04:17` | `03:57` | `04:17` | Video | `EjkFaIYaU60` |
| 06 | `EjkFaIYaU60` | `06:39` | `06:19` | `06:39` | Playlist | `PLIkXO9w8SPGg` |

---

## How to Run

### 1. Dry Run (No modifications made):
```powershell
python configure_endscreens.py --dry-run
```

### 2. Live Execution:
```powershell
python configure_endscreens.py --execute
```
