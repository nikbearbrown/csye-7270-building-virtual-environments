#!/usr/bin/env python3
"""make_crops.py - ACT III picture prep (no new pixels: crops of real renders and of the real Blender window).
  python3 evidence/act3/make_crops.py            (run from the reel folder)
Writes pantry/a3_crate_34.png, pantry/a3_lantern_34.png, pantry/a3_bl_crate_origin.png, and prints:
  * the crate render's corner pixels, projected from the render camera of evidence/renders/render_assets.py
    (orbit target (0,0,0.4), distance 3.6, azimuth 35, elevation 22, lens 50 mm, sensor 36 mm, 2400 x 1350): they match the
    render's alpha bounding box (646..1724 x 187..1272), so the dimension arrows in B23 sit on the real edges;
  * the lantern's silhouette (alpha > 10, dilated 14 px, simplified) in crop pixels, pasted into scenes_act3.py (A3_LANTERN_OUTLINE);
  * the crate's silhouette (alpha > 10, NOT dilated, simplified) in crop pixels (A3_CRATE_OUTLINE): B22 draws it in ink ON the render's own
    edge, so GATE T reads the render's dark edge pixels as one outline, not as text-like blobs (real 4K cut, 2026-10-06).
"""
import math, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from skimage import measure

REEL = Path(__file__).resolve().parents[2]
P = REEL / "pantry"

CROPS = {
    "a3_crate_34.png": ("ev_crate_34.png", (600, 150, 1780, 1310)),
    "a3_lantern_34.png": ("ev_lantern_34.png", (970, 295, 1431, 1120)),
    "a3_bl_crate_origin.png": ("a3_bl_crate_origin_window.png", (600, 300, 2240, 1680)),
}
for out, (src, box) in CROPS.items():
    im = Image.open(P / src).crop(box)
    im.save(P / out)
    print(f"{out}: {src} crop {box} -> {im.size}")


def cam(target, dist, az, el):
    a, e = math.radians(az), math.radians(el)
    t = np.array(target, float)
    return t + np.array([dist * math.cos(e) * math.sin(a), -dist * math.cos(e) * math.cos(a), dist * math.sin(e)])


def proj(p, target=(0, 0, 0.4), dist=3.6, az=35, el=22, W=2400, H=1350, lens=50, sw=36):
    c = cam(target, dist, az, el)
    f = np.array(target) - c; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    d = np.array(p, float) - c
    fx = lens / sw * W
    return W / 2 + fx * (d @ r) / (d @ f), H / 2 - fx * (d @ u) / (d @ f)


print("crate corners (render px; subtract the crop origin 600,150 for crop px):")
for name, p in [("x- y- z0", (-0.4, -0.4, 0)), ("x+ y- z0", (0.4, -0.4, 0)), ("x+ y+ z0", (0.4, 0.4, 0)),
                ("x+ y+ z0.8", (0.4, 0.4, 0.8)), ("x+ y- z0.8", (0.4, -0.4, 0.8)), ("x- y+ z0.8", (-0.4, 0.4, 0.8))]:
    x, y = proj(p)
    print(f"  {name:12s} render ({x:7.1f}, {y:7.1f})  crop ({x - 600:7.1f}, {y - 150:7.1f})")

# lantern silhouette from the crop's alpha channel
a = np.array(Image.open(P / "a3_lantern_34.png"))[..., 3]
mask = Image.fromarray(((a > 10) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(29))   # 14 px outward
m = np.array(mask) > 127
pad = np.pad(m, 2)
cs = max(measure.find_contours(pad.astype(float), 0.5), key=len)
poly = measure.approximate_polygon(cs, tolerance=5.0)
pts = [(round(float(c) - 2, 1), round(float(r) - 2, 1)) for r, c in poly[:-1]]
print("A3_LANTERN_OUTLINE (crop px x, y; image", m.shape[1], "x", m.shape[0], ") n =", len(pts))
print(json.dumps(pts))

# crate silhouette, on the edge (no dilation)
a = np.array(Image.open(P / "a3_crate_34.png"))[..., 3]
m = np.pad(a > 10, 2)
cs = max(measure.find_contours(m.astype(float), 0.5), key=len)
poly = measure.approximate_polygon(cs, tolerance=2.5)
pts = [(round(float(c) - 2, 1), round(float(r) - 2, 1)) for r, c in poly[:-1]]
print("A3_CRATE_OUTLINE (crop px x, y; image", m.shape[1] - 4, "x", m.shape[0] - 4, ") n =", len(pts))
print(json.dumps(pts))
