"""Arc-based visualization of Recamán's sequence.

Consecutive terms are joined by semicircular arcs alternating above and
below the number line (Edmund Harriss' popular visualization).
"""
from __future__ import annotations
from typing import Sequence
import numpy as np
import matplotlib.pyplot as plt


def draw_arc(a: float, b: float, index: int, ax) -> None:
    """Draw a single semicircular arc between two consecutive terms."""
    center = (a + b) / 2
    radius = abs(b - a) / 2
    if radius == 0:
        return
    direction = 1 if index % 2 == 0 else -1
    theta = np.linspace(0, np.pi, 200)
    ax.plot(center + radius * np.cos(theta),
            direction * radius * np.sin(theta),
            color="navy", lw=1.2)


def plot_sequence(seq: Sequence[int],
                  title: str = "Recamán's Sequence") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 6))
    for i in range(len(seq) - 1):
        draw_arc(seq[i], seq[i + 1], i, ax)
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.get_yaxis().set_visible(False)
    fig.tight_layout()
    return fig


def animate_sequence(seq, interval_ms: int = 50, save_path: str | None = None):
    """Build a matplotlib FuncAnimation that draws arcs one by one."""
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_aspect("equal")
    ax.get_yaxis().set_visible(False)
    max_val = max(seq)
    ax.set_xlim(-1, max_val + 1)
    ax.set_ylim(-max_val * 0.6, max_val * 0.6)

    def update(i):
        if i > 0:
            draw_arc(seq[i - 1], seq[i], i - 1, ax)
        ax.set_title(f"Recamán's Sequence — term {i} = {seq[i]}")
        return []

    anim = FuncAnimation(fig, update, frames=len(seq),
                         interval=interval_ms, blit=False, repeat=False)
    if save_path:
        anim.save(save_path, writer="pillow")
    return anim