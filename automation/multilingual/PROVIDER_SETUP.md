# Cloud Provider Setup & Credentials

The Codealytica Multilingual Engine utilizes provider abstraction to decouple post-production logic from external cloud APIs.

---

## 1. Supported Providers

| Service Category | Supported Providers | Environment Variables |
| :--- | :--- | :--- |
| **Translation** | Azure Translator, Google Cloud Translate, OpenAI, DeepL | `AZURE_TRANSLATOR_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`, `OPENAI_API_KEY` |
| **Speech (TTS)** | Azure Speech Services, ElevenLabs, Google Cloud TTS, AWS Polly | `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`, `ELEVENLABS_API_KEY`, `AWS_ACCESS_KEY_ID` |
| **Audio Processing**| FFmpeg, Rubber Band, SoX | Native system binaries on `PATH` |
| **YouTube Publishing**| Google OAuth2 Client, YouTube Studio CMS | `GOOGLE_CLIENT_SECRETS_FILE`, `YOUTUBE_TOKEN_FILE` |

---

## 2. Zero-Leakage Policy

- **NEVER** hardcode API keys or secret credentials inside code, configurations, or manifests.
- Credentials must always be supplied via operating system environment variables or user-level `.env` files explicitly excluded by `.gitignore`.
- If a provider is not configured, the engine safely returns `NOT_CONFIGURED` without failing other operational components.
