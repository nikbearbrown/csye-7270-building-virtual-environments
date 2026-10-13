#!/usr/bin/env python3
"""analyze_pngs.py: measures the Lab renders in png/ (edges, boxes, straightness) and prints one line per finding.
Run: python3 -I analyze_pngs.py > measurements.txt     (Pillow and numpy only; no Godot)
The Lab stage colour is #D9D5CA; any pixel that differs from it by more than 12 levels in some channel is the shape.
"""
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
STAGE = np.array([217, 213, 202])


def load(name):
    return np.asarray(Image.open(PNG / f"{name}.png").convert("RGB")).astype(int)


def mask(a):
    return (np.abs(a - STAGE).max(axis=2) > 12)


def bbox(m):
    ys, xs = np.where(m)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def left_edge(m, y):
    xs = np.where(m[y])[0]
    return int(xs.min()) if len(xs) else None


def right_edge(m, y):
    xs = np.where(m[y])[0]
    return int(xs.max()) if len(xs) else None


def top_edge(m, x):
    ys = np.where(m[:, x])[0]
    return int(ys.min()) if len(ys) else None


def bottom_edge(m, x):
    ys = np.where(m[:, x])[0]
    return int(ys.max()) if len(ys) else None


def line_fit_residual(xs, ys):
    """max absolute distance (px) of the points from their least-squares straight line"""
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    A = np.vstack([xs, np.ones_like(xs)]).T
    k, b = np.linalg.lstsq(A, ys, rcond=None)[0]
    return float(np.abs(ys - (k * xs + b)).max()), float(k), float(b)


def main():
    out = []
    p = out.append
    # ---------- slide ----------
    base = bbox(mask(load("c0-plain-white")))
    sl = bbox(mask(load("01-slide-white")))
    p(f"slide: plain white sprite box {base}; after `VERTEX.x += 40.0` box {sl}; left edge moved {sl[0]-base[0]} px, top {sl[1]-base[1]}, width {sl[2]-sl[0]+1} (was {base[2]-base[0]+1})")
    base2 = bbox(mask(load("c0-plain-white-scale2")))
    sl2 = bbox(mask(load("01-slide-white-scale2")))
    p(f"slide on a node scaled 2.0: plain box {base2}; after the same line {sl2}; left edge moved {sl2[0]-base2[0]} px on screen (the shader said 40)")
    sl225 = bbox(mask(load("01-slide-white-scale2.25-lab-default")))
    p(f"slide on the Lab default scale 2.25: box {sl225}; plain would start at x = 320 - 144 = 176, so the left edge moved {sl225[0]-176} px on screen (40 x 2.25 = 90)")
    # ---------- squash ----------
    sq = bbox(mask(load("02-squash-white")))
    p(f"squash `VERTEX *= vec2(1.5, 0.5)`: box {sq}: width {sq[2]-sq[0]+1} px (was 128), height {sq[3]-sq[1]+1} px (was 128); centre x {(sq[0]+sq[2])/2:.1f}, y {(sq[1]+sq[3])/2:.1f} (plain centre {(base[0]+base[2])/2:.1f}, {(base[1]+base[3])/2:.1f})")
    # ---------- lean ----------
    m = mask(load("03-lean-white"))
    b = bbox(m)
    y0, y1 = b[1], b[3]
    rows = [y0 + int(f * (y1 - y0)) for f in (0.0, 0.02, 0.25, 0.5, 0.75, 0.98, 1.0)]
    le = [left_edge(m, y) for y in rows]
    xs_all = list(range(y0, y1 + 1))
    all_le = [left_edge(m, y) for y in xs_all]
    resid, k, _ = line_fit_residual(xs_all, all_le)
    p(f"lean `VERTEX.x += 50.0 * UV.y`: box {b}, height {y1-y0+1}; left edge x at rows {[r-y0 for r in rows]} of the shape = {le}; first row {all_le[0]}, last row {all_le[-1]}, shift {all_le[-1]-all_le[0]} px over {y1-y0+1} rows")
    p(f"lean: the left edge fits a straight line to within {resid:.2f} px (slope {k:.3f} px per row; 50/127 = {50/127:.3f})")
    # ---------- ripple on four vertices (Sprite2D, 128 px at scale 1.0) ----------
    m = mask(load("04-ripple-white"))
    b = bbox(m)
    cols = list(range(b[0], b[2] + 1))
    tops = [top_edge(m, x) for x in cols]
    bots = [bottom_edge(m, x) for x in cols]
    rt, kt, _ = line_fit_residual(cols, tops)
    rb, kb, _ = line_fit_residual(cols, bots)
    p(f"ripple `VERTEX.y += sin(UV.x * 8.0) * 24.0` on a four-vertex 128 px sprite: box {b}; top edge y at the left end {tops[0]}, middle {tops[len(tops)//2]}, right end {tops[-1]}; bottom edge {bots[0]}, {bots[len(bots)//2]}, {bots[-1]}")
    p(f"ripple on four vertices: top edge fits a straight line within {rt:.2f} px, bottom within {rb:.2f} px (sin(8) x 24 = {np.sin(8.0)*24:.1f}; right end moved {tops[-1]-tops[0]} px)")
    # ---------- pinned flag on four vertices ----------
    m = mask(load("06-flag-pinned-white"))
    b = bbox(m)
    p(f"flag-pinned (06) on four vertices (Lab, a moment after start): box {b}")
    # ---------- amplitude 0 is flat ----------
    m = mask(load("07-flag-dials-amplitude0"))
    b = bbox(m)
    cols = list(range(b[0], b[2] + 1))
    tops = {top_edge(m, x) for x in cols}
    p(f"dials with amplitude = 0.0 (07): box {b}; distinct top-edge rows across the width: {sorted(tops)} (flat if one value)")
    # ---------- a far slide (beat B39) ----------
    far = bbox(mask(load("16-slide-far-white")))
    p(f"far slide `VERTEX.x += 200.0`: box {far}; left edge moved {far[0]-base[0]} px (the node's own rectangle stays at {base[0]}..{base[2]})")
    # ---------- the same pixel counts in the Compatibility renderer ----------
    sc = bbox(mask(load("01-slide-white-gl_compatibility")))
    p(f"slide in gl_compatibility: box {sc} (Forward+: {sl}); same: {sc == sl}")
    mc = mask(load("03-lean-white-gl_compatibility"))
    bc = bbox(mc)
    lec = [left_edge(mc, bc[1] + r) for r in (0, 2, 31, 63, 95, 124, 127)]
    p(f"lean in gl_compatibility: left edge x at rows [0, 2, 31, 63, 95, 124, 127] = {lec} (Forward+: {le}); same: {lec == le}")
    # ---------- check of the plain sprite box ----------
    p(f"plain white sprite box {base} (expected x 256..383, y 116..243)")
    print("\n".join(out))


if __name__ == "__main__":
    main()
