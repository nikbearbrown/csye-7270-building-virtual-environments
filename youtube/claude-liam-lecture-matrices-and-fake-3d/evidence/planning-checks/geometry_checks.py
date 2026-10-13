#!/usr/bin/env python3
"""geometry_checks.py: every Shader Lab run behind the numbers in FACTCHECK.md, with the expected value derived independently in Python.

Run:  python3 geometry_checks.py
It calls ../../../_godot-shaders-series/lab/check_shader.sh (real Godot 4.7.2, Forward+ unless a run says otherwise) once per check, saves
each frame under png/, and writes
    lab-results.jsonl     one line per run: the command, its exit code, and the RESULT line the Lab printed
    geometry-summary.txt  one PASS / FAIL line per check: what was measured, what the maths predicts
Nothing is hand-edited. A FAIL is a real disagreement between Godot and the maths and stops the claim that depends on it.
Sprites are 128 px white squares at scale 1.0 on the Lab's stage colour (#D9D5CA); measure.py turns a frame into bounding boxes and centroids.
"""
import datetime
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab"
SH = FILM / "lab-shaders"
UT = HERE / "shaders"
PNG = HERE / "png"
PNG.mkdir(exist_ok=True)
sys.path.insert(0, str(HERE))
import measure  # noqa: E402

TAU = 2 * math.pi
LOG, SUMMARY = [], []
WHITE = ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "1.0"]
CORNERS = [(-64, -64), (64, -64), (64, 64), (-64, 64)]


def lab(label, shader, *args, folder=SH):
    png = PNG / f"{label}.png"
    cmd = [str(LAB / "check_shader.sh"), str(folder / shader), *args, "--png", str(png)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    line = [ln for ln in out.stdout.splitlines() if ln.startswith("RESULT ")]
    res = json.loads(line[0][7:]) if line else None
    rel = ("evidence/planning-checks/shaders/" if folder == UT else "lab-shaders/") + shader
    LOG.append({"label": label, "when": datetime.datetime.now().isoformat(timespec="seconds"),
                "command": "lab/check_shader.sh " + rel + " " + " ".join(args) + f" --png png/{label}.png", "exit": out.returncode,
                "result": res, "error_lines": [ln for ln in out.stdout.splitlines() if "ERROR" in ln][:6]})
    if out.returncode != 0 or res is None or not res.get("ok"):
        print("!! run failed:", label, out.stdout[-400:])
    return res, png


def check(name, ok, detail):
    SUMMARY.append(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    print(SUMMARY[-1])
    return ok


def near(a, b, tol):
    return abs(a - b) <= tol


def strip_probes(n):
    return [x for k in range(n) for x in ("--probe", f"0.5,{(k + 0.5) / n:.4f}")]


def green(rgba):
    return rgba[1] > 0.5 and rgba[0] < 0.5


def rot(a, p):                      # y points down, so a positive angle turns clockwise on screen
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def bbox(points):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return (min(xs), min(ys), max(xs), max(ys))


def compare_bbox(name, png, expected, tol=1.6):
    m = measure.measure(png)
    got = m["bbox_edges_rel"]
    ok = all(near(g, e, tol) for g, e in zip(got, expected))
    check(name, ok, f"measured bbox {got}, expected {[round(e, 1) for e in expected]} (tolerance {tol} px)")
    return m


def px_probe(px, py, w=640, h=360):
    return f"{(px + 0.25) / (w - 1):.5f},{(py + 0.25) / (h - 1):.5f}"


def colour_name(rgba):
    r, g, b = rgba[:3]
    if r < 0.25 and g < 0.25:
        return "black"
    if r > 0.7 and g < 0.25:
        return "red"
    if r < 0.25 and g > 0.7:
        return "green"
    if r > 0.7 and g > 0.7:
        return "yellow"
    return f"other{[round(x, 2) for x in rgba[:3]]}"


# ───────────────────────────── unit tests (rect strips): green = true, red = false ─────────────────────────────
def strips(label, shader, expected):
    res, _ = lab(label, shader, "--kind", "rect", *strip_probes(len(expected)), folder=UT)
    got = ["G" if green(p["rgba"]) else "R" for p in res["probes"]]
    exp = ["G" if e else "R" for e in expected]
    check(f"{label} ({shader})", got == exp, f"rows {''.join(got)} expected {''.join(exp)} (G = check true, R = check false; the R rows are the negative controls)")


strips("u1-columns", "t01-columns.gdshader", [1] * 10 + [0, 0])
strips("u2-constants", "t02-constants.gdshader", [1, 1, 1, 1, 1, 1, 1, 0])
strips("u3-products", "t03-products.gdshader", [1] * 15 + [0, 0, 0])

# ───────────────────────────── 01 table check (the five-and-six example) ─────────────────────────────
res, _ = lab("s1-table-check", "01-table-check.gdshader", "--kind", "rect", "--probe", "0.5,0.5")
rgba = res["probes"][0]["rgba"]
check("01-table-check shows the agree colour", near(rgba[0], 0.3686, 0.01) and near(rgba[1], 0.6392, 0.01) and near(rgba[2], 0.5686, 0.01),
      f"probe {rgba}: teal (0.37, 0.64, 0.57) means the shader's answer equals (23, 34); the disagree colour would be (0.85, 0.2, 0.2)")

# ───────────────────────────── 02 grow (scale table in vertex) ─────────────────────────────
for g in (0.5, 1.0, 1.5, 2.0):
    _, png = lab(f"g1-grow-{g}", "02-grow.gdshader", *WHITE, "--set", f"grow={g}")
    h = 64 * g
    compare_bbox(f"02-grow at {g}: a 128 px square becomes {128 * g:g} px", png, (-h, -h, h, h))

# ───────────────────────────── 03 turn (rotation table) ─────────────────────────────
for a in (0.5236, 0.7854, 1.5708):
    _, png = lab(f"t1-turn-{a}", "03-turn.gdshader", *WHITE, "--set", f"angle={a}")
    pts = [rot(a, p) for p in CORNERS]
    compare_bbox(f"03-turn at {a} rad: corners turned clockwise", png, bbox(pts))
    m = measure.measure(png)
    check(f"03-turn at {a} rad keeps the area", near(m["area_px"], 16384, 200), f"area {m['area_px']} px, a 128 px square is 16384")
probe_corners = [px_probe(260, 119), px_probe(378, 119), px_probe(260, 238), px_probe(378, 238)]    # inside TL, TR, BL, BR of the 128 px sprite
for a, exp in ((0.0, ["black", "red", "green", "yellow"]), (1.5708, ["green", "black", "yellow", "red"])):
    pr = [x for p in probe_corners for x in ("--probe", p)]
    res, _ = lab(f"t2-turn-gradient-{a}", "03-turn.gdshader", "--kind", "sprite", "--sprite-tex", "gradient", "--sprite-scale", "1.0", "--set", f"angle={a}", *pr)
    got = [colour_name(p["rgba"]) for p in res["probes"]]
    check(f"03-turn gradient texture at {a} rad: corner colours TL, TR, BL, BR", got == exp, f"{got}, expected {exp} (a clockwise quarter turn moves black to the top right)")

# ───────────────────────────── 04 slide (translation in the last column) ─────────────────────────────
for sx, sy in ((100, 0), (0, 100), (100, -40)):
    _, png = lab(f"sl1-slide-{sx}-{sy}", "04-slide.gdshader", *WHITE, "--set", f"slide={sx},{sy}")
    m = measure.measure(png)
    check(f"04-slide by ({sx}, {sy}) moves the centre by exactly that", near(m["centroid_rel"][0], sx, 0.6) and near(m["centroid_rel"][1], sy, 0.6),
          f"centroid {m['centroid_rel']} (y counts DOWN); size {m['width']} x {m['height']}")

# ───────────────────────────── 05 / 06 order of two tables ─────────────────────────────
_, png = lab("o1-turn-then-slide", "05-turn-then-slide.gdshader", *WHITE, "--set", "angle=1.5708", "--set", "slide=100,0")
m = measure.measure(png)
check("05 slide_by * turn_by (turn first, then slide): centre at (100, 0)", near(m["centroid_rel"][0], 100, 0.6) and near(m["centroid_rel"][1], 0, 0.6), f"centroid {m['centroid_rel']}")
_, png = lab("o2-slide-then-turn", "06-slide-then-turn.gdshader", *WHITE, "--set", "angle=1.5708", "--set", "slide=100,0")
m = measure.measure(png)
check("06 turn_by * slide_by (slide first, then turn): centre at (0, 100)", near(m["centroid_rel"][0], 0, 0.6) and near(m["centroid_rel"][1], 100, 0.6), f"centroid {m['centroid_rel']}")

# ───────────────────────────── 07 three moves ─────────────────────────────
g, a, tx, ty = 1.5, 0.5236, 100.0, -40.0
_, png = lab("m1-three-moves", "07-three-moves.gdshader", *WHITE, "--set", f"grow={g}", "--set", f"angle={a}", "--set", f"slide={tx:g},{ty:g}")
pts = [tuple(c + t for c, t in zip(rot(a, (p[0] * g, p[1] * g)), (tx, ty))) for p in CORNERS]
m = compare_bbox("07-three-moves (grow 1.5, angle 0.5236, slide 100, -40) matches scale, then turn, then slide", png, bbox(pts))
check("07-three-moves: the slide was not scaled or turned", near(m["centroid_rel"][0], tx, 0.6) and near(m["centroid_rel"][1], ty, 0.6), f"centroid {m['centroid_rel']}, slide was ({tx:g}, {ty:g})")

# ───────────────────────────── 08 flip ─────────────────────────────
for f in (0.0, 0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.5, 0.75, 1.0):
    _, png = lab(f"f1-flip-{f}", "08-flip.gdshader", *WHITE, "--set", f"flip={f}")
    m = measure.measure(png)
    w_exp = 128 * abs(math.cos(TAU * f))
    if m.get("empty"):
        check(f"08-flip at {f}: edge-on, nothing drawn", w_exp < 1.0, f"frame is empty; expected width 128 * |cos| = {w_exp:.3f} px")
    else:
        check(f"08-flip at {f}: width is 128 * |cos(TAU * flip)|", near(m["width"], w_exp, 1.6) and m["height"] == 128, f"measured {m['width']} x {m['height']}, expected {w_exp:.1f} x 128")
    if f == 0.125:
        from measure import column_height  # noqa: E402
        hl, hr = column_height(png, -44.5), column_height(png, 44.5)
        check("08-flip at 45 degrees: the far and near edges are the same height (no perspective)", hl == 128 and hr == 128, f"columns 44.5 px left and right of centre are {hl} and {hr} px tall")
pr = [x for p in probe_corners for x in ("--probe", p)]
for f, exp in ((0.0, ["black", "red", "green", "yellow"]), (0.5, ["red", "black", "yellow", "green"]), (1.0, ["black", "red", "green", "yellow"])):
    res, _ = lab(f"f2-flip-gradient-{f}", "08-flip.gdshader", "--kind", "sprite", "--sprite-tex", "gradient", "--sprite-scale", "1.0", "--set", f"flip={f}", *pr)
    got = [colour_name(p["rgba"]) for p in res["probes"]]
    check(f"08-flip gradient texture at {f}: corner colours TL, TR, BL, BR", got == exp,
          f"{got}, expected {exp} ({'mirrored left to right' if f == 0.5 else 'the original picture'})")

# ───────────────────────────── 09 flip and tip ─────────────────────────────
Rx = lambda a: ((1, 0, 0), (0, math.cos(a), -math.sin(a)), (0, math.sin(a), math.cos(a)))      # rows; the shader's columns are (1,0,0), (0,c,s), (0,-s,c)
Ry = lambda a: ((math.cos(a), 0, math.sin(a)), (0, 1, 0), (-math.sin(a), 0, math.cos(a)))      # columns (c,0,-s), (0,1,0), (s,0,c)


def mul(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(3)) for i in range(3))


def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))


for flip, tip in ((0.0, 0.1), (0.125, 0.1), (0.125, 0.0)):
    _, png = lab(f"ft1-flip-{flip}-tip-{tip}", "09-flip-and-tip.gdshader", *WHITE, "--set", f"flip={flip}", "--set", f"tip={tip}")
    M = matmul(Rx(TAU * tip), Ry(TAU * flip))
    pts = [mul(M, (p[0], p[1], 0.0))[:2] for p in CORNERS]
    compare_bbox(f"09-flip-and-tip at flip {flip}, tip {tip}: bounding box follows Rx * Ry", png, bbox(pts))
    if (flip, tip) == (0.125, 0.1):
        lens = (math.dist(pts[0], pts[3]), math.dist(pts[1], pts[2]))
        check("09-flip-and-tip: the left and right edges are the same length (a parallelogram, still no perspective)", near(lens[0], lens[1], 0.01), f"expected edge lengths {lens[0]:.1f} and {lens[1]:.1f} px")
_, png = lab("tp1-tip-0.25", "09-flip-and-tip.gdshader", *WHITE, "--set", "flip=0.0", "--set", "tip=0.25")
check("09-flip-and-tip at tip 0.25: edge-on from above, nothing drawn", measure.measure(png).get("empty", False), "frame is empty")

# ───────────────────────────── 10 spin about a corner (2D matrix chain) ─────────────────────────────
for a in (0.7854, 1.5708):
    pv = (-64, -64)
    _, png = lab(f"c1-corner-{a}", "10-spin-about-corner.gdshader", *WHITE, "--set", f"angle={a}", "--set", "pivot=-64,-64")
    pts = [tuple(c + q for c, q in zip(rot(a, (p[0] - pv[0], p[1] - pv[1])), pv)) for p in CORNERS]
    m = compare_bbox(f"10-spin-about-corner at {a} rad, pivot (-64, -64): bounding box matches slide * turn * slide", png, bbox(pts))
    check(f"10-spin-about-corner at {a} rad: the pivot corner is still a corner of the picture", near(bbox(pts)[1], -64, 0.01) and near(m["bbox_edges_rel"][1], -64, 1.0),
          f"top of the picture at y = {m['bbox_edges_rel'][1]} (the pivot's y is -64)")
_, png = lab("c2-corner-middle", "10-spin-about-corner.gdshader", *WHITE, "--set", "angle=0.7854", "--set", "pivot=0,0")
compare_bbox("10-spin-about-corner at 0.7854 rad, pivot (0, 0): spins in place", png, bbox([rot(0.7854, p) for p in CORNERS]))

# ───────────────────────────── 11 door (pivot, flip) ─────────────────────────────
for f in (0.0625, 0.125, 0.1875):
    _, png = lab(f"d1-door-left-{f}", "11-door.gdshader", *WHITE, "--set", f"flip={f}", "--set", "pivot=-64,0")
    right = -64 + 128 * math.cos(TAU * f)
    m = compare_bbox(f"11-door pivot (-64, 0) at flip {f}: left edge fixed at -64, right edge at {right:.1f}", png, (-64, -64, right, 64))
_, png = lab("d2-door-left-0.5", "11-door.gdshader", *WHITE, "--set", "flip=0.5", "--set", "pivot=-64,0")
compare_bbox("11-door pivot (-64, 0) at flip 0.5: the card lies on the far side of the hinge", png, (-192, -64, -64, 64))
_, png = lab("d3-door-right-0.125", "11-door.gdshader", *WHITE, "--set", "flip=0.125", "--set", "pivot=64,0")
compare_bbox("11-door pivot (64, 0) at flip 0.125: right edge fixed at 64, left edge at 64 - 128 cos", png, (64 - 128 * math.cos(TAU * 0.125), -64, 64, 64))
# mirrored on the far side of the hinge: gradient texture, card now spans x -192..-64 (window px 128..256)
probes = [px_probe(132, 119), px_probe(250, 119), px_probe(132, 238), px_probe(250, 238)]
res, _ = lab("d4-door-gradient-0.5", "11-door.gdshader", "--kind", "sprite", "--sprite-tex", "gradient", "--sprite-scale", "1.0", "--set", "flip=0.5", "--set", "pivot=-64,0",
             *[x for p in probes for x in ("--probe", p)])
got = [colour_name(p["rgba"]) for p in res["probes"]]
check("11-door at flip 0.5: the card on the far side is mirrored", got == ["red", "black", "yellow", "green"], f"corner colours TL, TR, BL, BR {got}")

# ───────────────────────────── plain addition slides the same way; mismatched sizes do not compile ─────────────────────────────
_, png = lab("a1-add-slide", "t04-add-slide.gdshader", *WHITE, folder=UT)
m = measure.measure(png)
check("t04 VERTEX += vec2(100, 0): plain addition slides the card by exactly (100, 0), the same as the table", near(m["centroid_rel"][0], 100, 0.6) and near(m["centroid_rel"][1], 0, 0.6), f"centroid {m['centroid_rel']}")


def expect_compile_error(label, shader, what):
    cmd = [str(LAB / "check_shader.sh"), str(UT / shader), "--kind", "rect"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    text = (out.stdout + out.stderr).strip()
    msgs = [ln for ln in text.splitlines() if "ERROR" in ln or "Invalid" in ln or "Parse" in ln][:3]
    LOG.append({"label": label, "when": datetime.datetime.now().isoformat(timespec="seconds"), "command": f"lab/check_shader.sh evidence/planning-checks/shaders/{shader} --kind rect",
                "exit": out.returncode, "result": None, "error_lines": msgs, "note": "EXPECTED FAILURE: the shader must not compile"})
    check(f"{shader}: {what} does not compile", out.returncode == 1 and bool(msgs), f"exit {out.returncode}; compiler said: {' / '.join(msgs)[:300]}")


expect_compile_error("e1-mat3-times-mat2", "t05a-size-mismatch-mat3-times-mat2.gdshader", "a three-by-three table times a two-by-two table")
expect_compile_error("e2-mat3-times-vec2", "t05b-size-mismatch-mat3-times-vec2.gdshader", "a three-by-three table times a two-number point")

# ───────────────────────────── the same geometry in the Compatibility renderer ─────────────────────────────
# Every number above was read on Forward+. Vertex moves should not depend on the renderer; these runs check that they do not.
GL = ["--renderer", "gl_compatibility"]
res, png = lab("gl1-table-check", "01-table-check.gdshader", "--kind", "rect", "--probe", "0.5,0.5", *GL)
rgba = res["probes"][0]["rgba"]
check("[gl_compatibility] 01-table-check shows the agree colour", res["renderer"] == "gl_compatibility" and near(rgba[1], 0.6392, 0.02), f"renderer {res['renderer']}, probe {rgba}")
res, png = lab("gl2-flip-0.125", "08-flip.gdshader", *WHITE, "--set", "flip=0.125", *GL)
m = measure.measure(png)
check("[gl_compatibility] 08-flip at 0.125: width 90, height 128", res["renderer"] == "gl_compatibility" and near(m["width"], 90.5, 1.6) and m["height"] == 128, f"renderer {res['renderer']}, measured {m['width']} x {m['height']}")
res, png = lab("gl3-door-0.125", "11-door.gdshader", *WHITE, "--set", "flip=0.125", "--set", "pivot=-64,0", *GL)
compare_bbox("[gl_compatibility] 11-door pivot (-64, 0) at flip 0.125: left edge fixed", png, (-64, -64, -64 + 128 * math.cos(TAU * 0.125), 64))
g, a, tx, ty = 1.5, 0.5236, 100.0, -40.0
res, png = lab("gl4-three-moves", "07-three-moves.gdshader", *WHITE, "--set", f"grow={g}", "--set", f"angle={a}", "--set", f"slide={tx:g},{ty:g}", *GL)
pts = [tuple(c + t for c, t in zip(rot(a, (p[0] * g, p[1] * g)), (tx, ty))) for p in CORNERS]
compare_bbox("[gl_compatibility] 07-three-moves bounding box", png, bbox(pts))
res, png = lab("gl5-order-B", "06-slide-then-turn.gdshader", *WHITE, "--set", "angle=1.5708", "--set", "slide=100,0", *GL)
m = measure.measure(png)
check("[gl_compatibility] 06 slide first then turn: centre at (0, 100)", near(m["centroid_rel"][0], 0, 0.6) and near(m["centroid_rel"][1], 100, 0.6), f"centroid {m['centroid_rel']}")

# ───────────────────────────── write the logs ─────────────────────────────
with open(HERE / "lab-results.jsonl", "w") as fh:
    for entry in LOG:
        fh.write(json.dumps(entry) + "\n")
fails = [s for s in SUMMARY if s.startswith("FAIL")]
header = (f"Matrices and Fake 3D: geometry checks, {datetime.date.today()}. Machine: Apple M4 Pro, macOS, Godot 4.7.2 stable (official), Forward+ unless a line says "
          f"[gl_compatibility] (the RESULT lines in lab-results.jsonl name the renderer for every run).\n{len(SUMMARY) - len(fails)} PASS, {len(fails)} FAIL.\n\n")
(HERE / "geometry-summary.txt").write_text(header + "\n".join(SUMMARY) + "\n")
print(f"\n{len(SUMMARY) - len(fails)} PASS, {len(fails)} FAIL")
sys.exit(1 if fails else 0)
