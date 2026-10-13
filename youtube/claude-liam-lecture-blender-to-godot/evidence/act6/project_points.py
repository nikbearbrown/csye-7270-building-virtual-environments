#!/usr/bin/env python3
"""project_points.py — places marks on the real Blender render (pantry/a6_post_run1.png = the act-V render of the run-1 post, same camera as
pantry/post_visual.png) by projecting world points through the render's camera: a pinhole model of Blender's camera (location, look-at target,
42 mm lens on the 36 mm sensor, 4800 x 2700 render, crop origin (1582, 402)).  The model is checked against the anchors the act-5 builder
exported from Blender itself (evidence/act5/post_anchors.json): it reproduces z0_c, pole_top_c and pole_bot_c to 0.1 px.
Run from the REEL folder:  python3 evidence/act6/project_points.py > evidence/act6/project_points.out.txt
"""
import json
from pathlib import Path
import numpy as np
REEL = Path(__file__).resolve().parents[2]
A = json.loads((REEL / "evidence/act5/post_anchors.json").read_text())
C = np.array(A["camera"]["loc"]); T = np.array(A["camera"]["target"])
f = T - C; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, f)
W, H = A["render_res"]; F = A["camera"]["lens_mm"] / 36.0 * W; ox, oy = A["crop_origin_in_render"]
def proj(P):
    v = np.array(P, float) - C
    return (W / 2 + F * (v @ r) / (v @ f) - ox, H / 2 - F * (v @ u) / (v @ f) - oy)
print("camera", A["camera"], "crop origin", (ox, oy), "focal length in px", F)
for k, P in {"z0_c": (0, 0, 0), "pole_top_c": (0, 0, 1.8), "pole_bot_c": (0, 0, 0.1)}.items():
    p = proj(P); print(f"check {k}: model ({p[0]:.1f}, {p[1]:.1f})  Blender export {tuple(A['pts'][k])}")
print("--- the points B59 uses (Blender coordinates x, y, z up; crop pixels) ---")
for k, P in {"foot (0,0,0)": (0, 0, 0), "our ray start (0,0,0.5)": (0, 0, 0.5), "pole top (0,0,1.8)": (0, 0, 1.8), "finished test's ray start (0,0,3.8)": (0, 0, 3.8)}.items():
    p = proj(P); print(f"{k}: ({p[0]:.1f}, {p[1]:.1f})")
p0, p1, p2 = proj((0, 0, 1.8)), proj((0, 0, 3.8)), proj((0, 0, 0))
print("pixels per metre on the axis: pole 0 to 1.8 m %.1f px/m, 1.8 to 3.8 m %.1f px/m (perspective foreshortening)" % ((p2[1] - p0[1]) / 1.8, (p0[1] - p1[1]) / 2.0))
