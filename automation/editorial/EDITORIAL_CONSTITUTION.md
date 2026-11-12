# The Editorial Constitution
## Fundamental Laws of Codealytica Video Production

This document defines the non-negotiable, permanent editorial laws governing every automated cut, audio transformation, and metadata decision across Codealytica training productions.

---

### LAW 1: Absolute Source Protection
Original recordings stored in root directories (e.g. `D:\Codealytica\`) must NEVER be overwritten, moved, truncated, or deleted. All editing operates non-destructively through Edit Decision Lists (EDLs) and outputs into designated production directories (`D:\Codealytica\Enhanced_Videos\`).

### LAW 2: Zero Artificial / Hallucinated Voice
No synthetic voice cloning, text-to-speech injection, or artificial audio regeneration may replace the instructor's real voice in the primary English master. The instructor's authentic vocal delivery must be cleaned, restored, and preserved as spoken.

### LAW 3: The Learning-Value-Per-Minute Imperative
Every second of retained video must deliver educational value. Content that does not advance technical comprehension, illustrate system behavior, debug code, or establish necessary context must be removed. Length is never a metric of success; conciseness and clarity are.

### LAW 4: Semantic Continuity Above All Cuts
A cut is forbidden if it produces:
- A severed clause or mid-word truncation.
- An unresolved pronoun referring to an eliminated premise.
- A visual glitch or unnatural jump cut without an audio bridge or transition safety window.
- Loss of essential context required to understand subsequent code or technical demonstrations.

### LAW 5: Default Unlisted Privacy
All newly uploaded video assets and playlists must default to `UNLISTED`. Public exposure requires explicit human authorization and final multi-stakeholder quality review.

### LAW 6: Traceability of Every Edit
Every decision in an EDL must contain:
1. `decision_id`: Unique identifier.
2. `start_time` & `end_time`: High-precision timestamps.
3. `action`: KEEP, REMOVE, SHORTEN, REPLACE_WITH_NATURAL_CUT, RETAIN_AS_CONTEXT, SEPARATE_SPEAKERS, or HUMAN_REVIEW.
4. `category`: Taxonomic classification of the edit.
5. `confidence`: Algorithmic confidence score (0.00 to 1.00).
6. `rule_reference`: Explicit policy citation from the Editorial Standard.
7. `semantic_impact`: Rationale explaining why the edit enhances or preserves learning value.\n