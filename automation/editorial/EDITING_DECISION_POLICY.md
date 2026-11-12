# Editing Decision Policy
## Comprehensive Classification and Action Guidelines

---

## 1. Content Categories & Permitted Actions

| Content Category | Action | Confidence Required | Cross-Fade Buffer | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Open-Mic Pre-Class Chatter** | `REMOVE` | ≥ 0.90 | None | Cut everything prior to formal lecture start |
| **Dead Air (> 2.0s)** | `SHORTEN` | ≥ 0.95 | 10ms | Shorten to 0.40s - 0.50s natural pause |
| **Hesitation Pause (0.8s - 2.0s)** | `SHORTEN` | ≥ 0.85 | 10ms | Shorten to 0.35s - 0.45s conversational pause |
| **Pedagogical Pause (0.5s - 1.2s)** | `KEEP` | ≥ 0.80 | N/A | Preserve cognitive processing time |
| **Pure Verbal Filler ("um", "uh")** | `REMOVE` | ≥ 0.90 | 12ms | Remove if flanked by valid speech |
| **False Start / Sentence Restart** | `REMOVE` | ≥ 0.85 | 15ms | Keep only final clean sentence formulation |
| **Unneeded Confirmation Loop** | `REMOVE` | ≥ 0.88 | 15ms | "Are you getting it?", "Clear na?", etc. |
| **Vital Participant Question** | `RETAIN_AS_CONTEXT` | ≥ 0.85 | 20ms | Clean audio, level volume, keep instructor answer |
| **Trivial / Logistics Interaction** | `REMOVE` | ≥ 0.90 | 15ms | Mute checks, attendance, connection issues |
| **Code Execution Delay (> 3.0s)** | `SHORTEN` | ≥ 0.90 | 10ms | Accelerate or jump to output appearance |

---

## 2. Decision Conflict Resolution Hierarchy

When two rules conflict, apply the following strict hierarchy:
1. **Safety Window / Non-Truncation Rule:** Never cut speech if doing so clips a legitimate word boundary, even if adjacent to a filler.
2. **Pedagogical Meaning:** Retain questionable discourse markers if they establish logical contrast ("However", "Consequently", "On the other hand").
3. **Instructor Preference:** When in doubt between `REMOVE` and `KEEP` on borderline explanations, generate `HUMAN_REVIEW` with conservative temporary `KEEP`.\n