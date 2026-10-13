#!/usr/bin/env python3
"""probe_mid.py <Class> ... — robustness probe on the 4K clips gates4k.py rendered: GATE T pixel checks on the frames at the
midpoint and +-1, 2, 3 frames (a re-encode or a frame-rounding shift moves GATE T's sample by about a frame).
  python3 evidence/act4/probe_mid.py B28_GreyTurnaround ...
"""
import sys, io, contextlib, subprocess
from pathlib import Path
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime")
sys.path.insert(0, str(TK / "scripts"))
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
import numpy as np
SCR = Path("/private/tmp/claude-501/lecture-walker-act4-4k/media/videos/scenes/2160p24")
for C in sys.argv[1:]:
    mp4 = SCR / f"{C}.mp4"; d = tc.video_duration(mp4); out = []
    for k in (-3, -2, -1, 0, 1, 2, 3):
        img = tc.extract_frame(mp4, t=d * 0.5 + k / 24); arr = np.array(img); pol, bg = tc.detect_polarity(arr)
        res = [tc.check_min_size(img, "X", "", polarity=pol), tc.check_overflow(img, "X", polarity=pol),
               tc.check_contrast(img, "X", "", polarity=pol, bg_rgb=bg), tc.check_contrast_per_blob(img, polarity=pol),
               tc.check_bbox_overlap(img, polarity=pol), tc.check_kerning_sanity(img, "X", True, False, C)]
        out.append(f"{k:+d}:{'ok' if all(r[0] != 'FAIL' for r in res) else 'FAIL'}")
    print(C, " ".join(out))
