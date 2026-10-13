#!/usr/bin/env python3
"""gatet_probe.py - a local, free GATE T + Gate V pre-check for Act V's Manim beats (not the real gate: `art run/final` own that).
Renders each class at 1080p (never 4K) into a private scratch, grabs the frame GATE T samples (the clip midpoint) plus 25% and 95%,
and runs type_check.py's own pixel functions on the midpoint (min-size, overflow, contrast, per-blob contrast, bbox overlap, kerning).
  python3 evidence/act5/gatet_probe.py B41_PlanPrompt [B42_... ...]          (from the reel folder; one render at a time)"""
import subprocess, sys, json
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]
TK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art")
sys.path.insert(0, str(TK / "runtime/scripts"))
import type_check as tc
from PIL import Image
SCR = Path("/private/tmp/claude-501/lecture-a3assets-act5-probe")
SCR.mkdir(parents=True, exist_ok=True)
subprocess.run(["python3", str(REEL / "assemble_scenes.py"), "--out", str(SCR), "--acts", "5"], check=True, capture_output=True)
for name in ("beat_sheet.json",):
    (SCR / name).write_bytes((REEL / name).read_bytes())
for link in ("pantry", "evidence"):
    l = SCR / link
    if not l.exists():
        l.symlink_to(REEL / link)
for cls in sys.argv[1:]:
    r = subprocess.run(["manim", "-qh", "--frame_rate", "24", "--media_dir", str(SCR / "media"), "scenes.py", cls],
                       cwd=SCR, capture_output=True, text=True)
    pace = [l for l in (r.stdout + r.stderr).splitlines() if "[pace]" in l]
    mp4 = SCR / "media/videos/scenes/1080p24" / f"{cls}.mp4"
    if not mp4.exists():
        print(cls, "RENDER FAILED", (r.stderr or r.stdout)[-800:]); continue
    dur = tc.video_duration(mp4)
    for pct in (25, 50, 95):
        im = tc.extract_frame(mp4, t=min(dur * pct / 100, dur - 0.05))
        im.save(SCR / f"{cls}_{pct}.png")
    import numpy as np
    for tag, img in (("1080", Image.open(SCR / f"{cls}_50.png").convert("RGB")),
                     ("4K-emu", Image.open(SCR / f"{cls}_50.png").convert("RGB").resize((3840, 2160), Image.LANCZOS))):
        pol, bg = tc.detect_polarity(np.array(img))
        res = {
            "min-size": tc.check_min_size(img, cls, cls, polarity=pol),
            "overflow": tc.check_overflow(img, cls, polarity=pol, pattern=cls),
            "contrast": tc.check_contrast(img, cls, cls, polarity=pol, bg_rgb=bg),
            "contrast-local": tc.check_contrast_per_blob(img, polarity=pol),
            "bbox-overlap": tc.check_bbox_overlap(img, polarity=pol),
            "kerning": tc.check_kerning_sanity(img, cls, True, False, cls),
        }
        print(f"=== {cls} [{tag}]  dur={dur:.2f}s  {pace[-1].strip() if pace else ''}")
        for k, (st, msg) in res.items():
            print(f"  {st:5s} {k:15s} {msg[:230]}")
print("frames:", SCR)
