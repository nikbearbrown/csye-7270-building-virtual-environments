#!/usr/bin/env python3
"""run-calc.py: runs calc/calc-values.gdshader in the Shader Lab and decodes every cell (value = 4 * red - 1).
Writes calc-results.txt next to this file. Expected values are written here, before the run, from hand arithmetic; the run is the check."""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab" / "check_shader.sh"
SHADER = HERE / "calc" / "calc-values.gdshader"
CELLS = [  # (index, what, expected)
    (0, "distance((0.62, 0.66), (0.5, 0.5)) equals 0.2 within 1e-6", 1),
    (1, "step(0.3, 0.2)   edge 0.3, x 0.2 (x below the edge)", 0),
    (2, "step(0.2, 0.3)   edge 0.2, x 0.3 (x above the edge)", 1),
    (3, "step(0.3, 0.3)   x equal to the edge", 1),
    (4, "step(0.4, 0.3)", 0),
    (5, "distance(a, b) equals length(a - b) within 1e-6", 1),
    (6, "ring at distance 0.20: outer 1 - inner 1", 0),
    (7, "ring at distance 0.33: outer 1 - inner 0", 1),
    (8, "ring at distance 0.45: outer 0 - inner 0", 0),
    (9, "a + b - hole for (1, 0, 0)", 1),
    (10, "a + b - hole for (1, 1, 0)  (the overlap)", 2),
    (11, "a + b - hole for (1, 1, 1)  (the overlap, in the hole)", 1),
    (12, "min(a + b, 1) - hole for (1, 1, 0)", 1),
    (13, "min(a + b, 1) - hole for (1, 1, 1)", 0),
    (14, "0 - 1 (a bite cut where no disc was drawn)", -1),
    (15, "0 - 1 + 1 (then a spot added)", 0),
    (16, "max(0 - 1, 0) + 1 (max first, then the spot)", 1),
    (17, "min(2, 1)", 1),
    (18, "max(-1, 0)", 0),
    (19, "1 * 1", 1),
    (20, "1 * 0", 0),
    (21, "max(1, 1)  (cross centre, union)", 1),
    (22, "1 - 1  (not, applied to a one)", 0),
    (23, "max(1 - 1, 0)", 0),
]
N = 24
def main():
    cmd = [str(LAB), str(SHADER), "--kind", "rect", "--size", "480x48"]
    for i, _, _ in CELLS:
        cmd += ["--probe", f"{(i + 0.5) / N:.5f},0.5"]
    cmd += ["--png", str(HERE / "png" / "calc-values.png")]
    p = subprocess.run(cmd, capture_output=True, text=True)
    line = next((l for l in p.stdout.splitlines() if l.startswith("RESULT ")), "")
    out = ["calc-values.gdshader, Shader Lab, 480 x 48 view; value = 4 * red - 1\n", f"exit code {p.returncode}\n"]
    if not line:
        out.append("NO RESULT\n" + p.stdout + p.stderr)
        (HERE / "calc-results.txt").write_text("".join(out)); print("".join(out)); return 1
    d = json.loads(line[7:])
    out.append(f"engine {d['engine']}, renderer {d['renderer']}, size {d['size']}\n")
    bad = 0
    for (i, what, want), pr in zip(CELLS, d["probes"]):
        r = pr["rgba"][0]
        got = 4 * r - 1
        ok = abs(got - want) < 0.05
        bad += not ok
        out.append(f"cell {i:2d}  want {want:>2}  got {got:+.3f}  {'OK ' if ok else 'BAD'}  {what}\n")
    out.append(f"\n{len(CELLS) - bad} of {len(CELLS)} cells as expected\n")
    (HERE / "calc-results.txt").write_text("".join(out)); print("".join(out))
    return 1 if bad else 0
if __name__ == "__main__":
    sys.exit(main())
