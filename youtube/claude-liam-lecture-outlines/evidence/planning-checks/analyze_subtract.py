#!/usr/bin/env python3
"""analyze_subtract.py: the subtraction form against the product form. Writes subtract-summary.txt."""
from pathlib import Path
import numpy as np
import ol_measure as M
HERE = Path(__file__).resolve().parent
L = []
def say(s=""):
    print(s); L.append(s)
base = M.solid(M.load(HERE / "png/01-look-0.000.png"))
im = M.load(HERE / "png/subtract-one.png"); c = M.classes(im)
other = ~(c["stage"] | c["teal"] | c["cream"] | c["line"])
inside_bad = other & base
say("== L1  one read, SUBTRACTION form (mix amount = right neighbor alpha - own alpha), disc sprite at 1:1")
say(f"   sprite pixels whose colour is neither teal, cream nor line: {int(inside_bad.sum())} of {int(base.sum())}; their most common colour: "
    + str(tuple(int(v) for v in max(set(map(tuple, im[inside_bad])), key=list(map(tuple, im[inside_bad])).count))) + "   (a negative mix amount runs away from the line colour: 2 x teal - line colour, clamped to 0..1)")
say("== L2  four reads on the disc plus one isolated opaque pixel at texel (104, 30): subtraction against the film's product form")
a = M.load(HERE / "png/speck-subtract-four.png"); b = M.load(HERE / "png/speck-product-four.png")
diff = (np.abs(a - b).max(axis=2) > 0)
ys, xs = np.nonzero(diff)
say(f"   pixels that differ: {int(diff.sum())}; at screen x {sorted(set(xs.tolist()))}, y {sorted(set(ys.tolist()))}")
sx, sy = 256 + 104, 116 + 30
say(f"   the speck pixel (screen {sx}, {sy}): subtraction {tuple(int(v) for v in a[sy, sx])}, product {tuple(int(v) for v in b[sy, sx])}; teal is (95, 163, 145)")
(HERE / "subtract-summary.txt").write_text("\n".join(L) + "\n")
