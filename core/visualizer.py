"""Arc-based and scatter visualizations of Recamán's sequence."""
from __future__ import annotations
from typing import Sequence
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D


def get_rotated_limits(x_min, x_max, y_min, y_max, angle):
    """Calculate new bounding box limits after rotation."""
    if angle == 0:
        return x_min, x_max, y_min, y_max
    trans = Affine2D().rotate_deg(angle)
    corners = [(x_min, y_min), (x_max, y_min), (x_min, y_max), (x_max, y_max)]
    rotated = [trans.transform_point(p) for p in corners]
    rot_x = [p[0] for p in rotated]
    rot_y = [p[1] for p in rotated]
    return min(rot_x), max(rot_x), min(rot_y), max(rot_y)


def draw_arc(a: float, b: float, index: int, ax, rainbow: bool = False, dark: bool = False, total_terms: int = 100, transform=None) -> None:
    """Draw a single semicircular arc between two consecutive terms."""
    center = (a + b) / 2
    radius = abs(b - a) / 2
    if radius == 0:
        return
    direction = 1 if index % 2 == 0 else -1
    theta = np.linspace(0, np.pi, 200)
    
    if rainbow:
        color = plt.cm.Spectral(index / max(1, total_terms))
    else:
        if dark:
            color = "#3498db" if direction == 1 else "#e74c3c"
        else:
            color = "#2980b9" if direction == 1 else "#c0392b"
        
    x_data = center + radius * np.cos(theta)
    y_data = direction * radius * np.sin(theta)
    
    if transform:
        ax.plot(x_data, y_data, color=color, lw=1.5, transform=transform)
    else:
        ax.plot(x_data, y_data, color=color, lw=1.5)


def plot_sequence(seq: Sequence[int], rainbow: bool = False, dark: bool = False, rotate_deg: float = 0.0, show_axis: bool = True, 
                  title: str = "Recamán's Sequence") -> plt.Figure:
    bg_color = "k" if dark else "white"
    line_color = "white" if dark else "black"
    text_color = "white" if dark else "black"
    
    fig, ax = plt.subplots(figsize=(16, 8), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    
    transform = Affine2D().rotate_deg(rotate_deg) + ax.transData if rotate_deg != 0 else None
    
    max_val = max(seq) if seq else 1
    max_radius = (len(seq) - 1) / 2.0 if len(seq) > 1 else 1
    x_min, x_max = -1, max_val + 1
    y_min, y_max = -max_radius * 1.2, max_radius * 1.2
    
    if show_axis:
        ax.plot([x_min, x_max], [0, 0], color=line_color, linewidth=1.5, zorder=1, transform=transform)
        ax.tick_params(axis='x', colors=text_color, labelsize=10)
        ax.get_yaxis().set_visible(False)
    else:
        ax.axis('off')
    
    for i in range(len(seq) - 1):
        draw_arc(seq[i], seq[i + 1], i, ax, rainbow, dark, len(seq), transform)
        
    if rotate_deg != 0:
        rx_min, rx_max, ry_min, ry_max = get_rotated_limits(x_min, x_max, y_min, y_max, rotate_deg)
        ax.set_xlim(rx_min, rx_max)
        ax.set_ylim(ry_min, ry_max)
    else:
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
    
    ax.set_aspect("equal")
    
    if show_axis:
        ax.set_title(title, fontsize=14, color=text_color)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        
    fig.tight_layout()
    return fig


def animate_sequence(seq, interval_ms: int = 50, save_path: str | None = None, rainbow: bool = False, dynamic: bool = False, dark: bool = False, show_axis: bool = True):
    """Build a matplotlib FuncAnimation that draws arcs one by one."""
    from matplotlib.animation import FuncAnimation

    bg_color = "k" if dark else "white"
    line_color = "white" if dark else "black"
    text_color = "white" if dark else "black"

    fig, ax = plt.subplots(figsize=(16, 8), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    
    if not show_axis:
        ax.axis('off')
    else:
        ax.get_yaxis().set_visible(False)
        ax.axhline(0, color=line_color, linewidth=1.5, zorder=1)
    
    if not dynamic:
        max_val = max(seq) if seq else 1
        max_radius = (len(seq) - 1) / 2.0 if len(seq) > 1 else 1
        x_min, x_max = -1, max_val + 1
        y_min, y_max = -max_radius * 1.2, max_radius * 1.2
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_aspect("equal")
    else:
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect("equal", adjustable="datalim")

    def update(i):
        if i > 0:
            draw_arc(seq[i - 1], seq[i], i - 1, ax, rainbow, dark, len(seq), transform=None)
            
        if dynamic:
            current_radius = i / 2.0 if i > 0 else 0.5
            current_max_val = max(seq[:i+1]) if i > 0 else 1
            margin = max(1, current_radius * 0.1)
            
            ax.set_xlim(-1 - margin, current_max_val + margin)
            ax.set_ylim(-current_radius - margin, current_radius + margin)
            
        if show_axis:
            ax.set_title(f"Recamán's Sequence — term {i} = {seq[i]}", fontsize=14, color=text_color)
        return []

    anim = FuncAnimation(fig, update, frames=len(seq),
                         interval=interval_ms, blit=False, repeat=False)
    if save_path:
        anim.save(save_path, writer="pillow", dpi=150, savefig_kwargs={'facecolor': bg_color})
    return anim


def plot_scatter(seq: Sequence[int], dark: bool = False,
                 title: str = "Recamán's Sequence Scatter Plot") -> plt.Figure:
    bg_color = "k" if dark else "white"
    text_color = "white" if dark else "black"
    
    x = np.arange(len(seq))
    y = np.asarray(seq, dtype=np.int64)
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    ax.scatter(x, y, s=0.5, color="#3498db" if dark else "navy", alpha=0.6) 
    
    ax.set_title(f"{title} (N = {len(seq)})", color=text_color)
    ax.set_xlabel("n (Index)", color=text_color)
    ax.set_ylabel("a(n) (Value)", color=text_color)
    ax.grid(True, linestyle=':', alpha=0.5, color=text_color)
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(text_color)
        
    fig.tight_layout()
    return fig


def plot_frequency(seq: Sequence[int], dark: bool = False,
                   base_hz: float = 220.0, scale: int = 12,
                   title: str = "Recamán's Sequence Frequency Mapping") -> plt.Figure:
    from core.audio import _to_frequency
    bg_color = "k" if dark else "white"
    text_color = "white" if dark else "black"
    
    n_terms = len(seq)
    t = np.arange(n_terms)
    freqs = np.array([_to_frequency(v, base_hz, scale) for v in seq])
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    ax.vlines(t, 0, freqs, colors='#e74c3c', linewidths=2)
    ax.scatter(t, freqs, color='#3498db', s=10)
    
    ax.set_title(f"{title} (N = {n_terms})", color=text_color)
    ax.set_xlabel("Time Step (n)", color=text_color)
    ax.set_ylabel("Frequency (Hz)", color=text_color)
    ax.grid(True, axis='y', linestyle=':', alpha=0.5, color=text_color)
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(text_color)
        
    fig.tight_layout()
    return fig


def plot_line(seq: Sequence[int], dark: bool = False,
              title: str = "Recamán's Sequence Line Plot") -> plt.Figure:
    bg_color = "k" if dark else "white"
    text_color = "white" if dark else "black"
    
    x = np.arange(len(seq))
    y = np.asarray(seq, dtype=np.int64)
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    ax.plot(x, y, color='#e74c3c', linewidth=1.5, marker='', linestyle='-')
    
    ax.set_title(f"{title} (N = {len(seq)})", color=text_color)
    ax.set_xlabel("n (Index)", color=text_color)
    ax.set_ylabel("a(n) (Value)", color=text_color)
    ax.grid(True, linestyle=':', alpha=0.5, color=text_color)
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(text_color)
        
    fig.tight_layout()
    return fig