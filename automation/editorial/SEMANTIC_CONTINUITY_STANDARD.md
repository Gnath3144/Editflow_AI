# Semantic Continuity Standard
## Boundary Protection, Transition Smoothing, and Logic Flow

---

## 1. Cut Boundary Safety Windows

Never cut on exact word boundaries. Cutting on an unbuffered word boundary causes:
- Clipped initial consonants (especially plosives /p/, /t/, /k/ and fricatives /s/, /f/).
- Unnatural truncated room decay on vowel offsets.

### Mandatory Buffer Rules:
- **Pre-Cut Lead-in Buffer:** `80ms to 120ms` before the start of removed content, OR `50ms` after previous retained word.
- **Post-Cut Lead-out Buffer:** `100ms to 150ms` before next retained word starts.
- **Cross-Fade Curve:** S-curve equal-power cross-fade duration of `10ms to 15ms` across audio splice points.

---

## 2. Sentence and Clause Wholeness

A segment may not be cut if:
1. It contains the primary subject or predicate of an ongoing sentence.
2. It provides the conditional clause (`"If you omit this parameter..."`) for an action performed on screen.
3. It names the variable, file, or class currently being typed or highlighted in the code editor.

---

## 3. Visual Continuity Verification

When cutting audio:
- If video displays continuous typing or cursor motion, an audio jump cut exceeding 1.5 seconds must use an editorial transition (e.g. slight dip-to-black, rapid whip, or smooth camera zoom cut) to prevent visual hitching.\n