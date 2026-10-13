#!/usr/bin/env python3
"""gate_frames.py <clip.mp4> <Class> — run the toolkit's GATE T pixel checks (type_check.py, exactly the calls run_check makes for a
Manim beat) on the clip's 50% frame, and Gate V (final_frame_check.analyze_frame) on its 50% and 85% frames; print the clip length
against the beat's measured audio. Frames are saved beside the clip (<Class>_50.png, <Class>_85.png) to LOOK at.
Read-only use of the toolkit's own functions."""
import contextlib, io, json, subprocess, sys
from pathlib import Path
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime")
sys.path.insert(0, str(TK / "scripts")); sys.path.insert(0, str(TK / "qc"))
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
    import final_frame_check as ff
import numpy as np

mp4, cls = Path(sys.argv[1]), sys.argv[2]
bid = cls.split("_")[0]
reel = Path(__file__).resolve().parents[2]
sheet = json.loads((reel / "beat_sheet.json").read_text())
beat = next(b for b in sheet["beats"] if b["beat_id"] == bid)
sparse = bool(beat.get("qc", {}).get("sparse_by_design"))
lanes = reel / "lanes" / "act3.json"
if lanes.exists():
    sparse = bool(json.loads(lanes.read_text()).get(bid, {}).get("sparse", sparse))
dur = tc.video_duration(mp4)
tgt = float(beat["actual_duration_s"])
print(f"  {cls}: clip {dur:.3f}s, audio {tgt:.3f}s, slack {tgt - dur:+.3f}s" + ("  OVER" if dur > tgt else ""))
bad = []
for pct in (50, 85):
    img = tc.extract_frame(mp4, min(dur * pct / 100, dur - 0.05))
    png = mp4.parent / f"{cls}_{pct}.png"
    img.save(png)
    if pct == 50:
        arr = np.array(img)
        pol, bg = tc.detect_polarity(arr)
        res = [("min-size 8.1", tc.check_min_size(img, bid, cls, polarity=pol)),
               ("overflow 8.2", tc.check_overflow(img, bid, polarity=pol, pattern=cls)),
               ("contrast 8.3", tc.check_contrast(img, bid, cls, polarity=pol, bg_rgb=bg)),
               ("contrast-local 8.3b", tc.check_contrast_per_blob(img, polarity=pol)),
               ("bbox-overlap 8.6b", tc.check_bbox_overlap(img, polarity=pol)),
               ("card-clip 8.13", tc.check_card_clip(img, bid, cls)),
               ("kerning 8.4", tc.check_kerning_sanity(img, bid, True, False, cls))]
        for name, (s, m) in res:
            print(f"    T {pct}% {name}: {s}  {m[:170]}")
            if s == "FAIL":
                bad.append(f"T {name}")
    dv, cover = ff.analyze_frame(str(png))
    waived = [d for d in dv if sparse and d[1] in ("underfill", "clustered")]
    dv = [d for d in dv if d not in waived]
    print(f"    V {pct}%: cover {cover * 100:.0f}%  " + ("; ".join(f"{d[0]} {d[1]}: {d[2]}" for d in dv) or "clean")
          + (f"  (waived as sparse: {', '.join(d[1] for d in waived)})" if waived else ""))
    bad += [f"V{pct} {d[1]}" for d in dv if d[0] in ("BLOCKER", "MAJOR")]
print(f"  RESULT {cls}: " + ("PASS" if not bad else "FAIL " + ", ".join(bad)))
