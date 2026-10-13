#!/usr/bin/env python3
"""analyze_lab.py: measures the PNGs written by run_lab_checks.py and writes lab-summary.txt (what FACTCHECK.md cites)."""
import json
from pathlib import Path
import numpy as np
import ol_measure as M

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
lines = []
def say(s=""):
    print(s); lines.append(s)

def im(name):
    return M.load(PNG / f"{name}.png")

say("== A1  reading one step to the right slides the picture to the left (sprite at scale 1.0; blob centre in screen pixels)")
base = None
for lk in ("0.000", "0.125", "0.250"):
    a = im(f"01-look-{lk}"); sol = M.solid(a)
    cx, cy = M.centroid(sol)
    if base is None: base = cx
    say(f"  look={lk}: blob centre x = {cx:.2f}  (shift {cx - base:+.2f} px)   expected shift = -look*128 = {-float(lk)*128:+.1f}")

say("\n== A2  one question: where is the outline? (counts of outline-coloured pixels, left and right of the blob centre)")
a = im("03-one-question"); c = M.classes(a); cx, cy = M.centroid(M.solid(a))
ys, xs = np.nonzero(c["line"] | c["over"])
say(f"  total outline px = {len(xs)}; left of centre = {(xs < cx).sum()}; right of centre = {(xs > cx).sum()}")

say("\n== A3  four questions, no min vs min (literal step 0.02 of the picture = 2.56 image pixels)")
for nm in ("04-lighter-diagonals", "05-four-questions"):
    c = M.classes(im(nm))
    say(f"  {nm}: line-colour px = {int(c['line'].sum())}, over-bright (128,128,255) px = {int(c['over'].sum())}, total ring = {int((c['line'] | c['over']).sum())}")
c = M.classes(im("04-lighter-diagonals")); tot = int((c["line"] | c["over"]).sum())
say(f"  share of the ring with the wrong colour when min is missing: {c['over'].sum()}/{tot} = {100*c['over'].sum()/tot:.1f}%")

say("\n== A4  axis widths of the outline in screen px (scale 1.0), by shader and thickness")
for shader in ("06-pixel-steps", "07-eight-reads", "08-loop", "10-ring"):
    for t in (1, 2, 3, 4, 8):
        a = im(f"{shader}-t{t}")
        say(f"  {shader} thickness {t}: " + ", ".join(f"{k}={v}" for k, v in M.axis_widths(a).items()))
say("  05-four-questions (literal 0.02): " + ", ".join(f"{k}={v}" for k, v in M.axis_widths(im('05-four-questions')).items()))

say("\n== A5  radial thickness (mean over +-3 degrees; E = 0, SE = 45) by shader, thickness 4 and 8: axis vs diagonal")
for t in (1, 2, 4, 8):
    for shader in ("06-pixel-steps", "07-eight-reads", "10-ring"):
        a = im(f"{shader}-t{t}")
        th = {ang: M.ring_thickness(a, ang) for ang in (0, 22.5, 45, 67.5, 90)}
        say(f"  t={t} {shader:16s}: " + "  ".join(f"{ang:>5}deg={v:5.2f}" for ang, v in th.items()) + f"   diag/axis = {th[45]/max(th[0],1e-9):.2f}")

say("\n== A6  loop against eight written-out reads: pixels that differ (scale 1.0)")
for t in (1, 2, 3, 4, 8):
    d = (np.abs(im(f"07-eight-reads-t{t}") - im(f"08-loop-t{t}")).max(axis=2) > 0).sum()
    say(f"  thickness {t}: {int(d)} pixels differ")

say("\n== A7  the step counts image pixels: thickness 2 at three sprite scales (E-axis width in screen px)")
for nm, sc in (("06-pixel-steps-t2", 1), ("06-pixel-steps-t2-scale2.0", 2), ("06-pixel-steps-t2-scale3.0", 3)):
    say(f"  sprite scale {sc}: " + ", ".join(f"{k}={v}" for k, v in M.axis_widths(im(nm)).items()))

say("\n== A8  thickness 0 against no shader effect (look = 0 render): pixels that differ")
d = (np.abs(im("06-pixel-steps-t0") - im("01-look-0.000")).max(axis=2) > 0).sum()
say(f"  {int(d)} pixels differ")

say("\n== A9  renderer: outline pixel colour, Forward+ against Compatibility")
for fw, cp in (("06-pixel-steps-t2", "06-pixel-steps-t2-compat"), ("05-four-questions", "05-four-questions-compat")):
    a, b = im(fw), im(cp)
    c = M.classes(a)
    y, x = np.argwhere(c["line"])[0]
    say(f"  {fw}: Forward+ pixel {tuple(int(v) for v in a[y,x])}, Compatibility pixel {tuple(int(v) for v in b[y,x])}; images identical: {bool((a == b).all())}")


say("\n== A10  first bug: no empty-check (02-paints-the-sprite): what happens to the sprite's own pixels? (scale 1.0)")
base = M.solid(im("01-look-0.000"))
c = M.classes(im("02-paints-the-sprite"))
inside_line = int((c["line"] & base).sum()); inside_teal = int(((c["teal"] | c["cream"]) & base).sum())
say(f"  sprite pixels: {int(base.sum())}; of those now line-coloured: {inside_line} ({100*inside_line/base.sum():.1f}%); still their own colour: {inside_teal}")

say("\n== A11  second bug at the film's two scales: share of the ring that comes out the wrong colour without min")
for nm in ("04-lighter-diagonals", "04-lighter-diagonals-fit"):
    c = M.classes(im(nm)); tot = int((c["line"] | c["over"]).sum())
    say(f"  {nm}: wrong-colour px {int(c['over'].sum())} of {tot} ring px = {100*c['over'].sum()/max(tot,1):.1f}%")

say("\n== A12  guard against loop (hard-edged sprite): pixels that differ")
for t in (1, 2, 3, 4, 8):
    d = (np.abs(im(f"08-loop-t{t}") - im(f"09-guard-t{t}")).max(axis=2) > 0).sum()
    say(f"  thickness {t}: {int(d)} pixels differ")
d = (np.abs(im("09-guard-t0") - im("01-look-0.000")).max(axis=2) > 0).sum()
say(f"  guard at thickness 0 against the untouched sprite: {int(d)} pixels differ")

say("\n== A13  the soft-edge composite (11-soft-edges) against the plain mix (06-pixel-steps) on a hard-edged sprite: pixels that differ")
for t in (1, 2, 3, 4, 8):
    d = (np.abs(im(f"06-pixel-steps-t{t}") - im(f"11-soft-edges-t{t}")).max(axis=2) > 1).sum()
    say(f"  thickness {t}: {int(d)} pixels differ (tolerance 1 of 255)")

say("\n== A14  where the over-bright ring pixels are (04-lighter-diagonals): angle of each ring pixel from the nearest axis (0 = straight right/left/up/down, 45 = a true diagonal)")
a = im("04-lighter-diagonals"); c = M.classes(a); cx, cy = M.centroid(M.solid(a))
ys, xs = np.nonzero(c["line"] | c["over"])
ang = np.degrees(np.arctan2(ys - cy, xs - cx)) % 90.0
fold = np.minimum(ang, 90.0 - ang)
over = c["over"][ys, xs]
for lo, hi in ((0, 10), (10, 20), (20, 30), (30, 45.01)):
    sel = (fold >= lo) & (fold < hi)
    say(f"  {lo:2d} to {min(hi, 45):2d} degrees from an axis: {int(sel.sum()):3d} ring pixels, {int((sel & over).sum()):3d} over-bright")

(HERE / "lab-summary.txt").write_text("\n".join(lines) + "\n")
