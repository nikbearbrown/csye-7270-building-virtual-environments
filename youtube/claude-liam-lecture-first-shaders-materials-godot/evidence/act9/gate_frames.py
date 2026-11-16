#!/usr/bin/env python3
"""gate_frames.py — runs the toolkit's OWN GATE T pixel checks (type_check.py functions) and GATE V analyze_frame (final_frame_check.py) on 4K PNG frames.
  python3 evidence/act9/gate_frames.py <frame.png> [<frame.png> ...]
The frames are the 50% and 85% frames of a Manim class rendered at 4K (see evidence/act9/RENDER-NOTES.md). Used by Builder 7 (Act IX) for the beats that show real captures.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime")
sys.path.insert(0, str(TK / "scripts")); sys.path.insert(0, str(TK / "qc"))
import type_check as tc            # noqa: E402
import final_frame_check as gv     # noqa: E402

for p in sys.argv[1:]:
    img = Image.open(p).convert("RGB")
    arr = np.array(img)
    pol, bg = tc.detect_polarity(arr)
    bid = Path(p).stem
    print(f"== {p}  {img.size} polarity={pol} bg={bg}")
    for name, fn in (
        ("min-size 8.1", lambda: tc.check_min_size(img, bid, bid, polarity=pol)),
        ("overflow 8.2", lambda: tc.check_overflow(img, bid, polarity=pol, pattern=bid)),
        ("contrast 8.3", lambda: tc.check_contrast(img, bid, bid, polarity=pol, bg_rgb=bg)),
        ("contrast-local 8.3b", lambda: tc.check_contrast_per_blob(img, polarity=pol)),
        ("bbox-overlap 8.6b", lambda: tc.check_bbox_overlap(img, polarity=pol)),
        ("kerning 8.4", lambda: tc.check_kerning_sanity(img, bid, True, False, bid)),
    ):
        try:
            s, m = fn()
        except Exception as e:      # noqa: BLE001
            s, m = "ERROR", repr(e)
        print(f"  {name:20s} {s:5s} {m[:230]}")
    defects, cover = gv.analyze_frame(p)
    print(f"  GATE V cover={cover*100:.0f}%  defects={defects}")
