# Security Policy

## Supported Versions

Editflow AI actively maintains and releases security patches for the following versions:

| Version | Supported          |
| :------ | :----------------- |
| `1.0.x` | :white_check_mark: |
| `< 1.0` | :x:                |

---

## Reporting a Vulnerability

The Codealytica Editflow AI team takes security, user privacy, and credential protection extremely seriously.

### How to Report
- **DO NOT** create a public GitHub Issue to disclose security vulnerabilities or secret leaks.
- Please report vulnerabilities directly using **GitHub Private Vulnerability Reporting** on this repository:  
  [Report a Security Vulnerability](https://github.com/respectfulnrespected59-source/qmm-autoedit/security/advisories/new)
- If Private Vulnerability Reporting is unavailable, contact the project maintainer securely through official Codealytica communication channels.

### What to Include
When reporting a potential issue, please include:
1. Detailed description of the potential vulnerability.
2. Steps to reproduce or proof-of-concept script.
3. Subsystem affected (e.g. YouTube API token handling, TTS provider authentication, subprocess invocation).
4. Any potential mitigations or patches identified.

### Response Timeline
- **Initial Acknowledgment:** Within 48 hours.
- **Triage & Assessment:** Within 5 business days.
- **Resolution & Patch Deployment:** Critical security issues will receive priority patching via an expedited release.

---

## Secret Management & Credential Safety Rules

Editflow AI enforces strict architectural rules regarding secrets:

1. **Zero Committed Secrets:** Never commit `.env`, `client_secret.json`, `token.json`, OAuth tokens, or private keys.
2. **Environment Variable Precedence:** Credentials for external APIs (OpenAI, DeepL, ElevenLabs, Azure, YouTube) must be provided via environment variables or git-ignored configuration files (`config/youtube/token.json`).
3. **Repository Exclusion:** The repository [`.gitignore`](.gitignore) excludes all token files, secrets, `.env` files, and `.pem` certificates.
4. **Git History Protection:** If a secret is ever inadvertently staged or pushed, it must be invalidated and rotated immediately. Never rely solely on deleting the file in a subsequent commit.
