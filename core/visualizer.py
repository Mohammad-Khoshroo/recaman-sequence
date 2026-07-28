"""Arc-based and scatter visualizations of Recamán's sequence."""
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


def plot_scatter(seq: Sequence[int], 
                 title: str = "Recamán's Sequence Scatter Plot") -> plt.Figure:
    """
    Render the sequence as a scatter plot.
    Highly efficient for large N (e.g., N > 10,000) where arcs would
    overlap completely or crash the memory.
    """
    x = np.arange(len(seq))
    y = np.asarray(seq, dtype=np.int64)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    # s=0.5 makes the dots very small so dense areas form patterns
    # alpha=0.6 helps visualize overlapping density
    ax.scatter(x, y, s=0.5, color="navy", alpha=0.6) 
    
    ax.set_title(f"{title} (N = {len(seq)})")
    ax.set_xlabel("n (Index)")
    ax.set_ylabel("a(n) (Value)")
    ax.grid(True, linestyle=':', alpha=0.5)
    fig.tight_layout()
    return fig


def plot_frequency(seq: Sequence[int], 
                   base_hz: float = 220.0, 
                   scale: int = 12,
                   title: str = "Recamán's Sequence Frequency Mapping") -> plt.Figure:
    """
    Plots the sequence mapped to musical frequencies over time.
    This visualizes the sonification (audio) data as a bar chart.
    """
    # Import the frequency mapper from audio module
    from core.audio import _to_frequency
    
    n_terms = len(seq)
    t = np.arange(n_terms)
    freqs = np.array([_to_frequency(v, base_hz, scale) for v in seq])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    # Draw vertical lines (like an equalizer/piano roll)
    ax.vlines(t, 0, freqs, colors='darkred', linewidths=2)
    ax.scatter(t, freqs, color='navy', s=10)
    
    ax.set_title(f"{title} (N = {n_terms})")
    ax.set_xlabel("Time Step (n)")
    ax.set_ylabel("Frequency (Hz)")
    ax.grid(True, axis='y', linestyle=':', alpha=0.5)
    fig.tight_layout()
    return fig