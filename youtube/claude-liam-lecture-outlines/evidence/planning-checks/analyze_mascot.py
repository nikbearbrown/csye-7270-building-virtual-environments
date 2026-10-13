#!/usr/bin/env python3
"""analyze_mascot.py: measures how much of the TRUE outline each shader draws.
True outline at thickness t = every empty pixel whose distance to some solid pixel is at most t (pixel-centre distance).
Coverage = share of those pixels the shader coloured; excess = coloured pixels that are NOT within t of a solid pixel (the brush reaching too far).
Writes mascot-summary.txt. Needs the PNGs from verify_d_mascot.gd (mascot) and run_lab_checks.py (disc)."""
from pathlib import Path
import numpy as np
from PIL import Image
import ol_measure as M

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
OX, OY = 256, 116            # sprite top-left on screen at scale 1.0 (128 x 128 image)
L = []
def say(s=""):
    print(s); L.append(s)

def ideal_ring(solid, t):
    h, w = solid.shape
    dil = np.zeros_like(solid)
    r = int(np.floor(t))
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= t * t + 1e-9:
                dil |= np.roll(np.roll(solid, dy, axis=0), dx, axis=1)
    return dil & ~solid

def window(im):
    return im[OY:OY + 128, OX:OX + 128]

def stats(name, solid, render_name, t):
    im = M.load(PNG / f"{render_name}.png")
    win = window(im)
    c = M.classes(win)
    line = c["line"] | c["over"]
    ideal = ideal_ring(solid, t)
    cov = (line & ideal).sum() / max(ideal.sum(), 1)
    exc = (line & ~ideal).sum()
    miss = (ideal & ~line).sum()
    return int(ideal.sum()), int(line.sum()), float(cov), int(exc), int(miss)

# solid masks
mascot_tex = np.array(Image.open(PNG / "mascot-texture.png").convert("RGBA"))
mascot_solid = mascot_tex[..., 3] > 0
disc_solid = M.solid(window(M.load(PNG / "01-look-0.000.png")))     # the Lab sprite at scale 1.0

say("== D1  how much of the true outline is drawn (coverage), how far past it the brush reaches (excess px), and how much is missing (px)")
say("   reads = samples around the pixel (the 4-read and 8-read shaders are the film's own; 16 is lab-shaders/10-ring; 32 and 64 are the same maths with more reads)")
say(f"   {'sprite':8s} {'reads':>5s} {'t':>2s} | {'true ring px':>12s} {'drawn px':>9s} {'coverage':>9s} {'excess':>7s} {'missing':>8s}")
rows = []
for sprite, solid, prefix in (("disc", disc_solid, None), ("antenna", mascot_solid, "mascot")):
    for t in (1, 2, 4, 6, 8):
        for reads in (4, 8, 16, 32, 64):
            if sprite == "disc":
                # Lab renders exist for 4 (06-pixel-steps), 8 (07-eight-reads) and 16 (10-ring) at t = 1, 2, 4, 8
                nm = {4: f"06-pixel-steps-t{t}", 8: f"07-eight-reads-t{t}", 16: f"10-ring-t{t}"}.get(reads)
            else:
                nm = f"mascot-{reads}-t{t}"
            if nm is None or not (PNG / f"{nm}.png").exists():
                continue
            ideal, drawn, cov, exc, miss = stats(sprite, solid, nm, t)
            say(f"   {sprite:8s} {reads:5d} {t:2d} | {ideal:12d} {drawn:9d} {100*cov:8.1f}% {exc:7d} {miss:8d}")
            rows.append((sprite, reads, t, ideal, drawn, cov, exc, miss))

say("\n== D2  the stem alone: the horizontal slice through the middle of the stem (texel row 21), '#' = outline colour, 'S' = stem, '.' = empty")
for t in (2, 4, 6, 8):
    for reads in (4, 8, 16, 32):
        im = M.load(PNG / f"mascot-{reads}-t{t}.png"); win = window(im)
        c = M.classes(win)
        row = 21
        s = ""
        for x in range(38, 92):
            if c["line"][row, x]: s += "#"
            elif c["teal"][row, x]: s += "S"
            else: s += "."
        say(f"   t={t} reads={reads:2d}: {s}")
(HERE / "mascot-summary.txt").write_text("\n".join(L) + "\n")
