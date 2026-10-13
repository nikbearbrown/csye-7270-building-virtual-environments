#!/usr/bin/env python3
"""crop_act1.py — Act I pantry crops from REAL captures (pure crop, no edits).
  a1_github_walker_crop.png : the public repo page nikbearbrown/walker (EVID/web-captures/github-walker.png, captured 2026-10-09 18:02 UTC),
                              the repo title and the first folder rows (names column), cropped only.
Re-run: python3 evidence/act1/crop_act1.py
"""
from PIL import Image
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]
EVID = REEL.parent / "_conducting-series-evidence"
im = Image.open(EVID / "web-captures/github-walker.png").convert("RGB")
k = 3840 / 2000.0                      # the capture is 3840 wide; coordinates below are read off the 2000-wide view
box = tuple(int(v * k) for v in (240, 225, 700, 770))
im.crop(box).save(REEL / "pantry/a1_github_walker_crop.png")
print("crop", box, "->", box[2] - box[0], "x", box[3] - box[1])
