#!/usr/bin/env python3
"""run_ellipse.py: why the circle stretches on a wide shape. Renders lab-shaders/10-disk.gdshader (step(0.3, distance(UV, vec2(0.5)))) on a
square (360x360) and on a 2:1 rectangle (640x320) in a real Godot 4.7.2 window and measures the dark disk in pixels.
UV runs 0..1 on both axes whatever the shape's proportions, so the disk is 0.6 of the width and 0.6 of the height.
Writes ellipse-measure.md. Needs Pillow and numpy."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T  # noqa: E402

HERE = Path(__file__).resolve().parent
PNG = HERE / "png-dense"
PNG.mkdir(exist_ok=True)
log = []
rows = []
for label, size in (("square_360x360", "360x360"), ("wide_640x320", "640x320"), ("tall_320x640", "320x640")):
    png = PNG / f"ellipse_{label}.png"
    res = T.run_lab(T.FILM / "lab-shaders" / "10-disk.gdshader", ["--kind", "rect", "--size", size, "--png", png], f"ellipse_{label}", log)
    img = np.array(Image.open(png).convert("L"))
    dark = img < 128
    ys, xs = np.where(dark)
    w = int(xs.max() - xs.min() + 1)
    h = int(ys.max() - ys.min() + 1)
    W, H = (int(v) for v in size.split("x"))
    rows.append((label, W, H, w, h, round(w / W, 3), round(h / H, 3), round(w / h, 3), res.get("renderer")))
    print(label, W, H, "disk width", w, "height", h, "w/W", round(w / W, 3), "h/H", round(h / H, 3), "w/h", round(w / h, 3))
md = ["| shape | pixels (W x H) | disk width (px) | disk height (px) | width / shape width | height / shape height | disk width / height | renderer |",
      "|---|---|---|---|---|---|---|---|"]
for label, W, H, w, h, fw, fh, r, ren in rows:
    md.append(f"| {label} | {W} x {H} | {w} | {h} | {fw} | {fh} | {r} | {ren} |")
(HERE / "ellipse-measure.md").write_text("\n".join(md) + "\n")
(HERE / "ellipse-raw-log.jsonl").write_text("\n".join(__import__("json").dumps(r) for r in log) + "\n")
