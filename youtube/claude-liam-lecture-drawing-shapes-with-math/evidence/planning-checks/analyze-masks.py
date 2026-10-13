#!/usr/bin/env python3
"""analyze-masks.py: checks every mask shader of the film against an independent model.
For each Lab render in png/ (480 x 480, Forward+), the expected mask is computed in float64 from the pixel centre's UV, using the
same maths the shader is written in; the rendered mask is recovered from the pixel colour (teal over the stage colour). The report
counts pixels where the two disagree. Writes analysis-masks.txt."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
TEAL = np.array([94, 163, 145], float)      # what 0.37, 0.64, 0.57 become in 8 bits (rounded)
STAGE = np.array([217, 213, 202], float)    # the Lab stage colour #D9D5CA

def uv_grid(w, h):
    u = (np.arange(w) + 0.5) / w
    v = (np.arange(h) + 0.5) / h
    return np.meshgrid(u, v)

def step(edge, x):
    return np.where(x < edge, 0.0, 1.0)

def dist(U, V, cx, cy):
    return np.hypot(U - cx, V - cy)

def rendered_alpha(img):
    """Recover the alpha from the red channel: pixel = teal * a + stage * (1 - a)."""
    a = np.asarray(img.convert("RGB"), float)
    return (STAGE[0] - a[..., 0]) / (STAGE[0] - TEAL[0]), a

MODELS = {}
def model(name):
    def deco(f):
        MODELS[name] = f
        return f
    return deco

@model("01-distance")
def _(U, V): return dist(U, V, .5, .5)
@model("02-circle")
def _(U, V): return step(dist(U, V, .5, .5), .3)
@model("03-slider-0.1")
def _(U, V): return step(dist(U, V, .5, .5), .1)
@model("03-slider-0.3")
def _(U, V): return step(dist(U, V, .5, .5), .3)
@model("03-slider-0.45")
def _(U, V): return step(dist(U, V, .5, .5), .45)
@model("04-ring")
def _(U, V):
    d = dist(U, V, .5, .5); return step(d, .35) - step(d, .3)
@model("05-overlap-sum")
def _(U, V):
    return step(dist(U, V, .38, .5), .25) + step(dist(U, V, .62, .5), .25)
@model("06-hole-bug")
def _(U, V):
    return step(dist(U, V, .38, .5), .25) + step(dist(U, V, .62, .5), .25) - step(dist(U, V, .5, .5), .08)
@model("07-hole-fixed")
def _(U, V):
    s = step(dist(U, V, .38, .5), .25) + step(dist(U, V, .62, .5), .25)
    return np.minimum(s, 1.0) - step(dist(U, V, .5, .5), .08)
@model("08-negative-bug")
def _(U, V):
    return step(dist(U, V, .5, .5), .3) - step(dist(U, V, .8, .5), .2) + step(dist(U, V, .88, .5), .08)
@model("09-negative-fixed")
def _(U, V):
    return np.maximum(step(dist(U, V, .5, .5), .3) - step(dist(U, V, .8, .5), .2), 0.0) + step(dist(U, V, .88, .5), .08)
@model("10-band")
def _(U, V): return step(abs(U - .5), .05)
@model("11-cross")
def _(U, V): return np.maximum(step(abs(U - .5), .05), step(abs(V - .5), .05))
@model("12-arm-rectangle")
def _(U, V): return step(abs(V - .5), .35) * step(abs(U - .5), .03)
@model("13-arms-gap")
def _(U, V):
    x = abs(U - .5); y = abs(V - .5); return step(.1, y) * step(y, .35) * step(x, .03)
@model("14-four-arms")
def _(U, V):
    x = abs(U - .5); y = abs(V - .5)
    return np.maximum(step(.1, y) * step(y, .35) * step(x, .03), step(.1, x) * step(x, .35) * step(y, .03))
@model("15-ring-tool")
def _(U, V):
    d = dist(U, V, .5, .5); return step(d, .35) - step(d, .3)

def crosshair(U, V, dot_size, ring_distance, ring_width, arm_gap, arm_length, arm_width):
    d = dist(U, V, .5, .5); x = abs(U - .5); y = abs(V - .5)
    dot_r, ring_r, ring_w = dot_size * .05, ring_distance * .4, ring_width * .05
    gap, ln, w = arm_gap * .2, arm_length * .3, arm_width * .03
    m = step(d, dot_r)
    m = np.maximum(m, step(d, ring_r + ring_w) - step(d, ring_r))
    h = step(gap, x) * step(x, gap + ln) * step(y, w)
    v = step(gap, y) * step(y, gap + ln) * step(x, w)
    return np.maximum(m, np.maximum(h, v))
DEFAULTS = dict(dot_size=.5, ring_distance=.55, ring_width=.3, arm_gap=.35, arm_length=.6, arm_width=.4)

def main():
    lines = ["Pixelwise model check, 480 x 480 Lab renders (Forward+ unless the name says otherwise)\n"]
    U, V = uv_grid(480, 480)
    worst = 0
    for name, f in MODELS.items():
        p = PNG / f"{name}.png"
        if not p.exists():
            lines.append(f"{name:24s} NO PNG\n"); continue
        img = Image.open(p)
        alpha, rgb = rendered_alpha(img)
        want = np.clip(f(U, V), 0.0, 1.0)
        diff = np.abs(alpha - want)
        bad = int((diff > 0.02).sum())
        worst = max(worst, bad)
        inside = float(want.mean())
        lines.append(f"{name:24s} pixels {alpha.size}  disagree {bad:5d}  max |diff| {diff.max():.4f}  model coverage {inside:.4f}\n")
    lines.append(f"\nworst case: {worst} pixels disagree (0 means every pixel matches the independent model)\n")
    (HERE / "analysis-masks.txt").write_text("".join(lines)); print("".join(lines))
if __name__ == "__main__":
    main()
