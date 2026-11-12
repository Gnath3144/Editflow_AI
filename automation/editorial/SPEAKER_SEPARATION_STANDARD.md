# Speaker Separation and Voice Protection Standard
## Resemblyzer & Acoustic Diarization Specification

---

## 1. Speaker Hierarchy & Roles

1. **`PRIMARY_INSTRUCTOR` (Gopinath Kshatriya):**
   - High voice similarity against golden studio reference (`cosine similarity ≥ 0.82`).
   - Protected audio channel. Audio receives full vocal presence mastering.
2. **`CO_INSTRUCTOR` / Guest Speaker:**
   - Pre-registered secondary voice profile.
   - Retained when delivering technical content.
3. **`PARTICIPANT_CONCEPTUAL`:**
   - Unregistered voice asking a direct, valuable technical question.
   - Action: Retained as context, volume boosted/leveled to match instructor (-16 LUFS).
4. **`PARTICIPANT_IRRELEVANT`:**
   - Background chatter, background domestic sounds, keyboard clatter, breathing, echo.
   - Action: Completely stripped from final audio master.

---

## 2. Resemblyzer Pure PyTorch Implementation

To guarantee platform stability and prevent Windows Application Control DLL blocks (`_helperlib.pyd` from `numba`/`librosa`), all voice embedding extraction MUST use a pure PyTorch STFT Mel-spectrogram implementation:

```python
# Pure PyTorch STFT Mel-spectrogram bypasses numba and librosa entirely:
mel_spec = torch.stft(
    wav_tensor,
    n_fft=400,
    hop_length=160,
    win_length=400,
    window=torch.hann_window(400),
    return_complex=True
).abs()
```

---

## 3. Reference Enrollment Profile

Reference enrollment audio files for Gopinath Kshatriya are stored in:
`D:\Codealytica\Enhanced_Videos\Day_02\Audio_Master\`
Every incoming segment is compared against an ensemble of at least 3 reference vectors.\n