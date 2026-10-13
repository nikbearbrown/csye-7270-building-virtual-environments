#!/usr/bin/env python3
"""run_lab_checks.py: re-runs every shader this film SHOWS (lab-shaders/*.gdshader) through the Shader Lab (a real Godot 4.7.2 window, Forward+)
with the uniform values the captures will use, and records pixel probes. The CAPTURE-PLAN's "verified result to reproduce" column comes from here.
Strips use the Lab's default 640x360 rect; the round pictures use a 360x360 rect (UV 0..1 maps to a square, so circles stay round).
Output: lab-results.jsonl (one record per run: command, exit code, RESULT), lab-summary.txt (readable), png/*.png.
Run: python3 run_lab_checks.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T  # noqa: E402

HERE = Path(__file__).resolve().parent
SH = T.FILM / "lab-shaders"
PNG = HERE / "png"
PNG.mkdir(exist_ok=True)
STRIP = ["--kind", "rect"]
SQ = ["--kind", "rect", "--size", "360x360"]
log = []
summary = []


def run(label, shader, base, sets, probes):
    args = list(base)
    for s in sets:
        args += ["--set", s]
    args += T.probes_arg(probes) + ["--png", PNG / f"{label}.png"]
    res = T.run_lab(SH / shader, args, label, log)
    ok = bool(res and res.get("ok"))
    pr = [] if not ok else [(p["at"], [round(v, 4) for v in p["rgba"][:3]]) for p in res["probes"]]
    summary.append(f"{label} | {shader} {' '.join(sets)} | {'ok' if ok else 'ERROR'} | {pr}")
    print(summary[-1])


# strips (x probes along the middle row)
run("01-ramp", "01-ramp.gdshader", STRIP, [], [(0.02, 0.5), (0.5, 0.5), (0.98, 0.5)])
for e in (0.2, 0.5, 0.8):
    run(f"02-step-edge{e}", "02-step.gdshader", STRIP, [f"edge={e}"], [(e - 0.05, 0.5), (e + 0.05, 0.5)])
for w in (0.45, 0.3, 0.03):
    run(f"03-smoothstep-width{w}", "03-smoothstep.gdshader", STRIP, [f"width={w}"], [(0.25, 0.5), (0.5, 0.5), (0.75, 0.5)])
run("04-mix-colors", "04-mix-colors.gdshader", STRIP, [], [(0.02, 0.5), (0.5, 0.5), (0.98, 0.5)])
for c in (1, 4, 6):
    run(f"05-fract-count{c}", "05-fract.gdshader", STRIP, [f"count={c}"], [(0.1, 0.5), (0.3, 0.5), (0.6, 0.5), (0.9, 0.5)])
run("06-stripes", "06-stripes.gdshader", STRIP, [], [(0.05, 0.5), (0.1, 0.5), (0.15, 0.5), (0.2, 0.5)])
for p in (1, 3, 6):
    run(f"07-pow-power{p}", "07-pow.gdshader", STRIP, [f"power={p}"], [(0.5, 0.5), (0.9, 0.5)])
# round pictures: probes along the middle row (y = 0.5): x = 0.5 + d
run("08-distance", "08-distance.gdshader", SQ, [], [(0.5, 0.5), (0.75, 0.5), (0.999, 0.5), (0.001, 0.001)])
run("09-glow", "09-glow.gdshader", SQ, [], [(0.5, 0.5), (0.75, 0.5), (0.999, 0.5), (0.001, 0.001)])
run("10-disk", "10-disk.gdshader", SQ, [], [(0.5, 0.5), (0.7, 0.5), (0.9, 0.5), (0.001, 0.001)])
run("11-disk-flip", "11-disk-flip.gdshader", SQ, [], [(0.5, 0.5), (0.7, 0.5), (0.9, 0.5), (0.001, 0.001)])
ring_pts = [(0.7, 0.5), (0.84, 0.5), (0.95, 0.5)]
run("12-ring-hard", "12-ring-hard.gdshader", SQ, [], ring_pts)
run("13-ring-color", "13-ring-color.gdshader", SQ, [], ring_pts)
run("14-ring-soft", "14-ring-soft.gdshader", SQ, [], [(0.7, 0.5), (0.78, 0.5), (0.84, 0.5), (0.9, 0.5), (0.95, 0.5)])
for r in (0.12, 0.3, 0.38):
    run(f"15-ring-final-radius{r}", "15-ring-final.gdshader", SQ, [f"radius={r}"],
        [(0.5 + r - 0.06, 0.5), (0.5 + r + 0.04, 0.5), (min(0.5 + r + 0.2, 0.999), 0.5)])

(HERE / "lab-results.jsonl").write_text("\n".join(json.dumps(r) for r in log) + "\n")
(HERE / "lab-summary.txt").write_text("\n".join(summary) + "\n")
errors = [r["check"] for r in log if r["exit"] != 0]
print("runs:", len(log), "errors:", errors if errors else "none")
