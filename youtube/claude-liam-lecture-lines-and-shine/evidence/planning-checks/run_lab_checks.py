#!/usr/bin/env python3
"""run_lab_checks.py: every Shader Lab and scene check behind FACTCHECK.md, in one re-runnable script.

What it does (about five minutes on Bear's Mac):
  * runs every shader this film shows (lab-shaders/01 to 13) through SER/lab/check_shader.sh, in the framing the captures will use:
    a 640 x 360 window, a 128 px sprite scaled 2.25 times, so the square test card is 288 x 288 px at (176, 36) on the Lab stage color;
  * reads probes and measures PNGs (band widths, band centres, line angles, pixel differences);
  * runs the two-panel scene (two_panels.gd) and the tween check (verify1.gd) in a scratch Godot project;
  * writes lab-results.jsonl (one line per Lab call), measurements.txt (every measured number and its PASS/FAIL), png/*.png.
Re-run:  python3 run_lab_checks.py          (needs godot on PATH, Pillow, and the series Lab)
Never edits anything outside this folder; the scratch project lives in /private/tmp/claude-501/godot-shaders-lines-and-shine/proj.
"""
import datetime
import json
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
SER = FILM.parent / "_godot-shaders-series"
LAB = SER / "lab" / "check_shader.sh"
SH = FILM / "lab-shaders"
SCR = HERE / "scratch-shaders"
PNGDIR = HERE / "png"
PROJ = Path("/private/tmp/claude-501/godot-shaders-lines-and-shine/proj")
JSONL = HERE / "lab-results.jsonl"
MEAS = HERE / "measurements.txt"

W, H = 640, 360
CARD = 288                # the card (sprite 128 px x 2.25) in the 640 x 360 frame
CX0, CY0 = 176, 36        # its top-left corner
CX, CY = 320, 180         # its centre
STAGE = (0.851, 0.8353, 0.7922)

OUT = []
FAILS = []


def say(s=""):
    print(s)
    OUT.append(s)


def check(name, ok, detail):
    say(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    if not ok:
        FAILS.append(name)


def lab(label, shader, args, save_png=True):
    cmd = [str(LAB), str(shader)] + list(args)
    rel_png = None
    if save_png:
        rel_png = f"png/{label}.png"
        cmd += ["--png", str(HERE / rel_png)]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    res = None
    for line in cp.stdout.splitlines():
        if line.startswith("RESULT "):
            res = json.loads(line[7:])
    rec = {"check": label, "shader": Path(shader).name, "args": list(args), "exit": cp.returncode, "png": rel_png, "result": res}
    if cp.returncode != 0 or res is None:
        rec["output"] = cp.stdout[-800:] + cp.stderr[-400:]
    with open(JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")
    if cp.returncode != 0 or res is None:
        say(f"FAIL  Lab run {label}: exit {cp.returncode}: {cp.stdout[-300:]}")
        FAILS.append(f"lab-run {label}")
    return res


CARD_ARGS = ["--kind", "sprite", "--sprite-tex", "white", "--size", "640x360"]
BLOB_ARGS = ["--kind", "sprite", "--size", "640x360"]
RECT_ARGS = ["--kind", "rect", "--size", "640x360"]


def card_pixel(u, v):
    return CX0 + int(u * CARD), CY0 + int(v * CARD)


def card_probe(u, v):
    ix, iy = card_pixel(u, v)
    return f"{(ix + 0.25) / (W - 1)},{(iy + 0.25) / (H - 1)}"


def pixel_uv(ix, iy):
    return (ix - CX0 + 0.5) / CARD, (iy - CY0 + 0.5) / CARD


def test_value(slope, u, v):
    px, py = 2 * u - 1, -(2 * v - 1)
    return py - slope * px


def rgb(res, i=0):
    return res["probes"][i]["rgba"][:3]


def load(png):
    return Image.open(png).convert("RGB")


def card_band(png, angle_deg, thresh=240, step=0.02):
    """Scan along the image-space normal (sin t, cos t) through the card centre. Returns (perpendicular width px, centre s px)."""
    im = load(png)
    px = im.load()
    th = math.radians(angle_deg)
    nx, ny = math.sin(th), math.cos(th)
    ss = []
    s = -CARD * 1.0
    while s <= CARD:
        x, y = CX + s * nx, CY + s * ny
        xi, yi = int(math.floor(x)), int(math.floor(y))
        if CX0 <= xi < CX0 + CARD and CY0 <= yi < CY0 + CARD and px[xi, yi][0] > thresh:
            ss.append(s)
        s += step
    if not ss:
        return 0.0, None
    return len(ss) * step, sum(ss) / len(ss)


def panel_band(png, centre, size, angle_deg, thresh=240, step=0.02):
    im = load(png)
    px = im.load()
    th = math.radians(angle_deg)
    nx, ny = math.sin(th), math.cos(th)
    cx, cy = centre
    half = size / 2.0
    ss = []
    s = -size * 1.0
    while s <= size:
        x, y = cx + s * nx, cy + s * ny
        xi, yi = int(math.floor(x)), int(math.floor(y))
        if cx - half <= xi < cx + half and cy - half <= yi < cy + half and px[xi, yi][0] > thresh:
            ss.append(s)
        s += step
    if not ss:
        return 0.0, None
    return len(ss) * step, sum(ss) / len(ss)


def fit_line(png, box, thresh=240):
    """Principal axis angle (degrees, counter-clockwise on screen) and mean thickness of the white band inside box = (x0, y0, x1, y1)."""
    im = load(png)
    px = im.load()
    x0, y0, x1, y1 = box
    pts = [(x + 0.5, -(y + 0.5)) for y in range(y0, y1) for x in range(x0, x1) if px[x, y][0] > thresh]
    n = len(pts)
    if n == 0:
        return None, 0.0
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts) / n
    syy = sum((p[1] - my) ** 2 for p in pts) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts) / n
    ang = 0.5 * math.atan2(2 * sxy, sxx - syy)
    ux, uy = math.cos(ang), math.sin(ang)
    across = [(-(p[0] - mx) * uy + (p[1] - my) * ux) for p in pts]
    var = sum(a * a for a in across) / n
    return math.degrees(ang), math.sqrt(12 * var)


def decode_bits(res):
    lo = [round(c * 255) for c in rgb(res, 0)]
    hi = round(rgb(res, 1)[0] * 255)
    u = lo[0] | (lo[1] << 8) | (lo[2] << 16) | (hi << 24)
    return struct.unpack("<f", struct.pack("<I", u))[0]


def run_two_panels(label, panels, probes=(), wait=4):
    cfg = {"out": str(HERE / f"png/{label}.png"), "panels": panels, "probes": list(probes), "wait_frames": wait}
    cfgp = PROJ / f"cfg-{label}.json"
    cfgp.write_text(json.dumps(cfg))
    cp = subprocess.run(["godot", "--path", str(PROJ), "--script", "res://two_panels.gd", "--", "--cfg", str(cfgp)], capture_output=True, text=True, timeout=180)
    res = None
    for line in cp.stdout.splitlines():
        if line.startswith("RESULT "):
            res = json.loads(line[7:])
    rec = {"check": label, "scene": "two_panels.gd", "cfg": cfg, "exit": cp.returncode, "png": f"png/{label}.png", "result": res}
    if res is None or "ERROR" in cp.stdout + cp.stderr:
        rec["output"] = cp.stdout[-600:] + cp.stderr[-600:]
        say(f"FAIL  scene {label}: {cp.stdout[-300:]} {cp.stderr[-300:]}")
        FAILS.append(f"scene {label}")
    with open(JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return res


def panel(shader, centre, size, kind, **uni):
    return {"shader": str(SH / shader) if (SH / shader).exists() else str(SCR / shader), "kind": kind, "center": centre, "size": size, "uniforms": uni}


def main():
    PNGDIR.mkdir(exist_ok=True)
    JSONL.write_text("")
    PROJ.mkdir(parents=True, exist_ok=True)
    for f in ("project.godot", "two_panels.gd", "verify1.gd"):
        shutil.copy(HERE / f, PROJ / f)
    shutil.copy(SH / "10-shine.gdshader", PROJ / "10-shine.gdshader")
    machine = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    ver = subprocess.run(["godot", "--version"], capture_output=True, text=True).stdout.strip()
    say("# Measurements: Lines and Shine")
    say(f"Run {datetime.date.today().isoformat()} on {machine}, Godot {ver}. Renderer Forward+ unless a line says otherwise.")
    say("Framing: Lab window 640 x 360; test card = sprite 128 px x 2.25 = 288 x 288 px at (176, 36); band widths are given as a percent of the card width.")
    say("")

    # ---------------------------------------------------------------- A. orientation and the signed test
    say("## A. Which way UV counts, and the signed test")
    r = lab("A0-uv-y-top", SCR / "uv-y.gdshader", RECT_ARGS + ["--probe", "0.5,0.0", "--probe", "0.5,1.0"], save_png=False)
    top, bottom = rgb(r, 0)[0], rgb(r, 1)[0]
    check("UV.y counts downward in canvas_item", top < 0.02 and bottom > 0.98, f"UV.y read as red: {top:.4f} at the top row, {bottom:.4f} at the bottom row of a ColorRect")

    probes = [(0.7, 0.1), (0.7, 0.4), (0.7, 0.7)]
    args = CARD_ARGS + ["--set", "slope=0.5"]
    for u, v in probes:
        args += ["--probe", card_probe(u, v)]
    r = lab("A1-signed-slope-0.5", SH / "01-signed-test.gdshader", args)
    for i, (u, v) in enumerate(probes):
        ix, iy = card_pixel(u, v)
        uu, vv = pixel_uv(ix, iy)
        expect = test_value(0.5, uu, vv)
        red, green, blue = rgb(r, i)
        measured = (red - 0.65) / 0.2
        px_, py_ = 2 * uu - 1, -(2 * vv - 1)
        check(f"signed test at p = ({px_:.2f}, {py_:.2f})", abs(measured - expect) < 0.04 and abs(green - 0.651) < 0.003,
              f"expected {expect:+.3f}, read {measured:+.3f} from red {red:.4f}, green {green:.4f}, blue {blue:.4f}")
    for s in (0.0, 1.0):
        lab(f"A2-signed-slope-{s}", SH / "01-signed-test.gdshader", CARD_ARGS + ["--set", f"slope={s}"])

    for what, name in ((1, "true distance d"), (2, "raw test |v|")):
        r = lab(f"A3-dist-map-what{what}", SCR / "dist-map.gdshader", CARD_ARGS + ["--set", "slope=0.5", "--set", f"what={what}", "--probe", card_probe(0.7, 0.1)], save_png=False)
        ix, iy = card_pixel(0.7, 0.1)
        uu, vv = pixel_uv(ix, iy)
        v = test_value(0.5, uu, vv)
        exp = abs(v) / math.sqrt(1.25) if what == 1 else abs(v)
        got = rgb(r)[0]
        check(f"{name} at p = (0.40, 0.80), slope 0.5", abs(got - exp) < 0.006, f"expected {exp:.4f} (test {v:.4f}, square root of 1.25 = {math.sqrt(1.25):.4f}), read {got:.4f}")

    # ---------------------------------------------------------------- B. tan on the GPU
    say("")
    say("## B. What the graphics card's tangent returns (bits of the float read from pixels; scratch-shaders/bits.gdshader)")
    rows = [("tan(radians(a))", 0, a) for a in (30, 45, 60, 75, 89, 89.9, 90, 90.1, 91)] + [("tan(a), no conversion", 1, 30), ("radians(a)", 2, 90), ("sqrt(1 + m*m) with m = tan(radians(a))", 3, 90)]
    tanvals = {}
    for name, mode, a in rows:
        r = lab(f"B-bits-mode{mode}-{a}", SCR / "bits.gdshader", RECT_ARGS + ["--set", f"mode={mode}", "--set", f"angle={a}", "--probe", "0.25,0.5", "--probe", "0.75,0.5"], save_png=False)
        val = decode_bits(r)
        tanvals[(mode, a)] = val
        say(f"      {name:42s} a = {a:>5}: {val:.6g}")
    r = lab("B-bits-self", SCR / "bits.gdshader", RECT_ARGS + ["--set", "mode=4", "--probe", "0.25,0.5", "--probe", "0.75,0.5"], save_png=False)
    check("self-test: the constant 1.0 decodes to 1.0", decode_bits(r) == 1.0, f"decoded {decode_bits(r)}")
    for a in (30, 45, 60, 75, 89, 89.9):
        exp = math.tan(math.radians(a))
        got = tanvals[(0, a)]
        check(f"tan(radians({a}))", abs(got - exp) / exp < 2e-3, f"GPU {got:.5f}, double-precision math {exp:.5f}")
    check("tan(30.0) without radians() is about -6.405", abs(tanvals[(1, 30)] + 6.405) < 0.01, f"GPU {tanvals[(1, 30)]:.5f} (30 radians = {30 / (2 * math.pi):.3f} turns)")
    check("radians(90.0) is the float32 nearest pi/2", abs(tanvals[(2, 90)] - 1.5707963705) < 1e-6, f"{tanvals[(2, 90)]:.10f}")
    check("tan(radians(89.9)) is large and positive, tan(radians(90.0)) large and negative", tanvals[(0, 89.9)] > 500 and tanvals[(0, 90)] < -1e6, f"89.9: {tanvals[(0, 89.9)]:.1f}; 90.0: {tanvals[(0, 90)]:.0f}; 90.1: {tanvals[(0, 90.1)]:.1f}")
    check("sqrt(1 + m*m) stays finite at 90", math.isfinite(tanvals[(3, 90)]) and tanvals[(3, 90)] > 1e6, f"{tanvals[(3, 90)]:.0f}")

    # ---------------------------------------------------------------- C. shown shaders compile and look as described
    say("")
    say("## C. Every shown shader compiles; pictures used by the captures")
    # positive angle climbs to the right after the flip: at p.y = +0.4 the zero line is at p.x = 0.4 / 0.577 = +0.693 (u = 0.846, v = 0.3);
    # at p.y = -0.4 it is at p.x = -0.693 (u = 0.154, v = 0.7). Warm (positive) above-left of it, cool below-right.
    pts = [(0.846, 0.3), (0.154, 0.7), (0.154, 0.3), (0.846, 0.7)]
    args = CARD_ARGS + ["--set", "angle=30"]
    for u, v in pts:
        args += ["--probe", card_probe(u, v)]
    r = lab("C-02-angle-30", SH / "02-angle-line.gdshader", args)
    col = [rgb(r, i) for i in range(4)]
    grey = [abs(c[0] - c[2]) < 0.03 for c in col[:2]]
    check("angle 30 draws a line climbing to the right", all(grey) and col[2][0] > col[2][2] and col[3][0] < col[3][2],
          f"zero line passes (0.846, 0.3) and (0.154, 0.7): {col[0]}, {col[1]} (grey); (0.154, 0.3) above-left is warm {col[2]}; (0.846, 0.7) below-right is cool {col[3]}")
    r = lab("C-03-no-radians-30", SH / "03-no-radians.gdshader", CARD_ARGS + ["--set", "angle=30"])
    check("03-no-radians compiles and draws", r is not None, "see png/C-03-no-radians-30.png")

    # ---------------------------------------------------------------- D. band widths
    say("")
    say("## D. Band width against angle (thickness 0.1; true full width = 2 x 0.1 / 2 = 10 percent of the card)")
    say("      angle    raw test (04)    true distance (05)      [percent of card width, measured along the perpendicular]")
    widths = {}
    for a in (0, 10, 15, 30, 45, 60, 75, 80, 85, 89, 90):
        row = []
        for shader, tag in (("04-band-raw.gdshader", "raw"), ("05-band-true.gdshader", "true")):
            lab(f"D-{tag}-{a}", SH / shader, CARD_ARGS + ["--set", f"angle={a}", "--set", "thickness=0.1"])
            w, c = card_band(HERE / f"png/D-{tag}-{a}.png", a)
            widths[(tag, a)] = 100.0 * w / CARD
            row.append(100.0 * w / CARD)
        say(f"      {a:>5}    {row[0]:6.2f} %         {row[1]:6.2f} %")
    for a in (0, 10, 15, 30, 60, 75, 80, 85, 89, 90):
        check(f"true band is 10 percent wide at {a} degrees", abs(widths[('true', a)] - 10.0) < 0.4, f"{widths[('true', a)]:.2f} %")
    check("true band at 45 degrees (corner to corner, pixel-lattice error larger)", abs(widths[('true', 45)] - 10.0) < 0.6, f"{widths[('true', 45)]:.2f} %")
    for a in (15, 45, 75):
        exp = 10.0 * math.cos(math.radians(a))
        check(f"raw band thins as cos(angle) at {a} degrees", abs(widths[('raw', a)] - exp) < 0.4, f"{widths[('raw', a)]:.2f} % (10 x cos = {exp:.2f})")
    check("raw band is under one pixel and vanishes at 89 and 90 degrees", widths[('raw', 89)] < 0.5 and widths[('raw', 90)] < 0.5, f"{widths[('raw', 89)]:.2f} % and {widths[('raw', 90)]:.2f} %")
    say("")
    say("      the same comparison in a 3840 x 2160 request (card 1728 px; the window itself is clamped to the screen height, the card is not)")
    big = {}
    for shader, tag in (("04-band-raw.gdshader", "raw"), ("05-band-true.gdshader", "true")):
        for a in (45, 75, 85, 89, 90):
            lab(f"D2-{tag}-{a}", SH / shader, ["--kind", "sprite", "--sprite-tex", "white", "--size", "3840x2160", "--set", f"angle={a}", "--set", "thickness=0.1"])
            im = load(HERE / f"png/D2-{tag}-{a}.png")
            pxs = im.load()
            th = math.radians(a)
            nx, ny = math.sin(th), math.cos(th)
            n = 0
            s_ = -1728.0
            while s_ <= 1728.0:
                x, y = 1920 + s_ * nx, 1080 + s_ * ny
                xi, yi = int(math.floor(x)), int(math.floor(y))
                if 1920 - 864 <= xi < 1920 + 864 and 1080 - 864 <= yi < 1080 + 864 and pxs[xi, yi][0] > 240:
                    n += 1
                s_ += 0.05
            big[(tag, a)] = 100.0 * (n * 0.05) / 1728
        say(f"      {tag:4s}: " + ", ".join(f"{a} deg {big[(tag, a)]:.2f} %" for a in (45, 75, 85, 89, 90)))
    check("at 4K size the raw band is a hairline at 89 degrees and gone at 90", 0.05 < big[("raw", 89)] < 0.3 and big[("raw", 90)] < 0.01, f"{big[('raw', 89)]:.2f} % and {big[('raw', 90)]:.2f} %")
    check("at 4K size the true band is 10 percent wide at every angle, including 90", all(abs(big[("true", a)] - 10.0) < 0.15 for a in (45, 75, 85, 89, 90)), ", ".join(f"{big[('true', a)]:.2f}" for a in (45, 75, 85, 89, 90)))
    # step argument order: inside the band reads 1.0 (white), outside reads 0.5 (grey)
    # card addresses (u, v): (0.5, 0.5) centre; (0.8, 0.2) is p = (0.6, 0.6) and (0.2, 0.8) is p = (-0.6, -0.6), both on the 45 degree line;
    # (0.75, 0.75) is p = (0.5, -0.5) and (0.25, 0.25) is p = (-0.5, 0.5), both far from it.
    r = lab("D-step-order", SH / "05-band-true.gdshader", CARD_ARGS + ["--set", "angle=45", "--set", "thickness=0.1", "--probe", card_probe(0.5, 0.5), "--probe", card_probe(0.8, 0.2), "--probe", card_probe(0.2, 0.8), "--probe", card_probe(0.75, 0.75), "--probe", card_probe(0.25, 0.25)])
    vals = [rgb(r, i)[0] for i in range(5)]
    check("step(d, thickness): 1 on the line, 0 away from it", vals[0] > 0.99 and vals[1] > 0.99 and vals[2] > 0.99 and abs(vals[3] - 0.502) < 0.01 and abs(vals[4] - 0.502) < 0.01,
          f"centre {vals[0]:.3f}, p = (0.6, 0.6) {vals[1]:.3f}, p = (-0.6, -0.6) {vals[2]:.3f} (all on the line: 1.0 = white); p = (0.5, -0.5) {vals[3]:.3f}, p = (-0.5, 0.5) {vals[4]:.3f} (off the line: 0.502 = grey = step gave 0)")
    check("at 45 degrees the band climbs to the right (lower left to upper right)", vals[1] > 0.99 and vals[2] > 0.99 and vals[4] < 0.6, "white at upper right and lower left, grey at upper left")
    for a in (91, 100, 120):
        lab(f"D-dir-{a}", SH / "12-direction.gdshader", CARD_ARGS + ["--set", f"angle={a}", "--set", "thickness=0.1"])
        w, c = card_band(HERE / f"png/D-dir-{a}.png", a)
        check(f"direction form keeps the band 10 percent wide at {a} degrees", abs(100 * w / CARD - 10) < 0.5, f"{100 * w / CARD:.2f} %")

    # ---------------------------------------------------------------- E. offset and centre shift
    say("")
    say("## E. Sliding the line")
    say("      offset slide (07): the band centre should sit at offset x 144 px (half the card) along the normal; width stays 10 percent")
    for ang in (0, 35, 70):
        for off in (-0.5, 0.0, 0.5):
            lab(f"E-slide-{ang}-{off}", SH / "07-slide.gdshader", CARD_ARGS + ["--set", f"angle={ang}", "--set", f"offset={off}", "--set", "thickness=0.1"])
            w, c = card_band(HERE / f"png/E-slide-{ang}-{off}.png", ang)
            exp = off * CARD / 2.0
            say(f"      angle {ang:>2}, offset {off:+.1f}: centre {c:+7.2f} px (expected {exp:+7.2f}); width {100.0 * w / CARD:5.2f} % of the card; as a fraction of the card width {abs(c) / CARD:.3f}")
            check(f"offset {off:+.1f} moves the band {abs(off) * 50:.0f} percent of the card at {ang} degrees", abs(c - exp) < 1.2 and abs(100.0 * w / CARD - 10.0) < 0.6, f"centre {c:+.2f} px vs {exp:+.2f}")
    say("      centre shift (08): shift of 0.5 along x, then along y; perpendicular movement expected x: 0.5 sin(a), y: 0.5 cos(a), times 144 px")
    for ang in (0, 45, 80):
        for label, cen in (("x", (0.5, 0.0)), ("y", (0.0, 0.5))):
            lab(f"E-center-{ang}-{label}", SH / "08-center-shift.gdshader", CARD_ARGS + ["--set", f"angle={ang}", "--set", f"center={cen[0]},{cen[1]}", "--set", "thickness=0.1"])
            w, c = card_band(HERE / f"png/E-center-{ang}-{label}.png", ang)
            th = math.radians(ang)
            exp = -(cen[1] * math.cos(th) - cen[0] * math.sin(th)) * CARD / 2.0
            check(f"centre shift along {label} at {ang} degrees", abs(c - exp) < 1.5, f"band moved {c:+.2f} px (expected {exp:+.2f}); {abs(c) / CARD * 100:.1f} percent of the card")

    # ---------------------------------------------------------------- F. the shine on the sprite
    say("")
    say("## F. The shine on the sprite (blob), angle 35, thickness 0.1")
    # a point on the band, outside the blob: p = 0.85 (cos 35, sin 35) -> card address
    ang = math.radians(35)
    ppx, ppy = 0.85 * math.cos(ang), 0.85 * math.sin(ang)
    leak_u, leak_v = (ppx + 1) / 2, (1 - ppy) / 2
    on_u, on_v = 0.5, 0.5
    cols = {}
    for shader, tag in (("09-shine-leak.gdshader", "leak"), ("10-shine.gdshader", "fixed")):
        r = lab(f"F-{tag}-0.0", SH / shader, BLOB_ARGS + ["--set", "offset=0.0", "--probe", card_probe(on_u, on_v), "--probe", card_probe(leak_u, leak_v), "--probe", card_probe(0.12, 0.12)])
        cols[tag] = [rgb(r, i) for i in range(3)]
        say(f"      {tag:5s} offset 0: blob centre {cols[tag][0]}, empty pixel on the band line (p = ({ppx:.2f}, {ppy:.2f})) {cols[tag][1]}, empty corner off the band {cols[tag][2]}")
    check("both versions put white on the blob where the band is", min(cols["leak"][0]) > 0.99 and min(cols["fixed"][0]) > 0.99, f"{cols['leak'][0]} / {cols['fixed'][0]}")
    check("the first attempt leaks onto the empty (transparent) pixels", min(cols["leak"][1]) > 0.99, f"{cols['leak'][1]} (white, solid) where the stage color {STAGE} should show")
    check("multiplying by alpha keeps the highlight on the sprite", all(abs(a - b) < 0.002 for a, b in zip(cols["fixed"][1], STAGE)), f"{cols['fixed'][1]} equals the stage color {STAGE}")
    r = lab("F-no-band-blob", SH / "10-shine.gdshader", BLOB_ARGS + ["--set", "offset=-2.0", "--probe", card_probe(0.5, 0.5)])
    check("COLOR holds the sprite's own color when fragment() starts (no band: teal blob)", abs(rgb(r)[0] - 0.3725) < 0.003 and abs(rgb(r)[1] - 0.6392) < 0.003, f"{rgb(r)} = #5FA391")
    r = lab("F-default-offset-rests", SH / "10-shine.gdshader", BLOB_ARGS + ["--probe", card_probe(0.5, 0.5)])
    check("default offset of -2.0 rests the band off the sprite", abs(rgb(r)[0] - 0.3725) < 0.003, f"centre {rgb(r)}")
    for off in (-0.6, -0.3, 0.3, 0.6):
        lab(f"F-fixed-{off}", SH / "10-shine.gdshader", BLOB_ARGS + ["--set", f"offset={off}"])
        lab(f"F-leak-{off}", SH / "09-shine-leak.gdshader", BLOB_ARGS + ["--set", f"offset={off}"])
    # clock version moves
    lab("F-clock-0.0", SH / "11-shine-clock.gdshader", BLOB_ARGS + ["--wait", "0.0"])
    lab("F-clock-0.8", SH / "11-shine-clock.gdshader", BLOB_ARGS + ["--wait", "0.8"])
    d = ImageChops.difference(load(HERE / "png/F-clock-0.0.png"), load(HERE / "png/F-clock-0.8.png")).convert("L")
    nz = sum(1 for v in d.get_flattened_data() if v > 0)
    check("the clock version moves with TIME", nz > 500, f"{nz} pixels differ between wait 0.0 s and wait 0.8 s")
    # sweep range: at offset +-1.5 (angle 35) the band must be off the sprite (the card extent along the normal is |cos| + |sin| = 1.39, band half-width 0.1)
    for off in (-1.5, 1.5):
        r = lab(f"F-blob-edge-{off}", SH / "10-shine.gdshader", BLOB_ARGS + ["--set", f"offset={off}"])
        im = load(HERE / f"png/F-blob-edge-{off}.png")
        whites = sum(1 for y in range(H) for x in range(W) if im.getpixel((x, y)) == (255, 255, 255))
        check(f"at offset {off:+.1f} the band is off the sprite", whites == 0, f"{whites} pure-white pixels")

    # ---------------------------------------------------------------- G. direction form
    say("")
    say("## G. The direction form against the slope form")
    for a in (30, 60, 89):
        lab(f"G-true-{a}", SH / "05-band-true.gdshader", CARD_ARGS + ["--set", f"angle={a}", "--set", "thickness=0.1"])
        lab(f"G-dir-{a}", SH / "12-direction.gdshader", CARD_ARGS + ["--set", f"angle={a}", "--set", "thickness=0.1"])
        diff = ImageChops.difference(load(HERE / f"png/G-true-{a}.png"), load(HERE / f"png/G-dir-{a}.png")).convert("L")
        nz = sum(1 for v in diff.get_flattened_data() if v > 0)
        check(f"direction form equals the slope form pixel for pixel at {a} degrees", nz == 0, f"{nz} of {W * H} pixels differ")
    lab("G-dir-90", SH / "12-direction.gdshader", CARD_ARGS + ["--set", "angle=90", "--set", "thickness=0.1"])
    w, c = card_band(HERE / "png/G-dir-90.png", 90)
    check("direction form at exactly 90 degrees draws a centred band 10 percent wide", abs(100 * w / CARD - 10) < 0.4 and abs(c) < 1.0, f"width {100 * w / CARD:.2f} %, centre {c:+.2f} px")
    say("      signed maps left (0.2, 0.5) and right (0.8, 0.5): red - blue > 0 means warm (positive)")
    sides = {}
    for shader, tag in (("02-angle-line.gdshader", "slope form (02)"), ("13-direction-signed.gdshader", "direction form (13)")):
        for a in (80, 89.9, 90, 90.1, 91, 100):
            r = lab(f"G-signed-{tag[:5]}-{a}", SH / shader, CARD_ARGS + ["--set", f"angle={a}", "--probe", card_probe(0.2, 0.5), "--probe", card_probe(0.8, 0.5)])
            left, right = rgb(r, 0), rgb(r, 1)
            sides[(tag, a)] = ("warm" if left[0] > left[2] else "cool", "warm" if right[0] > right[2] else "cool")
            say(f"      {tag:22s} angle {a:>5}: left {sides[(tag, a)][0]}, right {sides[(tag, a)][1]}")
    check("slope form: warm and cool swap sides between 89.9 and 90", sides[("slope form (02)", 89.9)] != sides[("slope form (02)", 90)] and sides[("slope form (02)", 90)] == sides[("slope form (02)", 90.1)], f"{sides[('slope form (02)', 89.9)]} -> {sides[('slope form (02)', 90)]} -> {sides[('slope form (02)', 90.1)]}")
    check("direction form: no swap from 80 to 100 degrees", len({sides[("direction form (13)", a)] for a in (80, 89.9, 90, 90.1, 91, 100)}) == 1, f"{sides[('direction form (13)', 90)]} throughout")

    # ---------------------------------------------------------------- H. wide shape
    say("")
    say("## H. A wide shape (a 640 x 360 ColorRect, 16:9)")
    for a in (0, 20, 45, 70):
        lab(f"H-wide-true-{a}", SH / "05-band-true.gdshader", RECT_ARGS + ["--set", f"angle={a}", "--set", "thickness=0.1"])
        ang, th = fit_line(HERE / f"png/H-wide-true-{a}.png", (0, 0, W, H))
        lab(f"H-wide-fix-{a}", SH / "06-wide-fix.gdshader", RECT_ARGS + ["--set", f"angle={a}", "--set", "thickness=0.1", "--set", "aspect=1.7778"])
        ang2, th2 = fit_line(HERE / f"png/H-wide-fix-{a}.png", (0, 0, W, H))
        say(f"      asked {a:>2} degrees: without the fix {ang:5.1f} degrees on screen, thickness about {th:5.1f} px; with p.x *= aspect {ang2:5.1f} degrees, thickness about {th2:5.1f} px")
        if a == 45:
            check("on 16:9, an address angle of 45 shows near 29 degrees", abs(ang - math.degrees(math.atan(360 / 640))) < 0.8, f"{ang:.1f} degrees (atan(360/640) = {math.degrees(math.atan(360 / 640)):.1f})")
        check(f"with the aspect fix the screen angle equals the asked angle at {a} degrees", abs(ang2 - a) < 0.7, f"{ang2:.1f}")
        check(f"with the aspect fix the thickness is constant at {a} degrees", abs(th2 - 36.0) < 0.8, f"{th2:.1f} px (expected 2 x 0.1 x 180 = 36)")

    # ---------------------------------------------------------------- I. two-panel scenes (the compare captures)
    say("")
    say("## I. The two-panel scenes the compare captures use (two_panels.gd; card 256 px at (170, 190) and (470, 190); wide 304 x 171 at (160, 180) and (480, 180))")
    CL, CR = [170, 190], [470, 190]
    WL, WR = [160, 180], [480, 180]
    r = run_two_panels("I-radians-30", [panel("02-angle-line.gdshader", CL, [256, 256], "card", angle=30.0), panel("03-no-radians.gdshader", CR, [256, 256], "card", angle=30.0)])
    say(f"      radians scene rendered on {r['renderer']}")
    for a in (15, 45, 75, 85):
        run_two_panels(f"I-bands-{a}", [panel("04-band-raw.gdshader", CL, [256, 256], "card", angle=float(a), thickness=0.1), panel("05-band-true.gdshader", CR, [256, 256], "card", angle=float(a), thickness=0.1)])
        wl, _ = panel_band(HERE / f"png/I-bands-{a}.png", CL, 256, a)
        wr, _ = panel_band(HERE / f"png/I-bands-{a}.png", CR, 256, a)
        say(f"      angle {a:>2}: raw {100 * wl / 256:5.2f} % of the card, true {100 * wr / 256:5.2f} %")
        check(f"two-panel band widths at {a} degrees match the Lab card", abs(100 * wr / 256 - 10) < 0.6 and abs(100 * wl / 256 - 10 * math.cos(math.radians(a))) < 0.6, f"raw {100 * wl / 256:.2f} %, true {100 * wr / 256:.2f} %")
    for cx in (-0.6, 0.0, 0.6):
        run_two_panels(f"I-center-{cx}", [panel("08-center-shift.gdshader", CL, [256, 256], "card", angle=0.0, thickness=0.1, center=[cx, 0.0]), panel("07-slide.gdshader", CR, [256, 256], "card", angle=0.0, thickness=0.1, offset=cx)])
        wl, cl = panel_band(HERE / f"png/I-center-{cx}.png", CL, 256, 0)
        wr, cr = panel_band(HERE / f"png/I-center-{cx}.png", CR, 256, 0)
        say(f"      flat line, shift {cx:+.1f}: centre-shift panel band centre {cl:+6.1f} px, offset panel band centre {cr:+6.1f} px")
        check(f"flat line: shifting the centre along x does nothing (shift {cx:+.1f})", abs(cl) < 1.0, f"{cl:+.2f} px")
        check(f"flat line: the offset slides it (offset {cx:+.1f})", abs(cr - cx * 128) < 1.5, f"{cr:+.2f} px vs {cx * 128:+.1f}")
    for off in (-0.6, -0.1, 0.4):
        r = run_two_panels(f"I-leak-{off}", [panel("09-shine-leak.gdshader", CL, [256, 256], "blob", angle=35.0, thickness=0.1, offset=off), panel("10-shine.gdshader", CR, [256, 256], "blob", angle=35.0, thickness=0.1, offset=off)])
    for a in (20, 45, 70):
        run_two_panels(f"I-wide-{a}", [panel("05-band-true.gdshader", WL, [304, 171], "wide", angle=float(a), thickness=0.1), panel("06-wide-fix.gdshader", WR, [304, 171], "wide", angle=float(a), thickness=0.1, aspect=1.7778)])
        a1, t1 = fit_line(HERE / f"png/I-wide-{a}.png", (8, 94, 312, 266))
        a2, t2 = fit_line(HERE / f"png/I-wide-{a}.png", (328, 94, 632, 266))
        say(f"      wide panels, asked {a:>2}: left {a1:5.1f} degrees on screen (thickness {t1:5.1f} px), right with the fix {a2:5.1f} degrees ({t2:5.1f} px)")
        if a == 45:
            check("two-panel wide scene: 45 asked, about 29 shown without the fix, 45 with it", abs(a1 - 29.4) < 1.2 and abs(a2 - 45) < 1.5, f"{a1:.1f} and {a2:.1f}")
    # the comparison at the seam
    for a in (89.9, 90.0, 91.0):
        run_two_panels(f"I-seam-{a}", [panel("02-angle-line.gdshader", CL, [256, 256], "card", angle=a), panel("13-direction-signed.gdshader", CR, [256, 256], "card", angle=a)],
                       probes=[[110, 190], [230, 190], [410, 190], [530, 190]])
    # sign check inside the two-panel scene
    seam = {}
    for a in (89.9, 90.0, 91.0):
        res = None
        for line in (HERE / "lab-results.jsonl").read_text().splitlines():
            rec = json.loads(line)
            if rec["check"] == f"I-seam-{a}":
                res = rec["result"]
        pr = res["probes"]
        seam[a] = [("warm" if p["rgba"][0] > p["rgba"][2] else "cool") for p in pr]
        say(f"      seam panels at {a}: slope form left/right {seam[a][0]}/{seam[a][1]}; direction form left/right {seam[a][2]}/{seam[a][3]}")
    check("two-panel seam scene: slope form swaps at 90, direction form does not", seam[89.9][:2] != seam[90.0][:2] and seam[89.9][2:] == seam[90.0][2:] == seam[91.0][2:], f"{seam}")

    # ---------------------------------------------------------------- J. Compatibility renderer
    say("")
    say("## J. The same shaders in the Compatibility renderer (gl_compatibility)")
    comp = [("01-signed-test.gdshader", CARD_ARGS + ["--set", "slope=0.5", "--probe", card_probe(0.7, 0.1), "--probe", card_probe(0.7, 0.7)]),
            ("05-band-true.gdshader", CARD_ARGS + ["--set", "angle=90", "--probe", card_probe(0.5, 0.5), "--probe", card_probe(0.8, 0.2)]),
            ("10-shine.gdshader", BLOB_ARGS + ["--set", "offset=0.0", "--probe", card_probe(0.5, 0.5), "--probe", card_probe(leak_u, leak_v)]),
            ("09-shine-leak.gdshader", BLOB_ARGS + ["--set", "offset=0.0", "--probe", card_probe(0.5, 0.5), "--probe", card_probe(leak_u, leak_v)]),
            ("12-direction.gdshader", CARD_ARGS + ["--set", "angle=90", "--probe", card_probe(0.5, 0.5), "--probe", card_probe(0.8, 0.2)]),
            ("13-direction-signed.gdshader", CARD_ARGS + ["--set", "angle=35", "--probe", card_probe(0.2, 0.2), "--probe", card_probe(0.8, 0.8)])]
    for shader, args in comp:
        a = lab(f"J-fp-{shader[:2]}", SH / shader, args, save_png=False)
        b = lab(f"J-compat-{shader[:2]}", SH / shader, args + ["--renderer", "gl_compatibility"], save_png=False)
        gradient = shader[:2] in ("01", "13")      # smooth maps: allow one level of 8-bit rounding between renderers
        tol = 1.0 / 255 + 1e-4 if gradient else 1e-6
        diffs = [abs(x - y) for p, q in zip(a["probes"], b["probes"]) for x, y in zip(p["rgba"], q["rgba"])]
        same = a is not None and b is not None and max(diffs) <= tol
        check(f"{shader}: same pixels in {a['renderer']} and {b['renderer']}" + (" (to one level of 255)" if gradient else ""), same,
              f"largest channel difference {max(diffs):.4f}; {[p['rgba'][:3] for p in a['probes']]} vs {[p['rgba'][:3] for p in b['probes']]}")
    seam_c = {}
    for ang in (89.9, 90.0):
        for rend in ("forward_plus", "gl_compatibility"):
            r = lab(f"J-seam-{rend[:3]}-{ang}", SH / "02-angle-line.gdshader", CARD_ARGS + ["--set", f"angle={ang}", "--probe", card_probe(0.2, 0.5), "--probe", card_probe(0.8, 0.5)] + ["--renderer", rend], save_png=False)
            seam_c[(rend, ang)] = ["warm" if rgb(r, i)[0] > rgb(r, i)[2] else "cool" for i in range(2)]
    check("the seam at 90 degrees is the same in both renderers", seam_c[("forward_plus", 89.9)] == seam_c[("gl_compatibility", 89.9)] and seam_c[("forward_plus", 90.0)] == seam_c[("gl_compatibility", 90.0)] and seam_c[("forward_plus", 89.9)] != seam_c[("forward_plus", 90.0)], f"{seam_c}")

    # ---------------------------------------------------------------- K. GDScript-side: the tween code shown in the film
    say("")
    say("## K. The tween code shown in the film (verify1.gd: Forward+, scratch project)")
    cp = subprocess.run(["godot", "--path", str(PROJ), "--script", "res://verify1.gd"], capture_output=True, text=True, timeout=180)
    (HERE / "run-1-verify1.log").write_text(cp.stdout + cp.stderr)
    say("      full log: run-1-verify1.log")
    t1 = None
    for line in cp.stdout.splitlines():
        if line.startswith("RESULT ") and '"T1-' in line:
            t1 = json.loads(line[7:])
    if t1:
        check("the film's tween code sweeps the band across the sprite once", t1["white_frames"] >= 3 and 0.33 < t1["first_white_s"] < 0.47 and abs(t1["offset_at_end"] - 1.5) < 0.01,
              f"centre white from {t1['first_white_s']} s to {t1['last_white_s']} s after the call (expected near 0.373 to 0.427 s); offset at end {t1['offset_at_end']}; offset before any set: {t1['offset_before_any_set']}")
    check("a tween on a uniform never set from code fails", "does not exist" in cp.stdout + cp.stderr, "engine error: The tweened property \"shader_parameter/offset\" does not exist")

    say("")
    say(f"## Result: {len(FAILS)} failed checks" + ("" if not FAILS else ": " + ", ".join(FAILS)))
    MEAS.write_text("\n".join(OUT) + "\n")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
