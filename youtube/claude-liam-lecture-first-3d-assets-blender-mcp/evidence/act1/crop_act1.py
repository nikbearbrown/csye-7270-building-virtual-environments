#!/usr/bin/env python3
"""crop_act1.py <raw_dir> — crops the Act I renders (render_act1.py) and the existing ev_ renders into pantry/a1_*.png.
Pictures that must stack (a shape-by-shape build) share ONE crop box, so they overlay exactly in Manim.
Pixel sizes are printed (and saved to crops_act1.json) because the scenes size images from them.
Nothing is redrawn or retouched: crops only.
"""
import json, sys, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
REEL = HERE.parents[1]
PAN = REEL / "pantry"
raw = pathlib.Path(sys.argv[1])
PAD = 14
log = {}


def bbox(im):
    return im.split()[-1].getbbox()


def union(boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))


def pad(b, w=2400, h=1350):
    return (max(0, b[0] - PAD), max(0, b[1] - PAD), min(w, b[2] + PAD), min(h, b[3] + PAD))


def save(im, box, name):
    c = im.crop(box)
    c.save(PAN / name)
    log[name] = {"crop_box": box, "size_px": c.size}
    print(f"{name:28s} {c.size[0]:5d} x {c.size[1]:5d}  from box {box}")


# B04 primitives: each its own box (same camera, so pixel sizes compare)
for n in ["cube", "cylinder", "cone", "sphere", "plane"]:
    im = Image.open(raw / f"prim_{n}.png")
    save(im, pad(bbox(im)), f"a1_clay_{n}.png")

# B04 lantern in clay, shape by shape; and the real coloured lantern, all in ONE box
lan = [Image.open(raw / f"lpart_{i}.png") for i in range(1, 6)] + [Image.open(raw / f"lcum_{i}.png") for i in range(1, 6)]
col = Image.open(PAN / "ev_lantern_34.png")
box = pad(union([bbox(i) for i in lan] + [bbox(col)]))
for i in range(1, 6):
    save(Image.open(raw / f"lpart_{i}.png"), box, f"a1_clay_lanpart_{i}.png")
    save(Image.open(raw / f"lcum_{i}.png"), box, f"a1_clay_lancum_{i}.png")
save(col, box, "a1_lantern_colour.png")

# B12 crate, shape by shape, real colours; and the real joined crate, all in ONE box
cr = [Image.open(raw / f"cpart_{i}.png") for i in range(1, 6)] + [Image.open(raw / f"ccum_{i}.png") for i in range(1, 6)]
ccol = Image.open(PAN / "ev_crate_34.png")
box = pad(union([bbox(i) for i in cr] + [bbox(ccol)]))
for i in range(1, 6):
    save(Image.open(raw / f"cpart_{i}.png"), box, f"a1_cpart_{i}.png")
    save(Image.open(raw / f"ccum_{i}.png"), box, f"a1_ccum_{i}.png")
save(ccol, box, "a1_crate_colour.png")

# B03 examples
for n in ["platform", "tree", "rock", "gem"]:
    im = Image.open(raw / f"ex_{n}.png")
    save(im, pad(bbox(im)), f"a1_ex_{n}.png")

# the three real assets, tight crops (B01, B03, B09A/B, B12)
for n in ["crate", "lantern", "coin"]:
    im = Image.open(PAN / f"ev_{n}_34.png")
    save(im, pad(bbox(im)), f"a1_{n}.png")

# B07: the two spheres of ev_sphere_default_vs_low.png, split down the middle
sp = Image.open(PAN / "ev_sphere_default_vs_low.png")
L = sp.crop((0, 0, 1200, 1350)); R = sp.crop((1200, 0, 2400, 1350))
bl, br = bbox(L), bbox(R)
save(sp, pad(bl), "a1_sphere_960.png")
save(sp, pad((br[0] + 1200, br[1], br[2] + 1200, br[3])), "a1_sphere_120.png")

(HERE / "crops_act1.json").write_text(json.dumps(log, indent=1))

# B11: the real Blender window (ev_bl_object_mode.png, Blender's own screenshot): the 3D viewport with its header (mode selector,
# View/Select/Add/Object), the toolbar and the selected lantern. The top bar is left out: at film size its dark strip reads as a
# low-contrast "text" blob under GATE T (tested: crop (0,0,1600,1500) fails, (0,105,1310,1600) passes).
bw = Image.open(PAN / "ev_bl_object_mode.png")
save(bw, (0, 105, 1310, 1600), "a1_blender_view.png")
(HERE / "crops_act1.json").write_text(json.dumps(log, indent=1))
