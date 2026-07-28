"""Arc-based and scatter visualizations of Recamán's sequence."""
from __future__ import annotations
from typing import Sequence
import numpy as np
import matplotlib.pyplot as plt


def draw_arc(a: float, b: float, index: int, ax, rainbow: bool = False) -> None:
    """Draw a single semicircular arc between two consecutive terms."""
    center = (a + b) / 2
    radius = abs(b - a) / 2
    if radius == 0:
        return
    direction = 1 if index % 2 == 0 else -1
    theta = np.linspace(0, np.pi, 200)
    
    if rainbow:
        # Map index to a vibrant rainbow color (cycling through hues)
        color = plt.cm.hsv((index * 10 % 360) / 360.0)
    else:
        # Different colors for top and bottom
        color = "#2980b9" if direction == 1 else "#c0392b"
        
    ax.plot(center + radius * np.cos(theta),
            direction * radius * np.sin(theta),
            color=color, lw=1.5)


def plot_sequence(seq: Sequence[int], rainbow: bool = False, 
                  title: str = "Recamán's Sequence") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Draw the number line
    ax.axhline(0, color='black', linewidth=1.5, zorder=1)
    ax.tick_params(axis='x', colors='black', labelsize=10)
    ax.get_yaxis().set_visible(False)
    
    for i in range(len(seq) - 1):
        draw_arc(seq[i], seq[i + 1], i, ax, rainbow)
        
    # Set limits to fit everything perfectly
    max_val = max(seq) if seq else 1
    # The maximum step size is always the last step (len(seq)-1)
    # So the max radius is exactly (len(seq)-1)/2
    max_radius = (len(seq) - 1) / 2.0 if len(seq) > 1 else 1
    
    ax.set_xlim(-1, max_val + 1)
    ax.set_ylim(-max_radius * 1.2, max_radius * 1.2)
    
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=14)
    fig.tight_layout()
    return fig


def animate_sequence(seq, interval_ms: int = 50, save_path: str | None = None, rainbow: bool = False, dynamic: bool = False):
    """Build a matplotlib FuncAnimation that draws arcs one by one."""
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.get_yaxis().set_visible(False)
    
    # Draw the number line for animation
    ax.axhline(0, color='black', linewidth=1.5, zorder=1)
    
    if not dynamic:
        # Fixed view: calculate absolute max limits from the start
        max_val = max(seq) if seq else 1
        max_radius = (len(seq) - 1) / 2.0 if len(seq) > 1 else 1
        ax.set_xlim(-1, max_val + 1)
        ax.set_ylim(-max_radius * 1.2, max_radius * 1.2)
    else:
        # Dynamic view: start with a small window
        ax.set_xlim(-1, 2)
        ax.set_ylim(-1, 1)
        
    ax.set_aspect("equal")

    def update(i):
        if i > 0:
            draw_arc(seq[i - 1], seq[i], i - 1, ax, rainbow)
            
        if dynamic:
            # The step size is exactly i, so the radius is i/2
            current_radius = i / 2.0 if i > 0 else 0.5
            # Find the maximum value reached so far
            current_max_val = max(seq[:i+1]) if i > 0 else 1
            
            # Add dynamic margins
            margin_x = max(1, current_max_val * 0.05)
            margin_y = max(1, current_radius * 0.2)
            
            # Expand the view smoothly
            ax.set_xlim(-1 - margin_x, current_max_val + margin_x)
            ax.set_ylim(-current_radius - margin_y, current_radius + margin_y)
            
        ax.set_title(f"Recamán's Sequence — term {i} = {seq[i]}", fontsize=14)
        return []

    anim = FuncAnimation(fig, update, frames=len(seq),
                         interval=interval_ms, blit=False, repeat=False)
    if save_path:
        anim.save(save_path, writer="pillow", dpi=150)
    return anim


def plot_scatter(seq: Sequence[int], 
                 title: str = "Recamán's Sequence Scatter Plot") -> plt.Figure:
    x = np.arange(len(seq))
    y = np.asarray(seq, dtype=np.int64)
    
    fig, ax = plt.subplots(figsize=(10, 8))
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
    from core.audio import _to_frequency
    n_terms = len(seq)
    t = np.arange(n_terms)
    freqs = np.array([_to_frequency(v, base_hz, scale) for v in seq])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.vlines(t, 0, freqs, colors='darkred', linewidths=2)
    ax.scatter(t, freqs, color='navy', s=10)
    
    ax.set_title(f"{title} (N = {n_terms})")
    ax.set_xlabel("Time Step (n)")
    ax.set_ylabel("Frequency (Hz)")
    ax.grid(True, axis='y', linestyle=':', alpha=0.5)
    fig.tight_layout()
    return fig


def plot_line(seq: Sequence[int], 
              title: str = "Recamán's Sequence Line Plot") -> plt.Figure:
    x = np.arange(len(seq))
    y = np.asarray(seq, dtype=np.int64)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, color='red', linewidth=1.5, marker='', linestyle='-')
    
    ax.set_title(f"{title} (N = {len(seq)})")
    ax.set_xlabel("n (Index)")
    ax.set_ylabel("a(n) (Value)")
    ax.grid(True, linestyle=':', alpha=0.5)
    fig.tight_layout()
    return fig