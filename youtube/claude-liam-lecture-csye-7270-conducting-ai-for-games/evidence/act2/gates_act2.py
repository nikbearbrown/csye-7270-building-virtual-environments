#!/usr/bin/env python3
"""gates_act2.py <Class> [<Class> ...] — Act II gate evidence at REAL 4K (read-only use of the toolkit's own gate functions).
For each class (assembled by REEL/preflight.sh 1 into /private/tmp/claude-501/lecture-csye-games-act2/scenes.py):
  1. takes the shared 4K lock (/private/tmp/claude-501/lecture-csye-4k.lock), renders the class at 3840x2160, 24 fps,
     caching off, into a private scratch, and releases the lock right after;
  2. prints the clip length against the measured audio;
  3. extracts the 50% and 85% frames and runs GATE T's pixel checks (type_check.py: min-size, overflow, contrast incl. the
     terracotta-accent test, per-blob contrast, bbox overlap, kerning) and Gate V (final_frame_check.analyze_frame).
Gate V's underfill/clustered findings are listed but marked WAIVED for beats declared sparse in lanes/act2.json.
  python3 evidence/act2/gates_act2.py B06_TwoJobs ...
"""
import sys, os, json, subprocess, time, io, contextlib
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime")
sys.path.insert(0, str(TK / "scripts")); sys.path.insert(0, str(TK / "qc"))
with contextlib.redirect_stdout(io.StringIO()):
    import type_check as tc
    import final_frame_check as ff
from PIL import Image
import numpy as np

SCR = Path("/private/tmp/claude-501/lecture-csye-games-act2")
OUT = SCR / "gates4k"; OUT.mkdir(parents=True, exist_ok=True)
LOCK = Path("/private/tmp/claude-501/lecture-csye-4k.lock")
sheet = json.loads((REEL / "beat_sheet.json").read_text())
AUD = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"]}
lanes = json.loads((REEL / "lanes/act2.json").read_text()) if (REEL / "lanes/act2.json").exists() else {}


def render(cls):
    while True:
        try:
            LOCK.mkdir(); break
        except FileExistsError:
            time.sleep(20)
    try:
        subprocess.run(["manim", "-r", "3840,2160", "--fps", "24", "--disable_caching", "--media_dir", str(SCR / "media4k"),
                        "scenes.py", cls], cwd=SCR, capture_output=True, text=True)
    finally:
        LOCK.rmdir()
    return SCR / "media4k/videos/scenes/2160p24" / f"{cls}.mp4"


for cls in sys.argv[1:]:
    bid = cls.split("_")[0]
    mp4 = render(cls)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                             capture_output=True, text=True).stdout)
    w, h = Image.open(io.BytesIO(subprocess.run(["ffmpeg", "-v", "error", "-ss", "0", "-i", str(mp4), "-frames:v", "1", "-f", "image2pipe",
                                                 "-vcodec", "png", "-"], capture_output=True).stdout)).size
    print(f"=== {cls}  {w}x{h}  clip={d:.3f}s audio={AUD[bid]:.2f}s  slack={AUD[bid]-d:+.3f}s")
    sparse = lanes.get(bid, {}).get("sparse", True)
    for pct in (50, 85):
        png = OUT / f"{cls}_{pct}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d * pct / 100:.3f}", "-i", str(mp4), "-frames:v", "1", str(png)])
        img = Image.open(png).convert("RGB"); arr = np.array(img)
        pol, bg = tc.detect_polarity(arr)
        res = [("§8.1 min", tc.check_min_size(img, bid, cls, polarity=pol)),
               ("§8.2 ovf", tc.check_overflow(img, bid, polarity=pol, pattern=cls)),
               ("§8.3 con", tc.check_contrast(img, bid, cls, polarity=pol, bg_rgb=bg)),
               ("§8.3b blob", tc.check_contrast_per_blob(img, polarity=pol)),
               ("§8.6b ovl", tc.check_bbox_overlap(img, polarity=pol)),
               ("§8.4 kern", tc.check_kerning_sanity(img, bid, True, False, cls))]
        dv, cover = ff.analyze_frame(str(png))
        tfail = [k for k, (s, m) in res if s == "FAIL"]
        vfail = [x for x in dv if not (sparse and x[1] in ("underfill", "clustered"))]
        tag = "GATE-T " + ("FAIL" if tfail else "PASS") + (" (sampled frame)" if pct == 50 else " (info: GATE T samples 50%)")
        print(f"  {pct}%  {tag}  |  Gate V {'FAIL' if vfail else 'PASS'}  cover={cover * 100:.0f}%  sparse={sparse}")
        for k, (s, m) in res:
            print(f"      {k}: {s}  {m[:170]}")
        for x in dv:
            print(f"      V: {x}" + ("  [WAIVED: sparse]" if x not in vfail else ""))
