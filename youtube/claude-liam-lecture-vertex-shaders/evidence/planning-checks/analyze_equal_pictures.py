#!/usr/bin/env python3
"""analyze_equal_pictures.py: pixel-for-pixel comparisons between two objects drawn side by side in one frame (so one shared clock).
Left object centred at x = 340, right at x = 940, 400 px window each, canvas 1280 x 720.
  cut-along        a flag cut 31 x 7 (297 vertices) against the same flag cut 31 x 0 (66 vertices), same ripple
  equiv-lit-color  the explicit-varying shading (10-flag-lit) against the COLOR shortcut (11-flag-final)
  polygon-grid     a Polygon2D with a grid of points and a cell list against the QuadMesh, same ripple
Run: python3 -I analyze_equal_pictures.py   (Pillow + numpy; no Godot)"""
from pathlib import Path

import numpy as np
from PIL import Image

PNG = Path(__file__).resolve().parent / "png"


def compare(name, label):
    a = np.asarray(Image.open(PNG / name).convert("RGB")).astype(int)
    left = a[:, 340 - 200:340 + 200]
    right = a[:, 940 - 200:940 + 200]
    d = np.abs(left - right)
    n = int((d.max(axis=2) > 0).sum())
    print(f"{label}: {n} of {left.shape[0] * left.shape[1]} pixels differ; largest channel difference {int(d.max())}  (frame {name})")


compare("scene-cut-along-t3.00.png", "cut-along (297 vertices against 66)")
compare("scene-equiv-lit-color-t1.50.png", "equiv-lit-color (explicit varying against the COLOR line)")
compare("scene-polygon-grid-t1.00.png", "polygon-grid (Polygon2D grid + cells against the mesh)")
