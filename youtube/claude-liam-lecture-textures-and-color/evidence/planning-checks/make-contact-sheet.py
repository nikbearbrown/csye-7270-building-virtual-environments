#!/usr/bin/env python3
"""make-contact-sheet.py: one picture of the renders the film's captures are built from (png/plus-*.png), so a reviewer can look at them at a glance.
Writes contact-sheet.png next to this file. Pillow only. Run: python3 -I make-contact-sheet.py"""
from pathlib import Path
from PIL import Image, ImageDraw
here = Path(__file__).resolve().parent
P = here / "png"
CELLS = [
    ("B03 lookup (checker)", "a1-01-lookup-checker"), ("B04 F table, default (smeared)", "a1-01-lookup-f-linear"), ("B05 filter_nearest", "a1-02-nearest-f"),
    ("B06 flipped address", "a1-03-flip-f"), ("B07 repeat off", "a1-04-repeat-off-f"), ("B07 repeat on", "a1-05-repeat-on-f"),
    ("B09 empty fragment, modulate 50%", "a2-06-empty-modulated"), ("B09 plain lookup", "a2-07-own-texture-modulated"), ("B10 tint", "a2-08-tint"),
    ("B11 invert", "a2-09-invert"), ("B12 invert all four", "a2-10-invert-all-sprite"), ("B13 brighten", "a2-11-brighten"),
    ("B14 gray: red channel", "a2-12-gray-red"), ("B15 gray: weighted", "a2-13-gray-weighted"), ("B16 mix, amount 0.5", "a2-14-mix-0.5"),
    ("B17 noise mask", "a3-15-noise-mask"), ("B19 step 0.5", "a3-16-step-0.5"), ("B20 cut only, 0.5", "a3-17-cut-0.5"),
    ("B23 dissolve, 0.25", "a3-18-dissolve-0.25"), ("B23 dissolve, 0.5", "a3-18-dissolve-0.5"), ("B24 wipe, 0.5", "a3-18-wipe-0.5"),
    ("B25 first version at 0", "a3-19-first-try-0.0"), ("B25 fixed at 0", "a3-18-dissolve-0.0"), ("B27 3D, Forward+", "a4-20-blend-3d-forward_plus"),
    ("B27 3D, Compatibility", "a4-20-blend-3d-gl_compatibility"), ("B32 2D, HDR 2D on", "a4-21-blend-2d-forward_plus-hdr2d"), ("B32 2D, default", "a4-21-blend-2d-forward_plus"),
    ("B37 hinted, Forward+", "a5-25-swatch-hinted-forward_plus"), ("B37 not hinted, Forward+", "a5-26-swatch-plain-forward_plus"), ("B37 not hinted, Compat.", "a5-26-swatch-plain-gl_compatibility"),
    ("B38 mask, no hint, F+", "a5-27-mask-plain-forward_plus"), ("B38 mask, hint, F+", "a5-28-mask-hinted-forward_plus"), ("B35 patches, HDR 2D on", "../scratch-patches-forward_plus-hdr2d"),
]
W, H, COLS, PAD = 320, 180, 6, 8
rows = (len(CELLS) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * (W + PAD) + PAD, rows * (H + PAD + 14) + PAD), (255, 255, 255))
d = ImageDraw.Draw(sheet)
for i, (cap, name) in enumerate(CELLS):
    f = P / f"plus-{name}.png" if not name.startswith("..") else P / (name.replace("../", "") + ".png")
    x, y = PAD + (i % COLS) * (W + PAD), PAD + (i // COLS) * (H + PAD + 14)
    if f.exists():
        im = Image.open(f).convert("RGB"); im.thumbnail((W, H)); sheet.paste(im, (x + (W - im.width) // 2, y + 14 + (H - im.height) // 2))
    else:
        print('MISSING', f)
    d.text((x, y), cap, fill=(61, 57, 41))
sheet.save(here / "contact-sheet.png")
print("wrote", here / "contact-sheet.png", sheet.size)
