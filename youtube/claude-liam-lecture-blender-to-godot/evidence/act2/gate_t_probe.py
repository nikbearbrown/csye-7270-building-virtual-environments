#!/usr/bin/env python3
"""gate_t_probe.py <Class> [<Class> ...]  — a per-scene dry run of the pixel half of GATE T (type_check.py), for BUILDERS.
Renders each scene from the preflight scratch (/private/tmp/claude-501/lecture-blender-act2/scenes.py) at 3840x2160, 6 fps (the animation clock
is the same; only the sampling is coarse), takes the MIDPOINT frame exactly as type_check.extract_frame does, and runs the same per-frame checks
the real gate runs on a Manim beat (min-size 8.1, overflow 8.2, contrast 8.3, contrast-local 8.3b, bbox-overlap 8.6b, kerning 8.4).
It is NOT the gate (that runs on the assembled reel); it exists so an act's scenes can be checked before the lead assembles anything.
  python3 gate_t_probe.py B09_LiveRoute B12_TwoRules      -> prints one line per check; frames saved to <scratch>/gate_t/<Class>.png
"""
import sys, subprocess, pathlib, importlib.util, json, re
SCR = pathlib.Path("/private/tmp/claude-501/lecture-blender-act2")
TC = pathlib.Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/type_check.py")
spec = importlib.util.spec_from_file_location("type_check", TC); tc = importlib.util.module_from_spec(spec)
sys.modules["type_check"] = tc; spec.loader.exec_module(tc)
import numpy as np
out = SCR / "gate_t"; out.mkdir(exist_ok=True)
for C in sys.argv[1:]:
    bid = C.split("_")[0]
    mdir = SCR / "media_4k"
    subprocess.run(["manim", "-r", "3840,2160", "--fps", "6", "--media_dir", str(mdir), "scenes.py", C], cwd=SCR,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    mp4 = next(iter(sorted(mdir.glob(f"videos/scenes/2160p6/{C}.mp4"))), None)
    if not mp4:
        print(C, "NO RENDER"); continue
    img = tc.extract_frame(mp4)
    img.save(out / f"{C}.png")
    pol, bg = tc.detect_polarity(np.array(img))
    res = []
    res.append(("min-size 8.1", *tc.check_min_size(img, bid, C, polarity=pol)))
    res.append(("overflow 8.2", *tc.check_overflow(img, bid, polarity=pol, pattern=C)))
    res.append(("contrast 8.3", *tc.check_contrast(img, bid, C, polarity=pol, bg_rgb=bg)))
    res.append(("contrast-local 8.3b", *tc.check_contrast_per_blob(img, polarity=pol)))
    res.append(("bbox-overlap 8.6b", *tc.check_bbox_overlap(img, polarity=pol)))
    res.append(("kerning 8.4", *tc.check_kerning_sanity(img, bid, True, False, C)))
    print(f"=== {C}  mid-frame {img.size}  polarity {pol}")
    for name, st, msg in res:
        print(f"  {st:5s} {name}: {msg[:230]}")
