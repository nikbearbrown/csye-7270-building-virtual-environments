#!/usr/bin/env python3
"""analyze-calcs.py: measurements on the calculator renders in png/: argument-order flip, vec2(single), the oval on a wide view, hard edges.
Writes analysis-calcs.txt."""
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
out = []
def load(n): return np.asarray(Image.open(PNG / f"{n}.png").convert("RGB"), int)

# 1. flip equals one-minus, every pixel
a = load("flip-equals-1minus")
out.append(f"flip-equals-1minus: {a.shape[1]} x {a.shape[0]} px, pixels where step(d, r) differs from 1 - step(r, d): {int((a[..., 0] > 0).sum())}\n")
# 2. vec2(0.5) equals vec2(0.5, 0.5)
b = load("vec2-single")
out.append(f"vec2-single: pixels where distance(UV, vec2(0.5)) differs from distance(UV, vec2(0.5, 0.5)): {int((b[..., 0] > 0).sum())}\n")
# 3. the oval on the wide view
c = load("circle-wide-640x360")
teal = (abs(c[..., 0] - 94) < 6) & (abs(c[..., 1] - 163) < 6) & (abs(c[..., 2] - 145) < 6)
H, W = teal.shape
row = teal[H // 2]; col = teal[:, W // 2]
xs = np.where(row)[0]; ys = np.where(col)[0]
wpx = xs.max() - xs.min() + 1; hpx = ys.max() - ys.min() + 1
out.append(f"circle-wide-640x360: view {W} x {H}; the 'circle' (radius 0.3) is {wpx} px wide and {hpx} px tall; ratio {wpx / hpx:.3f}; view ratio {W / H:.3f}\n")
out.append(f"   expected from UV running 0..1 on both axes: width 0.6 x {W} = {0.6 * W:.0f}, height 0.6 x {H} = {0.6 * H:.0f}\n")
# 4. hard edges: the colours present in the 480 x 480 circle
d = load("02-circle")
cols = {tuple(v) for v in d.reshape(-1, 3)}
out.append(f"02-circle (480 x 480): distinct colours in the whole picture: {len(cols)} -> {sorted((int(a), int(b), int(c)) for a, b, c in cols)}\n")
# 5. the staircase: width of the circle on consecutive rows near the top
t2 = (abs(d[..., 0] - 94) < 6)
rows = [(y, int(t2[y].sum())) for y in range(96, 112)]
out.append("   teal pixels per row, rows 96 to 111 (top of the circle): " + ", ".join(f"{y}:{n}" for y, n in rows) + "\n")
# 6. the function version draws the same ring as the inline version
r1 = load("04-ring"); r2 = load("15-ring-tool")
out.append(f"15-ring-tool against 04-ring (same radii 0.3 and 0.35): pixels that differ: {int((abs(r1 - r2).max(axis=2) > 0).sum())}\n")
# 7. max(a, b) is "add, then cap at one" for masks (the two-circle picture of the overlap bug)
m = load("max-equals-capped-sum")
out.append(f"max-equals-capped-sum: {m.shape[1]} x {m.shape[0]} px, pixels where min(a + b, 1) differs from max(a, b): {int((m[..., 0] > 0).sum())}\n")
(HERE / "analysis-calcs.txt").write_text("".join(out)); print("".join(out))
