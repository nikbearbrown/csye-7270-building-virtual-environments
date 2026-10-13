#!/usr/bin/env python3
"""run_batch.py: the many-variant checks of this film, in ONE Godot process (verify-batch.gd, own scratch project), then the maths on the PNGs.

1. builds cases.json (shader files from ../../lab-shaders, uniform values, waits, probes) with a PREDICTION for every probe, computed here from the
   maths (p = UV * 2 - 1, UV = (p + 1) / 2, angle growing clockwise because y counts down);
2. runs  godot --path <scratch project> --script res://verify-batch.gd -- --cases cases.json --out batch-results.json  (windowed, Forward+);
3. compares every probe with its prediction (batch-summary.txt) and measures the PNG series (analysis lines in the same file):
   moon angle against elapsed time (speed and direction), meteor angle relative to the moon, planet size on a wide view (oval and fixed),
   three moons' spacing, and the flower's turn.
Usage: python3 run_batch.py [--no-godot]      (--no-godot re-reads batch-results.json and redoes the comparison only)
"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
SH = FILM / "lab-shaders"
PNG = HERE / "png"
PNG.mkdir(exist_ok=True)
PROJ = Path("/private/tmp/claude-501/godot-shaders-trigonometry-for-shaders/proj")
CASES = HERE / "batch-cases.json"
RESULTS = HERE / "batch-results.json"
SUMMARY = HERE / "batch-summary.txt"

STAGE = (0.85, 0.84, 0.79)
LAB_STAGE = (0.851, 0.8353, 0.7922)
PLANET = (0.37, 0.64, 0.57)
MOON = (0.5, 0.6, 0.75)
METEOR = (0.9, 0.65, 0.25)
BLOB = (0.3725, 0.6392, 0.5686)
TOL = 0.008
BIG = (480, 480)


def uv(p):
    return ((p[0] + 1) / 2, (p[1] + 1) / 2)


def pos(r, th, origin=(0.0, 0.0)):
    return (origin[0] + r * math.cos(th), origin[1] + r * math.sin(th))


def flip_v(u):
    return (u[0], 1 - u[1])


def pc(u, v, w=480, h=480):
    px, py = int(u * (w - 1)), int(v * (h - 1))
    return ((px + 0.5) / w * 2 - 1, (py + 0.5) / h * 2 - 1)


def t_of(x, y):
    return math.atan2(y, x) / math.tau + 0.5


cases = []
expect = {}      # label -> list of (name, expected tuple/None, tol) per probe


def add(label, shader, kind="rect", size=BIG, sets=None, waits=(0.0,), probes=(), png=False, sprite_tex="sprite"):
    cases.append({"label": label, "shader": str(SH / shader), "kind": kind, "size": list(size), "set": sets or {}, "waits": list(waits),
                  "probes": [list(p[1]) for p in probes], "png": str(PNG / f"batch-{label}") if png else "", "sprite_tex": sprite_tex})
    expect[label] = [(p[0], p[2], p[3]) for p in probes]


# A. the moon at 15 exact angles (screen: y down)
for deg in (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, -30, -90, 390):
    th = math.radians(deg)
    spot = uv(pos(0.6, th))
    probes = [(f"moon at {deg} deg", spot, MOON, TOL), ("planet", (0.5, 0.5), PLANET, TOL)]
    if abs(spot[1] - 0.5) > 0.02:
        probes.append(("y-up mirror spot is empty", flip_v(spot), STAGE, TOL))
    add(f"angle{deg}", "22-check-orbit-angle.gdshader", sets={"angle": th}, probes=probes)

# B. TIME series (PNGs, measured below)
add("orbit02", "02-orbit.gdshader", waits=(0.0, 0.5, 1.0, 1.5, 2.0), png=True)
add("orbit03fast", "03-orbit-fast.gdshader", waits=(0.0, 0.5, 1.0, 1.5), png=True)
add("meteor06", "06-meteor-orbit.gdshader", waits=(0.0, 0.25, 0.5, 0.75, 1.0), png=True)
add("meteor07reverse", "07-meteor-reverse.gdshader", waits=(0.0, 0.25, 0.5, 0.75, 1.0), png=True)
add("flower12", "12-flower.gdshader", waits=(0.0, 0.2, 0.4), png=True)
add("moons05", "05-moons-evenly.gdshader", waits=(0.0, 0.5), png=True)

# C. the wide view
add("wide02", "02-orbit.gdshader", size=(640, 360), waits=(0.0,), png=True)
add("wide04a1.0", "04-orbit-aspect.gdshader", size=(640, 360), sets={"aspect": 1.0}, waits=(0.0,), png=True)
add("wide04a1.7778", "04-orbit-aspect.gdshader", size=(640, 360), sets={"aspect": 1.7778}, waits=(0.0,), png=True)
add("square04a1.0", "04-orbit-aspect.gdshader", sets={"aspect": 1.0}, waits=(0.0,), png=True)

# D. sweeps (sprite 128 px scaled to 384 px, centred in 480): wedge from the left (10) and from the top (11)
def sp(u, v):
    return ((240 + (u - 0.5) * 384) / 479.0, (240 + (v - 0.5) * 384) / 479.0)


corners = {"UL": (0.36, 0.36), "UR": (0.64, 0.36), "LR": (0.64, 0.64), "LL": (0.36, 0.64)}
for sw in (0.0, 0.25, 0.3, 0.5, 0.75, 1.0):
    probes = []
    for k, c in corners.items():
        t = math.atan2(2 * c[1] - 1, 2 * c[0] - 1) / math.tau + 0.5
        probes.append((f"{k} t={t:.3f}: {'shown' if t < sw else 'hidden'}", sp(*c), BLOB if t < sw else LAB_STAGE, TOL))
    add(f"sweep10-{sw}", "10-sweep.gdshader", kind="sprite", sets={"sweep": sw}, probes=probes, png=(sw in (0.25, 0.3, 0.5, 0.75)))
for sw in (0.0, 0.25, 0.3, 0.5, 0.75, 1.0):
    probes = []
    for k, c in corners.items():
        t = (math.atan2(2 * c[1] - 1, 2 * c[0] - 1) / math.tau + 0.25) % 1.0
        probes.append((f"{k} t={t:.3f}: {'shown' if t < sw else 'hidden'}", sp(*c), BLOB if t < sw else LAB_STAGE, TOL))
    add(f"sweep11top-{sw}", "11-sweep-top.gdshader", kind="sprite", sets={"sweep": sw}, probes=probes, png=(sw in (0.25, 0.3, 0.5, 0.75)))

# D2. the worked pixel: p = (-0.3, -0.3) has t = 0.125, so it appears when sweep passes one eighth (sprite uv (0.35, 0.35))
for sw, shown in ((0.12, False), (0.13, True)):
    add(f"sweep10-worked-pixel-{sw}", "10-sweep.gdshader", kind="sprite", sets={"sweep": sw},
        probes=[(f"pixel p = (-0.3, -0.3), t = {math.atan2(-0.3, -0.3) / math.tau + 0.5:.4f}, sweep {sw}: {'shown' if shown else 'hidden'}", sp(0.35, 0.35), BLOB if shown else LAB_STAGE, TOL)])

# E. meteor at exact angles
for a, b in ((0.8, 2.0), (0.8, -2.0), (0.0, 0.0), (1.5708, 3.1416), (4.0, 1.0), (2.5, -0.5), (-1.0, 5.0)):
    moon_p = pos(0.6, a)
    met_p = pos(0.2, b, moon_p)
    probes = [("moon", uv(moon_p), MOON, TOL), ("meteor = moon + 0.2 (cos b, sin b)", uv(met_p), METEOR, TOL), ("planet", (0.5, 0.5), PLANET, TOL)]
    other = pos(0.2, -b, moon_p)          # where the negated angle would have put the meteor
    if math.dist(other, met_p) > 0.15:
        probes.append(("negated-angle spot is empty", uv(other), STAGE, TOL))
    add(f"meteor-a{a}-b{b}", "23-check-meteor-angles.gdshader", sets={"a": a, "b": b}, probes=probes)

# F. the angle of a pixel: R = t (seam at the left), G = fract(.. + 0.25) (seam at the top), B = the PI form of R; 24 directions at radius 0.7
probes = []
for k in range(24):
    th = math.radians(-172.5 + 15 * k)
    u, v = uv(pos(0.7, th))
    x, y = pc(u, v)
    r = t_of(x, y)
    g = (math.atan2(y, x) / math.tau + 0.25) % 1.0
    probes.append((f"angle {math.degrees(th):7.1f}: R and B = t, G = top-seam t", (u, v), (r, g, r), 0.004))
add("atan-ring-480", "24-check-atan.gdshader", probes=probes)
add("atan-odd-481", "24-check-atan.gdshader", size=(481, 481),
    probes=[("top, exactly x = 0", (0.5, 0.1), None, 0), ("bottom, exactly x = 0", (0.5, 0.9), None, 0), ("left, exactly y = 0", (0.1, 0.5), None, 0), ("right, exactly y = 0", (0.9, 0.5), None, 0),
            ("the exact middle (x = 0, y = 0)", (0.5, 0.5), None, 0)])
# the one-argument form: opposite directions give the same number (32 pairs)
probes = []
for k in range(16):
    th = math.radians(-82.5 + 11.25 * k)
    u1, v1 = uv(pos(0.7, th))
    x, y = pc(u1, v1)
    probes.append((f"one-argument t at {math.degrees(th):6.1f} deg", (u1, v1), (math.atan(y / x) / math.pi + 0.5, None, None), 0.004))
    u2, v2 = uv(pos(0.7, th + math.pi))
    x2, y2 = pc(u2, v2)
    probes.append((f"  ... and at the opposite direction ({math.degrees(th + math.pi):6.1f} deg): the SAME number", (u2, v2), (math.atan(y2 / x2) / math.pi + 0.5, None, None), 0.004))
add("atan-one-arg-pairs", "25-check-atan-one-argument.gdshader", probes=probes)

# G. the flower: 32 directions, a probe just inside and just outside the edge radius 0.55 + 0.15 cos(petals * a)
for petals in (8, 6):
    probes = []
    for k in range(32):
        th = -math.pi + (k + 0.5) * math.tau / 32
        edge = 0.55 + 0.15 * math.cos(petals * th)
        probes.append((f"a = {math.degrees(th):7.2f} deg, edge {edge:.3f}: radius {edge - 0.04:.3f} inside", uv(pos(edge - 0.04, th)), PLANET, TOL))
        probes.append((f"a = {math.degrees(th):7.2f} deg, edge {edge:.3f}: radius {edge + 0.04:.3f} outside", uv(pos(edge + 0.04, th)), STAGE, TOL))
    add(f"flower-static-{petals}", "26-check-flower-static.gdshader", sets={"petals": petals}, probes=probes)

CASES.write_text(json.dumps(cases, indent=1))
print(f"{len(cases)} cases written")

if "--no-godot" not in sys.argv:
    PROJ.mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / "verify-batch.gd", PROJ / "verify-batch.gd")
    cmd = ["godot", "--path", str(PROJ), "--script", "res://verify-batch.gd", "--", "--cases", str(CASES), "--out", str(RESULTS)]
    cp = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    (HERE / "run-3-batch.log").write_text(cp.stdout + cp.stderr)
    print("godot exit", cp.returncode)

res = {r["label"]: r for r in json.loads(RESULTS.read_text())}
lines = []


def log(s):
    print(s)
    lines.append(s)


npass = nfail = 0
for c in cases:
    r = res.get(c["label"])
    if not r:
        log(f"MISSING {c['label']}")
        continue
    exps = expect[c["label"]]
    for cap in r["captures"][:1]:
        for (name, exp, tol), pr in zip(exps, cap["probes"]):
            got = tuple(pr["rgba"][:3])
            if exp is None:
                log(f"  {c['label']:22s} {name:62s} (reading) {got}")
                continue
            bad = [i for i, e in enumerate(exp) if e is not None and abs(got[i] - e) > tol]
            ok = not bad
            npass += ok
            nfail += (not ok)
            if not ok:
                log(f"  FAIL {c['label']:20s} {name:60s} predicted {tuple(None if e is None else round(e, 4) for e in exp)} read {got}")
log(f"probe comparison: {npass} PASS, {nfail} FAIL (every probe of every case; only failures and readings are listed above)")


# ------------------------------------------------------------------ measurements on the PNG series
def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(float)


def mask(img, rgb, tol=7):
    target = np.array([c * 255 for c in rgb])
    return (np.abs(img - target) <= tol).all(axis=2)


def centroid(m):
    ys, xs = np.nonzero(m)
    return (xs.mean(), ys.mean(), len(xs)) if len(xs) else None


def ang(cx, cy, x, y):
    return math.atan2(y - cy, x - cx)          # image coordinates: y down, so the angle grows clockwise on screen


def unwrap_diff(a1, a0):
    d = a1 - a0
    return (d + math.pi) % math.tau - math.pi


def series(label, pattern):
    r = res[label]
    pngs = [Path(c["png"]) for c in r["captures"]]
    els = [c["elapsed_s"] for c in r["captures"]]
    return pngs, els


log("\nMEASUREMENTS ON THE PNG SERIES (screen angles: image coordinates, y down; speed in radians per second of elapsed process time)")
for label, speed_expected, what in (("orbit02", 1.0, "a = TIME"), ("orbit03fast", 2.0, "a = TIME * 2.0")):
    pngs, els = series(label, None)
    angles, dists = [], []
    for p in pngs:
        img = load(p)
        h, w, _ = img.shape
        cx, cy = w / 2 - 0.5, h / 2 - 0.5
        m = centroid(mask(img, MOON))
        angles.append(ang(cx, cy, m[0], m[1]))
        dists.append(math.hypot(m[0] - cx, m[1] - cy) / (w / 2))
    for i in range(1, len(angles)):
        d = unwrap_diff(angles[i], angles[i - 1])
        dt = els[i] - els[i - 1]
        log(f"  {label} ({what}): wait {els[i - 1]:.3f}->{els[i]:.3f} s: moon angle {math.degrees(angles[i - 1]):7.2f}->{math.degrees(angles[i]):7.2f} deg; "
            f"change {d:+.3f} rad over {dt:.3f} s = {d / dt:+.3f} rad/s (expected {speed_expected:+.1f}, positive = clockwise); distance from middle {dists[i]:.3f} of half-width (expected 0.600)")
for label, rel_expected in (("meteor06", 3.0), ("meteor07reverse", -3.0)):
    pngs, els = series(label, None)
    moon_a, rel_a = [], []
    for p in pngs:
        img = load(p)
        h, w, _ = img.shape
        cx, cy = w / 2 - 0.5, h / 2 - 0.5
        mm = centroid(mask(img, MOON))
        mt = centroid(mask(img, METEOR))
        moon_a.append(ang(cx, cy, mm[0], mm[1]))
        rel_a.append(ang(mm[0], mm[1], mt[0], mt[1]))
    for i in range(1, len(moon_a)):
        dt = els[i] - els[i - 1]
        dm = unwrap_diff(moon_a[i], moon_a[i - 1])
        dr = unwrap_diff(rel_a[i], rel_a[i - 1])
        log(f"  {label}: wait {els[i - 1]:.3f}->{els[i]:.3f} s: moon around planet {dm / dt:+.2f} rad/s (expected +1.00); meteor around MOON {dr / dt:+.2f} rad/s (expected {rel_expected:+.1f})")
# the wide view: planet bounding box
for label, expect_ratio in (("wide02", 16 / 9), ("wide04a1.0", 16 / 9), ("wide04a1.7778", 1.0), ("square04a1.0", 1.0)):
    p = Path(res[label]["captures"][0]["png"])
    img = load(p)
    ys, xs = np.nonzero(mask(img, PLANET))
    wpx, hpx = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    log(f"  {label}: planet is {wpx} px wide and {hpx} px tall on a {img.shape[1]} x {img.shape[0]} view: width/height {wpx / hpx:.3f} (expected {expect_ratio:.3f})")
# three moons
for ci, cap in enumerate(res["moons05"]["captures"]):
    img = load(cap["png"])
    h, w, _ = img.shape
    cx, cy = w / 2 - 0.5, h / 2 - 0.5
    ys, xs = np.nonzero(mask(img, MOON))
    angs = np.array([math.atan2(y - cy, x - cx) for x, y in zip(xs, ys)])
    # cluster by sorting angles and splitting at the two largest gaps
    order = np.sort(angs)
    gaps = np.diff(np.concatenate([order, [order[0] + math.tau]]))
    big = np.argsort(gaps)[-3:]
    cuts = sorted(big)
    groups = []
    start = 0
    for c in cuts:
        groups.append(order[start:c + 1])
        start = c + 1
    # the last group wraps around: merge its tail with the first
    if start < len(order):
        groups[0] = np.concatenate([order[start:], groups[0]])
    centers = sorted([math.degrees(math.atan2(np.sin(g).mean(), np.cos(g).mean())) % 360 for g in groups if len(g)])
    spacing = [(centers[(i + 1) % len(centers)] - centers[i]) % 360 for i in range(len(centers))]
    log(f"  moons05 capture {ci}: {len(centers)} moons at {[round(c, 1) for c in centers]} deg; gaps {[round(s, 1) for s in spacing]} (expected 120.0 each)")
# the flower: boundary radius profile, and its turn between captures
def profile(img, n=720):
    h, w, _ = img.shape
    cx, cy = w / 2 - 0.5, h / 2 - 0.5
    m = mask(img, PLANET)
    out = []
    for k in range(n):
        th = k * math.tau / n
        r_edge = 0.0
        for r in np.arange(0.3, 0.8, 0.002):
            x = cx + r * (w / 2) * math.cos(th)
            y = cy + r * (h / 2) * math.sin(th)
            if m[int(round(y)), int(round(x))]:
                r_edge = r
        out.append(r_edge)
    return np.array(out)


pngs, els = series("flower12", None)
profs = [profile(load(p)) for p in pngs]
n = len(profs[0])
for i in range(1, len(profs)):
    best, best_s = None, None
    for s in range(-n // 2, n // 2):
        e = np.abs(np.roll(profs[i - 1], s) - profs[i]).mean()
        if best is None or e < best:
            best, best_s = e, s
    # the pattern repeats every pi/4 (8 petals): take the shift modulo one petal period
    shift_rad = best_s * math.tau / n
    period = math.tau / 8
    shift_mod = (shift_rad + period / 2) % period - period / 2
    dt = els[i] - els[i - 1]
    log(f"  flower12: wait {els[i - 1]:.3f}->{els[i]:.3f} s: pattern turned {shift_mod:+.3f} rad over {dt:.3f} s = {shift_mod / dt:+.2f} rad/s (expected +1.00 clockwise); edge radius range {profs[i].min():.3f} to {profs[i].max():.3f} (expected 0.4 to 0.7)")
# petal count: local maxima of the edge-radius profile around the circle (8 expected)
prof0 = profs[0]
n0 = len(prof0)
sm = np.convolve(np.concatenate([prof0[-5:], prof0, prof0[:5]]), np.ones(5) / 5, mode="same")[5:-5]
peaks = sum(1 for i in range(n0) if sm[i] > sm[i - 1] and sm[i] >= sm[(i + 1) % n0] and sm[i] > 0.62)
log(f"  flower12: petals counted as local maxima of the edge radius above 0.62: {peaks} (expected 8)")
SUMMARY.write_text("\n".join(lines) + "\n")
