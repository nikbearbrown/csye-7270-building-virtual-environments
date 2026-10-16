#!/usr/bin/env python3
"""Character sheet vs generated sprite vs the running game, one column per pose (CHARACTER-SHEET R2 order).

Row 1: pre-generation blockout (design-v1)   Row 2: generated, palette-locked frame (pc_sheet.png)
Row 3: the frame as captured in the game (evidence/screens/pose-*.png, via godot/tests/capture.gd)
Row 4: silhouette of the generated frame at actual size, x3

    python3 design/character/make_comparison.py           -> design/character/sheet-vs-game.png
    python3 design/character/make_comparison.py --facing  -> design/character/sheet-vs-game-facing.png
        (adds the frame facing left and with the F3 hurtbox, from scripts/capture_facing.gd)
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
POSES = ["turn_front", "idle", "walk_contact", "walk_passing", "cast", "hurt", "levelup", "sunflare", "defeat", "victory"]
BLOCKOUT_ORDER = ["turn_front", "turn_side", "turn_back", "idle", "walk_contact", "walk_passing",
                  "cast", "hurt", "levelup", "sunflare", "defeat", "victory"]
CELL = 160


def blockout(pose: str) -> Image.Image:
    sheet = Image.open(ROOT / "design/character/blockout-poses-x8.png").convert("RGBA")
    i = BLOCKOUT_ORDER.index(pose)
    tile_h = (sheet.height) // 2
    x, y = (i % 6) * 256, (i // 6) * tile_h
    return sheet.crop((x, y, x + 256, y + 256)).resize((CELL, CELL), Image.NEAREST)


def generated(pose: str) -> Image.Image:
    sheet = Image.open(ROOT / "godot/assets/art/pc_sheet.png").convert("RGBA")
    i = POSES.index(pose)
    frame = sheet.crop((i * 32, 0, i * 32 + 32, 32))
    ground = Image.new("RGBA", (32, 32), "#C7D0E0")
    ground.alpha_composite(frame)
    return ground.resize((CELL, CELL), Image.NEAREST)


def in_game(pose: str, suffix: str = "") -> Image.Image:
    shot = Image.open(ROOT / f"evidence/screens/pose-{pose}{suffix}.png").convert("RGBA")
    # window is 1280x720 = 2x the 640x360 viewport; the camera centres the courier, whose frame is drawn at (-16,-20)
    cx, cy = shot.width // 2, shot.height // 2
    crop = shot.crop((cx - 48, cy - 56, cx + 48, cy + 40))
    return crop.resize((CELL, CELL), Image.NEAREST)


def silhouette(pose: str) -> Image.Image:
    sheet = Image.open(ROOT / "godot/assets/art/pc_sheet.png").convert("RGBA")
    i = POSES.index(pose)
    a = sheet.crop((i * 32, 0, i * 32 + 32, 32)).split()[3]
    sil = Image.new("RGBA", (32, 32), "#C7D0E0")
    sil.paste(Image.new("RGBA", (32, 32), "#14121C"), (0, 0), a)
    return sil.resize((96, 96), Image.NEAREST)


def main(facing: bool = False) -> None:
    rows = [("blockout (design-v1)", blockout), ("generated frame x5", generated), ("in game (capture)", in_game)]
    if facing:
        rows = [("blockout (design-v1)", blockout), ("generated frame x5", generated), ("in game, facing right", in_game),
                ("in game, facing left", lambda p: in_game(p, "-left")),
                ("facing left + F3 hurtbox", lambda p: in_game(p, "-left-hurtbox"))]
    left = 170
    out = Image.new("RGB", (left + CELL * len(POSES), 30 + CELL * len(rows) + 110), "#0E1020")
    d = ImageDraw.Draw(out)
    for c, pose in enumerate(POSES):
        d.text((left + c * CELL + 6, 8), pose, fill="#FFF1C9")
    for r, (label, fn) in enumerate(rows):
        d.text((8, 30 + r * CELL + CELL // 2), label, fill="#C7D0E0")
        for c, pose in enumerate(POSES):
            out.paste(fn(pose).convert("RGB"), (left + c * CELL, 30 + r * CELL))
    y = 30 + CELL * len(rows) + 8
    d.text((8, y + 40), "silhouette, 32 px x3", fill="#C7D0E0")
    for c, pose in enumerate(POSES):
        out.paste(silhouette(pose).convert("RGB"), (left + c * CELL + 32, y))
    # the hurtbox (r = 10) on the generated idle frame, at the origin the game draws it from (player.gd SPRITE_ORIGIN)
    idle = Image.open(ROOT / "godot/assets/art/pc_sheet.png").convert("RGBA").crop((32, 0, 64, 32))
    ov = Image.new("RGBA", (32, 32), "#C7D0E0")
    ov.alpha_composite(idle)
    ov = ov.resize((256, 256), Image.NEAREST)
    od = ImageDraw.Draw(ov)
    ox, oy = 16, 23
    od.ellipse([(ox - 10) * 8, (oy - 10) * 8, (ox + 10) * 8, (oy + 10) * 8], outline="#FF3366", width=4)
    od.line([ox * 8, 0, ox * 8, 255], fill="#FF3366", width=1)
    od.line([0, oy * 8, 255, oy * 8], fill="#FF3366", width=1)
    if not facing:
        ov.save(ROOT / "design/character/collision-overlay-generated-x8.png")
    dest = ROOT / ("design/character/sheet-vs-game-facing.png" if facing else "design/character/sheet-vs-game.png")
    out.save(dest, optimize=True)
    print(dest)


if __name__ == "__main__":
    import sys
    main(facing="--facing" in sys.argv)
