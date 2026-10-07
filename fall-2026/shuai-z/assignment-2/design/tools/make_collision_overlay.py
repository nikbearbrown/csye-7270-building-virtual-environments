"""Draw the collision shapes the game uses over Rudy's game frames.

Makes design/character/collision-r2.png: every frame in game/content/rudy/frames/
on its canvas, with the body capsule (40 x 136 game px) and, on the slash frame,
the sword hitbox (56 x 70 game px), both as set in game/content/rudy/rudy.tscn.
The frames are at 2 texture px per game px (frames.json), so the sheet is at
twice game size. Under each frame it prints how far the art reaches past the
capsule, in game px. Reads only; it changes nothing in game/.

Run from the project root: python3 design/tools/make_collision_overlay.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FRAMES_DIR = ROOT / "game/content/rudy/frames"
OUT = ROOT / "design/character/collision-r2.png"

# From game/content/rudy/rudy.tscn (game px, relative to the body origin).
CAPSULE_RADIUS = 20.0
CAPSULE_HEIGHT = 136.0
CAPSULE_CENTER = (0.0, -68.0)
SWORD_SIZE = (56.0, 70.0)
SWORD_CENTER = (50.0, -76.0)

ORDER = [
    "CHAR-IDLE", "CHAR-RUN-A", "CHAR-RUN-B", "CHAR-RISE", "CHAR-FALL", "CHAR-HURT",
    "CHAR-DEFEAT", "CHAR-RESPAWN", "CHAR-CELEBRATE", "CHAR-SWORD-IDLE",
    "CHAR-SWORD-RUN-A", "CHAR-SWORD-RUN-B", "CHAR-SWORD-RISE", "CHAR-SWORD-FALL",
    "CHAR-SWORD-SLASH", "CHAR-SWORD-BLOCK",
]
COLS = 4
LABEL_H = 64
PAD = 16
BG = (226, 222, 212)
CAPSULE_RGB = (30, 120, 220)
SWORD_RGB = (220, 60, 40)


def font(size):
    for name in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"):
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def main():
    meta = json.loads((FRAMES_DIR / "frames.json").read_text())
    density = meta["density"]
    cw, ch = meta["canvas"]
    ox, oy = meta["origin"]

    def tex(x, y):
        return ox + x * density, oy + y * density

    cap_l, cap_t = tex(CAPSULE_CENTER[0] - CAPSULE_RADIUS, CAPSULE_CENTER[1] - CAPSULE_HEIGHT / 2)
    cap_r, cap_b = tex(CAPSULE_CENTER[0] + CAPSULE_RADIUS, CAPSULE_CENTER[1] + CAPSULE_HEIGHT / 2)
    sw_l, sw_t = tex(SWORD_CENTER[0] - SWORD_SIZE[0] / 2, SWORD_CENTER[1] - SWORD_SIZE[1] / 2)
    sw_r, sw_b = tex(SWORD_CENTER[0] + SWORD_SIZE[0] / 2, SWORD_CENTER[1] + SWORD_SIZE[1] / 2)

    rows = (len(ORDER) + COLS - 1) // COLS
    title_h = 90
    sheet = Image.new("RGB", (COLS * (cw + PAD) + PAD, title_h + rows * (ch + LABEL_H + PAD) + PAD), BG)
    d = ImageDraw.Draw(sheet)
    d.text((PAD, 14), "Rudy's collision, revision 2: capsule 40 x 136 game px (blue), sword hitbox 56 x 70 (red, slash only)",
           fill=(20, 20, 20), font=font(26))
    d.text((PAD, 50), "Game frames at 2x game size. Under each frame: art past the capsule, in game px (left / right / top).",
           fill=(60, 60, 60), font=font(20))

    small = font(19)
    for i, pose in enumerate(ORDER):
        frame = Image.open(FRAMES_DIR / f"{pose}.png").convert("RGBA")
        x0 = PAD + (i % COLS) * (cw + PAD)
        y0 = title_h + (i // COLS) * (ch + LABEL_H + PAD)
        sheet.paste(frame, (x0, y0), frame)

        alpha = np.asarray(frame)[:, :, 3] > 32
        ys, xs = np.nonzero(alpha)
        over_l = max(0.0, (cap_l - xs.min()) / density)
        over_r = max(0.0, (xs.max() + 1 - cap_r) / density)
        over_t = max(0.0, (cap_t - ys.min()) / density)

        d.rounded_rectangle((x0 + cap_l, y0 + cap_t, x0 + cap_r, y0 + cap_b),
                            radius=CAPSULE_RADIUS * density, outline=CAPSULE_RGB, width=3)
        if pose == "CHAR-SWORD-SLASH":
            d.rectangle((x0 + sw_l, y0 + sw_t, x0 + sw_r, y0 + sw_b), outline=SWORD_RGB, width=3)
        d.line((x0 + ox - 8, y0 + oy, x0 + ox + 8, y0 + oy), fill=(20, 20, 20), width=2)

        d.text((x0, y0 + ch + 6), pose, fill=(20, 20, 20), font=small)
        d.text((x0, y0 + ch + 32), f"past capsule: {over_l:.0f} / {over_r:.0f} / {over_t:.0f}",
               fill=(60, 60, 60), font=small)
        print(f"{pose:18s} left {over_l:5.1f}  right {over_r:5.1f}  top {over_t:5.1f}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)} {sheet.size}")


if __name__ == "__main__":
    main()
