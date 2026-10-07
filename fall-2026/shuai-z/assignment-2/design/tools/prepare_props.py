#!/usr/bin/env python3
"""Turn the accepted props and the goblin into game sprites, sized to the greybox's collision shapes.

    python3 design/tools/prepare_props.py

Each source is keyed like Rudy's frames (design/tools/matte_sprites.py); a prop that glows keeps its
glow as semi-transparent light of the glow's color. Then it is scaled so its main body has the size the
greybox already uses (SIZES), stored at 2 texture px per game px, and placed on a canvas shared by its
variants (the dark and lit waystone, the goblin's three frames), so that swapping frames never moves it:
- grounded things stand with the bottom of their solid body on the canvas's origin line;
- the portal's origin is the middle of its disc, where the greybox draws the circle on the ground;
- the pickup's origin is its middle, since it floats.

Writes the PNGs and props.json to game/content/level_1/art/ (the goblin's to game/content/goblin/frames/, the
hearts' to game/ui/art/),
and generated/checks/PROPS-layers-check.jpg: a 1920x1080 mock-up over the Level 1 layers, with Rudy.
The originals in generated/accepted/ are never changed. Code written by Claude Code; it draws nothing new.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ACCEPTED = ROOT / "generated" / "accepted"
LEVEL_ART = ROOT / "game" / "content" / "level_1" / "art"
GOBLIN_ART = ROOT / "game" / "content" / "goblin" / "frames"
UI_ART = ROOT / "game" / "ui" / "art"
CHECK = ROOT / "generated" / "checks" / "PROPS-layers-check.jpg"

_spec = importlib.util.spec_from_file_location("matte_sprites", HERE / "matte_sprites.py")
ms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ms)

DENSITY = 2
PAD = 6 * DENSITY

# group -> output folder, the measure that sets the scale, the target in game px, the origin rule, and frames
# (asset ID -> accepted original, glow color or None, and optionally which half of the image). The targets are the greybox's sizes:
# the waystone 112 px tall (waystone.gd) and the portal's disc 300 px wide (portal.gd). The spikes are 64 px
# tall and the goblin 128 px (walk frame A): at the greybox's sizes (160 px wide, 104 px tall) the spikes stood
# twice as tall as their hazard box and the goblin hid among the ground's wheat tufts, so I asked for these
# (the hazard and goblin boxes change to match). The pickup is about 72 px tall and a heart 48 px wide
# (Claude's calls; the HUD's code-drawn hearts are 44 px).
GROUPS = {
    "spikes": dict(out=LEVEL_ART, measure="height", target=64, origin="bottom",
                   frames={"ENV-SPIKES": ("ENV-SPIKES-02.jpg", None)}),
    "waystone": dict(out=LEVEL_ART, measure="height", target=112, origin="bottom",
                     frames={"ENV-WAYSTONE": ("ENV-WAYSTONE-01.jpg", None),
                             "ENV-WAYSTONE-LIT": ("ENV-WAYSTONE-LIT-01.jpg", (205, 240, 255))}),
    "portal": dict(out=LEVEL_ART, measure="width", target=300, origin="middle", squash_y=0.55,
                   frames={"ENV-PORTAL": ("ENV-PORTAL-02.jpg", (255, 240, 205))}),
    "pickup": dict(out=LEVEL_ART, measure="height", target=72, origin="middle",
                   frames={"PROP-SWORDSHIELD": ("PROP-SWORDSHIELD-02.jpg", (255, 185, 115))}),
    "hearts": dict(out=UI_ART, measure="width", target=48, origin="middle",
                   frames={"UI-HEART-FULL": ("UI-HEART-01.jpg", None, "left"),
                           "UI-HEART-EMPTY": ("UI-HEART-01.jpg", None, "right")}),
    "goblin": dict(out=GOBLIN_ART, measure="height", target=128, origin="bottom",
                   frames={"ENEMY-GOBLIN-WALK-A": ("ENEMY-GOBLIN-WALK-A-01.jpg", None),
                           "ENEMY-GOBLIN-WALK-B": ("ENEMY-GOBLIN-WALK-B-01.jpg", None),
                           "ENEMY-GOBLIN-SQUASH": ("ENEMY-GOBLIN-SQUASH-01.jpg", None)}),
}
# The squashed goblin was generated in its own turn at its own scale, so it cannot share walk A's scale:
# it is scaled so that its length is 1.3 times the walking goblin's height (Claude's call).
SQUASH_LENGTH = 1.3
# squash_y flattens a group vertically after scaling. Gemini drew the circle from a high angle, a
# 2:1 ellipse; at 0.55 it is about 3.5:1, closer to lying on the ground (Claude's call).


def solid_box(img, thr=230):
    """Bounding box of the nearly opaque pixels: the body, without glow, motes or soft edges."""
    a = np.asarray(img.getchannel("A")) > thr
    ys, xs = np.nonzero(a)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def main():
    report = {}
    for gname, g in GROUPS.items():
        cut = {}
        for fid, (src, glow, *half) in g["frames"].items():
            source = Image.open(ACCEPTED / src)
            if half:  # two icons side by side in one image: split at the middle
                w, h = source.size
                source = source.crop((0, 0, w // 2, h) if half[0] == "left" else (w // 2, 0, w, h))
            rgba, _ = ms.matte(source, glow=glow, min_glow_area=300)
            img = ms.to_image(rgba)
            img = img.crop(img.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox())
            cut[fid] = (img, src, glow)
        first = next(iter(cut.values()))[0]
        x0, y0, x1, y1 = solid_box(first)
        size = (x1 - x0) if g["measure"] == "width" else (y1 - y0)
        scale = g["target"] * DENSITY / size
        placed = {}
        for fid, (img, src, glow) in cut.items():
            s = scale
            if fid == "ENEMY-GOBLIN-SQUASH":
                bx0, _, bx1, _ = solid_box(img)
                s = g["target"] * SQUASH_LENGTH * DENSITY / (bx1 - bx0)
            im = ms.shrink(img, s)
            if g.get("squash_y"):
                im = im.convert("RGBa").resize((im.width, round(im.height * g["squash_y"])), Image.LANCZOS).convert("RGBA")
            bx0, by0, bx1, by1 = solid_box(im)
            ax = (bx0 + bx1) / 2
            ay = by1 if g["origin"] == "bottom" else (by0 + by1) / 2
            placed[fid] = dict(img=im, ax=ax, ay=ay, scale=s, src=src, glow=glow)
        left = max(p["ax"] for p in placed.values())
        right = max(p["img"].width - p["ax"] for p in placed.values())
        up = max(p["ay"] for p in placed.values())
        down = max(p["img"].height - p["ay"] for p in placed.values())
        half = int(np.ceil(max(left, right))) + PAD
        W, H = 2 * half, int(np.ceil(up + down)) + 2 * PAD
        origin = (half, int(np.ceil(up)) + PAD)
        g["out"].mkdir(parents=True, exist_ok=True)
        for fid, p in placed.items():
            canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            canvas.alpha_composite(p["img"], (round(origin[0] - p["ax"]), round(origin[1] - p["ay"])))
            canvas.save(g["out"] / f"{fid}.png")
            report[fid] = {"file": str((g["out"] / f"{fid}.png").relative_to(ROOT / "game")),
                           "source": f"generated/accepted/{p['src']}", "group": gname, "density": DENSITY,
                           "canvas": [W, H], "origin": list(origin), "origin_rule": g["origin"],
                           "scale": round(p["scale"], 5), "squash_y": g.get("squash_y", 1.0), "glow_rgb": list(p["glow"]) if p["glow"] else None,
                           "body_game_px": [round((solid_box(p["img"])[2] - solid_box(p["img"])[0]) / DENSITY, 1),
                                            round((solid_box(p["img"])[3] - solid_box(p["img"])[1]) / DENSITY, 1)]}
            print(f"{fid:22s} body {report[fid]['body_game_px']} game px, canvas {W}x{H}, scale {p['scale']:.4f}")
    manifest = {"about": "Props and the goblin, made by design/tools/prepare_props.py from generated/accepted/. "
                         "Canvas and origin in texture px; draw at scale 1/density. Paths are relative to game/.",
                "frames": report}
    (LEVEL_ART / "props.json").write_text(json.dumps(manifest, indent=2) + "\n")
    mockup(report)


def view_at(cam, env, motion):
    """The Level 1 layers as the camera sees them at x = cam, with the far and middle layers scrolled
    at their motion scales and the ground at the camera's speed."""
    view = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255))
    sky = Image.open(LEVEL_ART / "sky_castle.jpg").convert("RGBA")
    view.alpha_composite(sky, (-round(cam * motion["far"]), 0))
    f = Image.open(LEVEL_ART / "fields.png")
    off = round(cam * motion["mid"]) % f.width
    for x in range(-off, 1920, f.width):
        view.alpha_composite(f, (x, env["fields"]["y"]))
    tile = ms.shrink(Image.open(LEVEL_ART / "ground_tile.png"), 0.5)
    off = cam % tile.width
    for x in range(-off, 1920, tile.width):
        view.alpha_composite(tile, (x, round(env["ground_tile"]["y"])))
    return view


def mockup(report):
    """Two views of the level (the camera at x 0 and at the far end), with every prop, the goblin and Rudy."""
    env = json.loads((LEVEL_ART / "env.json").read_text())["layers"]
    motion = {"far": env["sky_castle"]["max_motion_scale"], "mid": 0.4}
    G = 840

    def put(view, fid, x, y):
        r = report[fid]
        im = ms.shrink(Image.open(ROOT / "game" / r["file"]), 1 / DENSITY)
        view.alpha_composite(im, (round(x - r["origin"][0] / DENSITY), round(y - r["origin"][1] / DENSITY)))

    man = json.loads((ROOT / "game/content/rudy/frames/frames.json").read_text())
    ox, oy = (v / man["density"] for v in man["origin"])

    def rudy(view, fid, x):
        fr = ms.shrink(Image.open(ROOT / f"game/content/rudy/frames/{fid}.png"), 1 / man["density"])
        view.alpha_composite(fr, (round(x - ox), round(G - oy)))

    a = view_at(0, env, motion)
    put(a, "ENV-SPIKES", 380, G)
    rudy(a, "CHAR-IDLE", 560)
    put(a, "ENEMY-GOBLIN-WALK-A", 760, G)
    put(a, "ENEMY-GOBLIN-WALK-B", 960, G)
    put(a, "ENEMY-GOBLIN-SQUASH", 1170, G)
    put(a, "PROP-SWORDSHIELD", 1460, G - 90)
    put(a, "ENV-WAYSTONE", 1700, G)
    for i, fid in enumerate(("UI-HEART-FULL", "UI-HEART-FULL", "UI-HEART-EMPTY")):
        put(a, fid, 48 + 60 * i, 48)
    b = view_at(7700 - 1920, env, motion)
    put(b, "ENV-WAYSTONE-LIT", 300, G)
    rudy(b, "CHAR-SWORD-IDLE", 700)
    put(b, "ENV-PORTAL", 1500, G - 6)  # the disc's middle where the greybox draws it
    rudy(b, "CHAR-CELEBRATE", 1500)
    view = Image.new("RGBA", (3840, 1080))
    view.alpha_composite(a, (0, 0))
    view.alpha_composite(b, (1920, 0))
    rgb = view.convert("RGB")
    sheet = Image.new("RGB", (rgb.width, rgb.height * 2))
    sheet.paste(rgb, (0, 0))
    sheet.paste(ImageOps.grayscale(rgb).convert("RGB"), (0, rgb.height))
    sheet.save(CHECK, quality=88)
    print("wrote", CHECK.relative_to(ROOT), f"(far layer at {motion['far']}, fields at {motion['mid']} of the camera)")


if __name__ == "__main__":
    main()
