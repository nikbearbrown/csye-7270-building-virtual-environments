#!/usr/bin/env python3
"""run_extra_checks.py: a few more exact probes in a real Godot 4.7.2 window (Shader Lab): the mix overshoot (weight 2), the re-centred ramp, the five
distances drawn in the film, and the normalized (3, 4). Writes extra-checks.md / extra-checks.jsonl."""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_tools as T  # noqa: E402

HERE = Path(__file__).resolve().parent
CS = HERE / "check-shaders"
CS.mkdir(exist_ok=True)
log, out = [], []


def run_table(name, xs, expr, scale, offset, expected, note):
    path = CS / f"{name}.gdshader"
    T.table_shader(path, xs, expr, scale, offset)
    res = T.run_lab(path, ["--kind", "rect", "--size", "500x100"] + T.probes_arg([(c, 0.5) for c in T.BAND_CENTRES]), name, log)
    got = T.decode(res, scale, offset)
    tol = 0.75 / 255 / scale + 1e-6
    err = None if got is None else max(abs(g - e) for g, e in zip(got, expected))
    ok = got is not None and err <= tol
    out.append({"name": name, "expr": expr, "xs": xs, "expected": [round(e, 4) for e in expected], "measured": got, "max_error": None if err is None else round(err, 5),
                "pass": ok, "note": note})
    print(f"[{'ok' if ok else 'FAIL'}] {name}: expected {[round(e, 4) for e in expected]} measured {got}")


# 1. mix does not pin its weight: weight 2 overshoots the end (encoded (v + 1) / 4: values from -1 to 3 fit)
xs = [-1.0, 0.0, 1.0, 2.0, 3.0]
run_table("mix_overshoot", xs, "mix(0.2, 0.9, x)", 0.25, 0.25, [0.2 * (1 - x) + 0.9 * x for x in xs],
          "mix(0.2, 0.9, w): w = 2 gives 1.6 (past the end 0.9), w = -1 gives -0.5 (before the start)")
# 2. the re-centred ramp (encoded (v + 1) / 2)
Q = [0.0, 0.25, 0.5, 0.75, 1.0]
run_table("recentre", Q, "x * 2.0 - 1.0", 0.5, 0.5, [x * 2 - 1 for x in Q], "x * 2 - 1 runs from -1 to 1 with zero in the middle")
# 3. the five distances drawn in B28 (custom shader: five bands, each a point p; value = distance(p, middle))
pts = [(0.9, 0.5), (0.5, 0.2), (0.15, 0.85), (0.95, 0.95), (0.55, 0.55)]
picks = " else ".join(f"if (k == {i}) {{ p = vec2({a!r}, {b!r}); }}" for i, (a, b) in enumerate(pts))
code = f"""shader_type canvas_item;

void fragment() {{
	int k = min(int(floor(UV.x * 5.0)), 4);
	vec2 p = vec2(0.0);
	{picks}
	COLOR = vec4(vec3(distance(p, vec2(0.5))), 1.0);
}}
"""
(CS / "distance_samples.gdshader").write_text(code)
res = T.run_lab(CS / "distance_samples.gdshader", ["--kind", "rect", "--size", "500x100"] + T.probes_arg([(c, 0.5) for c in T.BAND_CENTRES]), "distance_samples", log)
got = T.decode(res)
exp = [math.hypot(a - 0.5, b - 0.5) for a, b in pts]
ok = got is not None and max(abs(g - e) for g, e in zip(got, exp)) <= 0.75 / 255 + 1e-6
out.append({"name": "distance_samples", "expr": "distance(p, vec2(0.5)) for p in " + str(pts), "expected": [round(e, 4) for e in exp], "measured": got, "pass": ok,
            "note": "the five numbers drawn in B28 (0.40, 0.30, 0.49, 0.64, 0.07 when rounded to two places)"})
print(f"[{'ok' if ok else 'FAIL'}] distance_samples: expected {[round(e, 4) for e in exp]} measured {got}")
# 4. normalize(vec2(3, 4)) = (0.6, 0.8): read red and green of one pixel
(CS / "normalize_xy.gdshader").write_text("shader_type canvas_item;\n\nvoid fragment() {\n\tCOLOR = vec4(normalize(vec2(3.0, 4.0)), 0.0, 1.0);\n}\n")
res = T.run_lab(CS / "normalize_xy.gdshader", ["--kind", "rect", "--size", "100x100", "--probe", "0.5,0.5"], "normalize_xy", log)
rgba = res["probes"][0]["rgba"] if res and res.get("ok") else None
ok = rgba is not None and abs(rgba[0] - 0.6) < 0.004 and abs(rgba[1] - 0.8) < 0.004
out.append({"name": "normalize_xy", "expr": "normalize(vec2(3.0, 4.0))", "expected": [0.6, 0.8], "measured": None if rgba is None else rgba[:2], "pass": ok,
            "note": "red = x = 0.6, green = y = 0.8"})
print(f"[{'ok' if ok else 'FAIL'}] normalize_xy: measured {None if rgba is None else rgba[:2]}")
(HERE / "extra-checks.jsonl").write_text("\n".join(json.dumps(r) for r in out) + "\n")
(HERE / "extra-checks-raw-log.jsonl").write_text("\n".join(json.dumps(r) for r in log) + "\n")
md = ["| check | expression | expected | measured | result |", "|---|---|---|---|---|"]
for r in out:
    md.append(f"| {r['name']} | `{r['expr']}` | {r['expected']} | {r['measured']} | {'PASS' if r['pass'] else 'FAIL'} |")
(HERE / "extra-checks.md").write_text("\n".join(md) + "\n")
