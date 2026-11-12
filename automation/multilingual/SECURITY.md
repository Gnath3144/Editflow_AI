# Security, Privacy & Git Hygiene

---

## 1. Security Protocols

- **Never Commit Secrets:** OAuth tokens, client secrets, API keys, or private certificates must never be committed to git.
- **Local Scratch Media:** All generated WAV files and intermediate renders are isolated to `Enhanced_Videos/` and excluded via `.gitignore`.
- **Default Privacy:** All YouTube uploads and playlist references default strictly to `UNLISTED`.
