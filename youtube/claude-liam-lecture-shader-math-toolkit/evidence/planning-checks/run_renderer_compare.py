#!/usr/bin/env python3
"""run_renderer_compare.py: do the film's shaders read the same pixels in Forward+ and in the Compatibility renderer?
Renders eight of the film's shader files in both (Shader Lab --renderer forward_plus / gl_compatibility) and compares every pixel.
These shaders use literal numbers, no `source_color` uniform, so the answer is yes (within one 8-bit level). A `source_color` colour would differ.
Writes renderer-compare.json. Needs Pillow and numpy."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T  # noqa: E402

HERE = Path(__file__).resolve().parent
SH = T.FILM / "lab-shaders"
PNG = HERE / "png-dense"
PNG.mkdir(exist_ok=True)
log, rows = [], []
cases = [("04-mix-colors.gdshader", ["--kind", "rect"], []), ("13-ring-color.gdshader", ["--kind", "rect", "--size", "360x360"], []),
         ("14-ring-soft.gdshader", ["--kind", "rect", "--size", "360x360"], []), ("15-ring-final.gdshader", ["--kind", "rect", "--size", "360x360"], ["radius=0.3"]),
         ("09-glow.gdshader", ["--kind", "rect", "--size", "360x360"], []), ("07-pow.gdshader", ["--kind", "rect"], ["power=3"]),
         ("05-fract.gdshader", ["--kind", "rect"], ["count=4"]), ("03-smoothstep.gdshader", ["--kind", "rect"], ["width=0.3"])]
for shader, base_args, sets in cases:
    base = shader.split(".")[0]
    outs = {}
    for ren in ("forward_plus", "gl_compatibility"):
        png = PNG / f"{base}-{ren}.png"
        args = list(base_args) + ["--png", png, "--renderer", ren]
        for s in sets:
            args += ["--set", s]
        r = T.run_lab(SH / shader, args, f"{base}-{ren}", log)
        outs[ren] = (r, np.array(Image.open(png).convert("RGB")).astype(int) if r and r.get("ok") else None)
    a, b = outs["forward_plus"][1], outs["gl_compatibility"][1]
    names = [outs[k][0].get("renderer") if outs[k][0] else None for k in ("forward_plus", "gl_compatibility")]
    if a is None or b is None:
        rows.append({"shader": shader, "sets": sets, "ok": False, "renderers": names})
        print(shader, "FAILED in one renderer", names)
        continue
    d = np.abs(a - b).max(axis=2)
    rows.append({"shader": shader, "sets": sets, "ok": True, "renderers": names, "max_diff_levels": int(d.max()), "pixels_off_by_2_or_more": int((d >= 2).sum()), "pixels": int(d.size)})
    print(rows[-1])
(HERE / "renderer-compare.json").write_text(json.dumps({"rows": rows, "log": log}, indent=1))
