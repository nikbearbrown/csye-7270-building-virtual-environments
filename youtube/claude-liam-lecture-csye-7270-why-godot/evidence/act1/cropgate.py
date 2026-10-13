#!/usr/bin/env python3
"""cropgate.py — quick synthetic GATE T check of a real capture crop pasted on the stage at 4K (a filter only: the real check is gates_act1.py).
  python3 evidence/act1/cropgate.py <capture.png> x0 y0 x1 y1 <window width units> <cx> <cy>"""
import sys, io, contextlib
from pathlib import Path
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime")
sys.path.insert(0, str(TK / "scripts")); sys.path.insert(0, str(TK / "qc"))
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
from PIL import Image
import numpy as np


def test(crop_img, wunits, cx, cy, label=""):
    W, H = 3840, 2160
    bg = Image.new("RGB", (W, H), (0xF2, 0xF0, 0xE9))
    w = int(wunits * 270); h = int(w * crop_img.height / crop_img.width)
    bg.paste(crop_img.resize((w, h), Image.LANCZOS), (int(W / 2 + cx * 270 - w / 2), int(H / 2 - cy * 270 - h / 2)))
    pol, _ = tc.detect_polarity(np.array(bg))
    r = tc.check_contrast_per_blob(bg, polarity=pol); o = tc.check_bbox_overlap(bg, polarity=pol)
    print(label, r[0], r[1][:110], "|", o[0], o[1][:80])


if __name__ == "__main__":
    f = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); wu, cx, cy = map(float, sys.argv[6:9])
    test(Image.open(f).convert("RGB").crop((x0, y0, x1, y1)), wu, cx, cy, f"{x0},{y0},{x1},{y1}")
