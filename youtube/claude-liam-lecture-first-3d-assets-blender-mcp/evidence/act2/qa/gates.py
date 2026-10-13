#!/usr/bin/env python3
"""gates.py <png> [<png> ...] — Act II QA (read-only use of the toolkit): run GATE T pixel checks (type_check.py) and Gate V (final_frame_check.analyze_frame)
on a still, upscaled to 3840x2160 (the master size). Read-only use of the toolkit's own functions."""
import sys
from pathlib import Path
TK = str(__import__("pathlib").Path(__file__).resolve().parents[6] / "brutalist.art" / "runtime")
sys.path.insert(0, TK + "/scripts"); sys.path.insert(0, TK + "/qc")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
    import final_frame_check as ff
from PIL import Image
import numpy as np

for p in sys.argv[1:]:
    img = Image.open(p).convert("RGB")
    if img.size != (3840, 2160):
        img = img.resize((3840, 2160), Image.LANCZOS)
    arr = np.array(img)
    pol, bg = tc.detect_polarity(arr)
    res = [("min", tc.check_min_size(img, "X", "", polarity=pol)),
           ("ovf", tc.check_overflow(img, "X", polarity=pol, pattern="")),
           ("con", tc.check_contrast(img, "X", "", polarity=pol, bg_rgb=bg)),
           ("blob", tc.check_contrast_per_blob(img, polarity=pol)),
           ("ovl", tc.check_bbox_overlap(img, polarity=pol))]
    tmp = p + ".gateV.png"
    img.save(tmp)
    dv, cover = ff.analyze_frame(tmp)
    __import__("os").remove(tmp)
    dv = [d for d in dv if d[1] not in ("underfill", "clustered")]
    bad = [k for k, (s, m) in res if s == "FAIL"] + [d[1] for d in dv]
    print(f"{'FAIL' if bad else 'PASS'}  {Path(p).name}  polarity={pol}  V-cover={cover*100:.0f}%")
    for k, (s, m) in res:
        if s == "FAIL":
            print(f"   T.{k}: {s} {m[:230]}")
    for d in dv:
        print(f"   V: {d}")
