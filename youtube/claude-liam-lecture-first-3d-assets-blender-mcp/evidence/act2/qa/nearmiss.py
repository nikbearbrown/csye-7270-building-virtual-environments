#!/usr/bin/env python3
"""nearmiss.py <png> — blobs that WOULD fail GATE T's per-blob contrast (§8.3b) if they were a few px taller/wider:
INK/MUTE-mask components (light polarity) with contrast < 3.0 and h >= 20 px at 4K, w >= 1.2 h, plus their margin to the
28.9-px fragment threshold. Also min-size text runs in the 30..41 px band. Read-only use of type_check's functions."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[6] / "brutalist.art" / "runtime" / "scripts"))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
from PIL import Image
import numpy as np
img = Image.open(sys.argv[1]).convert("RGB")
if img.size != (3840, 2160):
    img = img.resize((3840, 2160), Image.LANCZOS)
a = np.array(img); fh, fw = a.shape[:2]
lab, n = tc.labeled_blobs(tc.visible_text_mask(a, "light").astype(np.uint8), min_px=30)
pad = 10
for x0, y0, x1, y1, px in tc.blob_bboxes(lab, n):
    h, w = y1 - y0, x1 - x0
    if h < 20 or w < h * 1.2 or w > h * 15 or px < h * w * 0.04 or px > fh * fh * 16 / 9 * 0.15:
        continue
    reg = lab[y0:y1 + 1, x0:x1 + 1]
    ids, cnt = np.unique(reg[reg > 0], return_counts=True)
    bid = ids[cnt.argmax()]
    col = a[y0:y1 + 1, x0:x1 + 1][reg == bid].astype(float).mean(axis=0)
    r0 = a[max(0, y0 - pad):y1 + pad + 1, max(0, x0 - pad):x1 + pad + 1].astype(float)
    ring = np.ones(r0.shape[:2], bool); ring[min(pad, y0):min(pad, y0) + h + 1, min(pad, x0):min(pad, x0) + w + 1] = False
    bg = r0[ring].mean(axis=0)
    r = tc.contrast_ratio(tuple(int(v) for v in col), tuple(int(v) for v in bg))
    if r < 3.0:
        tag = "FLAGGED" if (h >= 28.9 and w >= h * 1.5) else "near"
        print(f"{tag:7s} ({x0},{y0})-({x1},{y1}) h={h} w/h={w/h:.2f} ratio={r:.2f} col={tuple(int(v) for v in col)}")
