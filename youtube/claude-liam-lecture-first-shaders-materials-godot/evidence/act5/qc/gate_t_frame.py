#!/usr/bin/env python3
"""gate_t_frame.py FRAME.png [CLASSNAME] — run the toolkit's own GATE T pixel checks (type_check.py functions) on one 4K frame."""
import sys
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
import numpy as np
from PIL import Image
import type_check as tc
p = sys.argv[1]; cls = sys.argv[2] if len(sys.argv) > 2 else "B00_X"
img = Image.open(p).convert("RGB")
print(p, img.size)
arr = np.array(img)
pol, bg = tc.detect_polarity(arr)
print("polarity", pol, bg)
bid = cls.split("_")[0]
res = []
res.append(("min-size", tc.check_min_size(img, bid, cls, polarity=pol)))
res.append(("overflow", tc.check_overflow(img, bid, polarity=pol, pattern=cls)))
res.append(("contrast", tc.check_contrast(img, bid, cls, polarity=pol, bg_rgb=bg)))
res.append(("contrast-local", tc.check_contrast_per_blob(img, polarity=pol)))
res.append(("bbox-overlap", tc.check_bbox_overlap(img, polarity=pol)))
res.append(("card-clip", tc.check_card_clip(img, bid, cls)))
res.append(("kerning", tc.check_kerning_sanity(img, bid, True, False, cls)))
bad = 0
for n, (s, m) in res:
    print(f"  {n:15s} {s:5s} {m[:160]}")
    bad += s == "FAIL"
print("RESULT", "FAIL" if bad else "PASS")
