#!/usr/bin/env python3
"""make_a4_pantry.py — B29's moving picture: 12 real frames (10 per second, clip time 2.0-3.2 s) of the REAL Godot capture
walker-claude-jumpman-gameplay.mp4 (scripted input, recorded 2026-10-09), cropped to x 380-1500, y 330-860 (sky, the 'MIND THE GAP'
sign and Clawd in the air; no ground, no HUD). Written to pantry/a4_g00.png .. a4_g11.png.   python3 evidence/act4/make_a4_pantry.py
"""
import subprocess, pathlib, tempfile
from PIL import Image
REEL = pathlib.Path(__file__).resolve().parents[2]
V = REEL.parent / "_conducting-series-evidence/godot-captures/walker-claude/walker-claude-jumpman-gameplay.mp4"
with tempfile.TemporaryDirectory() as td:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "2.0", "-t", "1.2", "-i", str(V), "-vf", "fps=10", f"{td}/f%02d.png"], check=True)
    for i in range(12):
        Image.open(f"{td}/f{i + 1:02d}.png").convert("RGB").crop((380, 330, 1500, 860)).save(REEL / f"pantry/a4_g{i:02d}.png")
print("wrote 12 frames")
