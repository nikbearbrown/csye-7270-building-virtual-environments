#!/usr/bin/env python3
"""Storyboard panel (left) next to the same moment captured from the game (right), one row per panel.
Inputs: evidence/storyboard-png/panel-NN.png (godot/tests/rasterize_storyboard.gd) and
evidence/screens/sb-PN.png (godot/tests/capture.gd).   Output: design/storyboard/storyboard-vs-game.png"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
W, H = 480, 270
rows = []
for n in range(1, 10):
    panel = ROOT / f"evidence/storyboard-png/panel-{n:02d}.png"
    shot = ROOT / f"evidence/screens/sb-P{n}.png"
    rows.append((n, Image.open(panel).convert("RGB").resize((W, H)), Image.open(shot).convert("RGB").resize((W, H))))
out = Image.new("RGB", (W * 2 + 30, len(rows) * (H + 24)), "#0E1020")
d = ImageDraw.Draw(out)
for i, (n, p, s) in enumerate(rows):
    y = i * (H + 24)
    d.text((10, y + 4), f"P{n}  storyboard (design-v1)", fill="#FFF1C9")
    d.text((W + 20, y + 4), f"P{n}  game capture", fill="#FFF1C9")
    out.paste(p, (10, y + 20))
    out.paste(s, (W + 20, y + 20))
dest = ROOT / "design/storyboard/storyboard-vs-game.png"
out.save(dest, optimize=True)
print(dest)
