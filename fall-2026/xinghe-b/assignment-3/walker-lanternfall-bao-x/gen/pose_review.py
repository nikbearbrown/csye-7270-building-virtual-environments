#!/usr/bin/env python3
"""Review sheet for per-pose generations: one row per pose, one column per candidate.
Each cell shows the raw thumbnail and the palette-locked 32 x 32 result (x4) on the game's ground colour,
so candidates are judged at the size the player sees.

    gen/.venv-art/bin/python gen/pose_review.py ART-PC-01   -> gen/rejected/ART-PC-01-pose-review.png
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from art_process import fit, key_background, lock_palette, rgb

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["turn_front", "idle", "walk_contact", "walk_passing", "cast", "hurt", "levelup", "sunflare", "defeat", "victory"]


def faces_left(im: Image.Image) -> bool:
    """True when the glowing lens sits left of the figure's centre of mass."""
    a = np.asarray(im.convert("RGBA")).astype(np.int16)
    body = a[..., 3] > 0
    lens = body & (a[..., 0] > 200) & (a[..., 1] > 150) & (a[..., 2] < 120)
    if lens.sum() < 20 or body.sum() == 0:
        return False
    return bool(np.nonzero(lens)[1].mean() < np.nonzero(body)[1].mean())


def game_preview(src: Path, palette) -> tuple:
    im = key_background(Image.open(src).convert("RGBA"), 235)
    flipped = faces_left(im)
    if flipped:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    k = 4
    locked = lock_palette(fit(im, 32 * k, 32 * k, 0.95 * 30 / 32, "bottom"), palette, rgb("#14121C"), 14.0, supersample=k)
    return locked, flipped


def main() -> None:
    asset = sys.argv[1]
    palette = [rgb(c) for c in json.loads((ROOT / "godot/assets/art/palettes.json").read_text())["character"]]
    rows: dict = {}
    for side in sorted((ROOT / "gen" / "log" / asset).glob("*.json")):
        m = json.loads(side.read_text())
        pose = m["settings"].get("pose")
        if pose:
            rows.setdefault(pose, []).append(m)
    poses = [p for p in ORDER if p in rows]
    cols = max(len(v) for v in rows.values())
    cw, ch = 300, 150
    sheet = Image.new("RGB", (140 + cols * cw, len(poses) * ch), "#0E1020")
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except OSError:
        font = ImageFont.load_default()
    for r, pose in enumerate(poses):
        d.text((8, r * ch + 60), pose, fill="#FFF1C9", font=font)
        for c, m in enumerate(sorted(rows[pose], key=lambda x: x["created_utc"])):
            x0, y0 = 140 + c * cw, r * ch
            raw = Image.open(ROOT / m["raw_outputs"][0]).convert("RGB")
            raw.thumbnail((140, 140))
            sheet.paste(raw, (x0 + 4, y0 + 5))
            locked, flipped = game_preview(ROOT / m["raw_outputs"][0], palette)
            ground = Image.new("RGBA", (32, 32), "#1F2540")
            ground.alpha_composite(locked)
            sheet.paste(ground.convert("RGB").resize((128, 128), Image.NEAREST), (x0 + 150, y0 + 11))
            verdict = ((m.get("decision") or {}).get("verdict") or "pending").upper()
            tag = f"s{m['settings']['seed']} {verdict}" + (" (mirrored)" if flipped else "")
            d.text((x0 + 150, y0 + 138 - 16), tag, fill="#C7D0E0", font=ImageFont.load_default())
    out = ROOT / "gen" / "rejected" / f"{asset}-pose-review.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, optimize=True)
    print(out)


if __name__ == "__main__":
    main()
