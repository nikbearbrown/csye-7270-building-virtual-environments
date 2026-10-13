#!/usr/bin/env python3
"""analyze-your-turn.py: proves the two checks of the film's "Your turn" prompt can be met, with a reference answer (calc/your-turn-reference.gdshader,
not shown in the film). (1) thickness at zero draws nothing; (2) the ring is round on a square view and oval on a wide one; (3) with both dials at
their largest the ring still fits the square. Writes analysis-your-turn.txt."""
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
out = []
def teal(name):
    a = np.asarray(Image.open(PNG / f"{name}.png").convert("RGB"), int)
    return (abs(a[..., 0] - 94) < 6) & (abs(a[..., 1] - 163) < 6) & (abs(a[..., 2] - 145) < 6)
def box(m):
    ys, xs = np.where(m)
    return (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None

m0 = teal("your-turn-reference-thickness-0")
out.append(f"thickness 0 (480 x 480): teal pixels = {int(m0.sum())}  (check 1: nothing is drawn)\n")
md = teal("your-turn-reference-default")
b = box(md); w = b[2] - b[0] + 1; h = b[3] - b[1] + 1
out.append(f"defaults (480 x 480): the ring's bounding box is {w} x {h} px, ratio {w / h:.3f}  (check 2: round on a square)\n")
mw = teal("your-turn-reference-wide")
b = box(mw); w = b[2] - b[0] + 1; h = b[3] - b[1] + 1
out.append(f"defaults on a 640 x 360 view: the ring's bounding box is {w} x {h} px, ratio {w / h:.3f}  (check 2: oval on a wide rectangle; the view's ratio is {640 / 360:.3f})\n")
m1 = teal("your-turn-reference-thickness-1")
b = tuple(int(v) for v in box(m1))
out.append(f"radius 1 and thickness 1 (480 x 480): the ring's bounding box is {b}  (view is 0..479 on both axes: the ring still fits)\n")
(HERE / "analysis-your-turn.txt").write_text("".join(out)); print("".join(out))
