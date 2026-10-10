#!/usr/bin/env python3
"""Find every separate figure in a generated sheet and number it, so a human can pick figures by number.

FLUX does not honour "a 3 x 4 grid", so frames are cut by figure, not by grid cell.

    python gen/figures.py gen/raw/ART-PC-01/<run>.png      -> gen/thumbs/ART-PC-01/<run>-figures.png + .json

The JSON lists {"n": 1, "box": [x0, y0, x1, y1]} per figure, left-to-right within rows; mapping files
refer to a figure as {"src": ..., "box": [...]} (art_process.py) so the crop stays explicit in the log.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def find_figures(im: Image.Image, threshold: int = 235, merge_px: int = 14, min_area: int = 1500) -> list:
    from scipy import ndimage
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    ink = (a < threshold).any(axis=2)
    # merge a figure's separate parts (glow rays, cast shadow, thin limbs) before labelling
    grown = ndimage.binary_dilation(ink, structure=np.ones((3, 3)), iterations=merge_px)
    labels, _ = ndimage.label(grown)
    boxes = []
    for i, sl in enumerate(ndimage.find_objects(labels), start=1):
        if sl is None:
            continue
        real = ink[sl] & (labels[sl] == i)
        if real.sum() < min_area:
            continue
        ys, xs = np.nonzero(real)
        boxes.append([int(sl[1].start + xs.min()), int(sl[0].start + ys.min()), int(sl[1].start + xs.max()) + 1, int(sl[0].start + ys.max()) + 1])
    h = ink.shape[0]
    band = max(1, h // 6)
    boxes.sort(key=lambda b: (((b[1] + b[3]) // 2) // band, b[0]))
    return boxes


def main() -> None:
    src = Path(sys.argv[1])
    im = Image.open(src).convert("RGB")
    boxes = find_figures(im)
    asset = src.parent.name
    out_dir = ROOT / "gen" / "thumbs" / asset
    out_dir.mkdir(parents=True, exist_ok=True)
    overlay = im.copy()
    d = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except OSError:
        font = ImageFont.load_default()
    for i, b in enumerate(boxes, start=1):
        d.rectangle(b, outline="#E0287A", width=4)
        d.text((b[0] + 6, b[1] + 4), str(i), fill="#E0287A", font=font)
    overlay.thumbnail((1024, 1024))
    overlay.save(out_dir / f"{src.stem}-figures.png", optimize=True)
    (out_dir / f"{src.stem}-figures.json").write_text(json.dumps([{"n": i, "box": b} for i, b in enumerate(boxes, start=1)], indent=1) + "\n")
    print(f"{src.name}: {len(boxes)} figures -> gen/thumbs/{asset}/{src.stem}-figures.png")


if __name__ == "__main__":
    main()
