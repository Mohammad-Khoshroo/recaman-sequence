"""Statistical / number-theoretic analysis of Recamán's sequence."""
from __future__ import annotations
from typing import Sequence, Dict
import numpy as np


def basic_stats(seq: Sequence[int]) -> Dict[str, float]:
    arr = np.asarray(seq, dtype=np.int64)
    return {
        "n_terms": len(seq),
        "min": int(arr.min()),
        "max": int(arr.max()),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "unique": len(set(seq)),
    }


def missing_integers(seq: Sequence[int], upto: int) -> list[int]:
    """Integers in [0, upto) NOT appearing in the sequence
    (relevant to the open conjecture that every non-negative integer
    eventually appears)."""
    present = set(seq)
    return [k for k in range(upto) if k not in present]


def first_occurrence(seq: Sequence[int]) -> Dict[int, int]:
    """Mapping value -> first index at which it appears."""
    seen: Dict[int, int] = {}
    for i, v in enumerate(seq):
        if v not in seen:
            seen[v] = i
    return seen


def jumps(seq: Sequence[int]) -> np.ndarray:
    """Absolute step sizes between consecutive terms."""
    arr = np.asarray(seq, dtype=np.int64)
    return np.abs(np.diff(arr))