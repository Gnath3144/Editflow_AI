# Multilingual Dubbing Preparation Standard
## Master Alignment and Prosodic Mapping for 12 Languages

---

## 1. Target Language Coverage

The Codealytica localization pipeline supports 12 standardized language profiles:
1. **Telugu (`te`)** - Primary Indic
2. **Hindi (`hi`)** - National Indic
3. **Tamil (`ta`)** - South Indic
4. **Kannada (`kn`)** - South Indic
5. **Malayalam (`ml`)** - South Indic
6. **Marathi (`mr`)** - Western Indic
7. **Bengali (`bn`)** - Eastern Indic
8. **Gujarati (`gu`)** - Western Indic
9. **Spanish (`es`)** - Global European/Americas
10. **French (`fr`)** - Global European
11. **German (`de`)** - Central European
12. **Japanese (`ja`)** - East Asian

---

## 2. Pre-Dubbing Timing Constraints

Languages expand or contract relative to English spoken duration. The dubbing engine applies expansion factor limits:

| Language | Typical Syllable Rate | Expansion Factor vs EN | Maximum Allowed Drift |
| :--- | :--- | :--- | :--- |
| **Telugu** | 5.8 syl/sec | `1.18x` | `± 250ms` per sentence |
| **Hindi** | 5.2 syl/sec | `1.12x` | `± 200ms` per sentence |
| **Tamil** | 6.0 syl/sec | `1.20x` | `± 250ms` per sentence |
| **Kannada** | 5.6 syl/sec | `1.16x` | `± 250ms` per sentence |
| **Malayalam** | 6.2 syl/sec | `1.22x` | `± 300ms` per sentence |
| **Spanish** | 7.8 syl/sec | `1.15x` | `± 200ms` per sentence |
| **German** | 5.5 syl/sec | `1.10x` | `± 150ms` per sentence |
| **Japanese** | 8.0 mora/sec | `1.05x` | `± 150ms` per sentence |

---

## 3. Strict Pre-Dubbing Validation Rules

Before an English master video can be approved for translation:
1. Every retained sentence must have valid start and end timestamps.
2. English transcript words must be clean, devoid of stutters, fillers, and interruptions.
3. Pause slots between sentences must be at least `400ms` to provide breathing room for localized target speech expansion.\n