#!/usr/bin/env python3
"""make_crops.py — crops of REAL captures for Act X (Builder 3). Nothing is drawn; every file is a rectangle cut from a real PNG.
  pantry/a10_lab_panel.png  : the V verification panel of captures/lab/lab_000609.png (scripted input), 3840x2160 source, box (2222,436,3326,1040): the panel exactly (text rows measured at y 486-530, 579-637, 671-730, 764-809, 858-916, 951-1009)
  pantry/a10_pad_idle.png   : the pad of captures/lab/lab_000300.png (scripted input), the lane plan's box (1150,640,1760,1190)
  pantry/a10_pad_half.png   : a centre cut of pantry/ev_pad_0.5.png (the example's pad at activation 0.5, Compatibility), 1620x1080 -> 1200x800
Run from anywhere:  python3 evidence/act10/make_crops.py"""
from pathlib import Path
from PIL import Image
R = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot")
jobs = [("captures/lab/lab_000609.png", (2222, 436, 3326, 1040), "pantry/a10_lab_panel.png"),
        ("captures/lab/lab_000300.png", (1150, 640, 1760, 1190), "pantry/a10_pad_idle.png"),
        ("pantry/ev_pad_0.5.png", (210, 140, 1410, 940), "pantry/a10_pad_half.png")]
for s, box, o in jobs:
    im = Image.open(R / s).convert("RGB")
    c = im.crop(box)
    c.save(R / o)
    print(o, c.size, "from", s, box, "source", im.size)
