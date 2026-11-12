# Engineering Backlog & Technical Debt Tracking

This backlog tracks prioritized engineering items, architectural enhancements, and scheduled maintenance for **Codealytica Editflow AI**.

---

## 1. High Priority (Sprint 1 - Immediate Execution)

| ID | Module | Title | Description | Target |
| :--- | :--- | :--- | :--- | :--- |
| **ENG-101** | `automation/editorial` | **Day 03 Post-Production Pipeline** | Run speech diarization, pause compaction, audio mastering, and pedagogical lesson chunking on `Gen Ai Day-03.mp4`. | Days 03 Master |
| **ENG-102** | `automation/thumbnail` | **Day 02 & Day 03 Branded Thumbnails** | Generate high-contrast portrait thumbnails with instructor cutout and code terminal themes. | Production Assets |
| **ENG-103** | `ci/cd` | **GitHub Actions Initial Workflow Run** | Execute `.github/workflows/ci.yml` and verify cross-platform test matrix results on GitHub. | GitHub Actions |

---

## 2. Medium Priority (Sprint 2 - Localisation & Provider Expansion)

| ID | Module | Title | Description | Target |
| :--- | :--- | :--- | :--- | :--- |
| **ENG-201** | `automation/multilingual` | **Cloud Translation Provider Adapters** | Implement live API connectors for Google Cloud Translation v3 and DeepL API with token shielding. | `providers/` |
| **ENG-202** | `automation/multilingual` | **ElevenLabs Voice Cloning Pipeline** | Integrate ElevenLabs Voice Cloning API using approved Gopinath Kshatriya audio samples. | `speech_generator.py` |
| **ENG-203** | `automation/editorial` | **Days 04–09 Video Post-Production** | Sequentially process raw Zoom recordings `Gen Ai Day-04.mp4` through `Gen Ai Day 09.mp4`. | Enhanced Videos |

---

## 3. Architectural Enhancements & Technical Debt

| ID | Subsystem | Description | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **DEBT-01** | `audio_master.py` | Dual FFmpeg passes for 2-pass Loudnorm | Current implementation uses single-pass loudness normalization. Upgrade to 2-pass dynamic JSON measurement for ±0.5 LUFS precision. |
| **DEBT-02** | `speaker_diarizer.py` | Resemblyzer Scipy Deprecation Warning | Resemblyzer audio import uses deprecated `scipy.ndimage.morphology.binary_dilation`. Update import to `scipy.ndimage.binary_dilation`. |
| **DEBT-03** | `workers/` | Decoupled worker process implementation | Transition worker stubs into asynchronous background worker daemons using multiprocessing. |
