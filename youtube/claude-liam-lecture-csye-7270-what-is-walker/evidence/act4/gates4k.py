#!/usr/bin/env python3
"""gates4k.py <Class> [<Class> ...] [--norender] — Act IV QA at REAL 4K (read-only use of the toolkit's own gate functions).
For each class: assemble kit + scenes_act4.py into a private scratch, take the shared 4K lock, render the class at 3840x2160 24 fps
(caching off), release the lock, then on the 50% and 85% frames run GATE T's pixel checks (type_check.py: min-size, overflow,
contrast, per-blob contrast, bbox overlap, kerning) and Gate V (final_frame_check.analyze_frame); ffprobe the clip vs its audio.
Frames are kept in <scratch>/frames/ for LOOKING.
  python3 evidence/act4/gates4k.py B28_GreyTurnaround B29_TwoFields ...
"""
import sys, os, json, shutil, subprocess, io, contextlib, time
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime")
sys.path.insert(0, str(TK / "scripts")); sys.path.insert(0, str(TK / "qc"))
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
    import final_frame_check as ff
from PIL import Image
import numpy as np
SCR = Path("/private/tmp/claude-501/lecture-walker-act4-4k"); LOCK = Path("/private/tmp/claude-501/lecture-csye-4k.lock")
args = [a for a in sys.argv[1:] if not a.startswith("--")]; norender = "--norender" in sys.argv
SCR.mkdir(parents=True, exist_ok=True); (SCR / "frames").mkdir(exist_ok=True)
subprocess.run([sys.executable, str(REEL / "assemble_scenes.py"), "--out", str(SCR), "--acts", "4"], check=True, capture_output=True)
shutil.copy(REEL / "beat_sheet.json", SCR / "beat_sheet.json")
for l in ("pantry", "evidence"):
    if not (SCR / l).exists():
        os.symlink(REEL / l, SCR / l)
sheet = json.loads((REEL / "beat_sheet.json").read_text()); DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"]}
for C in args:
    bid = C.split("_")[0]
    mp4 = SCR / "media/videos/scenes/2160p24" / f"{C}.mp4"
    if not norender:
        while True:
            try:
                LOCK.mkdir(); break
            except FileExistsError:
                time.sleep(20)
        try:
            r = subprocess.run(["manim", "-r", "3840,2160", "--fps", "24", "--disable_caching", "--media_dir", str(SCR / "media"),
                                "scenes.py", C], cwd=SCR, capture_output=True, text=True)
        finally:
            LOCK.rmdir()
        pace = [l for l in r.stdout.splitlines() + r.stderr.splitlines() if "[pace]" in l]
        if r.returncode:
            print(C, "RENDER FAILED", r.stderr[-800:]); continue
        print(pace[-1].strip() if pace else "")
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                             capture_output=True, text=True).stdout)
    print(f"== {C}  clip {d:.3f}s  audio {DUR[bid]:.3f}s  slack {DUR[bid] - d:+.3f}s")
    for frac in (0.5, 0.85):
        img = tc.extract_frame(mp4, t=min(d * frac, d - 0.05))
        png = SCR / "frames" / f"{C}_{int(frac * 100)}.png"; img.save(png)
        arr = np.array(img); pol, bg = tc.detect_polarity(arr)
        res = [("min", tc.check_min_size(img, bid, "", polarity=pol)), ("ovf", tc.check_overflow(img, bid, polarity=pol)),
               ("con", tc.check_contrast(img, bid, "", polarity=pol, bg_rgb=bg)), ("blob", tc.check_contrast_per_blob(img, polarity=pol)),
               ("ovl", tc.check_bbox_overlap(img, polarity=pol)), ("kern", tc.check_kerning_sanity(img, bid, True, False, C))]
        dv, cover = ff.analyze_frame(str(png))
        tfail = [(k, m[:200]) for k, (s, m) in res if s == "FAIL"]
        print(f"  {int(frac*100)}%  GATE T {'PASS' if not tfail else 'FAIL'}{'' if frac == 0.5 else ' (info: GATE T samples 50%)'}"
              f"  | Gate V cover {cover*100:.0f}% {[x[1] + ': ' + x[2][:90] for x in dv] or 'clean'}")
        for k, m in tfail:
            print(f"     T.{k}: {m}")
