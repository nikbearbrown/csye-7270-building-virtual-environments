#!/usr/bin/env python3
"""analyze_ringconst.py: the ring with sine and cosine per read (lab-shaders/10-ring) against the same ring with its sixteen directions written as constants
(shaders/ring-const, used for the cost timing). Counts the pixels that differ at thickness 1, 2, 3, 4, 8 on the disc and on the thin-stem sprite.
Writes ringconst-summary.txt."""
from pathlib import Path
import numpy as np
import ol_measure as M
HERE = Path(__file__).resolve().parent
L = ["== O1  the ring with sine and cosine per read against the ring with constant directions: pixels that differ (scale 1)"]
for kind in ("disc", "stem"):
    for t in (1, 2, 3, 4, 8):
        a = M.load(HERE / f"png/ringconst-{kind}-sincos-t{t}.png").astype(int)
        b = M.load(HERE / f"png/ringconst-{kind}-const-t{t}.png").astype(int)
        diff = int((np.abs(a - b).max(axis=2) > 0).sum())
        L.append(f"  {kind:5s} thickness {t}: {diff} pixels differ")
print("\n".join(L))
(HERE / "ringconst-summary.txt").write_text("\n".join(L) + "\n")
