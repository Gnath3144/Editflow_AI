# Secret Management & Credential Lifecycle Policy

This policy governs the management, isolation, rotation, and lifecycle of sensitive secrets, API keys, and authorization tokens in **Codealytica Editflow AI**.

---

## 1. Secret Classification

| Category | Secret Examples | Storage Location | Ingestion Method |
| :--- | :--- | :--- | :--- |
| **OAuth 2.0 Client Secrets** | YouTube `client_secret.json` | `config/youtube/` (Git-Ignored) | Local filesystem via `PathManager` |
| **OAuth 2.0 User Tokens** | YouTube `token.json` | `config/youtube/` (Git-Ignored) | Google Auth client library |
| **Provider API Keys** | DeepL, ElevenLabs, Azure Speech | `.env` (Git-Ignored) | `os.environ` / `ConfigManager` |
| **Cloud Service Accounts** | Google Cloud JSON keyfile | Specified in `GOOGLE_APPLICATION_CREDENTIALS` | Secure OS path outside repo |

---

## 2. Git Exclusion Safeguards

The repository [`.gitignore`](../../.gitignore) enforces strict pattern-based matching against all credentials:
```gitignore
# Credentials and Secrets
.env
*.pem
*.key
client_secret*.json
client_secrets*.json
token*.json
oauth*.json
!*.example
```

---

## 3. Incident Response Protocol for Inadvertent Leaks

If credentials or secrets are inadvertently committed or exposed:
1. **Immediate Revocation:** Invalidate the token/secret immediately in the respective cloud console (Google Cloud Console, ElevenLabs, Azure, DeepL).
2. **Key Rotation:** Issue a fresh secret and update local `.env` or `config/youtube/` files.
3. **Audit History:** Run `git log` and `git diff` to identify the commit.
4. **Git History Scrubbing:** Use `git-filter-repo` or BFG Repo-Cleaner to permanently purge the compromised commit from all branches and tags.
5. **Team Disclosure:** Notify repository maintainers to ensure all local forks update their remotes.
