"""Command-line entry point for the Recamán simulation project."""
from __future__ import annotations
import argparse
from pathlib import Path

from core.sequence import recaman
from core.visualizer import plot_sequence, animate_sequence, plot_scatter, plot_frequency, plot_line
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
    p.add_argument("--scatter", type=Path, help="save scatter plot to PNG (recommended for large N)")
    p.add_argument("--freq", type=Path, help="save frequency mapping plot to PNG")
    p.add_argument("--line", type=Path, help="save connected line plot (values vs index) to PNG")
    p.add_argument("--gif", type=Path, help="save animation to GIF")
    p.add_argument("--wav", type=Path, help="sonify sequence to WAV")
    p.add_argument("--rainbow", action="store_true", help="Color each arc with a different rainbow color")
    p.add_argument("--dynamic", action="store_true", help="Dynamic zoom-out for GIF (camera follows the sequence step-by-step)")
    
    p.add_argument("--interval", type=int, default=50,
                   help="delay between frames in GIF in milliseconds (default: 50, lower=faster, higher=slower)")
    
    p.add_argument("--stats", action="store_true", help="print statistics")
    p.add_argument("--missing", type=int, metavar="K",
                   help="print integers in [0,K) missing from the sequence")
    p.add_argument("--show", action="store_true", help="display the plot")
    return p


def main() -> None:
    args = build_parser().parse_args()
    
    print(f"Generating {args.terms} terms of Recamán's sequence...")
    seq = recaman(args.terms)
    print("Generation complete.")

    # Create output directory if it doesn't exist
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    if args.csv:  
        save_path = output_dir / args.csv
        save_csv(seq, save_path)
        print(f"Saved CSV to {save_path}")
        
    if args.json: 
        save_path = output_dir / args.json
        save_json(seq, save_path)
        print(f"Saved JSON to {save_path}")
    
    if args.png:
        print("Drawing arc visualization...")
        fig = plot_sequence(seq, rainbow=args.rainbow)
        save_path = output_dir / args.png
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved arc plot to {save_path}")
        
    if args.scatter:
        print("Drawing scatter plot...")
        fig_s = plot_scatter(seq)
        save_path = output_dir / args.scatter
        fig_s.savefig(save_path, dpi=200)
        print(f"Saved scatter plot to {save_path}")
        
    if args.freq:
        print("Drawing frequency plot...")
        fig_f = plot_frequency(seq)
        save_path = output_dir / args.freq
        fig_f.savefig(save_path, dpi=150)
        print(f"Saved frequency plot to {save_path}")
        
    if args.line:
        print("Drawing line plot...")
        fig_l = plot_line(seq)
        save_path = output_dir / args.line
        fig_l.savefig(save_path, dpi=150)
        print(f"Saved line plot to {save_path}")
        
    if args.gif:
        print(f"Generating animation with interval {args.interval}ms (this may take a moment)...")
        save_path = output_dir / args.gif
        animate_sequence(
            seq, 
            save_path=str(save_path), 
            rainbow=args.rainbow, 
            dynamic=args.dynamic,
            interval_ms=args.interval
        )
        print(f"Saved GIF to {save_path}")
        
    if args.wav:  
        save_path = output_dir / args.wav
        sonify(seq, out_path=str(save_path))
        print(f"Saved WAV to {save_path}")
        
    if args.stats:
        for k, v in basic_stats(seq).items():
            print(f"{k:>10}: {v}")
            
    if args.missing:
        print("missing:", missing_integers(seq, args.missing))
        
    if args.show:
        import matplotlib.pyplot as plt
        if not (args.png or args.scatter or args.freq or args.line):
            plot_sequence(seq, rainbow=args.rainbow)
        plt.show()


if __name__ == "__main__":
    main()