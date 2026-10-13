#!/usr/bin/env python3
"""measure.py: measure shapes in a Shader Lab PNG (UV Space film, planning checks).

  python3 measure.py bbox  <png> [--color r,g,b] [--tol 12]   bounding box, width, height, pixel count, centroid of pixels near a color
  python3 measure.py edge  <png> --row Y  [--color r,g,b]      first and last x (0-based) of the color on row Y
  python3 measure.py first <png> --row Y --axis x|y --channel r|g|b  --above 0.5   first index along a row/column where a channel passes a level

Colors are 0..255. The default color is the film's teal, #5FA391 (95, 163, 145), which is what `COLOR = vec4(0.373, 0.639, 0.569, 1.0)`
becomes after 8-bit rounding in the PNG. Prints one JSON line per command so a log can be pasted into RESULTS.md.
"""
import json
import sys

import numpy as np
from PIL import Image


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(int)


def near(img, color, tol):
    c = np.array(color).reshape(1, 1, 3)
    return (np.abs(img - c) <= tol).all(axis=2)


def main(argv):
    cmd, path = argv[0], argv[1]
    args = argv[2:]

    def opt(name, default=None, cast=str):
        if name in args:
            return cast(args[args.index(name) + 1])
        return default

    img = load(path)
    H, W = img.shape[:2]
    color = [int(x) for x in opt("--color", "95,163,145").split(",")]
    tol = opt("--tol", 12, int)
    if cmd == "bbox":
        m = near(img, color, tol)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            print(json.dumps({"png": path, "image": [W, H], "count": 0}))
            return
        out = {"png": path.split("/")[-1], "image": [W, H], "color": color, "count": int(m.sum()),
               "x0": int(xs.min()), "x1": int(xs.max()), "y0": int(ys.min()), "y1": int(ys.max()),
               "width": int(xs.max() - xs.min() + 1), "height": int(ys.max() - ys.min() + 1),
               "centroid": [round(float(xs.mean()), 1), round(float(ys.mean()), 1)],
               "centroid_norm": [round(float(xs.mean()) / W, 3), round(float(ys.mean()) / H, 3)]}
        print(json.dumps(out))
    elif cmd == "edge":
        y = opt("--row", H // 2, int)
        m = near(img, color, tol)[y]
        xs = np.nonzero(m)[0]
        print(json.dumps({"png": path.split("/")[-1], "row": y, "first_x": int(xs.min()) if len(xs) else None,
                          "last_x": int(xs.max()) if len(xs) else None, "count": int(m.sum())}))
    elif cmd == "first":
        axis = opt("--axis", "x")
        ch = {"r": 0, "g": 1, "b": 2}[opt("--channel", "r")]
        level = opt("--above", 0.5, float) * 255.0
        if axis == "x":
            y = opt("--row", H // 2, int)
            line = img[y, :, ch]
        else:
            x = opt("--row", W // 2, int)
            line = img[:, x, ch]
        idx = np.nonzero(line >= level)[0]
        print(json.dumps({"png": path.split("/")[-1], "axis": axis, "at": opt("--row", None), "first_index_at_or_above": int(idx.min()) if len(idx) else None}))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
