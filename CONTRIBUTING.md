# Contributing to Codealytica Editflow AI

Thank you for your interest in contributing to **Codealytica Editflow AI**! We welcome community contributions, bug fixes, feature proposals, and documentation enhancements.

Please read this document carefully to understand our development workflows, architectural standards, testing requirements, and security obligations.

---

## 1. Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat all members of the community with dignity, empathy, and professional respect.

---

## 2. Development Setup

### Prerequisites
- **Operating System:** Windows 10/11 64-bit (Production validated), Linux Ubuntu 22.04+ (CI validated)
- **Python:** Version 3.10, 3.11, or 3.12 (Recommended: Python 3.12.8 64-bit)
- **FFmpeg & FFprobe:** Version 6.0+ or 7.0+ on system PATH
- **Git:** Version 2.40+

### Local Environment Setup
1. Fork or clone the repository:
   ```bash
   git clone https://github.com/respectfulnrespected59-source/qmm-autoedit.git
   cd qmm-autoedit
   ```
2. Create and activate a virtual environment:
   ```powershell
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   ```bash
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
4. Verify system health:
   ```bash
   python -m editflow health
   ```

---

## 3. Branching Strategy & Git Workflow

- **Default Branch:** `main` (Production-stable code only)
- **Branch Naming Conventions:**
  - `feature/<description>` — New capabilities, provider integrations, or tools
  - `fix/<description>` — Bug fixes and behavioral corrections
  - `docs/<description>` — Documentation improvements and guides
  - `chore/<description>` — CI/CD, dependency updates, and maintenance
  - `refactor/<description>` — Code reorganization without changing external behavior

### Workflow
1. Create a dedicated branch from latest `main`:
   ```bash
   git checkout -b feature/adaptive-pacing-v2
   ```
2. Make modular, logically atomic commits with clear semantic commit messages:
   ```bash
   git commit -m "feat(multilingual): implement token shielding for SQL keywords"
   ```
3. Ensure all tests and validation checks pass locally before opening a PR:
   ```bash
   python -m editflow validate
   python -m unittest discover -s automation/editorial/tests
   python -m unittest discover -s automation/multilingual/tests
   ```
4. Push to your branch and submit a Pull Request targeting `main`.

---

## 4. Coding & Architecture Standards

- **PEP 8 & Formatting:** All Python code must be formatted consistently. We use Ruff for linting and style checking.
- **Type Annotations:** Use explicit type hints (`typing.Optional`, `typing.List`, `typing.Dict`, `pathlib.Path`) for all public function arguments and return types.
- **Path Resolution:** Never hardcode absolute system paths (e.g. `C:\Users\...`). Always use `core.filesystem.paths.PathManager` or `pathlib.Path` relative to project roots.
- **Error Handling:** Use structured exceptions defined in `core.error_handling.exceptions`. Never swallow exceptions with bare `except: pass`.
- **Media Preservation:** Never write code that modifies, re-encodes, or deletes source raw classroom recordings in `D:\Codealytica\*.mp4`. Source files are strictly read-only.
- **YouTube Privacy:** All automated publishing routines must default video privacy to `UNLISTED`. Never upload as `PUBLIC` automatically.

---

## 5. Submitting Pull Requests

All Pull Requests must:
1. Complete all sections of the [Pull Request Template](.github/pull_request_template.md).
2. Pass all automated CI tests and code quality checks.
3. Include new unit tests for any new modules or modified algorithmic logic.
4. Update corresponding documentation in `docs/` or module READMEs.
5. Strictly avoid committing any secrets, API keys, client secrets, or personal tokens.

---

## 6. Security & Vulnerability Reporting

If you discover a security vulnerability or credential leak, **DO NOT** open a public issue. Follow our [Security Policy](SECURITY.md) to report the vulnerability privately.
