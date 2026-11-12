# Codealytica Editorial Intelligence Engine

The **Codealytica Editorial Intelligence Engine** is a permanent, reusable, and automated video post-production system designed to transform raw classroom and Zoom training recordings into broadcast-grade, semantically coherent, high-density educational video courses.

---

## 1. Core Mission & Philosophy

> **Primary Principle:** *Optimize for learning value per minute, not video length. The editorial intelligence must become part of the software, not remain dependent on repeated instructions from the user.*

Raw technical training sessions inevitably suffer from:
- Long unmuted pre-session chatter, open-mic background noise, and dead air.
- Repetitive confirmation loops ("Are you following?", "Is my screen visible?", "Understood?").
- False starts, hesitation silences, sentence stumbles, and non-semantic verbal crutches.
- Participant interruptions, logistical digressions, and audio overlap.
- Room resonance, HVAC rumble, mic plosives, and inconsistent speech loudness levels.

The Editorial Intelligence Engine automates the removal of these distractions while rigorously preserving pedagogical clarity, authentic instructor voice, and semantic continuity.

---

## 2. Directory Architecture

```
D:\Codealytica\Video_PostProduction\automation\editorial\
├── README.md                          # Master system overview and operational manual
├── EDITORIAL_CONSTITUTION.md          # Immutable pedagogical laws and decision principles
├── EDITING_DECISION_POLICY.md         # Operational classification rules (KEEP vs REMOVE)
├── AUDIO_CLEANUP_STANDARD.md          # Spectral denoising, highpass, EQ, dynamic mastering
├── SPEAKER_SEPARATION_STANDARD.md     # Voice diarization, instructor vs participant policy
├── SEMANTIC_CONTINUITY_STANDARD.md    # Transition smoothing, cut safety windows, flow preservation
├── REPETITION_REMOVAL_STANDARD.md     # Exact vs near repetition, restarts vs reinforcement
├── PAUSE_AND_SILENCE_POLICY.md        # Natural, pedagogical, hesitation, dead air pause rules
├── MULTILINGUAL_DUBBING_STANDARD.md   # Pre-dubbing validation, prosody mapping across 12 languages
├── QUALITY_CONTROL_STANDARD.md        # Technical, acoustic, and pedagogical acceptance criteria
│
├── configuration/                     # Machine-readable rule definitions
│   ├── editorial_config.json          # Global pipeline orchestration parameters
│   ├── filler_words.json              # Multi-tier filler and discourse marker rules
│   ├── repetition_rules.json          # N-gram and semantic similarity thresholds
│   ├── silence_rules.json             # Pause thresholds and micro-fade specifications
│   ├── speaker_rules.json             # Speaker embedding and isolation thresholds
│   ├── audio_quality_rules.json       # LUFS, true peak, SNR, and EQ profiles
│   ├── semantic_quality_rules.json    # Coherence, transition, and pedagogical metrics
│   └── language_profiles.json         # Dubbing timing constraints for 12 languages
│
├── schemas/                           # JSON Schema definitions for data validation
│   ├── edit_decision.schema.json      # Schema for EDL edit actions
│   ├── speaker_segment.schema.json    # Schema for diarization output
│   ├── editorial_report.schema.json   # Schema for production reports
│   └── quality_report.schema.json     # Schema for automated QA validation
│
├── examples/                          # Golden reference test cases and EDL samples
│   ├── good_edit_decisions.json       # Examples of valid, high-confidence cuts
│   ├── rejected_edit_decisions.json   # Examples of invalid / prohibited cuts
│   └── sample_editorial_report.json   # Reference production run report
│
├── core/                              # Production Python engine modules
│   ├── __init__.py
│   ├── filler_detector.py             # 4-tier filler word and discourse marker analyzer
│   ├── repetition_engine.py           # Multi-sentence repetition and restart analyzer
│   ├── silence_manager.py             # VAD silence detector with micro-fade logic
│   ├── speaker_diarizer.py            # Voice embedding matching (PyTorch STFT Resemblyzer)
│   ├── audio_master.py                # FFmpeg broadcast audio restoration (-16 LUFS)
│   ├── editorial_decision_engine.py   # Multi-pass semantic EDL generator
│   ├── multilingual_integrator.py     # Pre-dubbing alignment and duration validator
│   ├── quality_validator.py           # Automated QC analyzer across 4 quality dimensions
│   └── pipeline_orchestrator.py       # End-to-end command-line orchestrator
│
└── tests/                             # Automated regression and unit test suite
    ├── __init__.py
    ├── test_filler_detection.py
    ├── test_repetition_detection.py
    ├── test_pause_detection.py
    ├── test_speaker_overlap.py
    ├── test_semantic_continuity.py
    ├── test_audio_quality.py
    └── test_edit_decision_validation.py
```

---

## 3. Quick Start & Execution

### Running the Complete Production Pipeline:
```bash
python -m automation.editorial.core.pipeline_orchestrator \
    --input "D:\Codealytica\Gen Ai Day-03.mp4" \
    --output-dir "D:\Codealytica\Enhanced_Videos\Day_03" \
    --reference-audio "D:\Codealytica\Enhanced_Videos\Day_02\Audio_Master\Lesson_01_Audio.wav" \
    --mode full
```

### Running Automated Test Suite:
```bash
python -m unittest discover -s automation/editorial/tests -v
```\n