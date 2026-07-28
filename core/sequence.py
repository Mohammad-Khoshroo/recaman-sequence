"""Generation of Recamán's sequence (OEIS A005132).

Definition:
    a(0) = 0
    a(n) = a(n-1) - n   if a(n-1) - n > 0 and not already in the sequence
         = a(n-1) + n   otherwise
"""
from __future__ import annotations
from typing import Iterator, List


def recaman(n_terms: int) -> List[int]:
    """Return the first n_terms of Recamán's sequence.

    Uses an auxiliary set for O(1) membership tests -> overall O(n)
    expected time and O(n) memory. The naive `proposal not in list`
    check would degrade to O(n^2).
    """
    if n_terms <= 0:
        return []
    seq: List[int] = [0] * n_terms
    seen = {0}
    for n in range(1, n_terms):
        prev = seq[n - 1]
        candidate = prev - n
        if candidate > 0 and candidate not in seen:
            seq[n] = candidate
        else:
            seq[n] = prev + n
        seen.add(seq[n])
    return seq


def recaman_iter() -> Iterator[int]:
    """Lazy infinite generator of Recamán's sequence."""
    a = 0
    seen = {0}
    n = 0
    yield a
    while True:
        n += 1
        candidate = a - n
        if candidate > 0 and candidate not in seen:
            a = candidate
        else:
            a = a + n
        seen.add(a)
        yield a