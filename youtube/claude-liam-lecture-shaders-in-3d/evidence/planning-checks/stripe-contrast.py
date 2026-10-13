#!/usr/bin/env python3
"""stripe-contrast.py: how visible are the pad's stripes at each activation, and how close is the dark stripe to the ink color (GATE T)?
Reads lab-results.jsonl and lab-results-extra.jsonl (the Lab's own probes of the dark stripe centre, UV.x 0.03125, and the light stripe centre, 0.09375).
Prints, per renderer and activation: both stripe colors in 8 bits, the CIE76 color difference between them (dE76; about 2.3 is the smallest step an
eye notices side by side, 5 and up reads clearly), the lightness difference, and the dark stripe's distance from ink #3D3929 (largest single channel and sum).
Run:  python3 -I stripe-contrast.py > stripe-contrast.txt
"""
import json, math, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = []
for name in ("lab-results.jsonl", "lab-results-extra.jsonl"):
    rows += [json.loads(l) for l in (HERE / name).read_text().splitlines()]


def probes(check):
    for r in rows:
        if r["check"] == check:
            d = json.loads(re.search(r"RESULT (\{.*\})", r["output"]).group(1))
            return [p["rgba"][:3] for p in d["probes"]]
    return None


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lab(rgb):
    r, g, b = [lin(c) for c in rgb]
    X, Y, Z = 0.4124 * r + 0.3576 * g + 0.1805 * b, 0.2126 * r + 0.7152 * g + 0.0722 * b, 0.0193 * r + 0.1192 * g + 0.9505 * b
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(X / 0.95047), f(Y), f(Z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(lab(a), lab(b))))


INK = (61 / 255, 57 / 255, 41 / 255)
print("dark = stripe centre UV.x 0.03125, light = 0.09375; Godot 4.7.2, Apple M4 Pro, unshaded pad shader on the Lab quad")
print(f"{'renderer':17s}{'act':>5s}  {'dark (8-bit)':17s} {'light (8-bit)':17s} {'dE76':>5s} {'dL*':>5s}   dark to ink: largest channel / sum")
for rend in ("forward_plus", "gl_compatibility", "mobile"):
    for a in ("0.0", "0.25", "0.3", "0.5", "0.75"):
        p = probes(f"12-signal-pad-{rend}-{a}")
        if not p:
            continue
        dark, light = p[0], p[1]
        d8 = tuple(round(c * 255) for c in dark)
        l8 = tuple(round(c * 255) for c in light)
        linf = max(abs(x - y) * 255 for x, y in zip(dark, INK))
        l1 = sum(abs(x - y) * 255 for x, y in zip(dark, INK))
        print(f"{rend:17s}{a:>5s}  {str(d8):17s} {str(l8):17s} {de(dark, light):5.1f} {lab(light)[0] - lab(dark)[0]:5.1f}   {linf:5.0f} / {l1:5.0f}")
