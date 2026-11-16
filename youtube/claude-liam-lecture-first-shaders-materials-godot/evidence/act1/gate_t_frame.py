#!/usr/bin/env python3
"""gate_t_frame.py <video.mp4 | frame.png> <BEAT_ID> <Class> <reel_dir_with_scenes.py> [pct ...]
Runs the toolkit's own GATE T pixel checks (type_check.py functions) on a frame of a rendered clip (at each pct of its length)
or on a PNG. Same call sequence as type_check.run_check for a Manim beat. Prints PASS/FAIL per check."""
import sys, json
from pathlib import Path
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
import numpy as np
import type_check as tc
src, bid, cls, reel = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
pcts = [float(p) for p in sys.argv[5:]] or [50, 85]
beat = {"beat_id": bid, "lane": "manim", "shot": {"type": "GRAPHIC", "manim": {"class": cls}}, "qc": {}}
imgs = []
if src.endswith(".mp4"):
    dur = tc.video_duration(Path(src))
    for p in pcts:
        im = tc.extract_frame(Path(src), min(dur * p / 100.0, dur - 0.05))
        imgs.append((f"{p:g}%", im))
else:
    from PIL import Image
    imgs.append(("png", Image.open(src).convert("RGB")))
font_named = tc.font_is_named_in_scenes(reel)
mathtex = tc.has_mathtex_in_scenes(reel)
bad = 0
for tag, im in imgs:
    img = tc.typography_frame(im, beat, reel=reel)
    pol, bg = tc.detect_polarity(np.array(img))
    res = [("min-size", tc.check_min_size(img, bid, cls, polarity=pol)),
           ("overflow", tc.check_overflow(img, bid, polarity=pol, pattern=cls)),
           ("contrast", tc.check_contrast(img, bid, cls, polarity=pol, bg_rgb=bg)),
           ("contrast-local", tc.check_contrast_per_blob(img, polarity=pol)),
           ("bbox-overlap", tc.check_bbox_overlap(img, polarity=pol)),
           ("card-clip", tc.check_card_clip(img, bid, cls)),
           ("kerning", tc.check_kerning_sanity(img, bid, font_named, mathtex, cls))]
    print(f"== {bid} {cls} @ {tag}  size={im.size} polarity={pol}")
    for name, (s, m) in res:
        print(f"   {name:15s} {s:5s} {m[:200]}")
        if s == "FAIL": bad += 1
print("GATE T:", "FAIL" if bad else "PASS", f"({bad} failing checks)")
sys.exit(2 if bad else 0)
