#!/usr/bin/env python3
"""decode_scenes2.py: reads the Movie Maker PNG frames of the Act II to V scenes and checks what they show against the formulas (TIME decoded from the verification-only encoder)."""
import glob, math
from PIL import Image
import numpy as np

TEAL = (0.37, 0.64, 0.57); CREAM = (0.98, 0.97, 0.96)
def mixc(p): return tuple(255 * (a * (1 - p) + b * p) for a, b in zip(TEAL, CREAM))
def frames(name): return sorted(glob.glob(f"frames_{name}/f*.png"))
def time_of(im):
    r, g, b = im.getpixel((10, 10)); return r + (g + b / 255.0) / 255.0
def maxdiff(c1, c2): return max(abs(a - b) for a, b in zip(c1, c2))
def curve(x):
    # the breath curve through (0,0) (0.4,1) (0.55,1) (1,0) with flat tangents: cubic Hermite between points (what Curve.sample does for tangent 0); used for a coarse check only
    pts = [(0.0, 0.0), (0.40, 1.0), (0.55, 1.0), (1.0, 0.0)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + (y1 - y0) * (3 * t * t - 2 * t * t * t)
    return 0.0

# ---- C18: five squares, instance offsets
ims = [Image.open(f).convert("RGB") for f in frames("c18_rolling_row")]
ts = [time_of(im) for im in ims]
worst = 0.0
for i in range(10, len(ims)):
    for k in range(5):
        x = int(640 * (0.18 + 0.16 * k)); y = 180
        worst = max(worst, maxdiff(ims[i].getpixel((x, y)), mixc(0.5 + 0.5 * math.sin(2 * math.pi * (ts[i] * 0.5 + k / 5.0)))))
print("C18 five squares vs formula 0.5+0.5 sin(TAU (TIME*0.5 + i/5)) over %d frames: at most %.1f steps" % (len(ims) - 10, worst))
brightest = []
for i in (60, 72, 84, 96, 108):
    vals = [ims[i].getpixel((int(640 * (0.18 + 0.16 * k)), 180))[0] for k in range(5)]
    brightest.append((i, vals, int(np.argmax(vals))))
print("C18 red channel of the five squares at frames 60..108 and the brightest square:", brightest)

# ---- C23: curve loop
ims = [Image.open(f).convert("RGB") for f in frames("c23_curve_loop")]
ts = [time_of(im) for im in ims]
worst = 0.0
for i in range(10, len(ims)):
    t = (ts[i] * 0.5) % 1.0
    worst = max(worst, maxdiff(ims[i].getpixel((320, 180)), mixc(curve(t))))
print("C23 square vs the breath curve (Hermite model) at fract(TIME*0.5): at most %.1f steps over %d frames" % (worst, len(ims) - 10))
print("C23 red channel at frames 0, 15, 30, 45, 60, 90, 119 (one loop = 60 frames):", [ims[i].getpixel((320, 180))[0] for i in (0, 15, 30, 45, 60, 90, 119)])

# ---- C35: together / logo / banner
def teal_extent_row(im, y, x0=0, x1=640):
    row = np.asarray(im)[y, x0:x1].astype(int)
    m = (abs(row[:, 0] - 95) < 8) & (abs(row[:, 1] - 163) < 8) & (abs(row[:, 2] - 145) < 8)
    xs = np.where(m)[0]
    return (xs.min() + x0, xs.max() + x0) if len(xs) else None
for part, ycen in (("together", int(0.30 * 360)), ("logo", 180)):
    ims = [Image.open(f).convert("RGB") for f in frames(f"c35_together_{part}")]
    ts = [time_of(im) for im in ims]
    widths = []
    worst = 0.0
    for i in range(10, len(ims)):
        e = teal_extent_row(ims[i], ycen, 100, 540)
        w = e[1] - e[0] + 1 if e else 0
        k = curve((ts[i] * 0.4) % 1.0)
        want = 76.8 * (0.5 * 360 / 128.0) * (1 + 0.25 * k)
        worst = max(worst, abs(w - want))
        widths.append(w)
    print("C35 %s: logo width ranges %d..%d px, within %.1f px of 76.8*scale*(1+0.25 k) (Hermite model of the curve)" % (part, min(widths), max(widths), worst))

def banner_waviness(im, cx, cy, width_px, ignore_above=None):
    """peak-to-peak vertical movement of the banner's top edge across its width (pixels)"""
    a = np.asarray(im).astype(int)
    a[: int(ignore_above if ignore_above is not None else cy - 100)] = 255          # ignore everything above the banner (the logo)
    x0 = int(cx - width_px / 2) + 4; x1 = int(cx + width_px / 2) - 4
    tops = []
    for x in range(x0, x1):
        col = a[:, x]
        m = (abs(col[:, 0] - 95) < 10) & (abs(col[:, 1] - 163) < 10) & (abs(col[:, 2] - 145) < 10)
        ys = np.where(m)[0]
        if len(ys): tops.append(ys.min())
    return int(max(tops) - min(tops)) if tops else None
ims = [Image.open(f).convert("RGB") for f in frames("c35_together_banner")]
print("C35 banner alone: top edge peak-to-peak (px) at frames 30, 90, 150, 240, 290:", [banner_waviness(ims[i], 320, 180, 0.55 * 640) for i in (30, 90, 150, 240, 290)])

# ---- C40: the click
ims = [Image.open(f).convert("RGB") for f in frames("c40_wind_click")]
series = [(i, banner_waviness(ims[i], 320, 180, 0.55 * 640)) for i in (60, 120, 134, 136, 140, 160, 180, 200, 220, 240, 255, 260, 300, 400)]
print("C40 banner top edge peak-to-peak (px): frame, value ->", series)

# ---- the banner has transparent margin, so a ripple repeats an empty edge row and nothing smears: the longest vertical teal run in any column is one stripe
ims_b = [Image.open(f).convert("RGB") for f in frames("c35_together_banner")]
maxrun = 0
for im in ims_b[10:300:5]:
    a = np.asarray(im).astype(int)
    teal = (abs(a[:, :, 0] - 95) < 10) & (abs(a[:, :, 1] - 163) < 10) & (abs(a[:, :, 2] - 145) < 10)
    for x in range(140, 500):
        run = 0
        for v in teal[:, x]:
            run = run + 1 if v else 0
            maxrun = max(maxrun, run)
print(f"C35 banner alone: longest vertical teal run in any column over 58 frames is {maxrun} px; one stripe is 24 rows x 1.375 = 33 px, so nothing is stretched")

# ---- C28: the stripes slide right at speed 0.5, then left after the step at frame 330
fs28 = sorted(glob.glob("frames_c28_travel/f*.png"))
def crest28(i, y=180):
    a = np.asarray(Image.open(fs28[i]).convert("RGB")).astype(int)
    return int(np.argmax(a[y, 30:, 0])) + 30
def move28(a, b):
    xs = [crest28(i) for i in range(a, b)]
    d = [xs[j + 1] - xs[j] for j in range(len(xs) - 1)]
    d = [v if abs(v) < 100 else (v - 213 if v > 0 else v + 213) for v in d]
    return sum(d) / len(d)
print(f"C28 crest movement in pixels per frame (640 px wide frame; 0.5 of the width per second = 10.67): speed 0.5 {move28(100, 110):+.2f}, after the step to -0.5 {move28(340, 350):+.2f}")
