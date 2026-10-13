#!/usr/bin/env python3
"""make_crops.py — crops the real captures Act VI shows (read-only on the evidence; writes pantry/a6_*.png).
  python3 evidence/act6/make_crops.py"""
from PIL import Image
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]
EV = REEL.parent / "_conducting-series-evidence"
P = REEL / "pantry"; P.mkdir(exist_ok=True)
# B25: the folder names of the real public GitHub page (3840x2160 capture, 2026-10-09T18:03Z): the six folders asset-gen, docs, engines, legacy, prompts, scripts
im = Image.open(EV / "web-captures/github-walker.png").convert("RGB")
im.crop((460, 880, 1330, 1475)).save(P / "a6_github_list.png")
# B26: two real Godot frames of the Clawd game (1920x1080, scripted input, recorded 2026-10-09), copied unchanged
for src, dst in [("03-clawd-jumping-the-gap.png", "a6_frame_jump.png")]:
    Image.open(EV / "godot-captures/walker-claude" / src).convert("RGB").save(P / dst)
print("ok")
