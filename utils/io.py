"""I/O helpers: persist sequences to CSV / JSON and load them back."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Sequence


def save_csv(seq: Sequence[int], path: str | Path) -> None:
    with open(path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["index", "value"])
        for i, v in enumerate(seq):
            writer.writerow([i, v])


def save_json(seq: Sequence[int], path: str | Path) -> None:
    with open(path, "w") as fh:
        json.dump({"sequence": list(seq)}, fh, indent=2)


def load_json(path: str | Path) -> list[int]:
    with open(path) as fh:
        return json.load(fh)["sequence"]