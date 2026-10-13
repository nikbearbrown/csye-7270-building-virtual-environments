#!/usr/bin/env python3
"""make_planning_stills.py: renders the key poses of this film's Godot captures as small planning stills (png/still-*.png) and a contact sheet.

These are PLANNING stills: 640 x 360, Forward+, rendered with runner-card.gd, a scratch copy of the series Lab runner with two additions
(a "card" texture and a --dot marker; nothing else changed). They let a reviewer LOOK at what each capture will show before anything is built;
the real captures are made at 4K by the build session (CAPTURE-PLAN.md). The shaders are the files in ../../lab-shaders/, unchanged.
Run:  python3 make_planning_stills.py
"""
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab"
WORK = Path("/private/tmp/claude-501/godot-shaders-matrices-and-fake-3d/lab-card")
PNG = HERE / "png"
WORK.mkdir(parents=True, exist_ok=True)
shutil.copy(LAB / "project.godot", WORK / "project.godot")
shutil.copy(HERE / "runner-card.gd", WORK / "runner.gd")
subprocess.run(["godot", "--headless", "--path", str(WORK), "--import"], capture_output=True)

CARD = ["--kind", "sprite", "--sprite-tex", "card", "--sprite-scale", "1.0"]
STILLS = [
    ("flip-0", "08-flip", CARD + ["--set", "flip=0.0"]),
    ("flip-0.125", "08-flip", CARD + ["--set", "flip=0.125"]),
    ("flip-0.25-edge-on", "08-flip", CARD + ["--set", "flip=0.25"]),
    ("flip-0.5-mirrored", "08-flip", CARD + ["--set", "flip=0.5"]),
    ("grow-1.5", "02-grow", CARD + ["--set", "grow=1.5"]),
    ("turn-0.7854", "03-turn", CARD + ["--set", "angle=0.7854"]),
    ("slide-100-0", "04-slide", CARD + ["--set", "slide=100,0"]),
    ("order-A-turn-then-slide", "05-turn-then-slide", CARD + ["--set", "angle=1.5708", "--set", "slide=100,0"]),
    ("order-B-slide-then-turn", "06-slide-then-turn", CARD + ["--set", "angle=1.5708", "--set", "slide=100,0"]),
    ("three-moves", "07-three-moves", CARD + ["--set", "grow=1.5", "--set", "angle=0.5236", "--set", "slide=100,-40"]),
    ("flip-and-tip", "09-flip-and-tip", CARD + ["--set", "flip=0.125", "--set", "tip=0.1"]),
    ("door-0.125-hinge-left", "11-door", CARD + ["--set", "flip=0.125", "--set", "pivot=-64,0", "--dot", "-64,0"]),
    ("door-0.5-far-side", "11-door", CARD + ["--set", "flip=0.5", "--set", "pivot=-64,0", "--dot", "-64,0"]),
    ("corner-0.7854", "10-spin-about-corner", CARD + ["--set", "angle=0.7854", "--set", "pivot=-64,-64", "--dot", "-64,-64"]),
    ("table-check-teal", "01-table-check", ["--kind", "rect"]),
]
tiles = []
for label, shader, args in STILLS:
    out = PNG / f"still-{label}.png"
    cmd = ["godot", "--path", str(WORK), "--script", "res://runner.gd", "--", "--shader", str(FILM / "lab-shaders" / f"{shader}.gdshader"), *args, "--png", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    ok = "RESULT" in r.stdout and '"ok":true' in r.stdout
    print(("ok  " if ok else "FAIL"), label)
    tiles.append((label, out))

W, H, COLS = 320, 180, 3
rows = (len(tiles) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * W, rows * (H + 22)), (250, 249, 245))
d = ImageDraw.Draw(sheet)
for i, (label, p) in enumerate(tiles):
    im = Image.open(p).convert("RGB").resize((W, H))
    x, y = (i % COLS) * W, (i // COLS) * (H + 22)
    sheet.paste(im, (x, y))
    d.text((x + 6, y + H + 4), label, fill=(61, 57, 41))
sheet.save(PNG / "contact-sheet-planning-stills.png")
print("wrote", PNG / "contact-sheet-planning-stills.png")
