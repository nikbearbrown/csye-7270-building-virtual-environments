#!/usr/bin/env python3
"""analyze-bands.py: counts the stripe bands in the Lab render of lab-shaders/10-stripes-grey.gdshader (png/10-stripes-grey-fp.png)
and prints where each band starts, in units of UV.x. Claim: step(0.5, fract(UV.x * 8.0)) makes 8 dark and 8 light bands, a dark one first."""
from pathlib import Path
from PIL import Image

here = Path(__file__).resolve().parent
for name in ("10-stripes-grey-fp.png", "10-stripes-grey-gc.png"):
    p = here / "png" / name
    if not p.exists():
        continue
    im = Image.open(p).convert("RGB")
    W, H = im.size
    row = [im.getpixel((x, H // 2))[0] for x in range(W)]
    bands = []
    start = 0
    for x in range(1, W):
        if abs(row[x] - row[x - 1]) > 40:        # a jump between 0.3-ish and 0.9-ish grey is about 70+ levels of 255
            bands.append((start, x - 1, row[start]))
            start = x
    bands.append((start, W - 1, row[start]))
    print(name, W, "x", H, "->", len(bands), "bands; first band value", bands[0][2], "(dark first)" if bands[0][2] < row[bands[1][0]] else "(light first)")
    dark = sum(1 for b in bands if b[2] < 160)
    print("   dark bands:", dark, " light bands:", len(bands) - dark)
    print("   band edges in UV.x:", [round(b[0] / W, 4) for b in bands])
