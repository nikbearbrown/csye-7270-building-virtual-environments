#!/usr/bin/env python3
"""analyze-plus.py: measures the PNGs written by run-plus-checks.sh (Pillow). Writes plus-analysis.txt.
  - share of the frame that is teal (kept) for the three step thresholds
  - for the dissolve: sprite pixels left (teal + cream eyes) and burning pixels at several progress values, for the first version and the fixed one
  - the bounding boxes of the burning specks the first version shows at progress 0 (for the ring in the film)
  - for the wipe: the x of the left edge of what is left
Stage colour is (217, 213, 202); sprite teal (95, 163, 145); eyes cream (250, 249, 245)."""
from pathlib import Path
from PIL import Image
import numpy as np
here = Path(__file__).resolve().parent
P = here / "png"
out = []
def arr(name): return np.array(Image.open(P / f"plus-{name}.png").convert("RGB")).astype(int)
def near(a, rgb, tol): return (np.abs(a - np.array(rgb)).max(axis=2) <= tol)
STAGE, TEAL, CREAM = (217, 213, 202), (95, 163, 145), (250, 249, 245)
out.append("== step shares (a3-16-step-T, 360 x 360 rect): share of pixels that are teal (step = 1)")
for t in ("0.25", "0.5", "0.75"):
    a = arr(f"a3-16-step-{t}"); teal = near(a, TEAL, 3).mean()
    out.append(f"threshold {t}: teal share {teal:.3f}")
out.append("")
out.append("== dissolve (sprite on the stage, 640 x 360): counts of pixels")
def counts(name):
    a = arr(name); st = near(a, STAGE, 2); te = near(a, TEAL, 3); cr = near(a, CREAM, 3)
    burn = ~(st | te | cr)
    return int(te.sum()), int(cr.sum()), int(burn.sum()), a, burn
for p in ("0.0", "0.25", "0.5", "0.75", "1.0"):
    te, cr, bu, _, _ = counts(f"a3-18-dissolve-{p}")
    out.append(f"fixed        progress {p}: teal {te:6d}  cream {cr:4d}  burning {bu:5d}")
te, cr, bu, a, burn = counts("a3-19-first-try-0.0")
out.append(f"first try    progress 0.0: teal {te:6d}  cream {cr:4d}  burning {bu:5d}   <- pixels already burning at zero")
ys, xs = np.nonzero(burn)
if len(xs):
    from scipy import ndimage
    lab, n = ndimage.label(ndimage.binary_dilation(burn, iterations=3))
    boxes = []
    for sl in ndimage.find_objects(lab):
        boxes.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop))
    out.append(f"first-try specks at progress 0: {len(boxes)} clusters (x0, y0, x1, y1 in the 640 x 360 frame): {boxes}")
    out.append("   as fractions of the frame (x0, y0, x1, y1): " + str([(round(b[0]/640, 3), round(b[1]/360, 3), round(b[2]/640, 3), round(b[3]/360, 3)) for b in boxes]))
sprite_full = counts("a3-18-dissolve-0.0")[0] + counts("a3-18-dissolve-0.0")[1]
out.append(f"sprite pixels at progress 0 (teal + cream): {sprite_full}")
for p in ("0.0", "0.25", "0.5", "0.75", "1.0"):
    te, cr, bu, _, _ = counts(f"a3-17-cut-{p}")
    out.append(f"cut only (no edge) progress {p}: sprite pixels left {te + cr:6d} = {100.0 * (te + cr) / sprite_full:5.1f} % of the sprite")
out.append("")
out.append("== wipe (gradient as the mask): leftmost column that still has teal/burn/cream, per progress")
for p in ("0.35", "0.5", "0.65"):
    a = arr(f"a3-18-wipe-{p}"); st = near(a, STAGE, 2)
    cols = np.nonzero((~st).any(axis=0))[0]
    out.append(f"progress {p}: sprite spans x = {cols.min()} to {cols.max()} of 640")
text = "\n".join(out) + "\n"
(here / "plus-analysis.txt").write_text(text)
print(text)
