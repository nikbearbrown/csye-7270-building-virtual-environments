#!/usr/bin/env python3
"""run_gate_t_advisory.py: an EARLY WARNING for GATE T, not the gate. Uses the toolkit's own blob detector (type_check.py: visible_text_mask, labeled_blobs,
blob_bboxes, text_run_bboxes; read only) on (1) the film's real Lab renders pasted into two stand-in layouts at 4K and (2) synthetic ramp strips
(continuous against tiled) as the Manim scenes could draw them. A 'text-like run' is what GATE T would go on to measure and may FAIL.
Writes gate-t-advisory.json. Needs Pillow, numpy, scipy."""
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True      # never leave a bytecode cache beside the toolkit file this script imports (read only)

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T  # noqa: E402

HERE = Path(__file__).resolve().parent
TC = T.FILM.parents[2] / "brutalist.art" / "runtime" / "scripts" / "type_check.py"
spec = importlib.util.spec_from_file_location("type_check", TC)
tc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tc)
SH = T.FILM / "lab-shaders"
PNG = HERE / "png-gate"
PNG.mkdir(exist_ok=True)
BG = (242, 240, 233)           # the Claude stage #F2F0E9
log, rows = [], []
SQ = ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "5.625", "--size", "1280x720"]
RE = ["--kind", "rect", "--size", "1280x720"]
CASES = [("ramp", "01-ramp.gdshader", RE, []), ("step-0.5", "02-step.gdshader", RE, ["edge=0.5"]), ("smoothstep-0.4", "03-smoothstep.gdshader", RE, ["width=0.4"]),
         ("smoothstep-0.03", "03-smoothstep.gdshader", RE, ["width=0.03"]), ("mix-colors", "04-mix-colors.gdshader", RE, []), ("fract-1", "05-fract.gdshader", RE, ["count=1"]),
         ("fract-6", "05-fract.gdshader", RE, ["count=6"]), ("stripes", "06-stripes.gdshader", RE, []), ("pow-1", "07-pow.gdshader", RE, ["power=1"]),
         ("pow-6", "07-pow.gdshader", RE, ["power=6"]), ("distance", "08-distance.gdshader", SQ, []), ("glow", "09-glow.gdshader", SQ, []),
         ("disk", "10-disk.gdshader", SQ, []), ("disk-flip", "11-disk-flip.gdshader", SQ, []), ("ring-hard", "12-ring-hard.gdshader", SQ, []),
         ("ring-color", "13-ring-color.gdshader", SQ, []), ("ring-soft", "14-ring-soft.gdshader", SQ, []),
         ("ring-final-0.12", "15-ring-final.gdshader", SQ, ["radius=0.12"]), ("ring-final-0.3", "15-ring-final.gdshader", SQ, ["radius=0.3"]),
         ("ring-final-0.38", "15-ring-final.gdshader", SQ, ["radius=0.38"])]


def text_like_runs(arr):
    mask = tc.visible_text_mask(arr, "light")
    lab, n = tc.labeled_blobs(mask)
    bb = tc.blob_bboxes(lab, n)
    return bb, tc.text_run_bboxes(bb, arr.shape[0])


for name, shader, base, sets in CASES:
    png = PNG / f"{name}.png"
    args = list(base) + ["--png", png]
    for s in sets:
        args += ["--set", s]
    T.run_lab(SH / shader, args, f"gate-{name}", log)
    img = Image.open(png).convert("RGB")
    for layout, W, x0 in (("side", 1900, 1700), ("video", 2900, 470)):          # stand-ins for ShaderLab's code-left window and result-only window
        H = int(W * 9 / 16)
        y0 = (2160 - H) // 2
        canvas = Image.new("RGB", (3840, 2160), BG)
        canvas.paste(img.resize((W, H), Image.LANCZOS), (x0, y0))
        bb, runs = text_like_runs(np.array(canvas))
        rows.append({"kind": "lab render", "capture": name, "layout": layout, "blobs": len(bb), "text_like_runs": len(runs)})
        print(name, layout, "blobs", len(bb), "text-like runs", len(runs))

# synthetic ramp strips as a Manim scene might draw them (3840 x 2160 frame, strip 2000 px wide, 130 px tall, true grays 0..1)
for label, tiles, gap in (("continuous", 0, 0), ("64 tiles, 6 px gaps", 64, 6), ("48 tiles, 8 px gaps", 48, 8)):
    canvas = np.full((2160, 3840, 3), BG, dtype=np.uint8)
    W, H, x0, y0 = 2000, 130, 920, 1500
    if tiles == 0:
        for i in range(W):
            g = int(round(255 * i / (W - 1)))
            canvas[y0:y0 + H, x0 + i] = (g, g, g)
    else:
        tw = (W - gap * (tiles - 1)) / tiles
        for t in range(tiles):
            g = int(round(255 * t / (tiles - 1)))
            xa = int(round(x0 + t * (tw + gap)))
            xb = int(round(xa + tw))
            canvas[y0:y0 + H, xa:xb] = (g, g, g)
    bb, runs = text_like_runs(canvas)
    rows.append({"kind": "synthetic ramp strip", "capture": label, "blobs": len(bb), "text_like_runs": len(runs),
                 "runs": [(b[2] - b[0] + 1, b[3] - b[1] + 1) for b in runs][:4]})
    print("strip", label, "blobs", len(bb), "text-like runs", len(runs), rows[-1]["runs"])
(HERE / "gate-t-advisory.json").write_text(json.dumps({"rows": rows}, indent=1))
