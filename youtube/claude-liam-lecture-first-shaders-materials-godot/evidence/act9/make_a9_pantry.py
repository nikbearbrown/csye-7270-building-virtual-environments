#!/usr/bin/env python3
"""make_a9_pantry.py — Act IX (Check What You See) cut pictures, all crops (or circular masks) of REAL captures. Nothing is redrawn or recoloured.
Run:  python3 evidence/act9/make_a9_pantry.py        (from anywhere; safe to re-run)

  a9_panel_609.png ........ the verification panel of captures/lab/lab_000609.png: box (2220,435,3330,1044) = 1110 x 609 (scripted input)
  a9_pad_lab_<frame>.png .. the pad of captures/lab frames 503, 597, 609, 610: box (1290,745,1766,1100) = 476 x 355: the whole pad (green/brown pixels x 1329-1768, y 871-1091, measured) and the mascot, stopping at x 1766 before the black gate post (x 1766+, y 1008+)
  a9_sweep_<param>_<i>.png  the 12 sphere crops of pantry/ev_sweep_*, masked to the sphere's own silhouette (a circle of 648 px: radius 0.6 units,
                           orthographic camera size 4.0 over 2160 px = 540 px/unit, so the sphere is exactly 648 px across) so the dark engine ground drops out
  a9_mat_<baseline|shared|one>_<l|r>.png  the two spheres of the three material frames, same circular mask (pair crop 1512 x 648: spheres at x 0..648 and 864..1512)
  a9_probe_c_<value>.png ... the interior of one constant-ALBEDO patch of captures/forward-plus/constant_albedo_compatibility.png (Compatibility), patch centre from
                           evidence/runs/R9-constant-albedo-compatibility.json (pixel [x, 270]); the interior only (no ground)
  a9_pad_strip_0.5.png / a9_pad_strip_fp_0.5.png ... B63: 1080 x 540 band (0,270,1080,810) of ev_pad_0.5 / ev_pad_fp_0.5
  a9_hud_<frame>.png ...... the HUD text strip of each lab frame (not used by a scene unless a lane says so)
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json

HERE = Path(__file__).resolve().parents[2]
CAP = HERE / "captures"
PAN = HERE / "pantry"


def circ(im):
    w, h = im.size
    s = min(w, h)
    mask = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, w * 4 - 1, h * 4 - 1), fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


lab = CAP / "lab"
Image.open(lab / "lab_000609.png").convert("RGB").crop((2220, 435, 3330, 1044)).save(PAN / "a9_panel_609.png")
for f in ("000503", "000597", "000609", "000610"):
    im = Image.open(lab / f"lab_{f}.png").convert("RGB")
    im.crop((1290, 745, 1766, 1100)).save(PAN / f"a9_pad_lab_{f}.png")
    im.crop((100, 1960, 1130, 2060)).save(PAN / f"a9_hud_{f}.png")

for p in ("roughness_gain", "uv_scale", "tint", "metallic_gain"):
    for i in range(3):
        im = Image.open(PAN / f"ev_sweep_{p}_{i}.png").convert("RGB")
        circ(im).save(PAN / f"a9_sweep_{p}_{i}.png")

for tag, src in (("baseline", "ev_mat_baseline.png"), ("shared", "ev_mat_shared_edit.png"), ("one", "ev_mat_one_edit.png")):
    im = Image.open(PAN / src).convert("RGB")
    circ(im.crop((0, 0, 648, 648))).save(PAN / f"a9_mat_{tag}_l.png")
    circ(im.crop((864, 0, 1512, 648))).save(PAN / f"a9_mat_{tag}_r.png")

# B63: the left 1080 x 540 band of the half-activation pad captures (both renderers); the light-stripe pixel (UV.x 0.21875) sits at x 354, y 270 of the band
for src, dst in (("ev_pad_0.5.png", "a9_pad_strip_0.5.png"), ("ev_pad_fp_0.5.png", "a9_pad_strip_fp_0.5.png")):
    Image.open(PAN / src).convert("RGB").crop((0, 270, 1080, 810)).save(PAN / dst)

rows = json.load(open(HERE / "evidence/runs/R9-constant-albedo-compatibility.json"))["rows"]
cap = Image.open(CAP / "forward-plus" / "constant_albedo_compatibility.png").convert("RGB")
for r in rows:
    if r["row"] == "const" and r["value"] in (0.0585, 0.09, 0.104, 0.12):
        x, y = r["pixel"]
        cap.crop((x - 140, y - 190, x + 140, y + 190)).save(PAN / f"a9_probe_c_{r['value']}.png")
        print("probe", r["value"], r["rgb8"], "at", r["pixel"])
print("done")
