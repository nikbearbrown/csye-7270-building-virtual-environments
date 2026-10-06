#!/usr/bin/env python3
"""After running Walker's grid_slice.py --grid 2x2 on TERM-REF-02, count foreground
(any channel <= 235) pixels that touch each cell's edges. Foreground on an inside
edge means a creature was cut in two."""
import sys
import numpy as np
from PIL import Image
d = sys.argv[1]
for n in ["tl", "tr", "bl", "br"]:
    a = np.asarray(Image.open(f"{d}/{n}.png").convert("RGB")).astype(int)
    fg = a.min(axis=2) <= 235
    edge = {"left": int(fg[:, 0].sum()), "right": int(fg[:, -1].sum()), "top": int(fg[0, :].sum()), "bottom": int(fg[-1, :].sum())}
    print(n, "foreground px", int(fg.sum()), "foreground rows/cols touching each edge", edge)
