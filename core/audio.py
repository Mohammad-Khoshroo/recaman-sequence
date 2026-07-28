"""Sonification (audification) of Recamán's sequence."""
from __future__ import annotations
from typing import Sequence
import numpy as np
from scipy.io.wavfile import write


def _to_frequency(value: int, base_hz: float = 220.0, scale: int = 12) -> float:
    """Map an integer to a frequency via a chromatic scale (mod `scale`)."""
    semitone = value % scale
    return base_hz * (2 ** (semitone / scale))


def sonify(seq: Sequence[int],
           sample_rate: int = 44100,
           note_duration: float = 0.15,
           out_path: str = "recaman.wav") -> str:
    n_samples = int(sample_rate * note_duration)
    t = np.linspace(0, note_duration, n_samples, endpoint=False)
    envelope = np.exp(-3 * t)                       # exponential decay
    waveform = np.zeros(n_samples * len(seq))
    for i, v in enumerate(seq):
        freq = _to_frequency(int(v))
        chunk = envelope * np.sin(2 * np.pi * freq * t)
        waveform[i * n_samples:(i + 1) * n_samples] = chunk
    # normalize to 16-bit PCM
    waveform = np.int16(waveform / np.max(np.abs(waveform)) * 32767)
    write(out_path, sample_rate, waveform)
    return out_path