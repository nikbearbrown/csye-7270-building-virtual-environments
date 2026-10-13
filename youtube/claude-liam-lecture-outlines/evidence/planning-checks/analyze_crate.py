#!/usr/bin/env python3
"""analyze_crate.py: corner pixels. For a square sprite, the pixels the eight-read outline draws that the four-read outline does not = the four corner squares."""
from pathlib import Path
import numpy as np
import ol_measure as M
HERE = Path(__file__).resolve().parent
L = []
def say(s=""):
    print(s); L.append(s)
say("== K1  square sprite (64 x 64 image pixels): outline pixels, four reads against eight reads (scale 1.0)")
say(f"   {'t':>2s} {'four reads':>11s} {'eight reads':>12s} {'only in eight':>14s} {'expected 4*t*t':>15s}")
for t in (1, 2, 3, 4):
    a = M.classes(M.load(HERE / f"png/crate-4-t{t}.png")); b = M.classes(M.load(HERE / f"png/crate-8-t{t}.png"))
    la = a["line"] | a["over"]; lb = b["line"] | b["over"]
    only8 = int((lb & ~la).sum()); only4 = int((la & ~lb).sum())
    say(f"   {t:2d} {int(la.sum()):11d} {int(lb.sum()):12d} {only8:14d} {4*t*t:15d}   (only in four: {only4})")
(HERE / "crate-summary.txt").write_text("\n".join(L) + "\n")
