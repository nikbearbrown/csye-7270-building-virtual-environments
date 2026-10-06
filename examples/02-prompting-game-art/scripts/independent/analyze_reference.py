#!/usr/bin/env python3
"""Measure TERM-REF-02: background share, the three soldiers' bounding boxes
(connected components of non-white pixels, dilated 6 px to join thin legs),
and the spacing of colour edges inside the black soldier (the drawn 'pixel' size)."""
import sys
from collections import Counter
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
fg = a.min(axis=2) <= 235
print("size", a.shape[1], "x", a.shape[0], "; near-white background share", round(1 - fg.mean(), 3))
lab, n = ndimage.label(ndimage.binary_dilation(fg, iterations=6))
for i, sl in enumerate(ndimage.find_objects(lab)):
    print("object", i + 1, "x", sl[1].start, "-", sl[1].stop, "y", sl[0].start, "-", sl[0].stop,
          "(", sl[1].stop - sl[1].start, "x", sl[0].stop - sl[0].start, ")")
runs = Counter()
for y in range(380, 800, 3):
    d = np.abs(np.diff(a[y, 363:672], axis=0)).sum(axis=1)
    e = np.where(d > 40)[0]
    for g in np.diff(e):
        if g > 2: runs[int(g)] += 1
print("most common gaps between colour edges (px: count)", sorted(runs.items(), key=lambda kv: -kv[1])[:10])
