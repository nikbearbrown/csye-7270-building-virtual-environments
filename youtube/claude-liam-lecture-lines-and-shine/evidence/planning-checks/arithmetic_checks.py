#!/usr/bin/env python3
"""arithmetic_checks.py: the numbers the film speaks or shows that follow from arithmetic or geometry alone (no Godot).
Writes arithmetic.txt next to this file. Re-run: python3 arithmetic_checks.py
"""
import math
from pathlib import Path

out = []


def line(s=""):
    print(s)
    out.append(s)


def check(name, ok, detail):
    line(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    return ok


ok = True
line("# Arithmetic and geometry cross-checks: Lines and Shine")
line()
# B06, B07: the test y - m x at three points for slope one half, and along a parallel line
m = 0.5
pts = [(0.4, 0.2), (0.4, 0.8), (0.4, -0.4)]
vals = [y - m * x for x, y in pts]
ok &= check("B06 three points, slope 0.5", all(abs(a - b) < 1e-12 for a, b in zip(vals, [0.0, 0.6, -0.6])), f"{vals}")
ok &= check("B07 along the parallel line y = 0.5x + 0.6 the test is 0.6 everywhere", all(abs((0.5 * x + 0.6) - m * x - 0.6) < 1e-12 for x in (-1, -0.3, 0.2, 0.9)), "y - m x = 0.6 at x = -1, -0.3, 0.2, 0.9")
# B10: tangent is rise per step across
for a in (30, 45, 60):
    line(f"      tan({a} degrees) = {math.tan(math.radians(a)):.5f}")
ok &= check("B10 tangent = height at one step across", abs(math.tan(math.radians(45)) - 1.0) < 1e-12, "tan 45 = 1")
# B11: full turn
ok &= check("B11 a full turn is about 6.28 radians", abs(2 * math.pi - 6.2832) < 1e-4, f"{2 * math.pi:.4f}")
# B12: tan(30 radians)
ok &= check("B12 thirty radians gives a slope of about -6.4", abs(math.tan(30.0) + 6.405331) < 1e-5, f"tan(30.0) = {math.tan(30.0):.6f}; 30 radians = {30 / (2 * math.pi):.3f} turns")
# B13: slopes toward ninety
for a in (45, 75, 89, 89.9):
    line(f"      tan({a} degrees) = {math.tan(math.radians(a)):.4f}")
# B17: raw band width = full width x cos(angle); full width = 2 x thickness / 2 (the address spans 2) = 10 percent of the card
for a in (0, 15, 45, 75, 85, 89):
    line(f"      raw band at {a:>2} degrees: {10 * math.cos(math.radians(a)):.2f} percent of the card (true band: 10.00)")
# B18: shortest distance for a straight-up gap of 0.6
for a in (0, 45, 60):
    line(f"      straight-up gap 0.6 at {a} degrees: shortest distance {0.6 * math.cos(math.radians(a)):.3f}")
ok &= check("B18 numbers 0.60, 0.42, 0.30", [round(0.6 * math.cos(math.radians(a)), 2) for a in (0, 45, 60)] == [0.6, 0.42, 0.3], "0.60, 0.42, 0.30")
# B19: the triangle and the divide
h = math.sqrt(1 + 0.5 ** 2)
ok &= check("B19 long side of the 1, 0.5 triangle is 1.118; 0.6 / 1.118 = 0.54", abs(h - 1.1180) < 1e-4 and abs(0.6 / h - 0.5367) < 1e-4, f"sqrt(1.25) = {h:.4f}; 0.6 / {h:.4f} = {0.6 / h:.4f}")
# the shortest distance from (0.4, 0.8) to the line y = 0.5 x by projection
d_direct = abs(0.8 - 0.5 * 0.4) / math.hypot(1, 0.5)
ok &= check("B19 the same distance by projection onto the normal", abs(d_direct - 0.6 / h) < 1e-12, f"{d_direct:.4f}")
# B20: thickness 0.1 each side, address spans 2 across: band is 0.2 / 2 = 10 percent of the card
ok &= check("B20 thickness 0.1 gives a band a tenth of the card wide", abs(2 * 0.1 / 2.0 - 0.10) < 1e-12, "2 x 0.1 / 2 = 0.10")
# B22: offset 0.5 in address units is a quarter of the card width (the address spans 2)
ok &= check("B22 offset 0.5 is a quarter of the card", abs(0.5 / 2.0 - 0.25) < 1e-12, "0.5 / 2 = 0.25")
# B30: 45 degrees in the address on a 16:9 shape
ok &= check("B30 on 16:9, a 45 degree address line is about 29 degrees on screen", abs(math.degrees(math.atan(9 / 16)) - 29.36) < 0.01, f"atan(9/16) = {math.degrees(math.atan(9 / 16)):.2f} degrees")
# B33: the divide is a disguised cosine
for mm in (0.5, 1.0, 3.7):
    th = math.atan(mm)
    ok &= check(f"B33 cosine = 1 / sqrt(1 + m^2) at m = {mm}", abs(math.cos(th) - 1 / math.sqrt(1 + mm * mm)) < 1e-12 and abs(math.sin(th) - mm / math.sqrt(1 + mm * mm)) < 1e-12, f"cos = {math.cos(th):.6f}, sin = {math.sin(th):.6f}")
p = (0.4, 0.8)
for a in (20, 35, 70):
    th = math.radians(a)
    mm = math.tan(th)
    slope_form = (p[1] - mm * p[0]) / math.sqrt(1 + mm * mm)
    dir_form = p[0] * (-math.sin(th)) + p[1] * math.cos(th)
    ok &= check(f"B33 (y - m x) / sqrt(1 + m^2) equals dot(p, n) at {a} degrees", abs(slope_form - dir_form) < 1e-12, f"{slope_form:.6f} = {dir_form:.6f}")
line()
line("## Result: " + ("all arithmetic checks pass" if ok else "SOME FAILED"))
(Path(__file__).resolve().parent / "arithmetic.txt").write_text("\n".join(out) + "\n")
