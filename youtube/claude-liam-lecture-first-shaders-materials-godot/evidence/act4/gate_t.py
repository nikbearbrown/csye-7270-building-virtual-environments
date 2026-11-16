#!/usr/bin/env python3
"""gate_t.py <mp4> <BEAT_ID> [pct ...] — runs the toolkit's own GATE T functions (runtime/scripts/type_check.py) and GATE V's analyze_frame on frames of one rendered Manim beat.
Frames: the 50% frame (what GATE T and Gate V sample) and the 85% frame (Gate V's second sample), plus any extra pct given. Writes frames to <scratch>/frames/."""
import sys, json, subprocess, io
from pathlib import Path
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc")
import numpy as np
import type_check as tc
from PIL import Image
mp4, bid = sys.argv[1], sys.argv[2]
pcts = [50, 85] + [int(x) for x in sys.argv[3:]]
out = Path("/private/tmp/claude-501/lecture-a5shaders-act4-4k/frames"); out.mkdir(parents=True, exist_ok=True)
dur = tc.video_duration(Path(mp4))
beat = {"beat_id": bid, "lane": "MANIM", "shot": {"type": "GRAPHIC", "manim": {"class": bid}}, "qc": {}}
import final_frame_check as ffc
for pct in pcts:
    t = min(dur * pct / 100.0, dur - 0.05)
    img = tc.extract_frame(Path(mp4), t)
    img.save(out / f"{bid}_{pct}.png")
    chk = tc.typography_frame(img, beat, reel=None)
    arr = np.array(chk)
    pol, bg = tc.detect_polarity(arr)
    res = []
    res.append(("min-size", *tc.check_min_size(chk, bid, bid, polarity=pol)))
    res.append(("overflow", *tc.check_overflow(chk, bid, polarity=pol, pattern=bid)))
    res.append(("contrast", *tc.check_contrast(chk, bid, bid, polarity=pol, bg_rgb=bg)))
    res.append(("contrast-local", *tc.check_contrast_per_blob(chk, polarity=pol)))
    res.append(("bbox-overlap", *tc.check_bbox_overlap(chk, polarity=pol)))
    res.append(("card-clip", *tc.check_card_clip(chk, bid, bid)))
    res.append(("kerning", *tc.check_kerning_sanity(chk, bid, True, False, bid)))
    print(f"--- {bid} @ {pct}% (t={t:.2f}s of {dur:.2f}s, polarity {pol}, frame {img.size})")
    for name, st, msg in res:
        print(f"  {name:15s} {st:5s} {msg[:230]}")
    v = ffc.analyze_frame(str(out / f"{bid}_{pct}.png"))
    print("  GATE V:", json.dumps(v, default=str)[:400])
