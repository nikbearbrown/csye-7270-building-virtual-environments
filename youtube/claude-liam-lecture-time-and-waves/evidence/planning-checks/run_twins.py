#!/usr/bin/env python3
"""run_twins.py: pixel-probe checks of the shaders in ../../lab-shaders/ against formulas, in real Godot 4.7.2 (the Shader Lab).

See twin_lib.py for what a twin is (the shown shader with TIME replaced by a uniform `tv`). Each check renders a twin at chosen values
and compares the probed pixels with the formula computed here in Python, within about one 8-bit step.
Writes twin-results.jsonl and twin-summary.txt; exit code 1 if any check fails.   Usage: python3 run_twins.py
"""
import math
import sys

import twin_lib as L

TAU = L.TAU
TEAL, CREAM, TRACK = L.TEAL, L.CREAM, L.TRACK
check, pulse_color = L.check, L.pulse_color

# ---- 01-age: the same pulse counted from a uniform instead of TIME
for age in (0.0, 0.25, 0.5, 0.75, 3.0):
    p = 0.5 + 0.5 * math.sin(TAU * age)
    check(f"01-age age={age}", "01-age.gdshader", ["--kind", "rect", "--set", f"age={age}"], [((0.5, 0.5), pulse_color(p))])

# ---- 02-pulse: 0.5 + 0.5 sin(TAU t); the period is exactly one second (t and t + 1 agree)
for tv in (0.0, 0.125, 0.25, 0.5, 0.75, 1.25, 7.25):
    p = 0.5 + 0.5 * math.sin(TAU * tv)
    check(f"02-pulse tv={tv}", "02-pulse.gdshader", ["--kind", "rect", "--set", f"tv={tv}"], [((0.5, 0.5), pulse_color(p))])

# ---- 03-dials: 0.5 + amplitude * sin(TAU * (t * speed + offset))
cases = [dict(a=0.5, s=0.5, o=0.0, tv=0.5), dict(a=0.5, s=0.5, o=0.0, tv=1.0), dict(a=0.25, s=0.5, o=0.0, tv=0.5),
         dict(a=0.0, s=0.5, o=0.0, tv=0.5), dict(a=0.5, s=2.0, o=0.0, tv=0.125), dict(a=0.5, s=0.5, o=0.25, tv=0.0),
         dict(a=0.5, s=0.5, o=0.5, tv=0.5), dict(a=0.5, s=0.5, o=0.5, tv=1.0), dict(a=0.5, s=1.0, o=0.2, tv=0.3)]
for c in cases:
    p = 0.5 + c["a"] * math.sin(TAU * (c["tv"] * c["s"] + c["o"]))
    check(f"03-dials amplitude={c['a']} speed={c['s']} offset={c['o']} tv={c['tv']}", "03-dials.gdshader",
          ["--kind", "rect", "--set", f"amplitude={c['a']}", "--set", f"speed={c['s']}", "--set", f"offset={c['o']}", "--set", f"tv={c['tv']}"],
          [((0.5, 0.5), pulse_color(p))])

# offset 0.5 is exactly opposite: the two pulse values add up to 1 at every time
for tv in (0.0, 0.1, 0.37, 0.6):
    p0 = 0.5 + 0.5 * math.sin(TAU * (tv * 0.5))
    p1 = 0.5 + 0.5 * math.sin(TAU * (tv * 0.5 + 0.5))
    assert abs(p0 + p1 - 1.0) < 1e-9
    check(f"03-dials opposite pair, offset 0.5, tv={tv} (the first copy would read {p0:.3f}, this one {p1:.3f})", "03-dials.gdshader",
          ["--kind", "rect", "--set", "offset=0.5", "--set", f"tv={tv}"], [((0.5, 0.5), pulse_color(p1))])

# the period of a pulse is 1 / speed seconds: speed 2 repeats every 0.5 s, speed 0.5 every 2 s
for s, per in ((2.0, 0.5), (0.5, 2.0)):
    a = 0.5 + 0.5 * math.sin(TAU * (0.3 * s))
    b = 0.5 + 0.5 * math.sin(TAU * ((0.3 + per) * s))
    assert abs(a - b) < 1e-9
    check(f"03-dials period {per} s at speed {s}: tv = 0.3 + period reads the same as tv = 0.3", "03-dials.gdshader",
          ["--kind", "rect", "--set", f"speed={s}", "--set", f"tv={0.3 + per}"], [((0.5, 0.5), pulse_color(a))])


# ---- 04-three-shapes: where each bar ends is the sine, triangle or sawtooth value at tv
def shapes(tv):
    cycles = tv * 0.5
    saw = cycles - math.floor(cycles)
    tri = 1.0 - abs(saw * 2.0 - 1.0)
    sine = 0.5 + 0.5 * math.sin(TAU * (cycles - 0.25))
    return sine, tri, saw


ROW_Y = {"sine": 0.17, "tri": 0.5, "saw": 0.83}
for tv in (0.5, 1.0, 1.5, 1.9):
    sine, tri, saw = shapes(tv)
    exp = []
    for name, v in (("sine", sine), ("tri", tri), ("saw", saw)):
        y = ROW_Y[name]
        # 0.03 inside the edge is the teal bar; 0.03 outside it is the light track
        if v - 0.03 > 0.01:
            exp.append(((v - 0.03, y), TEAL))
        if v + 0.03 < 0.99:
            exp.append(((v + 0.03, y), TRACK))
    check(f"04-three-shapes tv={tv}: sine {sine:.2f} triangle {tri:.2f} sawtooth {saw:.2f}", "04-three-shapes.gdshader",
          ["--kind", "rect", "--set", f"tv={tv}"], exp, tol=1.5)

# ---- 05-curve-loop with the Lab's identity ramp (red = x) standing in for the curve strip
for tv in (0.0, 0.5, 1.0, 1.4):
    t = (tv * 0.5) % 1.0
    check(f"05-curve-loop identity strip, tv={tv}: reads the strip at fract(TIME * 0.5) = {t:.2f}", "05-curve-loop.gdshader",
          ["--kind", "rect", "--tex", "curve=gradient", "--set", f"tv={tv}"], [((0.5, 0.5), pulse_color(t))], tol=2.0)

# ---- 06-stripes: frozen stripes; frequency is the number of cycles (bright stripes) across the shape
for freq in (2.0, 3.0, 5.0):
    exp = []
    for k in range(0, 8):
        c = (0.25 + k) / freq
        if 0.02 < c < 0.98:
            exp.append(((c, 0.5), CREAM))
        tr = (0.75 + k) / freq
        if 0.02 < tr < 0.98:
            exp.append(((tr, 0.5), TEAL))
    n_crests = len([1 for k in range(0, 12) if 0 < (0.25 + k) / freq < 1.0])
    assert n_crests == int(freq), (freq, n_crests)
    check(f"06-stripes frequency={freq}: {int(freq)} bright stripes, crests at (0.25 + k) / frequency", "06-stripes.gdshader",
          ["--kind", "rect", "--set", f"frequency={freq}"], exp, tol=2.0)


# ---- 07-travel: crests at x = speed * t + (0.25 + k) / frequency, whatever the frequency
def travel_expect(freq, speed, tv):
    crests = []
    k = -8
    while True:
        xc = speed * tv + (0.25 + k) / freq
        if xc > 1.0:
            break
        if 0.02 < xc < 0.98:
            crests.append(xc)
        k += 1
    troughs = [c + 0.5 / freq for c in crests if 0.02 < c + 0.5 / freq < 0.98]
    return [((c, 0.5), CREAM) for c in crests] + [((tr, 0.5), TEAL) for tr in troughs]


for freq, speed, tv in ((3.0, 0.5, 0.0), (3.0, 0.5, 0.4), (3.0, 0.0, 0.4), (1.0, 0.5, 0.6), (2.0, 0.5, 0.6), (5.0, 0.5, 0.6), (3.0, -0.5, 0.4), (3.0, 1.0, 0.4)):
    check(f"07-travel frequency={freq} speed={speed} tv={tv}: crests at speed * t + (0.25 + k) / frequency", "07-travel.gdshader",
          ["--kind", "rect", "--set", f"frequency={freq}", "--set", f"speed={speed}", "--set", f"tv={tv}"], travel_expect(freq, speed, tv), tol=2.0)

# ---- 08-rings: distance from the middle in place of the address across. A square sprite (288 px of a 640 x 360 window) so the rings are circles.
# along the +x axis from the centre: window x = 0.5 + 0.45 r, window y = 0.5, r in UV units (0 at the middle, 0.5 at the edge)
def rings_expect(freq, speed, tv):
    exp = []
    for k in range(-4, 6):
        rc = speed * tv + (0.25 + k) / freq          # a crest
        rt = speed * tv + (0.75 + k) / freq          # a trough
        if 0.03 < rc < 0.47:
            exp.append(((0.5 + 0.45 * rc, 0.5), CREAM))
        if 0.03 < rt < 0.47:
            exp.append(((0.5 + 0.45 * rt, 0.5), TEAL))
    return exp


for freq, speed, tv in ((4.0, 0.25, 0.0), (4.0, 0.25, 0.8), (4.0, 0.25, 2.0), (6.0, 0.25, 0.8), (4.0, 0.5, 0.8)):
    check(f"08-rings frequency={freq} speed={speed} tv={tv}: ring radii at speed * t + (0.25 + k) / frequency", "08-rings.gdshader",
          ["--kind", "sprite", "--sprite-tex", "white", "--set", f"frequency={freq}", "--set", f"speed={speed}", "--set", f"tv={tv}"],
          rings_expect(freq, speed, tv), tol=2.5)

sys.exit(L.finish("twin"))
