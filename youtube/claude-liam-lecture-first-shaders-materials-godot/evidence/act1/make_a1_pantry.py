#!/usr/bin/env python3
"""make_a1_pantry.py — cuts the Act I pictures (crops of real captures; nothing redrawn). Re-run:
    python3 evidence/act1/make_a1_pantry.py        (from the reel folder)
a1_pad_idle.png   crop of captures/lab/lab_000503.png (scripted input; pad terracotta, mascot on it)   box (1290, 650, 1765, 1110)
a1_pad_open.png   crop of captures/lab/lab_000610.png (scripted input; 'GATE OPEN', pad green)          same box
                  (x1 = 1765 is the pillar's left edge: the black pillar stays out of shot, which GATE T would read as a text blob)
a1_sphere_matte.png / a1_sphere_coated.png   the two spheres of pantry/ev_mat_baseline.png (a crop of captures/example-native/materials-baseline.png,
                  the example, 14 Oct), each cut to a circle with an alpha mask so the dark engine ground does not come along
"""
from pathlib import Path
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parents[2]
P = R / "pantry"
BOX = (1290, 650, 1765, 1110)
for src, dst in (("lab_000503.png", "a1_pad_idle.png"), ("lab_000610.png", "a1_pad_open.png")):
    Image.open(R / "captures/lab" / src).convert("RGB").crop(BOX).save(P / dst)
    print(dst, "<-", src, BOX)
base = Image.open(P / "ev_mat_baseline.png").convert("RGB")
for dst, box in (("a1_sphere_matte.png", (0, 0, 648, 648)), ("a1_sphere_coated.png", (864, 0, 1512, 648))):
    im = base.crop(box).convert("RGBA")
    s = im.size[0]
    mask = Image.new("L", (s * 4, s * 4), 0)
    ImageDraw.Draw(mask).ellipse((8, 8, s * 4 - 9, s * 4 - 9), fill=255)       # 4x supersampled circle, 2 px inside the sphere's edge
    im.putalpha(mask.resize((s, s), Image.LANCZOS))
    im.save(P / dst)
    print(dst, "<-", "ev_mat_baseline.png", box)
