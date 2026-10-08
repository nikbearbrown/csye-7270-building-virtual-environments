#!/usr/bin/env python3
"""Independent check (not written by the agent): compare the termite collider
with the opaque pixels of each 48x48 frame.

Reads the strip PNG and the collider size from termite.tscn. Godot draws an
AnimatedSprite2D centred on its node by default (centered = true, offset 0), and
the CollisionShape2D sits at the Area2D origin, so both are centred on (0, 0):
collider cell rect = [24 - w/2, 24 + w/2) x [24 - h/2, 24 + h/2).
Usage: python3 verify_collider_vs_alpha.py <repo> [--overlay out.png]
"""
import re, sys
from pathlib import Path
import numpy as np
from PIL import Image

repo = Path(sys.argv[1])
strip = np.asarray(Image.open(repo / "godot/features/termite/termite_soldiers.png").convert("RGBA"))
tscn = (repo / "godot/features/termite/termite.tscn").read_text()
w, h = map(float, re.search(r"size = Vector2\(([\d.]+), ([\d.]+)\)", tscn).groups())
x0, x1 = int(24 - w / 2), int(24 + w / 2)
y0, y1 = int(24 - h / 2), int(24 + h / 2)
print(f"strip {strip.shape[1]}x{strip.shape[0]}; collider {w:g}x{h:g} -> cell cols {x0}..{x1-1}, rows {y0}..{y1-1}")
names = ["black", "red", "yellow"]
for i, name in enumerate(names):
    a = strip[:, i * 48:(i + 1) * 48, 3] > 0
    ys, xs = np.where(a)
    inside = a[y0:y1, x0:x1]
    empty_rows = [r for r in range(y0, y1) if not a[r, x0:x1].any()]
    empty_cols = [c for c in range(x0, x1) if not a[y0:y1, c].any()]
    outside = int(a.sum() - inside.sum())
    print(f"{name:6s} opaque px {int(a.sum()):4d}; art bbox cols {xs.min()}..{xs.max()} rows {ys.min()}..{ys.max()}"
          f" ({xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}); opaque inside collider {int(inside.sum())}"
          f" ({inside.sum()/a.sum():.0%}); collider area that is transparent {int((~inside).sum())} of {inside.size} px;"
          f" collider rows with no art {empty_rows or 'none'}; opaque px outside collider {outside}")
    rows_opaque = [int(a[r].sum()) for r in range(48)]
    print(f"       opaque count per row 0..47: {rows_opaque}")
if "--overlay" in sys.argv:
    out = sys.argv[sys.argv.index("--overlay") + 1]
    img = Image.fromarray(strip).resize((144 * 8, 48 * 8), Image.NEAREST)
    bg = Image.new("RGBA", img.size, (246, 243, 236, 255)); bg.alpha_composite(img)
    px = bg.load()
    for i in range(3):
        for x in range((i * 48 + x0) * 8, (i * 48 + x1) * 8):
            for y in (y0 * 8, y1 * 8 - 1): px[x, y] = (0, 160, 255, 255)
        for y in range(y0 * 8, y1 * 8):
            for x in ((i * 48 + x0) * 8, (i * 48 + x1) * 8 - 1): px[x, y] = (0, 160, 255, 255)
    bg.convert("RGB").save(out)
    print("overlay written", out)
