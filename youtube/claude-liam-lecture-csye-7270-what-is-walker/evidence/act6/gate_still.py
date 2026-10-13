#!/usr/bin/env python3
"""gate_still.py <Class> — quick check of a class's LAST frame (the 85-100% picture) at REAL 4K: renders one still (manim -s, 3840x2160,
caching off) under the shared 4K lock, then runs GATE T's pixel checks and Gate V on it. Faster than gates_act6.py (no full clip).
  python3 evidence/act6/gate_still.py B26_TheHabit"""
import sys, subprocess, time, io, contextlib
from pathlib import Path
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime")
sys.path.insert(0, str(TK / "scripts")); sys.path.insert(0, str(TK / "qc"))
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
    import final_frame_check as ff
from PIL import Image
import numpy as np
SCR = Path("/private/tmp/claude-501/lecture-csye-walker-act6")
LOCK = Path("/private/tmp/claude-501/lecture-csye-4k.lock")
cls = sys.argv[1]; bid = cls.split("_")[0]
while True:
    try:
        LOCK.mkdir(); break
    except FileExistsError:
        time.sleep(15)
try:
    subprocess.run(["manim", "-s", "-r", "3840,2160", "--disable_caching", "--media_dir", str(SCR / "media4ks"), "scenes.py", cls],
                   cwd=SCR, capture_output=True, text=True)
finally:
    LOCK.rmdir()
png = next((SCR / "media4ks/images/scenes").glob(f"{cls}_*.png"))
img = Image.open(png).convert("RGB"); arr = np.array(img)
pol, bg = tc.detect_polarity(arr)
res = [("8.1 min", tc.check_min_size(img, bid, cls, polarity=pol)), ("8.2 ovf", tc.check_overflow(img, bid, polarity=pol, pattern=cls)),
       ("8.3 con", tc.check_contrast(img, bid, cls, polarity=pol, bg_rgb=bg)), ("8.3b blob", tc.check_contrast_per_blob(img, polarity=pol)),
       ("8.6b ovl", tc.check_bbox_overlap(img, polarity=pol))]
dv, cover = ff.analyze_frame(str(png))
print(f"=== {cls} LAST FRAME {img.size}  Gate V cover={cover * 100:.0f}%  {dv}")
for k, (s, m) in res:
    print(f"   {k}: {s}  {m[:200]}")
print(png)
