#!/usr/bin/env python3
"""analyze_bigcopy.py: the "bigger copy behind the sprite" outline (verify_h_bigcopy.gd): a plus sign (arms 48 wide and 16 thick in image pixels) drawn at 2x with a tinted copy at
2.4x (a fifth bigger) behind it. Measures the border at the tip of an arm and along the side of an arm. Writes bigcopy-summary.txt."""
from pathlib import Path
import numpy as np
import ol_measure as M
HERE = Path(__file__).resolve().parent
im = M.load(HERE / "png/bigcopy-plus.png")
teal = M.mask_of(im, M.TEAL, 6)
copy_col = np.round(np.array(M.TEAL) * np.array([0.25, 0.25, 0.75])).astype(int)       # teal times the copy's modulate (0.25, 0.25, 0.75)
copy = M.mask_of(im, copy_col, 8)
cx, cy = 320, 180


def border(x, y, dx, dy):
    while teal[y, x]:
        x += dx; y += dy
    n = 0
    while copy[y, x]:
        n += 1; x += dx; y += dy
    return n


tip = border(cx, cy, 1, 0)                 # along the middle of the right arm, out past its tip
side = border(cx + 30, cy, 0, -1)          # from the middle of the right arm, 30 px out from the centre, up past its side
L = ["== H1  the bigger-copy outline on a plus sign (arms 24 long and 8 wide each side of the centre in image pixels; drawn at 2x, the copy at 2.4x)",
     f"  copy tinted (teal x (0.25, 0.25, 0.75)) = {tuple(int(v) for v in copy_col)}",
     f"  border at the tip of an arm: {tip} px   (expected 0.2 x 24 x 2 = 9.6)",
     f"  border along the side of an arm: {side} px   (expected 0.2 x 8 x 2 = 3.2)"]
print("\n".join(L))
(HERE / "bigcopy-summary.txt").write_text("\n".join(L) + "\n")
