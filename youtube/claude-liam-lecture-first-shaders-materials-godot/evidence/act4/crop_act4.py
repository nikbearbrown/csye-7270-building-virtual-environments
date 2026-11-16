#!/usr/bin/env python3
"""crop_act4.py — cuts the pictures Act IV (B25-B34) displays into pantry/a4_*. Every file is a crop (and, for the strip, an integer nearest-neighbour
enlargement) of a REAL capture already in the reel; nothing is redrawn or recoloured.
  a4_pad_strip.png ....... ev_pad_0.0.png (the pad shader on a flat quad, Compatibility, the example 14 Oct), rows 500-580, x2 nearest -> 3240 x 160.
                           UV.x 0.15625 -> crop x 253 (dark band), 0.21875 -> x 354 (light band); the 16 bands are 101.25 px wide in the 1620-px crop.
  a4_padc_<0.0|0.5|1.0>.png  ev_pad_*.png rows 135-945 (1620 x 810, 2:1): the quad at activation 0, 0.5, 1 (Compatibility, the example 14 Oct).
  a4_labpadT_<frame>.png .. frames 300 / 597 / 603 of captures/lab (the pad, and the mascot standing on it, in the game; scripted key input; an EARLIER take of the lab, 14 Oct 01:52), cropped: crop (1330,740,1790,1100) = 460 x 360 (the pad diamond and the mascot standing on it, little floor: GATE V averages every non-background pixel, and the cream floor sits near the stage colour).
Run:  python3 evidence/act4/crop_act4.py
"""
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent.parent.parent
PAN = HERE / "pantry"

im = Image.open(PAN / "ev_pad_0.0.png").convert("RGB")
strip = im.crop((0, 500, 1620, 580)).resize((3240, 160), Image.NEAREST)
strip.save(PAN / "a4_pad_strip.png"); print("a4_pad_strip.png", strip.size, "px@253:", im.getpixel((253, 540)), "px@354:", im.getpixel((354, 540)))
for v in ("0.0", "0.5", "1.0"):
    c = Image.open(PAN / f"ev_pad_{v}.png").convert("RGB").crop((0, 135, 1620, 945))
    c.save(PAN / f"a4_padc_{v}.png"); print(f"a4_padc_{v}.png", c.size)
for f in (300, 597, 603):
    c = Image.open(HERE / "captures" / "lab" / f"lab_{f:06d}.png").convert("RGB").crop((1330, 740, 1790, 1100))
    c.save(PAN / f"a4_labpadT_{f}.png"); print(f"a4_labpadT_{f}.png", c.size)
