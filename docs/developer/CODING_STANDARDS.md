# Coding Standards & Engineering Conventions

All code contributed to **Codealytica Editflow AI** must adhere to the engineering conventions and quality standards defined in this document.

---

## 1. Python Style & Formatting

- **PEP 8 Compliance:** Follow PEP 8 guidelines strictly.
- **Line Length:** Maximum 100 characters per line.
- **Indentation:** 4 spaces per indentation level. Never use tabs.
- **Naming Conventions:**
  - Modules & Packages: `lowercase_with_underscores.py`
  - Classes: `PascalCase` (e.g. `EditorialDecisionEngine`)
  - Functions & Methods: `snake_case()` (e.g. `detect_silence_gaps()`)
  - Constants: `UPPER_SNAKE_CASE` (e.g. `TARGET_LUFS = -16.0`)
- **Linting:** Code must pass `ruff check .` with zero errors.

---

## 2. Strong Typing & Annotations

All function signatures, method parameters, and class attributes must include explicit type annotations:

```python
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def align_audio_track(
    source_audio_path: Path,
    target_segments: List[Dict[str, float]],
    target_duration: float,
    tolerance_ms: float = 200.0,
) -> Tuple[Path, bool]:
    """
    Aligns and WSOLA-stretches an audio track to match target slot duration.
    """
    ...
```

---

## 3. Path Management & System Safety

- **Deterministic Paths:** Never hardcode machine-specific absolute paths. Always use `PathManager` from `core.filesystem.paths`:
  ```python
  from core.filesystem.paths import PathManager

  paths = PathManager()
  config_path = paths.config_dir / "editorial" / "silence_rules.json"
  ```
- **Windows Path Handling:** Accommodate spaces in directory paths (e.g., `D:\Codealytica\Editflow AI`) by wrapping paths in quotes when constructing subprocess CLI strings.
- **Read-Only Media Protection:** Any attempt to delete, truncate, or overwrite files in `PathManager.raw_recordings_root` must raise a `PermissionError` or `CriticalMediaSafetyException`.

---

## 4. Structured Error Handling

- Raise specific exceptions from `core.error_handling.exceptions` rather than generic `Exception` or `RuntimeError`.
- Include diagnostic context in exception messages:
  ```python
  from core.error_handling.exceptions import LoudnessComplianceError

  if measured_lufs < -17.5 or measured_lufs > -14.5:
      raise LoudnessComplianceError(
          f"Master audio loudness ({measured_lufs:.2f} LUFS) violates "
          f"broadcast specification of -16.0 ± 1.0 LUFS."
      )
  ```
- Never catch and silence exceptions with empty `except:` blocks.
