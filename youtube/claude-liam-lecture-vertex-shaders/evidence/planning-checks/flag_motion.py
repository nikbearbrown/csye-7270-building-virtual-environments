#!/usr/bin/env python3
"""flag_motion.py: what the flag's top edge does over time (frames from the `pinned` and `travel` scenes of capture_scenes.gd).
Claims checked: (1) `sin(UV.x * 8.0 - TIME * 3.0)` makes the ripple travel to the right; (2) `* UV.x` pins the left edge; (3) without it the left end bobs.
Method: for every frame, read the top edge of the flag (first non-stage pixel in each column, columns 449..831; the grey pole is left of 448),
then find the clock value T (mod the wave period 2*pi/3 = 2.094 s) that best fits the model; the fitted clock must advance with real time.
Run: python3 -I flag_motion.py   (Pillow + numpy; no Godot)"""
from pathlib import Path

import numpy as np
from PIL import Image

PNG = Path(__file__).resolve().parent / "png"
STAGE = np.array([217, 213, 202])
X0, W, Y0, AMP, F, S = 448, 384, 276.0, 24.0, 8.0, 3.0      # flag centred at (640, 360), 384 x 168: top edge at y = 360 - 84 = 276
PERIOD = 2 * np.pi / S


def profile(name):
    a = np.asarray(Image.open(PNG / name).convert("RGB")).astype(int)
    m = (np.abs(a - STAGE).max(axis=2) > 12)
    xs = np.arange(X0 + 1, X0 + W)
    ys = np.array([np.where(m[:, x])[0].min() for x in xs], float)
    return xs, ys


def model(T, xs, pinned):
    u = (xs - X0 + 0.5) / W
    return Y0 + AMP * np.sin(u * F - T * S) * (u if pinned else 1.0)


def fit(xs, ys, pinned):
    best = (1e9, 0.0)
    for T in np.arange(0.0, PERIOD, 0.002):
        e = np.abs(model(T, xs, pinned) - ys).mean()
        if e < best[0]:
            best = (e, T)
    return best


def run(scene, times, pinned, label):
    prev = None
    for t in times:
        name = f"scene-{scene}-t{t:.2f}.png"
        xs, ys = profile(name)
        e, T = fit(xs, ys, pinned)
        adv = "" if prev is None else f"  clock advanced {((T - prev[1]) % PERIOD):.3f} s (mod {PERIOD:.3f}) while real time advanced {t - prev[0]:.2f} s"
        print(f"{label} frame t={t:.2f}: top edge at the left end y={ys[0]:.0f}, next 3 columns {ys[1:4]}; best-fit clock {T:.3f} s, mean error {e:.2f} px{adv}")
        prev = (t, T)


print("== unpinned, travelling (05-flag-travelling): the left end should bob by up to +-24 px")
run("pinned", [1.0, 1.2, 1.4, 1.6], False, "unpinned")
print("== pinned, travelling (06-flag-pinned): the left end should stay at y = 276")
run("pinned", [6.0, 6.2, 6.4, 6.6], True, "pinned  ")
print("== scene travel after its switch at 58 % of the beat (05-flag-travelling, unpinned): the left end bobs again")
run("travel", [8.0, 8.2, 8.4, 8.6], False, "unpinned")
