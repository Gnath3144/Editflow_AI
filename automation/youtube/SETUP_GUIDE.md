# 🛠️ Codealytica YouTube Publisher: Setup & OAuth 2.0 Configuration Guide

This guide provides end-to-end instructions for configuring the Google Cloud Console, setting up OAuth 2.0 Desktop credentials, and launching the **Codealytica YouTube Publisher**.

---

## Part 1: Google Cloud Console Configuration

To publish videos using the official YouTube Data API v3, you need a Google Cloud Project with the YouTube Data API enabled and desktop OAuth credentials.

### Step 1: Create or Select a Google Cloud Project
1. Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. In the top navigation bar, click the project selector dropdown and click **New Project** (e.g. `Codealytica-Video-Publisher`).
3. Click **Create** and ensure the new project is active.

### Step 2: Enable the YouTube Data API v3
1. In the Google Cloud Console search bar, enter **YouTube Data API v3**.
2. Select **YouTube Data API v3** from Marketplace / APIs.
3. Click **Enable**.

### Step 3: Configure the OAuth Consent Screen
1. In the left navigation menu, go to **APIs & Services** > **OAuth consent screen**.
2. Select User Type: **External** (unless you are using Google Workspace internal).
3. Click **Create**.
4. Fill in the App Information:
   - **App name:** `Codealytica YouTube Publisher`
   - **User support email:** Select your Google account (`gnathan...` or official Codealytica email).
   - **Developer contact information:** Your email address.
5. Click **Save and Continue**.
6. **Scopes:** Click **Add or Remove Scopes**, filter and select:
   - `https://www.googleapis.com/auth/youtube.upload` (Upload YouTube videos)
   - `https://www.googleapis.com/auth/youtube` (Manage YouTube account, playlists, captions)
   - `https://www.googleapis.com/auth/youtube.force-ssl` (Manage YouTube assets)
7. Click **Update** and then **Save and Continue**.
8. **Test Users (Crucial):** While the app is in "Testing" mode, only designated Test Users can sign in.
   - Click **+ Add Users**.
   - Enter your YouTube channel owner Google Account email.
   - Click **Add**, then **Save and Continue**.

### Step 4: Create OAuth 2.0 Client Credentials
1. In the left navigation menu, go to **APIs & Services** > **Credentials**.
2. Click **+ Create Credentials** at the top, and select **OAuth client ID**.
3. In the **Application type** dropdown, select **Desktop app**.
4. Name it: `Codealytica Desktop Uploader`.
5. Click **Create**.
6. In the confirmation dialog, click **Download JSON**.
7. Rename the downloaded file to `client_secret.json` and move it to:
   ```
   D:\Codealytica\YouTube_Publisher\config\client_secret.json
   ```

---

## Part 2: Local Windows 11 Environment Setup

### Method A: Automated Setup Script (Recommended)
Open PowerShell and run:
```powershell
cd "D:\Codealytica\YouTube_Publisher"
.\scripts\setup.ps1
```
This script will:
1. Detect Python 3.11+ / Python 3.12.
2. Initialize `.venv` in `D:\Codealytica\YouTube_Publisher\.venv`.
3. Upgrade `pip` and install all dependencies from `requirements.txt`.

### Method B: Manual Pip Installation
```powershell
cd "D:\Codealytica\YouTube_Publisher"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Part 3: Launching the Application

### Launching Desktop GUI:
```powershell
.\scripts\launch.ps1
```
Or directly:
```powershell
.\.venv\Scripts\python.exe app.py
```

### Running CLI Pre-Flight Verification:
```powershell
.\.venv\Scripts\python.exe app.py --dry-run
```
