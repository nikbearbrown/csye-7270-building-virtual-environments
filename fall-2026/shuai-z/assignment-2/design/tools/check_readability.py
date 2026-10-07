#!/usr/bin/env python3
"""Re-measure Rudy's readability on the generated Level 1 (CHANGE-BRIEF.md, predicted failure 2).

    python3 design/tools/check_readability.py

Prints the luminance contrast (WCAG formula) between Rudy's colours (CHARACTER-SHEET.md,
revision 2) and colours sampled from the generated layers in game/content/level_1/art/,
and writes evidence/2b/2b-readability.png: in-engine crops of Rudy, with the outer outline,
beside grayscale copies. Run the 2b capture first. Code written by Claude Code.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "game/content/level_1/art"
EVIDENCE = ROOT / "evidence/2b"
RUDY = {"hair": "C9905A", "eyes": "475827", "robe": "6F717D", "skin": "FCC5A6",
        "leather": "754634", "trim": "D4BEA6", "outline": "290F0D"}
CROPS = [("2b-on-wheat.png", "default form over the wheat"),
         ("2b-sword-on-wheat.png", "sword form over the wheat"),
         ("2b-jump-over-sky.png", "a jump, over the sky")]


def luminance(rgb):
    c = np.asarray(rgb, float) / 255
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def backgrounds():
    """Median colours of what stands behind Rudy: the wheat and the meadow behind his body,
    the sky above the fields, and the path band at his feet."""
    env = json.loads((ART / "env.json").read_text())
    layers = env["layers"]
    fields = np.asarray(Image.open(ART / "fields.png").convert("RGBA"), float)
    top = layers["fields"]["horizon_row"] + 15
    band = fields[top:env["ground_y"] - layers["fields"]["y"]]
    px = band[..., :3][band[..., 3] > 200]
    r, g, b = px[:, 0], px[:, 1], px[:, 2]
    sky = np.asarray(Image.open(ART / "sky_castle.jpg").convert("RGB"), float)[100:600].reshape(-1, 3)
    ground = np.asarray(Image.open(ART / "ground_tile.png").convert("RGB"), float)
    walk = layers["ground_tile"]["walk_row_texture_px"]
    return {
        "wheat": np.median(px[(r > g * 0.98) & (r > b * 1.3)], axis=0),
        "meadow": np.median(px[(g > r) & (g > b)], axis=0),
        "sky": np.median(sky, axis=0),
        "path": np.median(ground[walk - 8:walk + 4].reshape(-1, 3), axis=0),
    }


def main():
    bg = backgrounds()
    print("| Rudy | " + " | ".join(f"{k} `#{''.join(f'{int(v):02X}' for v in c)}`" for k, c in bg.items()) + " |")
    print("|---|" + "---|" * len(bg))
    for name, hexcol in RUDY.items():
        rgb = [int(hexcol[i:i + 2], 16) for i in (0, 2, 4)]
        print(f"| {name} `#{hexcol}` | " + " | ".join(f"{contrast(rgb, c):.2f}" for c in bg.values()) + " |")

    crops = [(Image.open(EVIDENCE / f).convert("RGB"), label) for f, label in CROPS]
    w, h = crops[0][0].size
    sheet = Image.new("RGB", (20 + 2 * (w + 20), 60 + len(crops) * (h + 40)), (244, 241, 234))
    d = ImageDraw.Draw(sheet)
    d.text((20, 18), "Step 2b: Rudy over the generated Level 1, in colour and in grayscale (in-engine, game size)",
           fill=(41, 15, 13))
    for i, (im, label) in enumerate(crops):
        y = 60 + i * (h + 40)
        sheet.paste(im, (20, y))
        sheet.paste(ImageOps.grayscale(im).convert("RGB"), (40 + w, y))
        d.text((20, y + h + 8), label, fill=(41, 15, 13))
    out = EVIDENCE / "2b-readability.png"
    sheet.save(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
