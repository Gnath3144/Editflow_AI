# Environment Configuration & Variable Reference

This document explains environment variables, provider settings, output directory overrides, and local configuration templates for **Codealytica Editflow AI**.

---

## 1. `.env` Configuration File

Editflow AI reads environment variables from a local `.env` file located at the workspace root (`D:\Codealytica\Editflow AI\.env`). A template is provided at [`.env.example`](../../.env.example).

> [!CAUTION]
> The `.env` file is git-ignored and must **NEVER** be committed to version control.

---

## 2. Environment Variable Reference

### A. Core Workspace & Paths
| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `EDITFLOW_ROOT` | Workspace root | Root filesystem path of the Editflow AI installation |
| `EDITFLOW_LOG_LEVEL` | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `EDITFLOW_LOG_FILE` | `logs/editflow.log` | Path to rotating log file |
| `RAW_RECORDINGS_ROOT` | `D:\Codealytica` | Root directory containing raw Zoom recordings |
| `ENHANCED_VIDEOS_ROOT`| `D:\Codealytica\Enhanced_Videos` | Output directory for finished video masters |

### B. YouTube Publisher & Authentication
| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `YOUTUBE_CLIENT_SECRET_FILE` | `config/youtube/client_secret.json` | Path to Google OAuth2 Client Secret JSON |
| `YOUTUBE_TOKEN_FILE` | `config/youtube/token.json` | Path to stored OAuth2 user credentials |
| `YOUTUBE_DEFAULT_PRIVACY` | `unlisted` | Privacy status for new uploads (`unlisted`, `private`) |
| `YOUTUBE_PLAYLIST_ID` | `PLIkXO9w8SPGg` | Default Codealytica Masterclass playlist ID |

### C. Multilingual & Translation Providers
| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `GOOGLE_APPLICATION_CREDENTIALS` | None | Service account key for Google Cloud Translation |
| `DEEPL_API_KEY` | None | API authentication key for DeepL Translation |
| `ELEVENLABS_API_KEY` | None | API authentication key for ElevenLabs Voice Synthesis |
| `AZURE_SPEECH_KEY` | None | Subscription key for Azure Cognitive Speech Services |
| `AZURE_SPEECH_REGION` | `eastus` | Azure service region for speech synthesis |
