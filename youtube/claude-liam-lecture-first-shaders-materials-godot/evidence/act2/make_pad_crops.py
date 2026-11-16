#!/usr/bin/env python3
"""B10 pictures: crops of three REAL lab frames (captures/lab/, scripted input, native 3840x2160, Compatibility).
Nothing is redrawn: each file is PIL.crop of the frame. charge values are read from captures/lab/states.jsonl.
Run from the reel folder:  python3 evidence/act2/make_pad_crops.py
"""
import json
from pathlib import Path
from PIL import Image
REEL = Path(__file__).resolve().parents[2]
BOX = (1170, 650, 1766, 1130)          # the pad + Claude on a light floor; stops left of the black gate post (x >= 1768)
states = {}
for l in open(REEL / "captures/lab/states.jsonl"):
    r = json.loads(l)
    states[r["frame"]] = r
for frame in (300, 597, 609):
    im = Image.open(REEL / f"captures/lab/lab_{frame:06d}.png").convert("RGB").crop(BOX)
    out = REEL / f"pantry/a2_pad_{frame:06d}.png"
    im.save(out)
    s = states[frame]
    print(out.name, im.size, "charge", s["charge"], "uniform = charge/0.6 =", round(s["charge"] / 0.6, 3), "HUD percent =", int(s["charge"] / 0.6 * 100), "state", s["state"])
