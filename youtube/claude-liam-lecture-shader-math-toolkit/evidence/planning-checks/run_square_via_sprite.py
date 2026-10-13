#!/usr/bin/env python3
"""run_square_via_sprite.py: the round pictures of this film are SQUARE. The capture plan renders them as the Lab's own `sprite` kind (a white
128 px texture scaled 5.625x = 720 px, centred in a 1280x720 window on the #D9D5CA stage). This proves that route gives the same pixels as a plain
720x720 rect render (so UV runs 0 to 1 across the square, circles are round, and the stage colour is the one the film expects).
Writes square-via-sprite.json. Needs Pillow and numpy."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T  # noqa: E402

HERE = Path(__file__).resolve().parent
PNG = HERE / "png-dense"
PNG.mkdir(exist_ok=True)
SH = T.FILM / "lab-shaders"
log, rows = [], []
for shader, sets in (("15-ring-final.gdshader", ["radius=0.3"]), ("08-distance.gdshader", []), ("10-disk.gdshader", [])):
    base = shader.split(".")[0]
    args_rect = ["--kind", "rect", "--size", "720x720", "--png", PNG / f"{base}-rect720.png"]
    args_spr = ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "5.625", "--size", "1280x720", "--png", PNG / f"{base}-sprite1280.png"]
    for s in sets:
        args_rect += ["--set", s]
        args_spr += ["--set", s]
    r1 = T.run_lab(SH / shader, args_rect, f"{base}-rect720", log)
    r2 = T.run_lab(SH / shader, args_spr, f"{base}-sprite1280", log)
    a = np.array(Image.open(PNG / f"{base}-rect720.png").convert("RGB")).astype(int)
    b = np.array(Image.open(PNG / f"{base}-sprite1280.png").convert("RGB")).astype(int)
    x0 = (b.shape[1] - 720) // 2
    d = np.abs(b[:, x0:x0 + 720] - a).max(axis=2)
    rows.append({"shader": shader, "rect720_shape": list(a.shape), "sprite1280_shape": list(b.shape), "max_diff_levels": int(d.max()),
                 "pixels_off_by_2_or_more": int((d >= 2).sum()), "pixels": int(d.size), "stage_rgb_8bit": [int(v) for v in b[10, 10]],
                 "renderer": r2.get("renderer")})
    print(rows[-1])
(HERE / "square-via-sprite.json").write_text(json.dumps({"rows": rows, "log": log}, indent=1))
