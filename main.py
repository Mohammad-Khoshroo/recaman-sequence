"""Command-line entry point for the Recamán simulation project."""
from __future__ import annotations
import argparse
from pathlib import Path

from core.sequence import recaman
from core.visualizer import plot_sequence, animate_sequence
from core.analyzer import basic_stats, missing_integers
from core.audio import sonify
from utils.io import save_csv, save_json


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Recamán's sequence simulator")
    p.add_argument("-n", "--terms", type=int, default=100,
                   help="number of terms to generate (default: 100)")
    p.add_argument("--csv", type=Path, help="write sequence to CSV")
    p.add_argument("--json", type=Path, help="write sequence to JSON")
    p.add_argument("--png", type=Path, help="save arc visualization to PNG")
    p.add_argument("--gif", type=Path, help="save animation to GIF")
    p.add_argument("--wav", type=Path, help="sonify sequence to WAV")
    p.add_argument("--stats", action="store_true", help="print statistics")
    p.add_argument("--missing", type=int, metavar="K",
                   help="print integers in [0,K) missing from the sequence")
    p.add_argument("--show", action="store_true", help="display the plot")
    return p


def main() -> None:
    args = build_parser().parse_args()
    seq = recaman(args.terms)

    if args.csv:  save_csv(seq, args.csv)
    if args.json: save_json(seq, args.json)
    if args.png:
        fig = plot_sequence(seq)
        fig.savefig(args.png, dpi=150)
    if args.gif:
        animate_sequence(seq, save_path=str(args.gif))
    if args.wav:  sonify(seq, out_path=str(args.wav))
    if args.stats:
        for k, v in basic_stats(seq).items():
            print(f"{k:>10}: {v}")
    if args.missing:
        print("missing:", missing_integers(seq, args.missing))
    if args.show:
        import matplotlib.pyplot as plt
        plot_sequence(seq)
        plt.show()


if __name__ == "__main__":
    main()