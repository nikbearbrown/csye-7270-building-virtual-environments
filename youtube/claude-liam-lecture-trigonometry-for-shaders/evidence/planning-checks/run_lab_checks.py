#!/usr/bin/env python3
"""run_lab_checks.py: runs every shader of this film (the 12 shown on screen and the evidence-only ones) through the series' Shader Lab
(lab/check_shader.sh: a real Godot 4.7.2 window, Forward+ unless a label says compat) and checks each probe against a PREDICTION computed here
from the maths (p = UV * 2 - 1, UV = (p + 1) / 2), not against a remembered value.

Many agents share the Lab and it runs one job at a time, so this file holds the ESSENTIAL runs (one or two per shader). The many-variant sweeps
(every angle, every wait, every sweep value, the flower at several angles) run in ONE Godot process in verify-batch.gd (own scratch project).

Writes (incrementally): lab-results.jsonl (one line per run), lab-summary.txt (prediction vs reading, PASS/FAIL per probe), png/<label>.png.
Usage:  python3 run_lab_checks.py [label-prefix ...]
"""
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab"
SH = FILM / "lab-shaders"
OUT = HERE / "png"
OUT.mkdir(exist_ok=True)
RESULTS = HERE / "lab-results.jsonl"
SUMMARY = HERE / "lab-summary.txt"

STAGE = (0.85, 0.84, 0.79)          # the rect shaders paint their own stage
LAB_STAGE = (0.851, 0.8353, 0.7922)  # the Lab's clear colour behind sprites
PLANET = (0.37, 0.64, 0.57)
MOON = (0.5, 0.6, 0.75)
METEOR = (0.9, 0.65, 0.25)
TEAL, AMBER = PLANET, METEOR
BLOB = (0.3725, 0.6392, 0.5686)
TOL = 0.008                         # 8-bit rounding is 0.002; a little more for edge pixels

only = sys.argv[1:]


def log(line):
    print(line, flush=True)
    with SUMMARY.open("a") as f:
        f.write(line + "\n")


def uv(p):
    return ((p[0] + 1.0) / 2.0, (p[1] + 1.0) / 2.0)


def pos(r, theta, origin=(0.0, 0.0)):
    return (origin[0] + r * math.cos(theta), origin[1] + r * math.sin(theta))


def flip_v(u):
    return (u[0], 1.0 - u[1])


def pixel_center_p(u, v, w=480, h=480):
    """p of the pixel the Lab actually reads for a normalised probe (u, v): it reads pixel int(u * (w - 1))."""
    px, py = int(u * (w - 1)), int(v * (h - 1))
    return ((px + 0.5) / w * 2 - 1, (py + 0.5) / h * 2 - 1)


def t_of(x, y):
    return math.atan2(y, x) / math.tau + 0.5


def col_mix(t):
    return tuple(TEAL[i] + t * (AMBER[i] - TEAL[i]) for i in range(3))


def run(label, shader, args, probes=(), renderer=None):
    """probes: list of (name, (u, v), expected 3-tuple (None entries = not checked) or None for 'reading only', tolerance)."""
    if only and not any(label.startswith(o) for o in only):
        return
    cmd = [str(LAB / "check_shader.sh"), str(SH / shader)] + args
    for _, at, _, _ in probes:
        cmd += ["--probe", f"{at[0]:.5f},{at[1]:.5f}"]
    if renderer:
        cmd += ["--renderer", renderer]
    cmd += ["--png", str(OUT / f"{label}.png")]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    out = cp.stdout + cp.stderr
    res = None
    for ln in out.splitlines():
        if ln.startswith("RESULT "):
            res = json.loads(ln[7:])
    rec = {"check": label, "shader": shader, "args": " ".join(args + (["--renderer", renderer] if renderer else [])), "exit": cp.returncode,
           "result": res, "message": None if res else out.strip()[:600]}
    with RESULTS.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    log(f"[{cp.returncode}] {label}  ({shader} {' '.join(args)}{' --renderer ' + renderer if renderer else ''})")
    if res and probes:
        for (name, at, exp, tol), pr in zip(probes, res["probes"]):
            got = tuple(pr["rgba"][:3])
            if exp is None:
                verdict = "(reading)"
            else:
                bad = [i for i, e in enumerate(exp) if e is not None and abs(got[i] - e) > tol]
                verdict = "PASS" if not bad else "FAIL"
            shown = tuple(None if e is None else round(e, 4) for e in (exp or ()))
            log(f"     {name:52s} at ({at[0]:.4f},{at[1]:.4f})  predicted {shown}  read {got}  {verdict}")


S480 = ["--kind", "rect", "--size", "480x480"]
SPR480 = ["--kind", "sprite", "--size", "480x480"]

# ---- constants, values, pixel address
run("20-constants", "20-check-constants.gdshader", ["--kind", "rect"],
    [("PI, TAU, E match (all three channels 1.0)", (0.25, 0.5), (1, 1, 1), TOL), ("TAU == 2 PI, radians(45) == PI/4, degrees(PI) == 180", (0.75, 0.5), (1, 1, 1), TOL)])
sin30, cos30 = math.sin(math.radians(30)), math.cos(math.radians(30))
run("21-trig-values", "21-check-trig-values.gdshader", ["--kind", "rect", "--set", "deg=30", "--set", "forty_five=45"],
    [("sin 30 deg, cos 30 deg, 0.5 * tan 45 deg", (0.25, 0.5), (sin30, cos30, 0.5), 0.008),
     ("0.5 + 0.5 sin(30), 0.5 + 0.5 cos(30), turns/8", (0.75, 0.5), (0.5 + 0.5 * math.sin(30.0), 0.5 + 0.5 * math.cos(30.0), (30 / math.tau) / 8), 0.008)])
run("27-pixel-p", "27-check-pixel-p.gdshader", S480,
    [("corner (0.02, 0.02): UV echoed, outside the unit circle", (0.02, 0.02), (0.02, 0.02, 0.0), 0.012),
     ("middle: UV echoed 0.5, inside the unit circle", (0.5, 0.5), (0.5, 0.5, 1.0), 0.012), ("corner (0.98, 0.98)", (0.98, 0.98), (0.98, 0.98, 0.0), 0.012)])

# ---- the moon at exact angles (screen: y down)
th30 = math.radians(30)
run("01-moon-fixed", "01-moon-fixed.gdshader", S480,
    [("moon at 30 deg: predicted spot (right, BELOW middle)", uv(pos(0.6, th30)), MOON, TOL),
     ("the y-up mirror of that spot is empty", flip_v(uv(pos(0.6, th30))), STAGE, TOL), ("planet in the middle", (0.5, 0.5), PLANET, TOL)])
th90 = math.radians(90)
run("22-angle-90", "22-check-orbit-angle.gdshader", S480 + ["--set", f"angle={th90:.6f}"],
    [("moon at 90 deg: straight DOWN from the middle", uv(pos(0.6, th90)), MOON, TOL), ("the y-up spot (straight up) is empty", flip_v(uv(pos(0.6, th90))), STAGE, TOL)])
run("22-angle-30-compat", "22-check-orbit-angle.gdshader", S480 + ["--set", f"angle={th30:.6f}"],
    [("moon at 30 deg, Compatibility renderer", uv(pos(0.6, th30)), MOON, TOL), ("planet, Compatibility renderer", (0.5, 0.5), PLANET, TOL),
     ("stage, Compatibility renderer", (0.05, 0.05), STAGE, TOL)], renderer="gl_compatibility")

# ---- TIME-driven shaders (the PNGs are measured in analyze_lab.py; the batch run measures many waits)
run("02-orbit-w0.5", "02-orbit.gdshader", S480 + ["--wait", "0.5"])
run("03-orbit-fast-w0.5", "03-orbit-fast.gdshader", S480 + ["--wait", "0.5"])
run("04-aspect-1.7778-wide", "04-orbit-aspect.gdshader", ["--kind", "rect", "--size", "640x360", "--wait", "0.0", "--set", "aspect=1.7778"])
run("05-moons-evenly-w0.3", "05-moons-evenly.gdshader", S480 + ["--wait", "0.3"])
for nm, a, b in (("a0.8-b2.0", 0.8, 2.0), ("a0.8-bm2.0", 0.8, -2.0)):
    moon_p = pos(0.6, a)
    run(f"23-meteor-{nm}", "23-check-meteor-angles.gdshader", S480 + ["--set", f"a={a}", "--set", f"b={b}"],
        [("moon", uv(moon_p), MOON, TOL), ("meteor = moon + 0.2 * (cos b, sin b)", uv(pos(0.2, b, moon_p)), METEOR, TOL),
         ("the other sign's spot is empty", uv(pos(0.2, -b, moon_p)), STAGE, TOL), ("planet", (0.5, 0.5), PLANET, TOL)])
run("06-meteor-orbit-w0.5", "06-meteor-orbit.gdshader", S480 + ["--wait", "0.5"])
run("07-meteor-reverse-w0.5", "07-meteor-reverse.gdshader", S480 + ["--wait", "0.5"])
run("12-flower-w0.3", "12-flower.gdshader", S480 + ["--wait", "0.3"])

# ---- the pixel's angle (arc tangent). Pixel centres: the Lab reads pixel int(u * 479) of 480.
probes24 = []
for nm, (u, v) in {"right (3 o'clock)": (0.9, 0.5), "down (6 o'clock)": (0.5, 0.9), "up (12 o'clock)": (0.5, 0.1), "lower right (+45 deg)": (0.8, 0.8),
                   "upper left (-135 deg)": (0.2, 0.2), "upper right (-45 deg)": (0.8, 0.2), "lower left (+135 deg)": (0.2, 0.8)}.items():
    probes24.append((f"R = t at {nm}", (u, v), (t_of(*pixel_center_p(u, v)), None, None), 0.004))
for nm, v in (("just ABOVE the left axis (the seam)", 0.4975), ("just BELOW the left axis (the seam)", 0.5025)):
    probes24.append((f"R = t {nm}", (0.1, v), (t_of(*pixel_center_p(0.1, v)), None, None), 0.004))
for nm, u in (("just left of 12 o'clock", 0.4975), ("just right of 12 o'clock", 0.5025)):
    x, y = pixel_center_p(u, 0.1)
    probes24.append((f"G = fract(angle/TAU + 0.25) {nm}", (u, 0.1), (None, (math.atan2(y, x) / math.tau + 0.25) % 1.0, None), 0.004))
run("24-atan", "24-check-atan.gdshader", S480, probes24)
run("24-atan-odd-view-481", "24-check-atan.gdshader", ["--kind", "rect", "--size", "481x481"],
    [("top, exactly on the vertical axis (x = 0)", (0.5, 0.1), None, 0), ("bottom, exactly on the vertical axis", (0.5, 0.9), None, 0),
     ("left, exactly on the horizontal axis (y = 0)", (0.1, 0.5), None, 0), ("right, exactly on the horizontal axis", (0.9, 0.5), None, 0)])
run("25-atan-one-argument", "25-check-atan-one-argument.gdshader", S480,
    [("(0.8, 0.8) lower right", (0.8, 0.8), (0.75, None, None), 0.004), ("(0.2, 0.2) upper left: SAME number as lower right", (0.2, 0.2), (0.75, None, None), 0.004),
     ("(0.8, 0.2) upper right", (0.8, 0.2), (0.25, None, None), 0.004), ("(0.2, 0.8) lower left: SAME number as upper right", (0.2, 0.8), (0.25, None, None), 0.004)])
run("08-atan-colors", "08-atan-colors.gdshader", S480,
    [("mix at right (t about 0.5)", (0.9, 0.5), col_mix(t_of(*pixel_center_p(0.9, 0.5))), 0.01),
     ("mix at down (t about 0.75)", (0.5, 0.9), col_mix(t_of(*pixel_center_p(0.5, 0.9))), 0.01),
     ("mix at up (t about 0.25)", (0.5, 0.1), col_mix(t_of(*pixel_center_p(0.5, 0.1))), 0.01),
     ("seam, just above the left axis: teal", (0.1, 0.4975), TEAL, 0.012), ("seam, just below the left axis: amber", (0.1, 0.5025), AMBER, 0.012)])
run("09-atan-one-argument", "09-atan-one-argument.gdshader", S480,
    [("lower right", (0.8, 0.8), col_mix(0.75), 0.012), ("upper left: same colour as lower right", (0.2, 0.2), col_mix(0.75), 0.012),
     ("upper right", (0.8, 0.2), col_mix(0.25), 0.012), ("lower left: same colour as upper right", (0.2, 0.8), col_mix(0.25), 0.012)])


# ---- the sweep: a wedge revealed clockwise from the left (10) or from the top (11). Sprite: 128 px scaled to 0.8 * 480 = 384 px, centred.
def spr_probe(u, v):
    return ((240 + (u - 0.5) * 384) / 479.0, (240 + (v - 0.5) * 384) / 479.0)


corners = {"UL": (0.36, 0.36), "UR": (0.64, 0.36), "LR": (0.64, 0.64), "LL": (0.36, 0.64)}   # inside the teal blob (radius 0.30), away from the eyes
t10 = {k: math.atan2(2 * v - 1, 2 * u - 1) / math.tau + 0.5 for k, (u, v) in corners.items()}
t11 = {k: (math.atan2(2 * v - 1, 2 * u - 1) / math.tau + 0.25) % 1.0 for k, (u, v) in corners.items()}
sw = 0.5
run("10-sweep-0.5", "10-sweep.gdshader", SPR480 + ["--set", f"sweep={sw}"],
    [(f"{k}: t = {t10[k]:.3f}, sweep {sw}: {'shown' if t10[k] < sw else 'hidden'}", spr_probe(*c), BLOB if t10[k] < sw else LAB_STAGE, TOL) for k, c in corners.items()])
run("11-sweep-top-0.5", "11-sweep-top.gdshader", SPR480 + ["--set", f"sweep={sw}"],
    [(f"{k}: t = {t11[k]:.3f}, sweep {sw}: {'shown' if t11[k] < sw else 'hidden'}", spr_probe(*c), BLOB if t11[k] < sw else LAB_STAGE, TOL) for k, c in corners.items()])


# ---- the same two picture shaders in the Compatibility renderer (plain colour constants: the pixels should not change)
run("08-atan-colors-compat", "08-atan-colors.gdshader", S480,
    [("mix at right (t about 0.5), Compatibility", (0.9, 0.5), col_mix(t_of(*pixel_center_p(0.9, 0.5))), 0.01),
     ("mix at down (t about 0.75), Compatibility", (0.5, 0.9), col_mix(t_of(*pixel_center_p(0.5, 0.9))), 0.01),
     ("seam, just above the left axis: teal, Compatibility", (0.1, 0.4975), TEAL, 0.012), ("seam, just below the left axis: amber, Compatibility", (0.1, 0.5025), AMBER, 0.012)],
    renderer="gl_compatibility")
run("10-sweep-0.5-compat", "10-sweep.gdshader", SPR480 + ["--set", "sweep=0.5"],
    [(f"{k}: t = {t10[k]:.3f}, sweep 0.5: {'shown' if t10[k] < 0.5 else 'hidden'}, Compatibility", spr_probe(*c), BLOB if t10[k] < 0.5 else LAB_STAGE, TOL) for k, c in corners.items()],
    renderer="gl_compatibility")


# ---- the flower: edge radius 0.55 + 0.15 cos(8 a)
def petal_probe(theta, r, petals=8.0):
    edge = 0.55 + 0.15 * math.cos(petals * theta)
    return (f"angle {math.degrees(theta):6.1f} deg, radius {r}: {'inside' if r < edge else 'outside'} (edge {edge:.3f})", uv(pos(r, theta)), PLANET if r < edge else STAGE, TOL)


run("26-flower-static-8", "26-check-flower-static.gdshader", S480 + ["--set", "petals=8"],
    [petal_probe(0.0, 0.65), petal_probe(0.0, 0.75), petal_probe(math.pi / 8, 0.45), petal_probe(math.pi / 8, 0.55), petal_probe(math.pi / 4, 0.65), petal_probe(math.pi / 4, 0.75),
     petal_probe(math.pi * 0.9, 0.65), petal_probe(-math.pi * 0.9, 0.65)])

fails = 0
for ln in SUMMARY.read_text().splitlines():
    fails += ln.endswith("FAIL")
print(f"\ndone; {sum(1 for _ in RESULTS.open())} runs recorded; probe FAIL lines: {fails}")
