#!/usr/bin/env python3
"""analyze_filter.py: reads the black/white renders of verify_e_filter.gd, solves each pixel's alpha, writes filter-summary.txt.
Counts half-transparent pixels (alpha between 0.02 and 0.98) and the distinct alpha values: with nearest filtering the outline reads whole image pixels."""
from pathlib import Path
import numpy as np
import ol_measure as M
HERE = Path(__file__).resolve().parent
L = []
def say(s=""):
    print(s); L.append(s)
def alpha(name):
    b = M.load(HERE / f"png/{name}-on-black.png").astype(float); w = M.load(HERE / f"png/{name}-on-white.png").astype(float)
    return np.clip(1.0 - (w - b).mean(axis=2) / 255.0, 0, 1)
say("== E1  outline (08-loop, thickness 1) on the hard-edged sprite, by texture filter and sprite scale: half-transparent pixels and distinct alpha values")
for nm in ("filter-nearest-x2-t1", "filter-linear-x2-t1", "filter-default-x2-t1", "filter-nearest-x2.25-t1", "filter-linear-x2.25-t1",
           "filter-nearest-x2.25-t0", "filter-linear-x2.25-t0"):
    a = alpha(nm); part = (a > 0.02) & (a < 0.98)
    say(f"  {nm:26s} half-transparent px: {int(part.sum()):5d}   distinct alpha values: {len(set(np.round(a[a > 0.02], 2).tolist()))}")
say("\n  reading: 'default' = no filter set on the node or in the project (the scratch project changes nothing) and it matches linear exactly.")
(HERE / "filter-summary.txt").write_text("\n".join(L) + "\n")
