# Project Dependencies & Compatibility Reference

This document catalogs the runtime, multimedia, machine learning, and development dependencies required by **Codealytica Editflow AI**.

---

## 1. Core Dependency Matrix

| Package | Version | Purpose | Compatibility Notes |
| :--- | :--- | :--- | :--- |
| **`torch`** | `2.15.0+cpu` | Tensor computations & neural audio embeddings | CPU-only wheel installed to prevent CUDA footprint bloat on non-GPU nodes |
| **`faster-whisper`** | `1.2.1` | Fast CTranslate2 Whisper speech-to-text | Requires 16 kHz mono WAV input; word-level timestamp generation enabled |
| **`av` (PyAV)** | `13.1.0` | Direct libavformat / libavcodec Python bindings | High-performance frame seeking and demuxing |
| **`soundfile`** | `0.14.0` | High-fidelity linear audio I/O | Bundles libsndfile C library |
| **`webrtcvad`** | `2.0.10` | WebRTC Voice Activity Detection | Low-latency voice vs silence segmentation |
| **`resemblyzer`** | `0.1.4` | Voice embedding & speaker verification | Patched to bypass Numba dependency on Windows |
| **`Pillow`** | `10.2.0+` | Branded thumbnail image composition | Type rendering, drop shadows, and visual compositing |
| **`google-api-python-client`** | `2.118.0+` | YouTube Data API v3 integration | Video upload, thumbnail updates, playlist management |
| **`google-auth-oauthlib`** | `1.2.0+` | OAuth 2.0 user authorization | Token refresh flow for YouTube publisher |
| **`jsonschema`** | `4.21.0+` | JSON schema validation | Validates language profiles, edit decisions, and manifest schemas |
| **`pydantic`** | `2.6.0+` | Strongly-typed data validation | Config and schema validation models |
| **`numpy`** | `1.26.4` | Numerical array operations | Audio buffer manipulation and WSOLA calculations |
| **`scipy`** | `1.12.0+` | Digital signal processing | Audio filtering, resampling, and spectrogram calculations |

---

## 2. Windows Numba Workaround Note

On Windows systems operating under strict application control policies, the default `numba` JIT compiler used by `librosa` / `resemblyzer` may encounter execution policy restrictions. Editflow AI resolves this transparently:
- The `automation/editorial/core/speaker_diarizer.py` module applies an in-memory monkey patch replacing Librosa's numba-based Mel-spectrogram computation with native PyTorch STFT operations.
- This provides 100% functionality without requiring Numba compilation.
