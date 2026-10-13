#!/usr/bin/env python3
"""measure.py: geometry of a sprite in a Shader Lab PNG (640 x 360, stage colour #D9D5CA, sprite centred at (320, 180)).

Usage:  python3 measure.py <png> [<png> ...]
Prints one JSON line per file: the bounding box, the width and height, the centroid and the four extreme points, all in
pixels relative to the window centre (x right, y DOWN, like Godot). "Sprite" means any pixel more than 12/255 away from the stage colour.
This is the only measuring tool used for the corner, width and centroid numbers in FACTCHECK.md.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

STAGE = np.array([217, 213, 202])      # #D9D5CA
CX, CY = 320.0, 180.0                  # window centre in pixel-edge coordinates


def measure(path, tol=12):
    img = np.asarray(Image.open(path).convert("RGB")).astype(int)
    mask = (np.abs(img - STAGE).max(axis=2) > tol)
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return {"file": Path(path).name, "empty": True}
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1      # pixel EDGES (right/bottom edge exclusive)
    cx, cy = xs.mean() + 0.5, ys.mean() + 0.5
    def rel(x, y):
        return [round(float(x - CX), 1), round(float(y - CY), 1)]
    left = int(np.argmin(xs)); right = int(np.argmax(xs)); top = int(np.argmin(ys)); bottom = int(np.argmax(ys))
    return {"file": Path(path).name, "bbox_edges_rel": [round(float(x0 - CX), 1), round(float(y0 - CY), 1), round(float(x1 - CX), 1), round(float(y1 - CY), 1)],
            "width": int(x1 - x0), "height": int(y1 - y0), "area_px": int(mask.sum()),
            "centroid_rel": rel(cx, cy),
            "leftmost": rel(xs[left] + 0.5, ys[left] + 0.5), "rightmost": rel(xs[right] + 0.5, ys[right] + 0.5),
            "topmost": rel(xs[top] + 0.5, ys[top] + 0.5), "bottommost": rel(xs[bottom] + 0.5, ys[bottom] + 0.5)}


def column_height(path, x_rel, tol=12):
    """Number of sprite pixels in the pixel column at x_rel (relative to the window centre)."""
    img = np.asarray(Image.open(path).convert("RGB")).astype(int)
    mask = (np.abs(img - STAGE).max(axis=2) > tol)
    col = int(round(CX + x_rel))
    return int(mask[:, col].sum())


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(measure(p)))
