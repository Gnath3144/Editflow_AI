# Codealytica Multilingual Localisation & Production Engine

The **Codealytica Multilingual Engine** is an enterprise-grade localisation, speech synthesis, adaptive pacing, and YouTube multi-track delivery system designed specifically for developer education and technical video production.

---

## 1. System Mission

Technical training videos require far more than direct word-for-word translation. Sub-optimal machine translations translate programming code, ruin technical terminology, produce robotic unnatural voices, and cause severe audio-to-video desynchronization.

The Multilingual Engine solves this through:
- **12 Curated Language & Regional Profiles**: High-context configuration across Indic (Tamil, Telugu, Malayalam, Hindi, Urdu), East Asian (Mandarin, Japanese, Korean), Southeast Asian (Bahasa Melayu, Singapore English), and Western English (British, American).
- **Technical Glossary & Code Shielding**: Strict protection for programming syntax, variable names, CLI arguments, and AI/ML keywords (e.g. `Pydantic`, `LLM`, `PyTorch`, `h264_nvenc`).
- **Pitch-Preserving Adaptive Pacing**: Accelerating dead pauses while never exceeding 1.08x (preferred) or 1.12x (absolute limit) on technical explanations.
- **Segment-Level Audio Synchronization**: Time-stretching and pause insertion to ensure spoken explanations perfectly match on-screen coding actions.
- **Broadcast Mastering**: Standardized -16.0 LUFS (±0.5 LUFS), -1.5 dBTP maximum peak, and >= 38 dB SNR across all translated audio tracks.
- **YouTube Multi-Track & Package Publisher**: Automated inventory and manual fallback packaging for playlist `PLIkXO9w8SPGg`.
- **Zero-Secret Provider Abstraction**: Pluggable vendor interfaces (Azure, ElevenLabs, Google Cloud, AWS, OpenAI) with explicit `NOT_CONFIGURED` status handling.

---

## 2. Directory Structure

```
automation/multilingual/
├── README.md                          # Master overview and operational guide
├── PHASE_13_SPECIFICATION.md          # Comprehensive specification document
├── ARCHITECTURE.md                    # System architecture and dataflow
├── IMPLEMENTATION_GUIDE.md            # Developer setup and onboarding
├── PROVIDER_SETUP.md                  # Cloud vendor API and auth instructions
├── AUDIO_ENGINEERING.md               # DSP, mastering, time-stretch, and loudnorm
├── TRANSLATION_STANDARDS.md           # Glossaries, shielding, and tone standards
├── VOICE_AND_PRONUNCIATION.md         # Voice profiles and phonetic dictionaries
├── ADAPTIVE_PACING.md                 # Syllable rates and pitch-preserving stretch
├── YOUTUBE_AUDIO_TRACKS.md            # Track mapping, CMS capabilities, and fallbacks
├── QUALITY_ASSURANCE.md               # 4-tier acceptance and automated validation
├── TROUBLESHOOTING.md                 # Diagnostic guides and known issues
├── SECURITY.md                        # Key management, zero-leakage, and git hygiene
│
├── config/                            # Machine-readable configurations
│   ├── languages.json                 # 12 detailed language profiles
│   ├── voice_profiles.json            # Regional voice archetypes and pitches
│   ├── terminology_glossary.json      # Technical terms and shielding rules
│   ├── adaptive_pacing.json           # Acceleration limits and syllable targets
│   ├── translation_rules.json         # Formatting, code preservation, tone
│   ├── audio_quality_rules.json       # Acoustic, frequency, and loudness rules
│   ├── dubbing_quality_rules.json     # Drift limits and synchronization margins
│   └── youtube_config.example.json    # Safe template for YouTube configuration
│
├── app/                               # Core Python engine modules
│   ├── __init__.py
│   ├── localisation_orchestrator.py   # Master end-to-end pipeline runner
│   ├── language_detector.py           # Source and target language verifier
│   ├── transcript_normalizer.py       # Code shielding and markup preparation
│   ├── translation_engine.py          # Provider-backed translation executor
│   ├── translation_validator.py       # Syntax, code, and completeness checker
│   ├── glossary_manager.py            # Terminology enforcement and lookup
│   ├── speech_generator.py            # Synthesizer with provider fallback
│   ├── voice_profile_manager.py       # Actor voice selection and gender mapping
│   ├── pronunciation_dictionary.py    # IPA and phonetic override dictionary
│   ├── adaptive_pacing_engine.py      # Pitch-preserving speed adjustment
│   ├── speech_rate_analyzer.py        # Syllable and mora rate calculation
│   ├── language_specific_pacing.py    # Target language timing adaptation
│   ├── audio_timing_aligner.py        # Segment alignment against master video
│   ├── segment_timing_validator.py    # Drift and overlap detection
│   ├── audio_mixer.py                 # Ducking, room tone, and master mixing
│   ├── audio_validator.py             # LUFS, true peak, and SNR verifier
│   ├── subtitle_generator.py          # Synchronized SRT/VTT multilingual subs
│   ├── multilingual_comprehension_validator.py # Readability & cognitive load
│   └── youtube_audio_publisher.py     # Channel multi-track publisher / packager
│
├── providers/                         # Abstract vendor interfaces
│   ├── __init__.py
│   ├── translation_base.py            # Translation provider contract
│   ├── tts_base.py                    # TTS speech synthesis contract
│   ├── audio_processing_base.py       # DSP & time-stretching contract
│   ├── youtube_base.py                # YouTube publishing contract
│   └── README.md                      # Guide for implementing new cloud providers
│
├── schemas/                           # JSON Schema validation models
│   ├── language_profile.schema.json
│   ├── voice_profile.schema.json
│   ├── dubbing_manifest.schema.json
│   ├── translated_segment.schema.json
│   └── audio_quality_report.schema.json
│
├── manifests/                         # Checkpoint manifests (.gitkeep)
├── assets/                            # Static terminology & reference audio
├── tests/                             # 10 comprehensive unit & integration tests
├── scripts/                           # Standalone CLI tools & inventory scripts
└── reports/                           # Local production & validation reports
```

---

## 3. Quick Start & Execution

### 1. Validate All Configurations and Schemas:
```bash
python automation/multilingual/scripts/validate_configuration.py
```

### 2. Run Test Suite:
```bash
python -m unittest discover -s automation/multilingual/tests -v
```

### 3. Inventory Existing YouTube Playlist:
```bash
python automation/multilingual/scripts/inventory_playlist.py --playlist PLIkXO9w8SPGg
```

### 4. Generate Localised Dubbing Package:
```bash
python automation/multilingual/scripts/generate_dub.py \
    --video-id zP0kOyucuMA \
    --language ta-IN \
    --transcript D:/Codealytica/Enhanced_Videos/AIML_Day01/transcripts/lesson_01.json \
    --output-dir D:/Codealytica/Enhanced_Videos/Multilingual/Day_01/ta-IN
```
