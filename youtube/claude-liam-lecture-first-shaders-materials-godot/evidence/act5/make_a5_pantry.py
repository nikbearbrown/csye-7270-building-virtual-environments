#!/usr/bin/env python3
"""make_a5_pantry.py — cut the two real material spheres out of pantry/ev_mat_baseline.png (Act V, B39).
Each file is a circular cut-out of the REAL engine capture (pixels unaltered, 24 px inside the sphere rim so neither the dark-ground fringe nor the near-black rim pixels (GATE T reads those as text) are included),
placed on transparent alpha so it sits on the cream stage. Left = matte.tres, right = coated.tres (captures/example-native/materials-baseline.png).
Run from the reel folder:  python3 evidence/act5/make_a5_pantry.py
"""
from PIL import Image, ImageDraw
src = Image.open("pantry/ev_mat_baseline.png").convert("RGBA")
for name, cx in (("matte", 324), ("coated", 1188)):
    cy, r = 324, 300
    box = (cx - 324, 0, cx + 324, 648)
    im = src.crop(box)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse((324 - r, 324 - r, 324 + r, 324 + r), fill=255)
    im.putalpha(mask)
    im.save(f"pantry/a5_mat_{name}.png")
    print("wrote", f"pantry/a5_mat_{name}.png", im.size)
