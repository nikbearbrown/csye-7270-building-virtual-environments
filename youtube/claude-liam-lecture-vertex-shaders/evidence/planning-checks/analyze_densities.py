#!/usr/bin/env python3
"""analyze_densities.py: gap between the drawn top edge and the true sine, for a rippled flag cut into 4, 10 and 32 pieces.
Frames come from vtx11.gd (node scaled 3x, so one screen pixel = 1/3 logical pixel). Run: python3 -I analyze_densities.py"""
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
STAGE = np.array([217, 213, 202])
S = 3.0                 # node scale in the frames
W, H, AMP, FREQ = 288.0, 144.0, 24.0, 8.0
for n in (3, 9, 31):
    a = np.asarray(Image.open(HERE / "png" / f"density-x3-subdivide-{n}.png").convert("RGB")).astype(int)
    m = (np.abs(a - STAGE).max(axis=2) > 12)
    xs0 = np.where(m.any(axis=0))[0]
    x_left, x_right = xs0.min(), xs0.max()
    width_px = x_right - x_left + 1
    xs = np.arange(x_left, x_right + 1)
    ys = np.array([np.where(m[:, x])[0].min() for x in xs], float)
    u = (xs - x_left + 0.5) / width_px
    # the flag's undisturbed top edge is at screen y = 360 - (H/2)*S
    y0 = 360 - (H / 2) * S
    true = y0 + AMP * S * np.sin(FREQ * u)
    gap_logical = np.abs(ys - true).max() / S
    pieces = n + 1
    per_wave = pieces / (FREQ / (2 * np.pi))
    theory = AMP * (1 - np.cos((FREQ / pieces) / 2))
    print(f"subdivide_width {n}: {pieces} pieces, {per_wave:.1f} per wave; worst gap measured {gap_logical:.2f} px = {100 * gap_logical / AMP:.1f}% of the {AMP:.0f} px wave height (formula {theory:.2f} px = {100 * theory / AMP:.1f}%)")
print("worst gap for p pieces per wave = 1 - cos(pi / p) of the wave height:", {p: round(100 * (1 - np.cos(np.pi / p)), 1) for p in (3, 4, 6, 8, 12, 16, 25)})
