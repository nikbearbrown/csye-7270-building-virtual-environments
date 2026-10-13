#!/usr/bin/env python3
"""analyze_soft.py: reads the black/white/stage renders of verify_b_soft.gd, solves each pixel's alpha, and writes soft-summary.txt."""
from pathlib import Path
import numpy as np
import ol_measure as M

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
L = []
def say(s=""):
    print(s); L.append(s)

def alpha_rgb(name):
    b = M.load(PNG / f"{name}-on-black.png").astype(float)
    w = M.load(PNG / f"{name}-on-white.png").astype(float)
    a = 1.0 - (w - b).mean(axis=2) / 255.0
    a = np.clip(a, 0, 1)
    rgb = np.where(a[..., None] > 0.002, b / np.maximum(a[..., None], 0.002), 0.0)
    return a, rgb

plain_a, plain_rgb = alpha_rgb("soft-plain")
partial_in = (plain_a > 0.02) & (plain_a < 0.98)
say(f"== B0 the antialiased sprite alone: {int(partial_in.sum())} half-transparent rim pixels; alpha values from {plain_a[partial_in].min():.2f} to {plain_a[partial_in].max():.2f}")

for name in ("soft-four-t1", "soft-fix-t1"):
    a, rgb = alpha_rgb(name)
    seam = partial_in                                  # pixels that were half-transparent in the sprite itself
    outer = (plain_a < 0.02) & (a > 0.02)              # pixels the outline added where the sprite had nothing
    say(f"\n== B1 {name} (thickness 1, soft sprite)")
    say(f"  rim pixels (alpha 0.02 to 0.98 in the sprite): alpha in the output: min {a[seam].min():.2f}, mean {a[seam].mean():.2f}, max {a[seam].max():.2f}")
    say(f"  rim pixels that stay see-through (output alpha < 0.98): {int((a[seam] < 0.98).sum())} of {int(seam.sum())}")
    say(f"  outline pixels added outside the sprite: {int(outer.sum())}; their alpha: min {a[outer].min():.2f}, max {a[outer].max():.2f}")
    inside = plain_a > 0.98
    say(f"  pixels fully inside the sprite that changed colour: {int((np.abs(rgb[inside] - plain_rgb[inside]).max(axis=1) > 4).sum())}")

say("\n== B2 thickness 0: does the sprite stay untouched?")
for name in ("soft-four-t0", "soft-loop-t0", "soft-fix-t0", "soft-guard-t0", "hard-loop-t0"):
    base = "soft-plain" if name.startswith("soft") else "hard-plain"
    a, rgb = alpha_rgb(name); pa, prgb = alpha_rgb(base)
    da = np.abs(a - pa) > 0.01
    dc = (np.abs(rgb - prgb).max(axis=2) > 4) & (pa > 0.02)
    say(f"  {name}: pixels whose alpha differs from the plain sprite: {int(da.sum())}; whose colour differs: {int(dc.sum())}")

# the screen result over the stage colour, for the film's own pictures
for name in ("soft-plain", "soft-four-t1", "soft-fix-t1"):
    im = M.load(PNG / f"{name}-on-stage.png")
    say(f"\n{name} on the stage colour: distinct colours = {len(set(map(tuple, im.reshape(-1,3))))}")
(HERE / "soft-summary.txt").write_text("\n".join(L) + "\n")
