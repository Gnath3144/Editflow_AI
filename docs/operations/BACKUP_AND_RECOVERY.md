# Backup, Disaster Recovery & Data Protection Policy

This document establishes the data protection, backup schedules, and disaster recovery procedures for **Codealytica Editflow AI**.

---

## 1. Asset Classification & Protection Tiers

| Tier | Asset Category | Filesystem Location | Mutability | Backup Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Raw Classroom Recordings** | `D:\Codealytica\*.mp4` | **IMMUTABLE (Read-Only)** | Mirrored on secondary cold storage / offline drive. Never deleted. |
| **Tier 2** | **Source Code & Git History** | `D:\Codealytica\Editflow AI` | Version Controlled | Remote Git repository (`origin/main` on GitHub). |
| **Tier 3** | **Enhanced Video Masters & Audio** | `D:\Codealytica\Enhanced_Videos` | Reproducible Output | Daily incremental snapshot; retained until uploaded to YouTube. |
| **Tier 4** | **Configuration & Secrets** | `config/youtube/*.json`, `.env` | Sensitive | Encrypted local backup; never pushed to public Git. |
| **Tier 5** | **Cache & Logs** | `logs/`, `data/caches/` | Ephemeral | Automatic 30-day rotation; no backup required. |

---

## 2. Disaster Recovery Protocol

In the event of hardware failure, disk corruption, or accidental workspace damage:

1. **Restore Codebase:**
   ```powershell
   git clone https://github.com/respectfulnrespected59-source/qmm-autoedit.git "D:\Codealytica\Editflow AI"
   ```
2. **Re-initialize Virtual Environment:**
   ```powershell
   cd "D:\Codealytica\Editflow AI"
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
3. **Restore YouTube Credentials:**
   - Copy authenticated `token.json` and `client_secret.json` from encrypted credential store to `config/youtube/`.
4. **Verify System Integrity:**
   ```powershell
   python -m editflow health
   python -m editflow validate
   ```
