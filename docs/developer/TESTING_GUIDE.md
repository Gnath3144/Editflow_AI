# Testing Guide & Quality Assurance Policy

This guide explains how to write, execute, and debug unit tests, integration tests, and regression suites within **Codealytica Editflow AI**.

---

## 1. Test Organization

Tests are located within dedicated `tests/` directories inside their respective subsystem packages:

```
automation/
├── editorial/
│   └── tests/
│       ├── test_audio_quality.py           # FFmpeg filtergraph construction & mastering
│       ├── test_edit_decision_validation.py# Quality validator gating
│       ├── test_filler_detection.py        # 3-tier filler word detection
│       ├── test_pause_detection.py         # Silence compaction & pause preservation
│       ├── test_repetition_detection.py    # Stutter & false-start pruning
│       ├── test_semantic_continuity.py     # Keep timeline generation
│       └── test_speaker_overlap.py         # Resemblyzer diarization & fallback
│
└── multilingual/
    └── tests/
        ├── test_adaptive_pacing.py         # WSOLA stretch bounds (0.85x - 1.30x)
        ├── test_audio_alignment.py         # Drift detection (<= 200 ms)
        ├── test_audio_quality.py           # LUFS compliance (-16.0 +- 1.0)
        ├── test_glossary.py                # 54 technical token shielding
        ├── test_language_profiles.py       # 12 language schemas & phoneme expansion
        ├── test_manifest.py                # Cryptographic manifest generation
        ├── test_speech_rate.py             # Syllable rate calculation
        ├── test_subtitles.py               # Frame-accurate SRT generation
        ├── test_translation_preservation.py# XML code shielding roundtrip
        └── test_youtube_track_mapping.py   # Multi-track packaging & instructions
```

---

## 2. Running Tests Locally

### Run All Tests
```powershell
# From project root:
.\.venv\Scripts\python.exe -m unittest discover -s automation/editorial/tests -v
.\.venv\Scripts\python.exe -m unittest discover -s automation/multilingual/tests -v
```

### Run a Specific Test Module
```powershell
.\.venv\Scripts\python.exe -m unittest automation/editorial/tests/test_filler_detection.py -v
```

### Run a Specific Test Case
```powershell
.\.venv\Scripts\python.exe -m unittest automation.editorial.tests.test_filler_detection.TestFillerDetection.test_tier_1_non_semantic_filler -v
```

---

## 3. Writing New Tests

1. Inherit from `unittest.TestCase`.
2. Use deterministic mock data rather than requiring external network calls or billable cloud APIs.
3. Assert both positive cases (valid inputs succeed) and boundary/negative cases (invalid formats or out-of-spec loudness raise expected exceptions).
4. Clean up any temporary files created during testing using `setUp()` and `tearDown()`.
