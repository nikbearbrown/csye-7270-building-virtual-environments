#!/usr/bin/env python3
"""analysis.py: the arithmetic behind the film's measured numbers, from the saved renders. Usage: python3 analysis.py e3 | e7 | e9b | specks | all
Inputs: ../png/*.png and ../../../captures/*.png (real Godot 4.7.2 renders). Output goes to stdout; the film's logs/ files are made with: python3 analysis.py all > ../logs/analysis.txt"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
PNG = HERE.parent / "png"
CAP = HERE.parents[2] / "captures"


def lin(c):
    c = np.asarray(c, dtype=float) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def srgb(l):
    l = np.asarray(l, dtype=float)
    return 255 * np.where(l <= 0.0031308, 12.92 * l, 1.055 * l ** (1 / 2.4) - 0.055)


def load_lin(p):
    return lin(np.asarray(Image.open(p).convert("RGB")))


def probe(img, x, y):
    w, h = img.size
    return [int(v) for v in img.getpixel((int(x * (w - 1)), int(y * (h - 1))))[:3]]


def e3():
    print("E3: alpha blend arithmetic (unshaded plate, alpha 0.7, over a sand floor and over the background; 1280 x 720, Godot 4.7.2, Apple M4 Pro)")
    pts = {"floor alone": 0.06, "plate over floor": 0.30, "plate over background": 0.56, "background alone": 0.85}
    water = {"forward_plus": (25, 115, 178), "gl_compatibility": (22, 115, 179)}   # E1: the typed 0.10, 0.45, 0.70 as the renderer shows it
    for rend, f in (("forward_plus", "blend-fp.png"), ("gl_compatibility", "blend-compat.png")):
        im = Image.open(CAP / f)
        m = {k: probe(im, x, 0.5) for k, x in pts.items()}
        fl, bg = m["floor alone"], m["background alone"]
        w = water[rend]
        a = 0.7
        for k, behind in (("plate over floor", fl), ("plate over background", bg)):
            lin_pred = [round(float(srgb(a * lin(w[i]) + (1 - a) * lin(behind[i])))) for i in range(3)]
            typed_pred = [round(a * w[i] + (1 - a) * behind[i]) for i in range(3)]
            print(f"  {rend:17} {k:22} measured {m[k]}  linear-light blend {lin_pred}  mix of the typed numbers {typed_pred}")


def e7():
    print("E7: cell statistics (top view of the plane, 1080 x 1080, cell_density 8, shader clock about 0.06 s)")
    A, B = load_lin(PNG / "e7-reach1.png"), load_lin(PNG / "e7-reach2.png")
    f1a, ea, fa = A[..., 0] * 2, A[..., 1] * 2, A[..., 2]
    f1b, eb = B[..., 0] * 2, B[..., 1] * 2
    print(f"  mean nearest distance {f1a.mean():.3f} of a square; max {f1a.max():.3f}; pixels where it is above 1: {100 * (f1a > 1).mean():.3f} %")
    print(f"  3 x 3 search against 5 x 5: nearest distance differs at {100 * (np.abs(f1a - f1b) > 0.01).mean():.4f} % of pixels; second minus nearest at {100 * (np.abs(ea - eb) > 0.01).mean():.3f} %")
    print(f"  mean second-minus-nearest {ea.mean():.3f}")
    for n, ew in (("e7-ew0.05.png", 0.05), ("e7-reach1.png", 0.1), ("e7-ew0.2.png", 0.2), ("e7-ew0.3.png", 0.3)):
        print(f"  edge_width {ew:.2f}: mean foam mask {100 * load_lin(PNG / n)[..., 2].mean():.1f} %")


def e9b():
    print("E9b: GPU vertex height (read back as colour) against the same wave function in float64 on the CPU; top view 1080 x 1080, wave_clock set exactly")
    N = 1080
    xs = (np.arange(N) + 0.5) / N * 8 - 4
    X, Z = np.meshgrid(xs, xs)
    tau = 2 * np.pi

    def h(x, z, t, H=0.12, L=3.0, S=0.8):
        d1 = np.array([1.0, 0.3]); d1 /= np.linalg.norm(d1)
        d2 = np.array([-0.4, 1.0]); d2 /= np.linalg.norm(d2)
        k1, k2 = tau / L, tau / (0.6 * L)
        return H * (np.sin(k1 * (d1[0] * x + d1[1] * z - S * t)) + 0.6 * np.sin(k2 * (d2[0] * x + d2[1] * z - 0.8 * S * t)))
    for ck in ("0", "7.3", "20"):
        gpu = (load_lin(PNG / f"e9b-c{ck}.png")[..., 1] - 0.5) / 2
        err = (gpu - h(X, Z, float(ck)))[20:N - 20, 20:N - 20]
        print(f"  wave_clock {float(ck):4.1f}: rms {1000 * np.sqrt((err ** 2).mean()):.2f} mm, max {1000 * np.abs(err).max():.2f} mm (peak height 192 mm; one 8-bit level of the readout is about 2 mm)")


def specks():
    print("Pow of a negative base: exactly-black pixels in a 1080 x 1080 frame (shader 03b-power-curve, sharpness 5)")
    for n, label in (("pow-broken.png", "moving points (clock about 0.5 s), unclamped"), ("pow-clamped.png", "moving points, clamped"),
                     ("pow-static-broken.png", "frozen points (cell_speed 0), unclamped"), ("pow-static-clamped.png", "frozen points, clamped")):
        a = np.asarray(Image.open(PNG / n).convert("RGB")).astype(int)
        print(f"  {label}: {int((a.sum(axis=2) == 0).sum())} black pixels")


def sorting():
    print("E16: a red see-through plane under the water, node nearer the camera (cove, 1280 x 720, Forward+)")
    ims = {n: np.asarray(Image.open(PNG / f"sort-{n}.png").convert("RGB")).astype(int) for n in ("no-render-mode", "depth-opaque", "depth-always")}
    print("  no render_mode line against the three defaults written out: pixels that differ:", int((np.abs(ims["no-render-mode"] - ims["depth-opaque"]).max(axis=2) > 0).sum()))
    print("  default against depth_draw_always: pixels differing by more than 8 levels:", int((np.abs(ims["depth-opaque"] - ims["depth-always"]).max(axis=2) > 8).sum()))
    for n, im in ims.items():
        print(f"  {n:15} pixel at (0.5, 0.93) of the frame: {im[int(0.93 * 719), int(0.5 * 1279)].tolist()}")


def cull():
    print("E14: camera 1.2 m under the water, plane seen from below (1280 x 720, Forward+)")
    for n in ("under-cull-back", "under-cull-disabled"):
        a = np.asarray(Image.open(PNG / f"{n}.png").convert("RGB")).astype(int)
        print(f"  {n}: {100 * (a[..., 2] > a[..., 0] + 25).mean():.1f} % of the frame is water-blue")


if __name__ == "__main__":
    for fn in ([e3, e7, e9b, specks, sorting, cull] if sys.argv[1:] == ["all"] else [globals()[a] for a in sys.argv[1:]]):
        fn()
        print()
