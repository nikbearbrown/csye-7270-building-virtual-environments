#!/usr/bin/env python3
"""analyze_sheets.py: separate frame images (verify_c_sheets.gd, block C3): an AnimatedSprite2D with two SEPARATE padded textures (a disc and a wide pill), 08-loop at thickness 3, scale 1.
Measures, for the frame shown, how far the outline's bounding box reaches beyond the solid shape on each side (left, top, right, bottom). If every side reads 3, the outline follows the
frame that is shown and nothing leaks in from the other frame's texture. Writes sheets-summary.txt."""
from pathlib import Path
import ol_measure as M
HERE = Path(__file__).resolve().parent
L = ["== C3  AnimatedSprite2D with two separate frame images: outline margin beyond the solid shape of the frame shown (thickness 3, scale 1)"]
for name, label in (("anim-separate-frame0", "frame 0 (disc)"), ("anim-separate-frame1", "frame 1 (wide pill)")):
    im = M.load(HERE / f"png/{name}.png")
    c = M.classes(im)
    sol = c["teal"] | c["cream"]
    line = c["line"] | c["over"]
    sx0, sy0, sx1, sy1 = M.bbox(sol)
    lx0, ly0, lx1, ly1 = M.bbox(line)
    L.append(f"  {label:22s} solid box x {sx0}..{sx1}, y {sy0}..{sy1}; outline margin left {sx0 - lx0}, top {sy0 - ly0}, right {lx1 - sx1}, bottom {ly1 - sy1}; outline pixels {int(line.sum())}")
print("\n".join(L))
(HERE / "sheets-summary.txt").write_text("\n".join(L) + "\n")
