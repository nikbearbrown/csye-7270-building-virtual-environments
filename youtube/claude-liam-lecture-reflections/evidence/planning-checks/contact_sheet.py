#!/usr/bin/env python3
"""contact_sheet.py <frames dir> <out png>: one row per capture, its 50 % and 85 % frames (the ones Gate V samples) side by side.
Frames come from run-all.sh (scene_runner.gd --out). Planning evidence only: not film assets."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

src, out = Path(sys.argv[1]), Path(sys.argv[2])
rows = {}
for p in sorted(src.glob("C*-t*.png")):
    cid = p.name.split("-")[0]
    rows.setdefault(cid, []).append(p)
W, H = 480, 270
sheet = Image.new("RGB", (W * 2 + 130, (H + 8) * len(rows)), "#F2F0E9")
d = ImageDraw.Draw(sheet)
y = 0
for cid, files in rows.items():
    # pick the frames nearest to 50 % and 85 % by their time stamp: the runner names them C08-t07.25.png etc.; use the 2nd and 3rd from the end
    picks = files[-2:] if len(files) >= 2 else files
    d.text((8, y + H // 2 - 6), cid, fill="#3D3929")
    for i, f in enumerate(picks):
        im = Image.open(f).convert("RGB").resize((W, H))
        sheet.paste(im, (130 + i * W, y))
    y += H + 8
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out, optimize=True)
print("wrote", out, sheet.size, len(rows), "captures")
