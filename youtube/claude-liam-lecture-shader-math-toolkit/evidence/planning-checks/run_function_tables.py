#!/usr/bin/env python3
"""run_function_tables.py: probe every function the film names at exact inputs, in a real Godot 4.7.2 window (the Shader Lab).

Each row writes a five-band "table" shader into check-shaders/ and reads the five band centres. Outputs:
  function-tables.jsonl   one record per check: command, exit code, raw output, decoded values, expected, error
  function-tables.md      the readable table (expected against measured)
Run: python3 run_function_tables.py        (about a minute; the Lab runs one check at a time)
Observation rows (OBS-*) record behaviour the docs call "undefined"; they are NOT relied on by the film.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T  # noqa: E402

HERE = Path(__file__).resolve().parent
CS = HERE / "check-shaders"
CS.mkdir(exist_ok=True)
Q = [0.0, 0.25, 0.5, 0.75, 1.0]
X4 = [0.1, 0.3, 0.6, 0.9, 1.0]
NEG = [2.75, 0.75, 1.25, -0.25, -1.75]


def ss(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def fract(x):
    return x - math.floor(x)


def step(e, x):
    return 0.0 if x < e else 1.0


# name, xs, GLSL expr (uses float x), scale, offset, expected (python), note
ROWS = [
    ("step_edge_half", Q, "step(0.5, x)", 1, 0, [step(0.5, x) for x in Q], "x >= edge gives 1 (the equality case is x = 0.5)"),
    ("step_args_swapped", Q, "step(x, 0.5)", 1, 0, [step(x, 0.5) for x in Q], "swapped arguments: flips, but BOTH orders give 1 exactly at 0.5"),
    ("one_minus_step", Q, "1.0 - step(0.5, x)", 1, 0, [1 - step(0.5, x) for x in Q], "the exact flip"),
    ("smoothstep_25_75", Q, "smoothstep(0.25, 0.75, x)", 1, 0, [ss(0.25, 0.75, x) for x in Q], "S between the edges, 0.5 at the middle"),
    ("smoothstep_unit", Q, "smoothstep(0.0, 1.0, x)", 1, 0, [ss(0.0, 1.0, x) for x in Q], "3t^2 - 2t^3: 0.15625 at a quarter, 0.84375 at three quarters"),
    ("smoothstep_0_10_at_1", [0.5, 1.0, 1.0, 1.5, 1.0], "smoothstep(0.0, 10.0, x)", 15, 0, [ss(0.0, 10.0, x) for x in [0.5, 1.0, 1.0, 1.5, 1.0]],
     "THE CORRECTION: edges 0 and 10, input 1 -> 0.028, not 0.1 (output scaled by 15 to read four decimals)"),
    ("linear_clamp_0_10_at_1", [0.5, 1.0, 1.0, 1.5, 1.0], "clamp(x / 10.0, 0.0, 1.0)", 5, 0, [min(max(x / 10.0, 0), 1) for x in [0.5, 1.0, 1.0, 1.5, 1.0]],
     "what a straight line would say: 0.1"),
    ("mix_scalar", Q, "mix(0.2, 0.9, x)", 1, 0, [0.2 * (1 - x) + 0.9 * x for x in Q], "a at 0, b at 1, halfway at 0.5"),
    ("mix_extrapolates", [-1.0, 0.0, 0.5, 1.0, 2.0], "mix(0.2, 0.4, x)", 1, 0, [0.2 * (1 - x) + 0.4 * x for x in [-1.0, 0.0, 0.5, 1.0, 2.0]],
     "mix does not clamp its weight: weight 2 overshoots b (0.6), weight -1 undershoots a (0.0)"),
    ("clamp_range", Q, "clamp(x * 2.0 - 0.5, 0.0, 1.0)", 1, 0, [min(max(x * 2 - 0.5, 0), 1) for x in Q], "ramp that overshoots (-0.5 to 1.5) pinned to 0..1"),
    ("clamp_is_min_max", Q, "min(max(x * 2.0 - 0.5, 0.0), 1.0)", 1, 0, [min(max(x * 2 - 0.5, 0), 1) for x in Q], "docs: clamp = min(max(x, minVal), maxVal)"),
    ("min_half", Q, "min(x, 0.5)", 1, 0, [min(x, 0.5) for x in Q], "min picks the lower"),
    ("max_half", Q, "max(x, 0.5)", 1, 0, [max(x, 0.5) for x in Q], "max picks the higher"),
    ("abs_centered", Q, "abs(x * 2.0 - 1.0)", 1, 0, [abs(x * 2 - 1) for x in Q], "a ramp from -1 to 1 folded at zero: a V"),
    ("fract_x4", X4, "fract(x * 4.0)", 1, 0, [fract(x * 4) for x in X4], "four ramps in a row"),
    ("fract_negative", NEG, "fract(x)", 1, 0, [fract(x) for x in NEG], "docs: x - floor(x), so fract(-0.25) = 0.75"),
    ("floor_x4", X4, "floor(x * 4.0)", 1 / 6, 1 / 6, [math.floor(x * 4) for x in X4], "values 0,1,2,3 and 4 at x = 1 (encoded (v+1)/6)"),
    ("floor_negative", NEG[:2] + [-0.25, -1.75, 3.0], "floor(x)", 1 / 8, 3 / 8, [math.floor(x) for x in NEG[:2] + [-0.25, -1.75, 3.0]],
     "rounds toward minus infinity: floor(-0.25) = -1 (encoded (v+3)/8)"),
    ("floor_plus_fract", NEG, "floor(x) + fract(x)", 1 / 6, 3 / 6, NEG, "floor + fract gives x back, negatives too (encoded (v+3)/6)"),
    ("mod_one_negative", [-0.25, 0.25, 1.25, -1.25, 2.75], "mod(x, 1.0)", 1, 0, [fract(x) for x in [-0.25, 0.25, 1.25, -1.25, 2.75]],
     "THE TRAP: shader mod(-0.25, 1.0) = 0.75 (follows floor)"),
    ("mod_one_minus_fract", [-0.25, 0.25, 1.25, -1.25, 2.75], "mod(x, 1.0) - fract(x)", 1, 0.5, [0, 0, 0, 0, 0], "mod(x, 1.0) is fract(x) (offset 0.5: zero reads 0.5)"),
    ("mod_quarter", X4, "mod(x, 0.25)", 4, 0, [x - 0.25 * math.floor(x / 0.25) for x in X4], "repeats every 0.25, height 0.25 (scaled by 4)"),
    ("mod_formula", X4, "mod(x, 0.25) - (x - 0.25 * floor(x / 0.25))", 100, 0.5, [0, 0, 0, 0, 0], "docs formula x - y * floor(x/y) (offset 0.5: zero reads 0.5, gain 100)"),
    ("mod_is_y_times_fract", X4, "mod(x, 0.25) - 0.25 * fract(x / 0.25)", 100, 0.5, [0, 0, 0, 0, 0], "mod(x, y) = y * fract(x / y) (gain 100)"),
    ("length_3_4", [0, 0, 0, 0, 0], "length(vec2(3.0, 4.0)) - 5.0", 100, 0.5, [0, 0, 0, 0, 0], "length of (3, 4) is 5 (difference x100, zero reads 0.5)"),
    ("distance_to_middle", Q, "distance(vec2(x, 0.0), vec2(0.5, 0.5))", 1, 0, [math.hypot(x - 0.5, 0.5) for x in Q], "from the top edge: 0.7071 at the corners, 0.5 straight below the middle"),
    ("distance_corner_exact", [0, 0, 0, 0, 0], "distance(vec2(0.0, 0.0), vec2(0.5, 0.5)) - 0.70710678", 100, 0.5, [0, 0, 0, 0, 0], "corner to centre is sqrt(0.5) = 0.7071 (gain 100)"),
    ("normalize_length", [0, 0, 0, 0, 0], "length(normalize(vec2(3.0, 4.0))) - 1.0", 100, 0.5, [0, 0, 0, 0, 0], "normalize gives length 1 (gain 100)"),
    ("pow_3", [0.25, 0.5, 0.75, 1.0, 0.0], "pow(x, 3.0)", 1, 0, [x ** 3 for x in [0.25, 0.5, 0.75, 1.0, 0.0]], "power above 1 pulls a 0..1 ramp down"),
    ("pow_2", [0.25, 0.5, 0.75, 1.0, 0.0], "pow(x, 2.0)", 1, 0, [x ** 2 for x in [0.25, 0.5, 0.75, 1.0, 0.0]], ""),
    ("pow_half", [0.25, 0.5, 0.75, 1.0, 0.0], "pow(x, 0.5)", 1, 0, [x ** 0.5 for x in [0.25, 0.5, 0.75, 1.0, 0.0]], "power below 1 pushes it up"),
    ("pow_one", [0.25, 0.5, 0.75, 1.0, 0.0], "pow(x, 1.0)", 1, 0, [0.25, 0.5, 0.75, 1.0, 0.0], "power 1 changes nothing"),
    ("sine_squeezed", Q, "0.5 + 0.5 * sin(x * 6.28318530718)", 1, 0, [0.5 + 0.5 * math.sin(x * 2 * math.pi) for x in Q], "sine squeezed from -1..1 into 0..1"),
    ("sine_range_min", [0.75, 0.75, 0.75, 0.75, 0.75], "sin(x * 6.28318530718) + 1.0", 0.5, 0, [0, 0, 0, 0, 0], "sin(1.5 pi) = -1: the low end of the range (+1 shifts it to 0)"),
    ("ring_profile", [0.2, 0.3, 0.34, 0.38, 0.45], "step(0.3, x) - step(0.38, x)", 1, 0, [step(0.3, x) - step(0.38, x) for x in [0.2, 0.3, 0.34, 0.38, 0.45]],
     "one only from 0.3 up to (not including) 0.38"),
    ("disk_step", [0.2, 0.3, 0.34, 0.38, 0.45], "step(0.3, x)", 1, 0, [step(0.3, x) for x in [0.2, 0.3, 0.34, 0.38, 0.45]], "0 inside the radius, 1 from the radius outward"),
    ("disk_step_flipped", [0.2, 0.3, 0.34, 0.38, 0.45], "step(x, 0.3)", 1, 0, [step(x, 0.3) for x in [0.2, 0.3, 0.34, 0.38, 0.45]],
     "swapped: 1 inside (and exactly on) the radius"),
]

# Observations: behaviour the docs call undefined. Recorded, labelled, never relied on.
OBS = [
    ("OBS-smoothstep_reversed_edges", Q, "smoothstep(0.75, 0.25, x)", 1, 0, "docs: undefined if a >= b"),
    ("OBS-smoothstep_equal_edges", [0.25, 0.4999, 0.5, 0.5001, 0.75], "smoothstep(0.5, 0.5, x)", 1, 0, "docs: undefined if a >= b"),
    ("OBS-pow_negative_base", [-0.5, -0.25, 0.0, 0.25, 0.5], "pow(x, 2.0)", 1, 0, "docs: undefined if x < 0"),
    ("OBS-pow_zero_zero", [0.0, 0.0, 0.0, 0.0, 0.0], "pow(x, 0.0)", 1, 0, "docs: undefined if x == 0 and y <= 0"),
]


def main():
    log = []
    out_rows = []
    for name, xs, expr, scale, offset, expected, note in ROWS:
        path = CS / f"{name}.gdshader"
        T.table_shader(path, xs, expr, scale, offset)
        res = T.run_lab(path, ["--kind", "rect", "--size", "500x100"] + T.probes_arg([(c, 0.5) for c in T.BAND_CENTRES]), name, log)
        got = T.decode(res, scale, offset)
        tol = 0.75 / 255 / scale + 1e-6
        err = None if got is None else max(abs(g - e) for g, e in zip(got, expected))
        ok = got is not None and err <= tol
        out_rows.append({"name": name, "xs": xs, "expr": expr, "scale": scale, "offset": offset, "expected": [round(e, 5) for e in expected],
                         "measured": got, "max_error": None if err is None else round(err, 5), "tolerance": round(tol, 5), "pass": ok, "note": note,
                         "renderer": None if not res else res.get("renderer")})
        print(f"[{'ok' if ok else 'FAIL'}] {name}: expected {[round(e, 4) for e in expected]} measured {got}")
    for name, xs, expr, scale, offset, note in OBS:
        path = CS / f"{name}.gdshader"
        T.table_shader(path, xs, expr, scale, offset)
        res = T.run_lab(path, ["--kind", "rect", "--size", "500x100"] + T.probes_arg([(c, 0.5) for c in T.BAND_CENTRES]), name, log)
        got = T.decode(res, scale, offset)
        out_rows.append({"name": name, "xs": xs, "expr": expr, "scale": scale, "offset": offset, "expected": "undefined per docs", "measured": got,
                         "max_error": None, "tolerance": None, "pass": None, "note": note + " (observation only, not relied on)",
                         "renderer": None if not res else res.get("renderer")})
        print(f"[obs] {name}: measured {got}")
    (HERE / "function-tables.jsonl").write_text("\n".join(json.dumps({"row": r}) for r in out_rows) + "\n")
    (HERE / "function-tables-raw-log.jsonl").write_text("\n".join(json.dumps(r) for r in log) + "\n")
    md = ["| check | x values | expression | expected | measured | max error | result |", "|---|---|---|---|---|---|---|"]
    for r in out_rows:
        res = "obs" if r["pass"] is None else ("PASS" if r["pass"] else "FAIL")
        exp = r["expected"] if isinstance(r["expected"], str) else [round(e, 4) for e in r["expected"]]
        md.append(f"| {r['name']} | {[round(float(x), 4) for x in r['xs']]} | `{r['expr']}` | {exp} | {r['measured']} | {r['max_error']} | {res} |")
    (HERE / "function-tables.md").write_text("\n".join(md) + "\n")
    bad = [r["name"] for r in out_rows if r["pass"] is False]
    print("FAILED:", bad if bad else "none")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
