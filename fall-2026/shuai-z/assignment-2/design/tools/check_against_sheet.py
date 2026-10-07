#!/usr/bin/env python3
"""Put a generated image next to the character sheet at game size, where Rudy is 160 px tall.

    python3 design/tools/check_against_sheet.py _raw/CHAR-REF-04.jpg --views front,3q,side,back \
        -o generated/checks/CHAR-REF-04-check.png
    python3 design/tools/check_against_sheet.py _raw/CHAR-IDLE-01.png --views idle \
        -o generated/checks/CHAR-IDLE-01-check.png

Views are the turnaround's front, 3q, side and back, or any pose name in make_blockouts.POSES.
Rows: the v1 blockout (pose shape), the accepted reference CHAR-REF-07 (identity and proportions),
the generated image, the generated image with the in-engine outline on the planned wheat, the same
in grayscale, and a solid black silhouette. The flat background is keyed out by its color: a rough
matte for judging only (final sprites are matted with rembg). Every figure is scaled so that its
full height, cowlick included, is 160 px. Guide lines mark the chin and the top of the head from
CHARACTER-SHEET.md revision 2 (measured on CHAR-REF-07).
Code written by Claude Code; it draws nothing new, it only rescales and compares.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("make_blockouts", HERE / "make_blockouts.py")
bo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bo)

GAME_H = 160
CHIN, HEAD_TOP = 107, 151  # game px above the soles: CHARACTER-SHEET.md revision 2 (v1 blockout: 90, 150)
REFERENCE = HERE.parents[1] / "generated" / "accepted" / "CHAR-REF-07.jpg"
REF_INDEX = {"front": 0, "3q": 1, "side": 2, "back": 3}  # figures in the reference, left to right
CELL_W, CELL_H = 200, 200


def generated_figures(path):
    """Split an image with a flat background into figures, left to right, as RGBA crops."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    k = 16
    corners = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3),
                              a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    # background = close to the corner color AND as blue as it (the grey robe is close in value but not blue)
    near = np.abs(a - bg).sum(axis=2) < 90
    blue = (a[:, :, 2] - a[:, :, 0]) > (bg[2] - bg[0]) * 0.55
    mask = Image.fromarray(((~(near & blue)) * 255).astype(np.uint8))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    m = np.asarray(mask) > 0
    cols = m.any(axis=0)
    runs, start = [], None
    for x in range(w + 1):
        on = x < w and cols[x]
        if on and start is None:
            start = x
        if not on and start is not None:
            if x - start > 30:
                runs.append((start, x))
            start = None
    figs = []
    for x0, x1 in runs:
        rows = np.where(m[:, x0:x1].any(axis=1))[0]
        y0, y1 = int(rows.min()), int(rows.max()) + 1
        crop = im.crop((x0, y0, x1, y1)).convert("RGBA")
        crop.putalpha(mask.crop((x0, y0, x1, y1)))
        figs.append(crop)
    return figs, tuple(int(v) for v in bg)


def blockout_figure(view):
    made = bo.rudy_view(view, 1.0) if view in ("front", "3q", "side", "back") else bo.rudy(view, 1.0)
    img = made[0]
    img = img.crop(img.getchannel("A").getbbox())
    return img.resize((max(1, img.width // bo.SS), max(1, img.height // bo.SS)), Image.LANCZOS)


def to_game(img):
    s = GAME_H / img.height
    return img.resize((max(1, round(img.width * s)), GAME_H), Image.LANCZOS)


def with_outline(img, px=4):
    """Simulate the in-engine 4 px dark-brown outer outline at game size."""
    pad = px + 2
    big = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(img, (pad, pad))
    return bo.outline_under(big, px)


def row(figs, bg, guides=True, outline=False):
    strip = Image.new("RGBA", (CELL_W * len(figs), CELL_H), bg)
    d = ImageDraw.Draw(strip)
    base = CELL_H - 20
    if guides:
        for gy, col in ((CHIN, (200, 60, 60, 255)), (HEAD_TOP, (60, 90, 200, 255))):
            y = base - gy
            for x in range(0, strip.width, 10):
                d.line([(x, y), (x + 5, y)], fill=col, width=1)
    d.line([(0, base), (strip.width, base)], fill=(150, 140, 130, 255), width=1)
    for i, f in enumerate(figs):
        g = to_game(f)
        dy = 0
        if outline:
            g = with_outline(g)
            dy = (g.height - GAME_H) // 2
        strip.alpha_composite(g, (i * CELL_W + (CELL_W - g.width) // 2, base - GAME_H - dy))
    return strip


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("image")
    ap.add_argument("--views", required=True, help="comma-separated: front,3q,side,back or pose names")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--no-reference", action="store_true", help="skip the reference row (checking the reference itself)")
    args = ap.parse_args()
    views = [v.strip() for v in args.views.split(",")]
    gen, bg = generated_figures(args.image)
    ref_figs = None if args.no_reference else generated_figures(REFERENCE)[0]
    if len(gen) != len(views):
        print(f"warning: found {len(gen)} figures in the image, expected {len(views)}")
    gen = gen[:len(views)]
    sheet = [blockout_figure(v) for v in views]
    wheat = bo.rgb(bo.WHEAT)
    white = (255, 255, 255, 255)
    rows = [("character sheet v1 blockout (pose shape), 160 px", row(sheet, white))]
    if ref_figs:
        refs = [ref_figs[REF_INDEX.get(v, 2)] for v in views]
        rows.append(("accepted reference CHAR-REF-07 (identity, proportions), 160 px", row(refs, white)))
    rows.append((f"{Path(args.image).name}, 160 px", row(gen, white)))
    on_wheat = row(gen, wheat, guides=False, outline=True)
    rows.append(("generated + the in-engine 4 px outline, on the planned wheat", on_wheat))
    rows.append(("the same, in grayscale", ImageOps.grayscale(on_wheat.convert("RGB")).convert("RGBA")))
    sil = []
    for f in gen:
        black = Image.new("RGBA", f.size, (0, 0, 0, 255))
        black.putalpha(f.getchannel("A"))
        sil.append(black)
    rows.append(("silhouette at game size", row(sil, white, guides=False)))
    W = CELL_W * len(views) + 40
    H = 70 + sum(CELL_H + 30 for _ in rows) + 40
    out = Image.new("RGBA", (W, H), bo.rgb("#F4F1EA"))
    d = ImageDraw.Draw(out)
    d.text((20, 16), f"Check at game size: {Path(args.image).name} against the character sheet", font=bo.font(20),
           fill=bo.rgb(bo.LINE))
    d.text((20, 44), f"Red dashes: chin ({CHIN} px). Blue dashes: top of head ({HEAD_TOP} px), from the sheet's "
           "revision 2. Views: " + ", ".join(views), font=bo.font(14, bold=False), fill=bo.rgb(bo.LINE))
    y = 70
    for title, strip in rows:
        d.text((20, y), title, font=bo.font(15), fill=bo.rgb(bo.LINE))
        out.alpha_composite(strip, (20, y + 22))
        y += CELL_H + 30
    d.text((20, H - 28), "Rough color-key matte, for judging only. Generated figures keep the background color "
           f"{bg} outside the key.", font=bo.font(12, bold=False), fill=bo.rgb(bo.LINE))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(args.output)
    print("wrote", args.output)


if __name__ == "__main__":
    main()
