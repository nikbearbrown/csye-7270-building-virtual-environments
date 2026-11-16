#!/usr/bin/env python3
"""gateT.py Class [Class...] — render each Manim class of Act II at 4K (6 fps: the time axis is the same as the 24 fps film), cut the 50% and 85% frames, run the
toolkit's own GATE T per-frame checks on them (the same functions, in the same order, as type_check.run_check), save the frames, delete the scratch media."""
import subprocess, sys, shutil, json
from pathlib import Path
import numpy as np
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
import type_check as tc
SCR = Path("/private/tmp/claude-501/lecture-a5shaders-act2")   # made by: bash preflight.sh 2 <Classes>
OUT = SCR / "gateT_frames"        # the 50% and 85% frames are kept here for looking
OUT.mkdir(exist_ok=True)
for cls in [a for a in sys.argv[1:] if not a.startswith("-")]:
    media = SCR / "gateT_4k_media" / cls          # deleted after each class (disk is tight)
    shutil.rmtree(media, ignore_errors=True)
    r = subprocess.run(["manim", "-r", "3840,2160", "--fps", "6", "--media_dir", str(media), "scenes.py", cls], cwd=SCR, capture_output=True, text=True)
    vids = list(media.rglob(f"{cls}.mp4"))
    if not vids:
        print(cls, "NO VIDEO", (r.stdout + r.stderr)[-800:]); continue
    v = vids[0]
    dur = tc.video_duration(v)
    pace = [l for l in (r.stdout + r.stderr).splitlines() if "[pace]" in l]
    print(f"== {cls}  clip {dur:.2f}s  {pace[-1].strip() if pace else ''}")
    for frac in (0.5, 0.85):
        img = tc.extract_frame(v, min(dur * frac, dur - 0.05))
        img.save(OUT / f"{cls}_{int(frac*100)}.png")
        bid = cls.split("_")[0]
        beat = {"beat_id": bid, "lane": "MANIM", "shot": {"type": "GRAPHIC"}}
        im = tc.typography_frame(img, beat, reel=None)
        pol, bg = tc.detect_polarity(np.array(im))
        res = []
        res.append(("min-size", *tc.check_min_size(im, bid, cls, polarity=pol)))
        res.append(("overflow", *tc.check_overflow(im, bid, polarity=pol, pattern=cls)))
        res.append(("contrast", *tc.check_contrast(im, bid, cls, polarity=pol, bg_rgb=bg)))
        res.append(("contrast-local", *tc.check_contrast_per_blob(im, polarity=pol)))
        res.append(("bbox-overlap", *tc.check_bbox_overlap(im, polarity=pol)))
        res.append(("card-clip", *tc.check_card_clip(im, bid, cls)))
        res.append(("kerning", *tc.check_kerning_sanity(im, bid, True, False, cls)))
        bad = [x for x in res if x[1] == "FAIL"]
        print(f"  {int(frac*100)}%  {'FAIL' if bad else 'PASS'}")
        for name, s, m in res:
            if s == "FAIL" or "-v" in sys.argv:
                print(f"     {name}: {s}  {m[:240]}")
    shutil.rmtree(media, ignore_errors=True)
