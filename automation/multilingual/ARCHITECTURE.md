# System Architecture & Dataflow

---

## 1. High-Level System Architecture

```
[Master English Video & Subtitles]
               │
               ▼
   [Transcript Normalizer] ─── (Shields code, backticks, URLs, CLI commands)
               │
               ▼
   [Glossary & Translation Engine] ─── (Enforces domain terminology via TerminologyGlossary)
               │
               ▼
   [Translation Validator] ─── (Ensures 0% code leakage and 100% clause retention)
               │
               ▼
   [Adaptive Pacing & Rate Analyzer] ─── (Calculates syllable rates & time-stretch factors)
               │
               ▼
   [Speech Generator (TTS Abstraction)] ─── (Synthesizes localized audio via Provider API)
               │
               ▼
   [Audio Timing Aligner & Validator] ─── (Aligns segment offsets; enforces -16 LUFS / -1.5 dBTP)
               │
               ▼
   [Subtitle Generator] ─── (Produces synchronized multilingual SRT / VTT tracks)
               │
               ▼
   [YouTube Audio Publisher / Packager] ─── (Multi-track upload OR Manual Studio Package)
```

---

## 2. Component Directory Responsibilities

- **`config/`**: JSON configuration files defining languages, voice archetypes, terminology, acoustic thresholds, and pacing limits.
- **`app/`**: Core orchestrator and specialized functional engines for normalization, translation, synthesis, audio alignment, and validation.
- **`providers/`**: Abstract interfaces isolating cloud service SDKs (Azure, Google Cloud, ElevenLabs, AWS).
- **`schemas/`**: Formal JSON schemas ensuring strict validation of manifests, profiles, and reports.
- **`scripts/`**: CLI entrypoints for administrative operations, inventory, dubbing runs, and QA reports.
