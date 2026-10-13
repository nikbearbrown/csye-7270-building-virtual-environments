#!/usr/bin/env python3
"""run_dense_compare.py: does the curve the film DRAWS equal the picture Godot RENDERS?

For every curve in plot_data.py the shader `COLOR = vec4(vec3(f(UV.x)), 1.0)` is rendered in a real Godot 4.7.2 window (Shader Lab, 640x360,
Forward+), every pixel of the middle row is read from the saved PNG, and it is compared with numpy's value at the pixel centre
x = (i + 0.5) / 640 (rounded to 8 bits). The 2D shaders of the ring are compared pixel by pixel on a 360x360 square.
Writes dense-compare.md and dense-compare.jsonl. Needs Pillow and numpy.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T      # noqa: E402
import plot_data as P      # noqa: E402

HERE = Path(__file__).resolve().parent
PNG = HERE / "png-dense"
PNG.mkdir(exist_ok=True)
CS = HERE / "check-shaders"
SH = T.FILM / "lab-shaders"
W, H = 640, 360
log, rows = [], []


def levels(a):
    return np.rint(np.clip(a, 0.0, 1.0) * 255.0).astype(int)


def compare_strip(name, glsl, fn, vec3=False, W=W, H=H):
    shader = CS / f"dense_{name}.gdshader"
    if vec3:
        body = f"\tfloat x = UV.x;\n\tCOLOR = vec4({glsl}, 1.0);\n"
    else:
        body = f"\tfloat x = UV.x;\n\tfloat v = {glsl};\n\tCOLOR = vec4(vec3(v), 1.0);\n"
    shader.write_text("shader_type canvas_item;\n\nvoid fragment() {\n" + body + "}\n")
    png = PNG / f"{name}.png"
    res = T.run_lab(shader, ["--kind", "rect", "--png", png], f"dense_{name}", log)
    if not res or not res.get("ok"):
        rows.append({"name": name, "glsl": glsl, "ok": False})
        print("FAIL (no result)", name)
        return
    img = np.array(Image.open(png).convert("RGB"))
    row = img[H // 2]
    xs = (np.arange(W) + 0.5) / W
    if vec3:
        exp = levels(P.blend_rgb(fn(xs)))
        obs = row.astype(int)
        diff = np.abs(obs - exp)
        d = diff.max(axis=1)
    else:
        exp = levels(fn(xs))
        obs = row[:, 0].astype(int)
        grey_ok = bool((row[:, 0] == row[:, 1]).all() and (row[:, 1] == row[:, 2]).all())
        d = np.abs(obs - exp)
    worst = int(d.argmax())
    rec = {"name": name, "glsl": glsl, "ok": True, "pixels": W, "max_diff_levels": int(d.max()), "pixels_off_by_2_or_more": int((d >= 2).sum()),
           "pixels_off_by_1": int((d == 1).sum()), "worst_x": (round(float(xs[worst]), 4) if d.max() > 0 else "none: identical"), "renderer": res.get("renderer")}
    rows.append(rec)
    print(f"[{'ok' if d.max() <= 1 else 'CHECK'}] {name}: max diff {d.max()} level(s); off by >=2: {(d >= 2).sum()}; worst at x={xs[worst]:.4f}" if d.max() > 0 else f"[ok] {name}: identical to numpy at all {W} pixels")


for name, (glsl, fn) in P.CURVES.items():
    compare_strip(name, glsl, fn)
for name, (glsl, fn) in P.BLENDS.items():
    compare_strip(name, glsl, fn, vec3=True)


# ---- 2D shaders: the film's own files, square 360x360, compared pixel by pixel ----
S = 360
ii, jj = np.meshgrid((np.arange(S) + 0.5) / S, (np.arange(S) + 0.5) / S)   # ii = u (x), jj = v (y)
dist = np.hypot(ii - 0.5, jj - 0.5)
CREAM = np.array([0.98, 0.96, 0.92])
TEAL = np.array([0.37, 0.64, 0.57])


def mixc(w):
    w = w[..., None]
    return CREAM * (1 - w) + TEAL * w


def stepf(e, x):
    return np.where(x < e, 0.0, 1.0)


def compare_square(name, shader_file, expected_rgb, setargs=()):
    png = PNG / f"{name}.png"
    res = T.run_lab(SH / shader_file, ["--kind", "rect", "--size", f"{S}x{S}", "--png", png] + list(setargs), f"dense_{name}", log)
    if not res or not res.get("ok"):
        rows.append({"name": name, "ok": False})
        print("FAIL (no result)", name)
        return
    img = np.array(Image.open(png).convert("RGB")).astype(int)
    exp = levels(expected_rgb)
    diff = np.abs(img - exp).max(axis=2)
    # pixels that disagree: how close are they to a threshold? (float32 on the card against float64 here)
    bad = diff >= 2
    rec = {"name": name, "shader": f"lab-shaders/{shader_file}", "args": [str(a) for a in setargs], "ok": True, "pixels": S * S,
           "max_diff_levels": int(diff.max()), "pixels_off_by_2_or_more": int(bad.sum()), "renderer": res.get("renderer")}
    rows.append(rec)
    print(f"[{'ok' if diff.max() <= 1 else 'CHECK'}] {name}: max diff {diff.max()}; off by >=2: {bad.sum()} of {S*S}")


def grey(v):
    return np.stack([v, v, v], axis=-1)


compare_square("sq_08_distance", "08-distance.gdshader", grey(dist))
compare_square("sq_09_glow", "09-glow.gdshader", grey(1.0 - P.smoothstep(0.0, 0.5, dist)))
compare_square("sq_10_disk", "10-disk.gdshader", grey(stepf(0.3, dist)))
compare_square("sq_11_disk_flip", "11-disk-flip.gdshader", grey(np.where(0.3 >= dist, 1.0, 0.0)))
compare_square("sq_12_ring_hard", "12-ring-hard.gdshader", grey(stepf(0.3, dist) - stepf(0.38, dist)))
compare_square("sq_13_ring_color", "13-ring-color.gdshader", mixc(stepf(0.3, dist) - stepf(0.38, dist)))
compare_square("sq_14_ring_soft", "14-ring-soft.gdshader", mixc(P.smoothstep(0.26, 0.30, dist) - P.smoothstep(0.38, 0.42, dist)))
for r in (0.1, 0.3, 0.38):
    compare_square(f"sq_15_ring_final_r{r}", "15-ring-final.gdshader",
                   mixc(P.smoothstep(r - 0.04, r, dist) - P.smoothstep(r + 0.08, r + 0.12, dist)), ["--set", f"radius={r}"])

(HERE / "dense-compare.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
(HERE / "dense-compare-raw-log.jsonl").write_text("\n".join(json.dumps(r) for r in log) + "\n")
md = ["| curve / shader | pixels | max difference (8-bit levels) | pixels off by 2 or more | worst place |", "|---|---|---|---|---|"]
for r in rows:
    if r.get("ok"):
        md.append(f"| {r['name']} | {r['pixels']} | {r['max_diff_levels']} | {r['pixels_off_by_2_or_more']} | {r.get('worst_x', '')} |")
    else:
        md.append(f"| {r['name']} | | FAILED TO RUN | | |")
(HERE / "dense-compare.md").write_text("\n".join(md) + "\n")
