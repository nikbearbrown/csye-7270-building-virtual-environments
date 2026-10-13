#!/usr/bin/env python3
"""make_assets_act3.py — builds every image Act III shows into REEL/pantry/ (prefix a3_). Re-runnable; read-only on the sources.
Sources (all real Godot output, never redrawn):
  S  = /Users/bear/Documents/CoWork/bear-textbooks/books/walker/games/walker-jumpman/evidence/screens/   (the starter's own rendered-viewport screenshots, 1280x720)
  G  = EVID/godot-captures/walker-claude/   (Clawd in the same level, Godot 4.7.2 Movie Maker, 1920x1080)
  C4 = walker-jumpman-clawd/youtube/claude-liam-walker-jumpman-clawd-walkthrough/capture/controls.mp4  (native 3840x2160, scripted input; the left-boundary take)
"""
import subprocess, sys
from pathlib import Path
from PIL import Image
REEL = Path(__file__).resolve().parents[2]
PAN = REEL / "pantry"; PAN.mkdir(exist_ok=True)
BOOKS = Path("/Users/bear/Documents/CoWork/bear-textbooks/books")
S = BOOKS / "walker/games/walker-jumpman/evidence/screens"
G = BOOKS / "csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude"
C4 = BOOKS / "walker-jumpman-clawd/youtube/claude-liam-walker-jumpman-clawd-walkthrough/capture/controls.mp4"

# B16: the starter's own gameplay screenshot (the jump over the gap), whole. (Its menu screen carries a grey overlay that fails Gate V's
# ink/background separation at 4K, so the menu is not used.)
Image.open(S / "03-jump.png").convert("RGB").save(PAN / "a3_starter_jump_full.png")
# B19: the same level strip (y 240..1005 of a 1080 frame) from the starter's jump and from Clawd's jump
a = Image.open(S / "03-jump.png").convert("RGB")           # 1280x720: strip y 160..670
a.crop((0, 160, 1280, 670)).save(PAN / "a3_starter_jump.png")
b = Image.open(G / "03-clawd-jumping-the-gap.png").convert("RGB")   # 1920x1080: strip y 240..1005
b.crop((0, 240, 1920, 1005)).save(PAN / "a3_clawd_jump.png")
# B22: native-4K frames 44..72 of the controls take (Clawd runs left to the world's edge and stops), cropped to the bottom-left
# corner: x 0..1500, y 1400..2020 (4K px) = the 01 / GET MOVING corner of the level (a3_edgeb_NNN.png)
tmp = REEL / "evidence/act3/_frames"; tmp.mkdir(exist_ok=True)
for n in range(44, 66):
    out = tmp / f"c{n:03d}.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(C4), "-vf", f"select=eq(n\\,{n})", "-frames:v", "1", str(out)], check=True)
    Image.open(out).convert("RGB").crop((0, 1400, 1500, 2020)).save(PAN / f"a3_edgeb_{n:03d}.png")
print("ok", sorted(p.name for p in PAN.glob("a3_*"))[:6], "...")
