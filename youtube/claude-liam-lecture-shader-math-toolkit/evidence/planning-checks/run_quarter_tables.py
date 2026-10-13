#!/usr/bin/env python3
"""run_quarter_tables.py: every function of the film, one tiny shader each, probed at the five standard inputs x = 0, 0.25, 0.5, 0.75, 1.0
(the brief's requested record). Real Godot 4.7.2 window (Shader Lab), Forward+. Writes quarter-tables.md / quarter-tables.jsonl.
The expected values are computed here in Python from the docs' definitions (step: b < a ? 0 : 1; smoothstep: clamp then t*t*(3-2t); mix: a(1-c)+bc;
fract: x - floor(x); mod: x - y*floor(x/y); clamp: min(max(x, lo), hi); and so on)."""
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


def ss(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def fl(x):
    return math.floor(x)


def fr(x):
    return x - math.floor(x)


# name, glsl expression of float x, python function of x, encoding scale, offset
ROWS = [
    ("step", "step(0.5, x)", lambda x: 0.0 if x < 0.5 else 1.0, 1, 0),
    ("smoothstep", "smoothstep(0.25, 0.75, x)", lambda x: ss(0.25, 0.75, x), 1, 0),
    ("mix", "mix(0.2, 0.9, x)", lambda x: 0.2 * (1 - x) + 0.9 * x, 1, 0),
    ("clamp", "clamp(x * 2.0 - 0.5, 0.0, 1.0)", lambda x: min(max(x * 2 - 0.5, 0.0), 1.0), 1, 0),
    ("min", "min(x, 0.5)", lambda x: min(x, 0.5), 1, 0),
    ("max", "max(x, 0.5)", lambda x: max(x, 0.5), 1, 0),
    ("abs", "abs(x * 2.0 - 1.0)", lambda x: abs(x * 2 - 1), 1, 0),
    ("fract", "fract(x * 3.0)", lambda x: fr(x * 3), 1, 0),
    ("floor", "floor(x * 3.0)", lambda x: fl(x * 3), 0.25, 0),
    ("mod", "mod(x, 0.4)", lambda x: x - 0.4 * math.floor(x / 0.4), 1, 0),
    ("pow", "pow(x, 3.0)", lambda x: x ** 3, 1, 0),
    ("length", "length(vec2(x, 0.5))", lambda x: math.hypot(x, 0.5), 0.8, 0),
    ("distance", "distance(vec2(x, 0.0), vec2(0.5, 0.5))", lambda x: math.hypot(x - 0.5, 0.5), 1, 0),
    ("normalize", "normalize(vec2(x, 1.0)).x", lambda x: x / math.hypot(x, 1.0), 1, 0),
    ("sin", "0.5 + 0.5 * sin(x * 6.28318530718)", lambda x: 0.5 + 0.5 * math.sin(x * 2 * math.pi), 1, 0),
]
log, out = [], []
for name, expr, fn, scale, offset in ROWS:
    path = CS / f"quarter_{name}.gdshader"
    T.table_shader(path, Q, expr, scale, offset)
    res = T.run_lab(path, ["--kind", "rect", "--size", "500x100"] + T.probes_arg([(c, 0.5) for c in T.BAND_CENTRES]), f"quarter_{name}", log)
    got = T.decode(res, scale, offset)
    exp = [fn(x) for x in Q]
    tol = 0.75 / 255 / scale + 1e-6
    err = None if got is None else max(abs(g - e) for g, e in zip(got, exp))
    ok = got is not None and err <= tol
    out.append({"function": name, "glsl": expr, "x": Q, "expected": [round(e, 4) for e in exp], "measured": got, "max_error": None if err is None else round(err, 5), "pass": ok,
                "renderer": None if not res else res.get("renderer")})
    print(f"[{'ok' if ok else 'FAIL'}] {name}: expected {[round(e, 4) for e in exp]} measured {got}")
(HERE / "quarter-tables.jsonl").write_text("\n".join(json.dumps(r) for r in out) + "\n")
(HERE / "quarter-tables-raw-log.jsonl").write_text("\n".join(json.dumps(r) for r in log) + "\n")
md = ["| function | GLSL (x is the input) | x = 0, 0.25, 0.5, 0.75, 1.0: expected | measured | result |", "|---|---|---|---|---|"]
for r in out:
    md.append(f"| {r['function']} | `{r['glsl']}` | {r['expected']} | {r['measured']} | {'PASS' if r['pass'] else 'FAIL'} |")
(HERE / "quarter-tables.md").write_text("\n".join(md) + "\n")
