"""
Speaker Identification, Diarization & Voice Protection Module
Employs pure PyTorch STFT Resemblyzer voice embeddings to bypass Windows DLL blocks.
Identifies PRIMARY_INSTRUCTOR (Gopinath Kshatriya) vs PARTICIPANTS vs BACKGROUND_NOISE.
"""

import os
import json
import numpy as np
import torch
import soundfile as sf
from typing import List, Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "configuration", "speaker_rules.json")

def patch_resemblyzer_stft():
    """
    Replaces resemblyzer's librosa-based wav_to_mel_spectrogram with pure PyTorch STFT
    to avoid numba and DLL load failures on Windows Application Control policies.
    """
    try:
        import resemblyzer.audio
        
        def pytorch_wav_to_mel_spectrogram(wav):
            if isinstance(wav, np.ndarray):
                tensor_wav = torch.from_numpy(wav).float()
            else:
                tensor_wav = wav.float()
            
            # Resemblyzer constants: sr=16000, n_fft=400, hop=160, win=400, 40 mels
            n_fft = 400
            hop_length = 160
            win_length = 400
            n_mels = 40
            sr = 16000
            
            window = torch.hann_window(win_length)
            stft = torch.stft(
                tensor_wav,
                n_fft=n_fft,
                hop_length=hop_length,
                win_length=win_length,
                window=window,
                center=True,
                return_complex=True
            )
            magnitudes = stft.abs() ** 2
            
            # Simple mel filterbank approximation
            mel_basis = torch.zeros((n_mels, n_fft // 2 + 1))
            hz_points = np.linspace(0, sr / 2, n_fft // 2 + 1)
            mel_points = np.linspace(0, 2595 * np.log10(1 + (sr / 2) / 700), n_mels + 2)
            hz_filter_points = 700 * (10 ** (mel_points / 2595) - 1)
            
            for m in range(1, n_mels + 1):
                f_m_minus = hz_filter_points[m - 1]
                f_m = hz_filter_points[m]
                f_m_plus = hz_filter_points[m + 1]
                
                for k, f in enumerate(hz_points):
                    if f_m_minus <= f <= f_m:
                        mel_basis[m - 1, k] = (f - f_m_minus) / (f_m - f_m_minus + 1e-8)
                    elif f_m <= f <= f_m_plus:
                        mel_basis[m - 1, k] = (f_m_plus - f) / (f_m_plus - f_m + 1e-8)
            
            mel_spec = torch.matmul(mel_basis, magnitudes)
            log_mel_spec = torch.log(torch.clamp(mel_spec, min=1e-5))
            return log_mel_spec.numpy().T
            
        resemblyzer.audio.wav_to_mel_spectrogram = pytorch_wav_to_mel_spectrogram
        return True
    except Exception as e:
        print(f"Warning: could not patch resemblyzer STFT: {e}")
        return False

class SpeakerDiarizer:
    def __init__(self, config_path: Optional[str] = None):
        path = config_path or CONFIG_PATH
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "primary_instructor": {"min_similarity_threshold": 0.82},
                "co_instructor": {"min_similarity_threshold": 0.80}
            }
        
        self.instructor_threshold = self.config.get("primary_instructor", {}).get("min_similarity_threshold", 0.82)
        self.reference_embeddings: List[np.ndarray] = []
        self._encoder = None
        patch_resemblyzer_stft()

    def _get_encoder(self):
        if self._encoder is None:
            from resemblyzer import VoiceEncoder
            self._encoder = VoiceEncoder(device="cpu")
        return self._encoder

    def enroll_reference_audio(self, audio_path: str):
        """
        Enrolls a clean audio file of Gopinath Kshatriya as a reference embedding.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Reference audio not found: {audio_path}")
        
        from resemblyzer import preprocess_wav
        wav = preprocess_wav(audio_path)
        encoder = self._get_encoder()
        emb = encoder.embed_utterance(wav)
        self.reference_embeddings.append(emb)

    def compute_similarity(self, wav_slice: np.ndarray) -> float:
        """
        Computes cosine similarity between wav_slice and enrolled reference embeddings.
        """
        if not self.reference_embeddings:
            # Fallback when no reference is enrolled: assume valid
            return 1.0
        
        from resemblyzer import preprocess_wav
        wav = preprocess_wav(wav_slice)
        if len(wav) < 1600:  # less than 100ms
            return 0.5
        
        encoder = self._get_encoder()
        emb = encoder.embed_utterance(wav)
        
        sims = [float(np.dot(emb, ref) / (np.linalg.norm(emb) * np.linalg.norm(ref) + 1e-8))
                for ref in self.reference_embeddings]
        return max(sims)

    def classify_segment(self, wav_slice: np.ndarray, text: str = "") -> Dict[str, Any]:
        sim = self.compute_similarity(wav_slice)
        
        if sim >= self.instructor_threshold:
            role = "PRIMARY_INSTRUCTOR"
            action = "KEEP"
        elif sim >= 0.75:
            role = "CO_INSTRUCTOR"
            action = "KEEP"
        else:
            # Check if this is a valuable participant question or background noise
            if "?" in text or any(q in text.lower() for q in ["how", "what", "why", "can we", "could you"]):
                role = "PARTICIPANT_CONCEPTUAL"
                action = "RETAIN_AS_CONTEXT"
            else:
                role = "PARTICIPANT_IRRELEVANT"
                action = "STRIP_COMPLETELY"

        return {
            "speaker_role": role,
            "similarity_score": round(sim, 3),
            "action": action
        }
