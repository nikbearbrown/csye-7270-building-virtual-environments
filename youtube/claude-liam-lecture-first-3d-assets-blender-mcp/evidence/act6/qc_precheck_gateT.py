"""Pre-check GATE T pixel checks (type_check.py functions) on the midpoint frame of local 1080p clips; also on a 2x upscale (~4K)."""
import sys, importlib.util
from pathlib import Path
from PIL import Image
import numpy as np
spec = importlib.util.spec_from_file_location("tc", "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/type_check.py")
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
for mp4 in sys.argv[1:]:
    img = tc.extract_frame(Path(mp4))
    for tag, im in (("1080", img), ("x2", img.resize((img.width * 2, img.height * 2), Image.LANCZOS))):
        arr = np.array(im); pol, bg = tc.detect_polarity(arr)
        res = [("min", tc.check_min_size(im, "B", "", polarity=pol)), ("ovf", tc.check_overflow(im, "B", polarity=pol)),
               ("con", tc.check_contrast(im, "B", "", polarity=pol, bg_rgb=bg)), ("conb", tc.check_contrast_per_blob(im, polarity=pol)),
               ("ovl", tc.check_bbox_overlap(im, polarity=pol)), ("kern", tc.check_kerning_sanity(im, "B", True, False, ""))]
        bad = [(k, s, m[:150]) for k, (s, m) in res if s != "PASS"]
        print(Path(mp4).stem, tag, pol, "ALL PASS" if not bad else bad)
