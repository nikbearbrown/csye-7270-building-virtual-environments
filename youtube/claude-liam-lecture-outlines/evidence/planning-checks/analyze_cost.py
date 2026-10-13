#!/usr/bin/env python3
"""analyze_cost.py: reads the wall-clock stress-test logs (run-g-verify_g_cost.log from the full suite, plus run-g-repeat-*.log from run_cost_repeats.sh) and writes cost-summary.txt:
for every valid run the median ms per frame of each variant, then the median over the valid runs with the range, and a straight-line fit through the constant-bound loops.
A run in which the window stopped drawing (a variant with one round under 7.0 ms next to a round over 9.0 ms: the idle frame time is about 6.9 ms) is listed as INVALID and left out."""
import json
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
logs = [HERE / "run-g-verify_g_cost.log"] + sorted(HERE.glob("run-g-repeat-*.log"))
runs = []          # (name, env, g1, {variant: (reads, [rounds])})
invalid = []
for lg in logs:
    if not lg.exists():
        continue
    env, g1, rows = {}, None, {}
    for line in lg.read_text().splitlines():
        if not line.startswith("RESULT "):
            continue
        d = json.loads(line[7:])
        if d.get("id") == "env": env = d
        if d.get("id") == "G1-gpu-timer": g1 = d
        if d.get("id") == "G2-wallclock": rows[d["variant"]] = (d["reads_per_pixel"], d["median_ms_per_frame_by_round"])
    stalled = [v for v, (_, r) in rows.items() if min(r) < 7.0 and max(r) > 9.0]
    if not rows or stalled:
        invalid.append((lg.name, stalled))
        continue
    runs.append((lg.name, env, g1, rows))
L = []
def say(s=""):
    print(s); L.append(s)
if not runs:
    msg = "INVALID: no valid stress-test run (the window stopped drawing in: " + "; ".join(f"{n}: {', '.join(s)}" for n, s in invalid) + "). Repeat ./run_scratch_checks.sh g with nothing covering the Godot window."
    (HERE / "cost-summary.txt").write_text(msg + "\n")
    raise SystemExit(msg)
env, g1 = runs[0][1], runs[0][2]
say(f"stress test: {env.get('render_targets_per_frame')} render targets of {env.get('viewport')} per frame ({env.get('render_targets_per_frame', 0) * env.get('viewport', [0])[0] ** 2 / 1e6:.0f} million pixels shaded per frame), "
    f"vsync off, {env.get('adapter')}, {env.get('renderer')}, Godot {env.get('engine')}; wall-clock, three rounds per run, median of the rounds per run")
say(f"G1 graphics-card timer: {g1['samples']} samples, maximum {g1['max_ms']} ms  ->  {'unavailable on this setup' if g1['max_ms'] == 0 else 'readable'}")
say(f"valid runs: {len(runs)} ({', '.join(r[0] for r in runs)})" + (f"; INVALID and left out: {', '.join(n for n, _ in invalid)}" if invalid else ""))
say("")
variants = list(runs[0][3].keys())
say(f"{'variant':52s} {'reads':>5s}  " + "  ".join(f"run {i + 1:<2d}" for i in range(len(runs))) + "   median   range")
cross = {}
for v in variants:
    meds = [float(np.median(r[3][v][1])) for r in runs]
    cross[v] = (runs[0][3][v][0], float(np.median(meds)), min(meds), max(meds))
    say(f"{v:52s} {runs[0][3][v][0]:5d}  " + "  ".join(f"{m:6.2f}" for m in meds) + f"   {np.median(meds):6.2f}   {min(meds):.2f} to {max(meds):.2f}")
const = sorted((cross[v][0], cross[v][1]) for v in variants if "constant bounds" in v or v.startswith("08-loop"))
x = np.array([c[0] for c in const if c[0] >= 26]); y = np.array([c[1] for c in const if c[0] >= 26])
slope, icpt = np.polyfit(x, y, 1)
say("")
say(f"constant-bound loops with 26 or more reads, median of runs: time = {slope:.3f} ms per read + {icpt:.1f} ms  (reads {[int(t) for t in x]} -> {[round(float(t), 1) for t in y]})")
say("below about 26 reads the frame sits close to the no-shader floor (7.5 ms here, 8.3 ms in two earlier runs), so those points show little of the cost; run to run the absolute times move by a few percent with what else the Mac is doing.")
(HERE / "cost-summary.txt").write_text("\n".join(L) + "\n")
