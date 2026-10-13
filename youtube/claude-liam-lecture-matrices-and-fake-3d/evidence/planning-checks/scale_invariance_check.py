#!/usr/bin/env python3
"""scale_invariance_check.py: the 4K captures draw the card from a 1024 px texture (U = 8 times the 128 px card) so it stays crisp.
Every shader move is linear, so the picture must be the same if each pixel-valued uniform is multiplied by U and the node scale is divided by U.
This renders three shaders both ways with runner-card.gd (scratch copy of the Lab runner, same renderer) and compares bounding boxes. Run: python3 scale_invariance_check.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab"
WORK = Path("/private/tmp/claude-501/godot-shaders-matrices-and-fake-3d/lab-card")
WORK.mkdir(parents=True, exist_ok=True)
shutil.copy(LAB / "project.godot", WORK / "project.godot")
shutil.copy(HERE / "runner-card.gd", WORK / "runner.gd")
sys.path.insert(0, str(HERE))
import measure  # noqa: E402

U = 8
OUT = HERE / "png"
rows, bad = [], 0


def render(label, shader, n, scale, sets):
    png = OUT / f"scale-{label}.png"
    cmd = ["godot", "--path", str(WORK), "--script", "res://runner.gd", "--", "--shader", str(FILM / "lab-shaders" / shader), "--kind", "sprite", "--sprite-tex", "white",
           "--sprite-n", str(n), "--sprite-scale", str(scale)]
    for s in sets:
        cmd += ["--set", s]
    cmd += ["--png", str(png)]
    subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    return measure.measure(png)


cases = [
    ("three-moves", "07-three-moves.gdshader", ["grow=1.5", "angle=0.5236", "slide=100,-40"], ["grow=1.5", "angle=0.5236", f"slide={100 * U},{-40 * U}"]),
    ("door", "11-door.gdshader", ["flip=0.125", "pivot=-64,0"], ["flip=0.125", f"pivot={-64 * U},0"]),
    ("corner", "10-spin-about-corner.gdshader", ["angle=0.7854", "pivot=-64,-64"], ["angle=0.7854", f"pivot={-64 * U},{-64 * U}"]),
]
for label, shader, small, big in cases:
    a = render(f"{label}-128", shader, 128, 1.0, small)
    b = render(f"{label}-1024", shader, 128 * U, 1.0 / U, big)
    ok = all(abs(x - y) <= 1.01 for x, y in zip(a["bbox_edges_rel"], b["bbox_edges_rel"]))
    bad += not ok
    line = f"{'PASS' if ok else 'FAIL'}  {label}: 128 px card bbox {a['bbox_edges_rel']}, 1024 px card with uniforms x{U} and scale 1/{U}: {b['bbox_edges_rel']}"
    print(line)
    rows.append(line)
(HERE / "scale-invariance-summary.txt").write_text("\n".join(rows) + "\n")
sys.exit(1 if bad else 0)
