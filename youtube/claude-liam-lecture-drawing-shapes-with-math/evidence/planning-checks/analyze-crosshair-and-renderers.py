#!/usr/bin/env python3
"""analyze-crosshair-and-renderers.py: (1) every crosshair render (defaults, each dial at 0 and at 1, all 0, all 1) against an independent
float64 model, pixel by pixel; coverage numbers for the extremes; (2) the Compatibility renderer against Forward+ for every mask shader.
Writes analysis-crosshair-and-renderers.txt."""
from pathlib import Path
import numpy as np
from PIL import Image
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("am", HERE / "analyze-masks.py"); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
PNG = HERE / "png"
U, V = am.uv_grid(480, 480)
out = []
names = ["dot_size", "ring_distance", "ring_width", "arm_gap", "arm_length", "arm_width"]
def run_model(vals):
    return np.clip(am.crosshair(U, V, **vals), 0, 1)
def alpha_of(path):
    img = Image.open(path); a, _ = am.rendered_alpha(img); return a

out.append("1. The crosshair against an independent model (480 x 480, Forward+)\n")
cases = [("crosshair-default", dict(am.DEFAULTS))]
for n in names:
    for v in (0.0, 1.0):
        d = dict(am.DEFAULTS); d[n] = v; cases.append((f"crosshair-{n}-{int(v)}", d))
d = dict(am.DEFAULTS); d["dot_size"] = 0.0; d["ring_width"] = 0.0; cases.append(("crosshair-arms-only", d))
for label, ov in (("pair-dot1-ring0", dict(dot_size=1.0, ring_distance=0.0)), ("pair-dot1-ring1", dict(dot_size=1.0, ring_distance=1.0)),
                  ("pair-rw1-al0", dict(ring_width=1.0, arm_length=0.0)), ("pair-rw1-al1", dict(ring_width=1.0, arm_length=1.0)),
                  ("pair-aw1-ag0", dict(arm_width=1.0, arm_gap=0.0)), ("pair-aw1-ag1", dict(arm_width=1.0, arm_gap=1.0))):
    d = dict(am.DEFAULTS); d.update(ov); cases.append((label, d))
cases.append(("crosshair-all-0", {n: 0.0 for n in names}))
cases.append(("crosshair-all-1", {n: 1.0 for n in names}))
base = run_model(dict(am.DEFAULTS))
for label, vals in cases:
    a = alpha_of(PNG / f"{label}.png"); want = run_model(vals)
    bad = int((np.abs(a - want) > 0.02).sum())
    out.append(f"  {label:28s} disagree {bad:4d}   coverage (share of the picture drawn) {want.mean():.4f}   rendered {np.clip(a,0,1).mean():.4f}\n")
out.append("\n2. Compatibility renderer against Forward+ (same shader, same 480 x 480 view): pixels that differ\n")
pairs = ["02-circle", "04-ring", "05-overlap-sum", "06-overlap-hole-bug", "07-overlap-hole-fixed", "08-negative-eats-dot", "09-negative-fixed",
         "10-band", "11-cross", "12-arm-rectangle", "13-arms-gap", "14-four-arms", "15-ring-tool"]
fwd = {"02-circle": "02-circle", "04-ring": "04-ring", "05-overlap-sum": "05-overlap-sum", "06-overlap-hole-bug": "06-hole-bug",
       "07-overlap-hole-fixed": "07-hole-fixed", "08-negative-eats-dot": "08-negative-bug", "09-negative-fixed": "09-negative-fixed",
       "10-band": "10-band", "11-cross": "11-cross", "12-arm-rectangle": "12-arm-rectangle", "13-arms-gap": "13-arms-gap",
       "14-four-arms": "14-four-arms", "15-ring-tool": "15-ring-tool"}
tot = 0
for n in pairs:
    A = np.asarray(Image.open(PNG / f"{fwd[n]}.png").convert("RGB"), int); B = np.asarray(Image.open(PNG / f"compat-{n}.png").convert("RGB"), int)
    nd = int((np.abs(A - B).max(axis=2) > 0).sum()); tot += nd
    out.append(f"  {n:28s} differ {nd}\n")
for lab_f, lab_c in (("crosshair-default", "compat-17-crosshair-default"), ("crosshair-all-1", "compat-crosshair-all-1"), ("01-distance", "compat-01-distance")):
    A = np.asarray(Image.open(PNG / f"{lab_f}.png").convert("RGB"), int); B = np.asarray(Image.open(PNG / f"{lab_c}.png").convert("RGB"), int)
    nd = int((np.abs(A - B).max(axis=2) > 0).sum()); mx = int(np.abs(A - B).max())
    out.append(f"  {lab_f:28s} differ {nd} (largest channel difference {mx} of 255)\n")
    tot += nd
out.append(f"\n  total differing pixels over the hard-edged masks and the crosshair: see lines above\n")
(HERE / "analysis-crosshair-and-renderers.txt").write_text("".join(out)); print("".join(out))
