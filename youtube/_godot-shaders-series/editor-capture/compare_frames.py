#!/usr/bin/env python3
"""compare_frames.py <dirA> <dirB> [--names NAME ...] [--tol N]

Pixel comparison of same-named PNGs from two recordings (for example: factory editor settings vs the single-window settings, or Forward+
vs Compatibility). For each name prints the frame sizes, the largest per-channel difference, the share of pixels that differ by more than
--tol (default 0) and the bounding box of the differences. A name is skipped when it is missing from either folder.
"""
import argparse, os, sys
from PIL import Image, ImageChops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--names", nargs="*", default=None)
    ap.add_argument("--tol", type=int, default=0)
    a = ap.parse_args()
    names = a.names
    if not names:
        names = sorted(f[:-4] for f in os.listdir(a.a) if f.endswith(".png") and ".dock" not in f and ".inspector" not in f and f in set(os.listdir(a.b)))
    for n in names:
        pa, pb = os.path.join(a.a, n + ".png"), os.path.join(a.b, n + ".png")
        if not (os.path.exists(pa) and os.path.exists(pb)):
            print("  %-70s (missing in one folder)" % n)
            continue
        ia, ib = Image.open(pa).convert("RGB"), Image.open(pb).convert("RGB")
        if ia.size != ib.size:
            print("  %-70s DIFFERENT SIZES %s vs %s" % (n, ia.size, ib.size))
            continue
        d = ImageChops.difference(ia, ib)
        ext = d.getextrema()
        mx = max(e[1] for e in ext)
        hist = d.convert("L").histogram()
        bad = sum(hist[a.tol + 1:])
        total = ia.size[0] * ia.size[1]
        print("  %-70s max channel diff %3d, %.4f %% of pixels differ by > %d, bbox %s" % (n, mx, 100.0 * bad / total, a.tol, d.getbbox()))


if __name__ == "__main__":
    main()
