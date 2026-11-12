# Phase 13 Specification
## Autonomous Multilingual Production & Global Delivery System

---

## 1. Scope & Objective

Phase 13 establishes the end-to-end architecture and implementation for localising Codealytica's technical masterclasses into 12 targeted international and regional languages.

### Target Languages & Locales:
1. **Tamil (`ta-IN`)** — Dravidian / Indic (Tamil Nadu, Sri Lanka, Singapore)
2. **Telugu (`te-IN`)** — Dravidian / Indic (Andhra Pradesh, Telangana)
3. **Malayalam (`ml-IN`)** — Dravidian / Indic (Kerala)
4. **Hindi (`hi-IN`)** — Indo-Aryan / Indic (North India, Diaspora)
5. **Urdu (`ur-PK`)** — Indo-Aryan / Perso-Arabic (Pakistan, South Asia)
6. **Mandarin Chinese (`zh-CN`)** — Sinitic / Simplified Chinese (East Asia)
7. **Japanese (`ja-JP`)** — Japonic / Kanji-Kana (Japan)
8. **Korean (`ko-KR`)** — Koreanic / Hangul (South Korea)
9. **Bahasa Melayu (`ms-MY`)** — Austronesian / Latin script (Malaysia)
10. **Singapore English (`en-SG`)** — English / Local idiom & technical vernacular
11. **British English (`en-GB`)** — English / Received Pronunciation & Commonwealth
12. **American English (`en-US`)** — English / Standard General American

---

## 2. Fundamental Architectural Pillars

### Pillar 1: Code & Terminology Shielding
Under no circumstances may technical tokens, variable names, library identifiers, or shell commands be translated or phonetically altered.
- `pydantic` must NEVER become "py-dant-ic" translated literally.
- `git checkout -b` must remain verbatim in ASCII monospace.
- `torch.cuda.is_available()` must remain untouched in speech prompts and subtitles.

### Pillar 2: Pitch-Preserving Adaptive Pacing
- Original instructor English audio is selectively accelerated only during empty pauses or non-critical setup transitions.
- Maximum allowable acceleration: **1.08x (preferred)**, **1.12x (absolute ceiling)**.
- Acceleration of complex conceptual explanations is strictly forbidden.
- Localized target speech utilizes independent, language-specific syllable rate models.

### Pillar 3: Provider Abstraction & Safe Fallbacks
- The engine supports multiple cloud providers (Azure Cognitive Services, ElevenLabs, Google Cloud Text-to-Speech / Translation, AWS Polly, OpenAI).
- Missing API keys or unconfigured providers return `NOT_CONFIGURED` without crashing or producing synthetic silent audio masquerading as completed output.

### Pillar 4: YouTube Multi-Audio Track Strategy
- YouTube Studio's multi-audio feature is currently restricted by Google to YouTube Partner Program / CMS accounts and is not broadly available via third-party Data API v3 endpoints.
- If direct API insertion is unavailable, the pipeline generates a complete **Manual Upload Package** containing synchronized audio tracks, multilingual SRT subtitles, translated titles, descriptions, and operator step-by-step instructions.

### Pillar 5: Manifest & Idempotency Checkpoints
- Every video, language, and segment is recorded in a cryptographic manifest (`dubbing_manifest.schema.json`).
- If a pipeline run is interrupted by network failure or process restart, it resumes from the last completed segment without re-incurring API costs.
