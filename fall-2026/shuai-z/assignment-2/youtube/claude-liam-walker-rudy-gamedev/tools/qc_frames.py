#!/usr/bin/env python3
"""Sample a rendered film for the frame-level visual QC: every beat at 15/50/85 %
of its span, tiled into contact sheets of 9 (3×3), labelled with beat id and time.

    python3 tools/qc_frames.py <film.mp4>
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
film = Path(sys.argv[1])
beats = json.loads((REEL / "beat_sheet.json").read_text())["beats"]
out = REEL / "_qc/frames"; out.mkdir(parents=True, exist_ok=True)
font = ImageFont.truetype("/Users/eric/csye7270/brutalist.art/runtime/fonts/Inter/static/Inter_28pt-Medium.ttf", 28)
t, shots = 0.0, []
for b in beats:
    d = b.get("render_duration_s") or b["actual_duration_s"]
    for frac in (0.15, 0.5, 0.85):
        ts = t + d * frac
        p = out / f"{b['beat_id']}-{int(frac * 100):02d}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ts:.3f}", "-i", str(film), "-frames:v", "1", "-vf", "scale=1280:720", str(p)], check=True)
        shots.append((p, f"{b['beat_id']} {int(frac * 100)}% @ {ts:.1f}s"))
    t += d
for k in range(0, len(shots), 9):
    sheet = Image.new("RGB", (3 * 1280, 3 * 760), (30, 27, 24))
    for j, (p, label) in enumerate(shots[k:k + 9]):
        im = Image.open(p)
        x, y = (j % 3) * 1280, (j // 3) * 760
        sheet.paste(im, (x, y))
        ImageDraw.Draw(sheet).text((x + 10, y + 724), label, font=font, fill=(255, 255, 255))
    sheet.save(REEL / f"_qc/sheet-{k // 9 + 1:02d}.jpg", quality=85)
print(f"{len(shots)} frames, {(len(shots) + 8) // 9} sheets, film {t:.2f} s")
