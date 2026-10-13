#!/usr/bin/env python3
"""analyze_route.py: the 3840 x 2160 SubViewport route against the 1280 x 720 route (route_check.gd / run_route.sh).
For every scene and every time: take the 3840 x 2160 picture, keep the pixel at the centre of every 3 x 3 block (a 1280 x 720 picture) and compare it with the
1280 x 720 render of the same frame. Writes route-summary.txt. Usage: python3 analyze_route.py [png folder]"""
import os, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "outline-film-route-png"
L = []
def say(s=""):
    print(s); L.append(s)
say("The capture route: 3840 x 2160 SubViewport over the 1280 x 720 canvas, sampled at the centre of each 3 x 3 block, against the 1280 x 720 render of the same frame")
say("(no shader in this film reads window pixels; every offset is in texture units)")
total_pairs = total_diff_px = 0
worst = 0
for nat in sorted(folder.glob("*-native-t*.png")):
    big = folder / nat.name.replace("-native-", "-sub3-")
    if not big.exists():
        say(f"  {nat.name}: no matching 3840 x 2160 frame"); continue
    a = np.array(Image.open(nat).convert("RGBA")).astype(int)
    b = np.array(Image.open(big).convert("RGBA")).astype(int)
    if b.shape[:2] != (2160, 3840):
        say(f"  {big.name}: size {b.shape[1]}x{b.shape[0]}, expected 3840x2160"); continue
    s = b[1::3, 1::3]
    d = np.abs(s - a).max(axis=2)
    stage = np.array([217, 213, 202, 255])
    drawn = int((np.abs(a - stage).max(axis=2) > 0).sum())          # sanity: the frame holds a real picture, not just the stage colour
    n_diff = int((d > 0).sum())
    n_big = int((d > 2).sum())
    total_pairs += 1; total_diff_px += n_diff; worst = max(worst, int(d.max()))
    say(f"  {nat.name.replace('-native-', ' ').replace('.png', ''):<34} pixels that differ: {n_diff:>5} (by more than 2 of 255: {n_big}), largest difference {int(d.max())}; non-stage pixels in the frame: {drawn}")
say(f"{total_pairs} frame pairs, {total_diff_px} differing pixels in total, largest single-channel difference {worst} of 255")
(HERE / "route-summary.txt").write_text("\n".join(L) + "\n")
