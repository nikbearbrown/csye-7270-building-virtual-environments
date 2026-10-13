#!/usr/bin/env python3
"""decode_scenes.py: reads the Movie Maker PNG frames of the Act I scenes (scenes/scene_c01 / c03 / c07, run with --write-movie frames_<name>/f.png --fixed-fps 30 -- --verify)
and checks what they show: TIME per frame, the late square in step, the marker frozen under pause, the age counted from delta. Frames are 640 x 360.
TIME is decoded from the verification-only encoder at the top-left corner (pixel 10,10). PNG index n is process frame n + 1."""
import glob
import math
from PIL import Image

TEAL = (0.37, 0.64, 0.57)
CREAM = (0.98, 0.97, 0.96)
STAGE = (217, 213, 202)


def mixc(p):
    return tuple(255 * (a * (1 - p) + b * p) for a, b in zip(TEAL, CREAM))


def frames(name):
    return [Image.open(f).convert("RGB") for f in sorted(glob.glob(f"frames_{name}/f*.png"))]


def time_of(im):
    r, g, b = im.getpixel((10, 10))
    return r + (g + b / 255.0) / 255.0


def maxdiff(c1, c2):
    return max(abs(a - b) for a, b in zip(c1, c2))


# ---- C01: the late square is in step
ims = frames("c01_late_join")
ts = [time_of(im) for im in ims]
steps = [(ts[i + 1] - ts[i]) * 30 for i in range(8, len(ts) - 1)]
join = next(i for i in range(len(ims)) if maxdiff(ims[i].getpixel((448, 180)), STAGE) > 6)
worst = max(maxdiff(ims[i].getpixel((192, 180)), ims[i].getpixel((448, 180))) for i in range(join, len(ims)))
worst_formula = max(maxdiff(ims[i].getpixel((448, 180)), mixc(0.5 + 0.5 * math.sin(2 * math.pi * ts[i]))) for i in range(join, len(ims)))
print(f"C01  {len(ims)} frames; TIME advances {min(steps):.3f} to {max(steps):.3f} frames-worth (1/30 s) per frame from frame 8 on")
print(f"C01  the right square first appears at PNG index {join} (process frame {join + 1}, the join event); index {join - 1} shows the stage color there: {ims[join - 1].getpixel((448, 180))}")
print(f"C01  from the join to the end ({len(ims) - join} frames) the left and right squares differ by at most {worst:.1f} 8-bit steps; the right square against 0.5 + 0.5 sin(TAU TIME): at most {worst_formula:.1f} steps")

# ---- C03: time scale and pause
ims = frames("c03_scale_pause")
ts = [time_of(im) for im in ims]


def seg(a, b):
    return sum(ts[i + 1] - ts[i] for i in range(a, b)) / (b - a) * 30


print(f"C03  TIME per frame in units of 1/30 s: frames 20-80 normal {seg(20, 80):.3f} | 90-205 time scale 0.5 {seg(90, 205):.3f} | 215-225 back to 1.0 {seg(215, 225):.3f} | 235-355 paused {seg(235, 355):.3f}")


def marker_x(im):
    y = 100
    xs = [x for x in range(640) if abs(im.getpixel((x, y))[0] - 95) < 6 and abs(im.getpixel((x, y))[1] - 163) < 6]
    return (min(xs) + max(xs)) / 2 if xs else None


mx = [marker_x(im) for im in ims]


def speed(a, b):
    d = [mx[i + 1] - mx[i] for i in range(a, b) if mx[i] is not None and mx[i + 1] is not None and mx[i + 1] - mx[i] > 0]
    return sum(d) / len(d)


paused_x = [mx[i] for i in range(235, 355)]
print(f"C03  marker pixels per frame: normal {speed(20, 80):.3f} (0.2 of 640 px per game second = 4.267) | time scale 0.5: {speed(90, 205):.3f} | paused: frozen at x = {min(paused_x)} to {max(paused_x)} over 120 frames")
pulse_worst = max(maxdiff(ims[i].getpixel((320, int(0.68 * 360))), mixc(0.5 + 0.5 * math.sin(2 * math.pi * ts[i]))) for i in range(10, len(ims)))
print(f"C03  the pulse square against 0.5 + 0.5 sin(TAU TIME) over {len(ims) - 10} frames, paused frames included: at most {pulse_worst:.1f} steps")

# ---- C07: the late square counts its own age
ims = frames("c07_age")
ts = [time_of(im) for im in ims]
join = next(i for i in range(len(ims)) if maxdiff(ims[i].getpixel((448, 180)), STAGE) > 6)
worst_l = worst_r = 0.0
for i in range(join + 1, len(ims)):
    age = (i - join) / 30.0
    worst_l = max(worst_l, maxdiff(ims[i].getpixel((192, 180)), mixc(0.5 + 0.5 * math.sin(2 * math.pi * ts[i]))))
    worst_r = max(worst_r, min(maxdiff(ims[i].getpixel((448, 180)), mixc(0.5 + 0.5 * math.sin(2 * math.pi * (age + d)))) for d in (-1 / 30, 0, 1 / 30, 2 / 30)))
print(f"C07  the late square first appears at PNG index {join}; after it: the left square against 0.5 + 0.5 sin(TAU TIME) at most {worst_l:.1f} steps; the right square against 0.5 + 0.5 sin(TAU age), age = frames since the join / 30 (two frames of slack): at most {worst_r:.1f} steps")
out_of_step = max(maxdiff(ims[i].getpixel((192, 180)), ims[i].getpixel((448, 180))) for i in range(join + 1, join + 30))
print(f"C07  during the first second after the join the two squares differ by up to {out_of_step:.0f} steps: the late square starts its own pulse from the beginning")
