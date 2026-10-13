"""ol_measure.py: small measuring helpers for the Lab and scratch renders of the outline film (Pillow + numpy only).
Colours of the test sprite and stage are fixed by the Lab (runner.gd): stage #D9D5CA, teal #5FA391, cream eyes #FAF9F5.
The outline colour used by every shader in this film is vec4(0.25, 0.25, 0.75, 1.0) = (64, 64, 191) in 8-bit.
"""
import math
import numpy as np
from PIL import Image

STAGE = (217, 213, 202)
TEAL = (95, 163, 145)
CREAM = (250, 249, 245)
LINE = (64, 64, 191)
OVER = (128, 128, 255)       # what a mix factor of 2 does to the line colour (clamped)


def load(path):
    return np.array(Image.open(path).convert("RGB")).astype(int)


def mask_of(im, color, tol=6):
    return (np.abs(im - np.array(color)).max(axis=2) <= tol)


def classes(im):
    return {"stage": mask_of(im, STAGE), "teal": mask_of(im, TEAL), "cream": mask_of(im, CREAM),
            "line": mask_of(im, LINE), "over": mask_of(im, OVER)}


def solid(im):
    c = classes(im)
    return c["teal"] | c["cream"]


def centroid(mask):
    ys, xs = np.nonzero(mask)
    return xs.mean(), ys.mean()


def bbox(mask):
    ys, xs = np.nonzero(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def ray_extent(mask_a, cx, cy, theta_deg, rmax=400.0, step=0.1):
    """Farthest r along the ray (from the centre) at which mask_a is true, contiguous from r=0 (None if the ray never starts inside)."""
    h, w = mask_a.shape
    last = None
    r = 0.0
    th = math.radians(theta_deg)
    while r <= rmax:
        x = int(round(cx + r * math.cos(th))); y = int(round(cy + r * math.sin(th)))
        if not (0 <= x < w and 0 <= y < h):
            break
        if mask_a[y, x]:
            last = r
        r += step
    return last


def ring_thickness(im, theta_deg, spread=3.0, n=7):
    """Mean radial thickness of the outline colour beyond the solid sprite at a direction (E = 0 deg, S = 90 deg: y points down)."""
    c = classes(im)
    sol = c["teal"] | c["cream"]
    line = c["line"] | c["over"]
    cx, cy = centroid(sol)
    vals = []
    for k in range(n):
        th = theta_deg + (k - (n - 1) / 2.0) * (2 * spread / max(n - 1, 1))
        rs = ray_extent(sol, cx, cy, th)
        # walk outward from the solid edge while the pixel is line colour
        both = sol | line
        re = ray_extent(both, cx, cy, th)
        vals.append((re - rs) if (re is not None and rs is not None) else 0.0)
    return float(np.mean(vals))


def count_in_row(mask, y, x0, x1):
    return int(mask[y, x0:x1].sum())


def axis_widths(im):
    """Outline pixels met walking out from the sprite centre along the four axes (E, S, W, N): the literal width in screen pixels."""
    c = classes(im)
    sol = c["teal"] | c["cream"]
    line = c["line"] | c["over"]
    cx, cy = centroid(sol)
    cx, cy = int(round(cx)), int(round(cy))
    out = {}
    for name, (dx, dy) in {"E": (1, 0), "S": (0, 1), "W": (-1, 0), "N": (0, -1)}.items():
        x, y = cx, cy
        while sol[y, x]:
            x += dx; y += dy
        n = 0
        while line[y, x]:
            n += 1; x += dx; y += dy
        out[name] = n
    return out
