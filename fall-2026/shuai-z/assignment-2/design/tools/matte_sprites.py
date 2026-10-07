#!/usr/bin/env python3
"""Turn Rudy's accepted Gemini frames into game-ready sprites for game/content/rudy/frames/.

    python3 design/tools/matte_sprites.py
    python3 design/tools/matte_sprites.py --only CHAR-DEFEAT,CHAR-SWORD-SLASH

For every frame in FRAMES:
1. Key out the flat background, and the cast shadow, which is the same color only darker. Edge pixels
   get a soft alpha and have the background color unmixed from them, so no blue fringe is left.
   Frames in TRAIL also keep the slash's motion trail as semi-transparent white.
2. Measure the head (the hair and face, holes filled) and scale the frame so the head is the same size
   in every frame. CHAR-IDLE sets that size: its full height, cowlick included, becomes 160 px,
   as in CHARACTER-SHEET.md. Overall heights then differ by pose, as they should.
   Frames are stored at DENSITY texture px per game px (2: CHAR-IDLE is 320 px tall), and drawn at
   1/DENSITY scale in the game, so they stay sharp when the 1920x1080 view is enlarged up to 2x.
3. Place every frame on one shared canvas: the lowest opaque pixel (the soles, or the seat when he
   sits) on the bottom line, and the middle of the torso on the vertical center line. That point is
   the body origin in game/content/rudy/rudy.tscn, where the 40 x 136 px capsule stands.

Writes one PNG per asset ID, frames.json (canvas, origin, and each frame's source, scale and placement),
and generated/checks/rudy-frames-lineup.png, which shows every frame against the capsule.
HEAD_SCALE and X_SHIFT hold manual corrections after looking at the lineup; each one is logged in
ASSET-LOG.md. The originals in generated/accepted/ are never changed.
Code written by Claude Code; it draws nothing new, it only cuts out, rescales and places.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
ACCEPTED = ROOT / "generated" / "accepted"
OUT = ROOT / "game" / "content" / "rudy" / "frames"
LINEUP = ROOT / "generated" / "checks" / "rudy-frames-lineup.png"

# asset ID -> accepted original (see ASSET-LOG.md)
FRAMES = {
    "CHAR-IDLE": "CHAR-IDLE-01.jpg",
    "CHAR-RUN-A": "CHAR-RUN-A-01.jpg",
    "CHAR-RUN-B": "CHAR-RUN-B-02.jpg",
    "CHAR-RISE": "CHAR-RISE-01.jpg",
    "CHAR-FALL": "CHAR-FALL-01.jpg",
    "CHAR-HURT": "CHAR-HURT-02.jpg",
    "CHAR-DEFEAT": "CHAR-DEFEAT-01.jpg",
    "CHAR-RESPAWN": "CHAR-RESPAWN-01.jpg",
    "CHAR-CELEBRATE": "CHAR-CELEBRATE-01.jpg",
    "CHAR-SWORD-IDLE": "CHAR-SWORD-IDLE-01.jpg",
    "CHAR-SWORD-SLASH": "CHAR-SWORD-SLASH-01.jpg",
    "CHAR-SWORD-BLOCK": "CHAR-SWORD-BLOCK-01.jpg",
    "CHAR-SWORD-RUN-A": "CHAR-SWORD-RUN-A-01.jpg",
    "CHAR-SWORD-RUN-B": "CHAR-SWORD-RUN-B-01.jpg",
    "CHAR-SWORD-RISE": "CHAR-SWORD-RISE-01.jpg",
    "CHAR-SWORD-FALL": "CHAR-SWORD-FALL-01.jpg",
}
TRAIL = {"CHAR-SWORD-SLASH"}
ANCHOR = "CHAR-IDLE"
ANCHOR_HEIGHT = 160  # game px, CHARACTER-SHEET.md
DENSITY = 2  # texture px per game px; the game draws the frames at scale 1 / DENSITY

# Manual corrections after looking at the lineup. HEAD_SCALE multiplies a frame's final scale
# (the head measure is thrown off by windblown hair or a hand touching the head); X_SHIFT moves a
# frame sideways, in game px, positive to the right.
HEAD_SCALE: dict[str, float] = {
    # the raised arm hides the back of the head, so the head measures small and the frame came out
    # about 12% too big; judged by laying CHAR-IDLE's face outline over the face (2026-10-01)
    "CHAR-RISE": 0.88,
    "CHAR-SWORD-RISE": 0.88,
}
X_SHIFT: dict[str, int] = {}

PAD = 8 * DENSITY  # texture px of empty margin, so the in-engine 4 px outline fits
TRAIL_WHITE = np.array([236.0, 243.0, 252.0])


def sha12(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


def matte(path, trail=False, glow=None, min_glow_area=2000):
    """Return the figure in `path` (a file or a PIL image) as float RGBA (alpha 0..1) at full size,
    and the background color.

    trail keeps the slash's white trail as semi-transparent; glow does the same for a glow of another
    color (an RGB triple), for props that glow. min_glow_area is in px of a 2048 px image."""
    src = path if isinstance(path, Image.Image) else Image.open(path)
    im = np.asarray(src.convert("RGB")).astype(float)
    h, w, _ = im.shape
    px = w / 2048  # every distance below is tuned on 2048 px images
    k = max(4, round(24 * px))
    border = np.concatenate([im[:k].reshape(-1, 3), im[-k:].reshape(-1, 3),
                             im[:, :k].reshape(-1, 3), im[:, -k:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    d = np.linalg.norm(im - bg, axis=2)
    # the cast shadow is the background color, only darker: im ~ s * bg with s < 1
    s = (im @ bg) / (bg @ bg)
    shadow = (s > 0.45) & (s < 1.02) & (np.linalg.norm(im - s[..., None] * bg, axis=2) < 9)
    # the grey robe is close to the background in value, but not as blue
    blue = (im[..., 2] - im[..., 0]) > (bg[2] - bg[0]) * 0.55
    core = ((d < 22) | shadow) & blue
    lab, _ = ndimage.label(core)
    on_border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    # shadow counts only where it joins the image border; plain background counts anywhere (holes)
    bgm = np.isin(lab, on_border[on_border > 0]) | (core & (d < 22))
    fg = ~bgm
    ref = np.where(shadow[..., None], s[..., None] * bg, bg)  # what the background was at each pixel
    alpha = fg.astype(float)
    band = fg & ~ndimage.binary_erosion(fg, iterations=max(1, round(3 * px)))
    dd = np.linalg.norm(im - ref, axis=2)
    alpha[band] = np.clip((dd[band] - 18) / 70, 0, 1)
    col = im.copy()
    light = TRAIL_WHITE if glow is None else np.asarray(glow, dtype=float)
    if trail or glow is not None:
        # the trail is white laid over the background at partial strength: im = bg + t * (white - bg)
        v = light - bg
        t = ((im - bg) @ v) / (v @ v)
        # t > 0.08 leaves out the background's own faint shading, which also lies on this line
        on_line = (t > 0.08) & (t < 1.05) & (np.linalg.norm(im - bg - t[..., None] * v, axis=2) < 14)
        lab, n = ndimage.label(on_line)
        # only large stretches that touch the background directly; the blade's light steel is inside an outline
        touch = np.unique(lab[ndimage.binary_dilation(bgm, iterations=max(1, round(2 * px))) & on_line])
        big = np.nonzero(ndimage.sum(on_line, lab, range(1, n + 1)) > min_glow_area * px * px)[0] + 1
        tr = np.isin(lab, np.intersect1d(touch[touch > 0], big))
        alpha[tr] = np.clip(t[tr], 0, 1)
        col[tr] = light
    a = np.clip(alpha, 1e-3, 1)[..., None]
    unmix = band & ~(col == light).all(axis=2)
    col[unmix] = np.clip((im[unmix] - (1 - a[unmix]) * ref[unmix]) / a[unmix], 0, 255)
    return np.dstack([col, alpha]), bg


def head_size(rgba):
    """Square root of the head's area in source px: the hair and the face, holes filled."""
    r, g, b, a = (rgba[..., i] for i in range(4))
    light = (r > 150) & (g > 100) & (r - b > 55)  # hair and skin
    shade = (r > 110) & (g > 65) & (r - b > 40) & (r - g > 25)  # the hair's brown shadow strands
    warm = (a > 0.5) & (light | shade)
    px = rgba.shape[1] / 2048
    warm = ndimage.binary_closing(warm, iterations=max(1, round(4 * px)))  # bridge the drawn strand lines
    warm = ndimage.binary_fill_holes(warm)
    warm = ndimage.binary_opening(warm, iterations=max(2, round(6 * px)))  # cut thin joins to a hand
    lab, n = ndimage.label(warm)
    if n == 0:
        raise SystemExit("no head found")
    sizes = ndimage.sum(warm, lab, range(1, n + 1))
    head = ndimage.binary_fill_holes(lab == (np.argmax(sizes) + 1))
    ys, xs = np.nonzero(head)
    return float(np.sqrt(head.sum())), (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def to_image(rgba):
    out = np.dstack([rgba[..., :3], rgba[..., 3] * 255]).round().clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def shrink(img, scale):
    """Resize with premultiplied alpha, so edges do not darken."""
    size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
    return img.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def torso_x(img):
    """Horizontal middle of the solid pixels in the middle half of the figure's height."""
    a = np.asarray(img.getchannel("A")) > 230
    rows = np.nonzero(a.any(axis=1))[0]
    y0, y1 = rows.min(), rows.max()
    band = a[y0 + (y1 - y0) // 4: y1 - (y1 - y0) // 4]
    xs = np.nonzero(band)[1]
    return float(xs.mean())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", default="", help="comma-separated asset IDs (the anchor is always measured)")
    args = ap.parse_args()
    only = [s.strip() for s in args.only.split(",") if s.strip()] or list(FRAMES)

    results = {}
    for fid in dict.fromkeys([ANCHOR] + only):
        src = ACCEPTED / FRAMES[fid]
        rgba, bg = matte(src, trail=fid in TRAIL)
        hs, hbox = head_size(rgba)
        img = to_image(rgba)
        box = img.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
        results[fid] = dict(img=img.crop(box), head=hs, head_box=hbox, bg=bg, src=src)

    anchor = results[ANCHOR]
    s_anchor = ANCHOR_HEIGHT * DENSITY / anchor["img"].height
    target_head = anchor["head"] * s_anchor
    placed = {}
    for fid in only:
        r = results[fid]
        scale = target_head / r["head"] * HEAD_SCALE.get(fid, 1.0)
        g = shrink(r["img"], scale)
        cx = torso_x(g) - X_SHIFT.get(fid, 0) * DENSITY
        # the lowest solid row stands on the line; fainter edge pixels below it may hang over
        bottom = int(np.nonzero((np.asarray(g.getchannel("A")) > 127).any(axis=1))[0].max()) + 1
        placed[fid] = dict(img=g, scale=scale, cx=cx, bottom=bottom)

    # one canvas for every frame: wide enough on each side of the torso line, tall enough for the tallest
    left = max(p["cx"] for p in placed.values())
    right = max(p["img"].width - p["cx"] for p in placed.values())
    half = int(np.ceil(max(left, right))) + PAD
    W, H = 2 * half, max(p["bottom"] for p in placed.values()) + 2 * PAD
    W, H = W + W % 2, H + H % 2
    origin = (W // 2, H - PAD)

    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "frames.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() and args.only else {"frames": {}}
    if args.only and manifest.get("canvas") not in (None, [W, H]):
        print(f"note: canvas is now {W}x{H}; run without --only to rebuild every frame on it")
    manifest.update({
        "about": "Rudy's game frames, made by design/tools/matte_sprites.py from generated/accepted/. "
                 "Every PNG is canvas-sized; origin is the body origin (soles, torso line) in texture px. "
                 "Draw them at scale 1/density: then 1 texture px is 1/density game px.",
        "density": DENSITY, "canvas": [W, H], "origin": list(origin), "anchor": ANCHOR,
        "anchor_height_game_px": ANCHOR_HEIGHT, "head_texture_px": round(target_head, 2),
    })
    for fid, p in placed.items():
        g = p["img"]
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        x = round(origin[0] - p["cx"])
        y = origin[1] - p["bottom"]
        canvas.alpha_composite(g, (x, y))
        canvas.save(OUT / f"{fid}.png")
        r = results[fid]
        manifest["frames"][fid] = {
            "source": str(r["src"].relative_to(ROOT)), "source_sha256_12": sha12(r["src"]),
            "background_rgb": [int(v) for v in r["bg"]], "head_px_in_source": round(r["head"], 1),
            "scale": round(p["scale"], 5), "size_px": [g.width, g.height], "top_left_on_canvas": [x, y],
            "head_scale_correction": HEAD_SCALE.get(fid, 1.0), "x_shift_px": X_SHIFT.get(fid, 0),
        }
        print(f"{fid:18s} scale {p['scale']:.4f}  {g.width:3d}x{g.height:3d} texture px  head(src) {r['head']:.0f}")
    manifest["frames"] = dict(sorted(manifest["frames"].items(), key=lambda kv: list(FRAMES).index(kv[0])))
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"canvas {W}x{H} texture px (density {DENSITY}), origin {origin}; wrote {len(placed)} frames to {OUT.relative_to(ROOT)}")
    lineup(manifest)


def lineup(manifest):
    """Every frame on the wheat at 2x game size, with the capsule, the origin and CHAR-IDLE's height."""
    W, H = manifest["canvas"]
    ox, oy = manifest["origin"]
    ids = list(manifest["frames"])
    zoom = 2 / manifest["density"]  # texture px -> lineup px
    g = 2  # lineup px per game px
    cw, ch = round(W * zoom) + 16, round(H * zoom) + 40
    cols = 8
    rows = (len(ids) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw + 16, rows * ch + 70), (244, 241, 234))
    d = ImageDraw.Draw(sheet)
    d.text((16, 12), "Rudy's game frames at 2x game size, on the planned wheat (#DDB95A). Green: the 40 x 136 px "
                     "capsule. Red: the body origin. Blue dashes: CHAR-IDLE's height (160 px).", fill=(41, 15, 13))
    d.text((16, 30), f"textures {W}x{H} px at {manifest['density']} px per game px; every head scaled to "
                     f"{manifest['head_texture_px']} texture px (sqrt of the head area); made by "
                     "design/tools/matte_sprites.py", fill=(41, 15, 13))
    for i, fid in enumerate(ids):
        cx, cy = 16 + (i % cols) * cw, 56 + (i // cols) * ch
        cell = Image.new("RGBA", (W, H), (221, 185, 90, 255))
        cell.alpha_composite(Image.open(OUT / f"{fid}.png"))
        cell = cell.resize((round(W * zoom), round(H * zoom)), Image.LANCZOS)
        cd = ImageDraw.Draw(cell)
        X, Y = round(ox * zoom), round(oy * zoom)
        cd.rectangle([X - 20 * g, Y - 136 * g, X + 20 * g, Y], outline=(40, 150, 60, 255), width=2)
        for x in range(0, cell.width, 8):
            cd.line([(x, Y - 160 * g), (x + 4, Y - 160 * g)], fill=(60, 90, 200, 255), width=1)
        cd.line([(0, Y), (cell.width, Y)], fill=(120, 100, 80, 255), width=1)
        cd.ellipse([X - 4, Y - 4, X + 4, Y + 4], fill=(210, 40, 40, 255))
        sheet.paste(cell.convert("RGB"), (cx, cy))
        d.text((cx, cy + cell.height + 6), fid, fill=(41, 15, 13))
    LINEUP.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(LINEUP)
    print("wrote", LINEUP.relative_to(ROOT))


if __name__ == "__main__":
    main()
