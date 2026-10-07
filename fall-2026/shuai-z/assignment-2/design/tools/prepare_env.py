#!/usr/bin/env python3
"""Turn the accepted Level 1 environment images into game layers for game/content/level_1/art/.

    python3 design/tools/prepare_env.py

- sky_castle.jpg (ENV-SKY-CASTLE-03): the far layer, resized to the 1080 px view height, without the
  large trees at its left edge, which stood above the fields. Opaque. It does not repeat: env.json gives
  the largest motion scale at which this one image still covers the whole level.
- fields.png (ENV-FIELDS-01, re-downloaded): the middle layer. Its flat pale sky is keyed out, and one
  792 px period of the image (it is drawn twice across its width) is cut where the two copies match
  best, with a 40 px cross-fade, so the tile repeats without a seam.
- ground_tile.png (ENV-GROUND-03): the ground, cut to one period the same way, scaled so the wheat
  tufts are about half Rudy's height (plan B in the asset log). The slab's rounded bottom is replaced
  by its own soil, repeated downward with cross-fades, so the ground reaches the bottom of the view.
- ground_cliff_right.png (ENV-GROUND-CLIFF-02) and ground_cliff_left.png (its mirror): the end of a
  ground segment at a pit. They start with the ground tile's first column, so they join it without a seam.
- endcard.jpg (ENV-ENDCARD-02): the "Level complete" card, resized to 1920x1080.
- env.json: the size of each layer in game px, its texture density, and where its ground line or
  horizon falls, for the scene to place them.
- generated/checks/ENV-layers-check.jpg: a 1920x1080 mock-up built only from these files, with Rudy's
  frames standing on the ground line, in color and grayscale.

The originals in generated/accepted/ are never changed. Code written by Claude Code; it draws nothing
new: it cuts, keys, scales, mirrors and cross-fades the generated pixels.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ACCEPTED = ROOT / "generated" / "accepted"
OUT = ROOT / "game" / "content" / "level_1" / "art"
CHECK = ROOT / "generated" / "checks" / "ENV-layers-check.jpg"
FRAMES = ROOT / "game" / "content" / "rudy" / "frames"

_spec = importlib.util.spec_from_file_location("matte_sprites", HERE / "matte_sprites.py")
ms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ms)

VIEW_H = 1080
GROUND_Y = 840  # the greybox's ground line (game/content/level_1/level_1.tscn)
HORIZON_Y = 700  # where the fields layer's horizon sits, below the castle on the far layer
LEVEL_W = 7700  # the level's width (level_1.tscn), so the camera scrolls LEVEL_W - 1920 px
SKY_CROP_X = 500  # game px cut from the far layer's left edge: the large autumn trees

SKY = ACCEPTED / "ENV-SKY-CASTLE-03.jpg"
FIELDS = ACCEPTED / "ENV-FIELDS-01.jpg"
GROUND = ACCEPTED / "ENV-GROUND-03.jpg"
CLIFF = ACCEPTED / "ENV-GROUND-CLIFF-02.jpg"
ENDCARD = ACCEPTED / "ENV-ENDCARD-02.jpg"

# ENV-GROUND, measured on the 2750 x 1536 originals
GROUND_SCALE = 0.22  # game px per source px: the wheat tufts (about 362 px) become about 80 game px
GROUND_DENSITY = 2  # texture px per game px, like Rudy's frames
WALK_ROW = 722  # the top of the tan path band, where Rudy's soles go
WHEAT_TOP = 280  # a little above the tallest tuft
SOIL_BAND = (830, 1060)  # clean soil between the grass fringe and the slab's bottom outline
SLAB_CUT = 1060  # the slab's own pixels are kept down to here
CLIFF_FACE = (1150, 1500)  # clean rows of the cliff face, repeated below the image
FADE = 40  # source px of every cross-fade
DEPTH_FLOOR = 0.62  # brightness of the soil at the bottom of the view


def ramp(n):
    return np.linspace(0.0, 1.0, n)[None, :, None]


def best_seam(img, period, rows, x_range, width=40):
    """The column x0 where img[x0:x0+width] best matches img[x0+period:...], over the given rows."""
    best = None
    for x0 in range(*x_range):
        a = img[rows[0]:rows[1], x0:x0 + width]
        b = img[rows[0]:rows[1], x0 + period:x0 + period + width]
        d = float(np.abs(a - b).mean())
        if best is None or d < best[0]:
            best = (d, x0)
    return best


def best_period(img, rows, periods, x_range):
    return min((best_seam(img, p, rows, x_range)[0], p) for p in periods)[1]


def tile_cut(img, x0, period, k=FADE):
    """One period starting at x0; its first k columns fade in from the copy one period later, so its
    last column runs straight into its first."""
    t = img[:, x0:x0 + period].copy()
    w = ramp(k)
    t[:, :k] = (1 - w) * img[:, x0 + period:x0 + period + k] + w * img[:, x0:x0 + k]
    return t


def extend_down(img, top, band, to_row, k=FADE, shift=0):
    """Keep rows above `top`, then fill down to `to_row` by repeating rows band[0]:band[1], each
    repeat cross-faded over k rows into what is above it. With `shift`, each repeat is rolled sideways
    by that many more columns, so the stones do not line up in a grid (only for tiles, which wrap)."""
    out = img[:top].copy()
    piece = img[band[0]:band[1]]
    w = np.linspace(0, 1, k)[:, None, None]
    n = 0
    while out.shape[0] < to_row:
        n += 1
        p = np.roll(piece, n * shift, axis=1) if shift else piece
        out[-k:] = (1 - w) * out[-k:] + w * p[:k]
        out = np.concatenate([out, p[k:]], axis=0)
    return out[:to_row]


def darken_with_depth(img, start, end, floor=DEPTH_FLOOR):
    """Soil gets darker with depth, from full brightness at row `start` to `floor` at row `end`."""
    rows = np.arange(img.shape[0])
    f = 1 - (1 - floor) * np.clip((rows - start) / max(1, end - start), 0, 1)
    out = img.copy()
    out[..., :3] *= f[:, None, None]
    return out


def save_rgba(arr, path, scale):
    img = Image.fromarray(np.clip(arr, 0, 255).round().astype(np.uint8), "RGBA")
    img = ms.shrink(img, scale)
    img.save(path)
    return img


def key_flat_sky(path, rows=150):
    """Fields: key out the flat pale sky (sampled from the top rows), only where it joins the top edge."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(float)
    sky = np.median(im[:rows].reshape(-1, 3), axis=0)
    d = np.linalg.norm(im - sky, axis=2)
    lab, _ = ndimage.label(d < 14)
    top = np.unique(lab[0])
    bgm = np.isin(lab, top[top > 0])
    fg = ~bgm
    band = fg & ~ndimage.binary_erosion(fg, iterations=3)
    alpha = fg.astype(float)
    alpha[band] = np.clip((d[band] - 10) / 45, 0, 1)
    a = np.clip(alpha, 1e-3, 1)[..., None]
    col = im.copy()
    col[band] = np.clip((im[band] - (1 - a[band]) * sky) / a[band], 0, 255)
    return np.dstack([col, alpha * 255]), sky


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    env = {"about": "Level 1 layers made by design/tools/prepare_env.py from generated/accepted/. "
                    "Sizes and y positions are in game px; draw each texture at scale 1/density.",
           "view_height": VIEW_H, "ground_y": GROUND_Y, "layers": {}}

    # far layer
    sky = Image.open(SKY).convert("RGB")
    s = VIEW_H / sky.height
    sky = sky.resize((round(sky.width * s), VIEW_H), Image.LANCZOS).crop((SKY_CROP_X, 0, round(sky.width * s), VIEW_H))
    sky.save(OUT / "sky_castle.jpg", quality=92)
    env["layers"]["sky_castle"] = {"file": "sky_castle.jpg", "source": str(SKY.relative_to(ROOT)),
                                   "density": 1, "size": list(sky.size), "y": 0, "tiles": False,
                                   "scale_from_source": round(s, 5), "cropped_left_px": SKY_CROP_X,
                                   "max_motion_scale": round((sky.width - 1920) / (LEVEL_W - 1920), 4),
                                   "note": "does not repeat; scroll it at most max_motion_scale of the camera"}

    # middle layer
    rgba, skycol = key_flat_sky(FIELDS)
    period = best_period(rgba[..., :3], (380, rgba.shape[0]), range(786, 800, 2), (0, 200))
    d, x0 = best_seam(rgba[..., :3], period, (380, rgba.shape[0]), (0, 200))
    tile = tile_cut(rgba, x0, period)
    horizon = int(np.nonzero((tile[..., 3] > 128).mean(axis=1) > 0.5)[0].min())
    img = Image.fromarray(np.clip(tile, 0, 255).round().astype(np.uint8), "RGBA")
    img.save(OUT / "fields.png")
    env["layers"]["fields"] = {"file": "fields.png", "source": str(FIELDS.relative_to(ROOT)), "density": 1,
                               "size": list(img.size), "y": HORIZON_Y - horizon, "tiles": True,
                               "horizon_row": horizon, "period_source_px": period, "seam_x": x0,
                               "seam_mean_difference": round(d, 1), "keyed_sky_rgb": [int(v) for v in skycol]}

    # ground: one period, extended down to the bottom of the view
    scale = GROUND_SCALE * GROUND_DENSITY
    to_row = WALK_ROW + round((VIEW_H - GROUND_Y) / GROUND_SCALE) + 4
    g, _ = ms.matte(GROUND)
    g = g.copy()
    g[..., 3] *= 255
    # the seam is searched left of 700, so that one period later the cliff piece still starts on the slab
    gper = best_period(g[..., :3], (WHEAT_TOP, SLAB_CUT), range(960, 1060, 4), (150, 700))
    gd, gx0 = best_seam(g[..., :3], gper, (WHEAT_TOP, SLAB_CUT), (150, 700))
    gt = tile_cut(g, gx0, gper)
    gt = extend_down(gt, SLAB_CUT, SOIL_BAND, to_row, shift=gper * 3 // 7)
    gt[SLAB_CUT - FADE:, :, 3] = 255  # the soil below is solid
    gt = darken_with_depth(gt, WALK_ROW + 120, to_row)
    tile_img = save_rgba(gt[WHEAT_TOP:], OUT / "ground_tile.png", scale)
    walk = round((WALK_ROW - WHEAT_TOP) * scale)
    env["layers"]["ground_tile"] = {
        "file": "ground_tile.png", "source": str(GROUND.relative_to(ROOT)), "density": GROUND_DENSITY,
        "size": [round(tile_img.width / GROUND_DENSITY, 1), round(tile_img.height / GROUND_DENSITY, 1)],
        "tiles": True, "walk_row_texture_px": walk, "y": GROUND_Y - walk / GROUND_DENSITY,
        "period_source_px": gper, "seam_x": gx0, "seam_mean_difference": round(gd, 1),
        "scale_from_source": GROUND_SCALE}

    # cliff end: starts where the tile starts, one period further on, and runs to the cliff face
    c, _ = ms.matte(CLIFF)
    c = c.copy()
    c[..., 3] *= 255
    opaque_bottom = np.array([np.nonzero(c[:, x, 3] > 128)[0].max() if (c[:, x, 3] > 128).any() else 0
                              for x in range(c.shape[1])])
    face_x = int(np.nonzero(opaque_bottom > SLAB_CUT + 200)[0].min())  # first column of the cliff face
    start = gx0 + gper
    piece = c[:, start:].copy()
    w = ramp(FADE)
    piece[:, :FADE] = (1 - w) * g[:, gx0:gx0 + FADE] + w * c[:, start:start + FADE]
    # below the slab, the soil is the tile's own soil, continued column by column (the tile repeats every
    # gper columns), so the join with the tile is exact; the slab's rows above fade into it
    cols = np.arange(piece.shape[1]) % gper
    lit = darken_with_depth(piece, WALK_ROW + 120, to_row)  # the same darkening as the tile's
    under = np.concatenate([lit[:SLAB_CUT], gt[SLAB_CUT:to_row][:, cols]], axis=0)
    wv = np.linspace(0, 1, FADE)[:, None, None]
    under[SLAB_CUT - FADE:SLAB_CUT] = (1 - wv) * lit[SLAB_CUT - FADE:SLAB_CUT] + wv * gt[SLAB_CUT - FADE:SLAB_CUT][:, cols]
    face = darken_with_depth(extend_down(piece, CLIFF_FACE[1], CLIFF_FACE, to_row), WALK_ROW + 120, to_row)
    fx = face_x - start
    blend = np.clip((np.arange(piece.shape[1]) - (fx + 10)) / 40.0, 0, 1)[None, :, None]
    cliff = (1 - blend) * under + blend * face
    cliff[SLAB_CUT - FADE:, :fx + 50, 3] = 255
    right = save_rgba(cliff[WHEAT_TOP:], OUT / "ground_cliff_right.png", scale)
    left = ImageOps.mirror(right)
    left.save(OUT / "ground_cliff_left.png")
    # where the cliff face ends on the right (the edge of the pit), in game px from the image's left
    a = np.asarray(right.getchannel("A")) > 128
    edge = int(np.nonzero(a[walk + 40 * GROUND_DENSITY:].any(axis=0))[0].max()) + 1
    for name, img_, note in (("ground_cliff_right", right, "joins the tile on its left; the pit is on its right"),
                             ("ground_cliff_left", left, "the mirror; joins the tile on its right")):
        env["layers"][name] = {
            "file": f"{name}.png", "source": str(CLIFF.relative_to(ROOT)), "density": GROUND_DENSITY,
            "size": [round(img_.width / GROUND_DENSITY, 1), round(img_.height / GROUND_DENSITY, 1)],
            "walk_row_texture_px": walk, "y": GROUND_Y - walk / GROUND_DENSITY, "tiles": False,
            "cliff_edge_game_px": round((edge if name.endswith("right") else img_.width - edge) / GROUND_DENSITY, 1),
            "note": note}
    card = Image.open(ENDCARD).convert("RGB").resize((1920, VIEW_H), Image.LANCZOS)
    card.save(OUT / "endcard.jpg", quality=92)
    env["layers"]["endcard"] = {"file": "endcard.jpg", "source": str(ENDCARD.relative_to(ROOT)), "density": 1,
                                "size": [1920, VIEW_H], "y": 0, "tiles": False, "note": "full-screen card, not a layer"}
    (OUT / "env.json").write_text(json.dumps(env, indent=2) + "\n")
    for k, v in env["layers"].items():
        print(f"{k:20s} {v['size']} game px, density {v['density']}, y {v['y']}")
    mockup(env)


def mockup(env):
    """A 1920x1080 view built only from the layer files, with a pit and Rudy's frames."""
    L = env["layers"]
    view = Image.new("RGBA", (1920, VIEW_H), (0, 0, 0, 255))
    sky = Image.open(OUT / L["sky_castle"]["file"]).convert("RGBA")
    view.alpha_composite(sky.crop((sky.width - 1920, 0, sky.width, VIEW_H)))
    f = Image.open(OUT / "fields.png")
    x = -200
    while x < 1920:
        view.alpha_composite(f, (x, L["fields"]["y"]))
        x += f.width

    def ground(name):
        im = Image.open(OUT / L[name]["file"])
        return ms.shrink(im, 1 / L[name]["density"])

    tile, cr, cl = ground("ground_tile"), ground("ground_cliff_right"), ground("ground_cliff_left")
    gy = round(L["ground_tile"]["y"])
    # segment 1 from x = -tile.width to the pit at 1250, segment 2 from 1450
    pit_l, pit_r = 1250, 1460
    x = pit_l - round(L["ground_cliff_right"]["cliff_edge_game_px"])
    view.alpha_composite(cr, (x, gy))
    xx = x - tile.width
    while xx > -tile.width:
        view.alpha_composite(tile, (xx, gy))
        xx -= tile.width
    x = pit_r - round(L["ground_cliff_left"]["cliff_edge_game_px"])
    view.alpha_composite(cl, (x, gy))
    xx = x + cl.width
    while xx < 1920:
        view.alpha_composite(tile, (xx, gy))
        xx += tile.width
    man = json.loads((FRAMES / "frames.json").read_text())
    ox, oy = (v / man["density"] for v in man["origin"])
    for fid, fx in (("CHAR-IDLE", 300), ("CHAR-RUN-A", 640), ("CHAR-SWORD-IDLE", 980), ("CHAR-FALL", 1350),
                    ("CHAR-SWORD-RUN-B", 1700)):
        fr = ms.shrink(Image.open(FRAMES / f"{fid}.png"), 1 / man["density"])
        fy = GROUND_Y - (160 if fid == "CHAR-FALL" else 0)
        view.alpha_composite(fr, (round(fx - ox), round(fy - oy)))
    rgb = view.convert("RGB")
    sheet = Image.new("RGB", (1920, VIEW_H * 2))
    sheet.paste(rgb, (0, 0))
    sheet.paste(ImageOps.grayscale(rgb).convert("RGB"), (0, VIEW_H))
    sheet.save(CHECK, quality=90)
    print("wrote", CHECK.relative_to(ROOT))


if __name__ == "__main__":
    main()
