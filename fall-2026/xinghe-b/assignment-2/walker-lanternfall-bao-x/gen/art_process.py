#!/usr/bin/env python3
"""Cut frames out of accepted raws, fit them to game size, lock them to a palette and assemble a strip.

    python gen/art_process.py gen/mappings/ART-PC-01.json

Mapping file:
{
  "out": "godot/assets/art/pc_sheet.png", "preview": "design/character/pc_sheet_x8.png",
  "palette": "character", "frame": [32, 32], "fill": 0.95, "anchor": "bottom", "bg_threshold": 235, "outline": true,
  "frames": [{"name": "turn_front", "src": "gen/accepted/ART-PC-01/<run>.png", "box": [x0, y0, x1, y1]}, ...]
}
A frame is cut by "box" (pixel box from gen/figures.py), by "grid" + "cell", or is the whole image.
}
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cut(src: Image.Image, grid, cell, inset=0.02) -> Image.Image:
    rows, cols = grid
    r, c = cell
    cw, ch = src.width / cols, src.height / rows
    box = (int(c * cw + cw * inset), int(r * ch + ch * inset), int((c + 1) * cw - cw * inset), int((r + 1) * ch - ch * inset))
    return src.crop(box)


def key_background(im: Image.Image, threshold: int) -> Image.Image:
    """White background and pale grey drop shadows become transparent."""
    a = np.array(im.convert("RGBA"))
    rgb = a[..., :3].astype(np.float32)
    mx, mn = rgb.max(-1), rgb.min(-1)
    white = mn > threshold
    shadow = (mx > 185) & ((mx - mn) < 0.12 * np.maximum(mx, 1))
    a[white | shadow, 3] = 0
    return Image.fromarray(a)


def fit(im: Image.Image, fw: int, fh: int, fill: float, anchor: str) -> Image.Image:
    bbox = im.getbbox()
    if bbox is None:
        raise SystemExit("empty cell after background keying — wrong cell or threshold")
    im = im.crop(bbox)
    s = min(fw * fill / im.width, fh * fill / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    canvas = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    x = (fw - im.width) // 2
    y = fh - im.height if anchor == "bottom" else (fh - im.height) // 2
    canvas.alpha_composite(im, (x, y))
    return canvas


def _lab(rgb: np.ndarray) -> np.ndarray:
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    xyz = c @ np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]])
    xyz /= np.array([0.9505, 1.0, 1.089])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def lock_palette(im: Image.Image, palette, outline_rgb=None, ink_below_l: float = 14.0, supersample: int = 1) -> Image.Image:
    """Map every opaque pixel to the palette in Lab space. The outline colour is reserved for pixels darker than
    L* = ink_below_l and for the 1-px ring added around the silhouette. With supersample = k the input is k times
    the frame size and each k x k block becomes the block's most common palette colour (keeps pixel edges crisp)."""
    a = np.array(im).astype(np.float32)
    pal = np.array(palette, dtype=np.float32)
    lab, pal_lab = _lab(a[..., :3]), _lab(pal)
    d = ((lab[..., None, :] - pal_lab[None, None]) ** 2).sum(-1)
    if outline_rgb is not None:
        ink = [i for i, c in enumerate(palette) if tuple(c) == tuple(outline_rgb)]
        for i in ink:
            d[..., i] = np.where(lab[..., 0] < ink_below_l, -1.0, d[..., i] + 1e9)
    idx = d.argmin(-1)
    opaque = a[..., 3] >= 128
    k = supersample
    if k > 1:
        h, w = idx.shape[0] // k, idx.shape[1] // k
        blocks_idx = idx[:h * k, :w * k].reshape(h, k, w, k).transpose(0, 2, 1, 3).reshape(h, w, k * k)
        blocks_op = opaque[:h * k, :w * k].reshape(h, k, w, k).transpose(0, 2, 1, 3).reshape(h, w, k * k)
        new_idx = np.zeros((h, w), dtype=np.int64)
        new_op = blocks_op.sum(-1) * 2 >= k * k
        for y in range(h):
            for x in range(w):
                vals = blocks_idx[y, x][blocks_op[y, x]]
                if len(vals):
                    new_idx[y, x] = np.bincount(vals, minlength=len(palette)).argmax()
        idx, opaque = new_idx, new_op
    out = np.zeros(idx.shape + (4,), dtype=np.uint8)
    out[opaque, :3] = pal[idx[opaque]].astype(np.uint8)
    out[opaque, 3] = 255
    if outline_rgb is not None:
        o = opaque
        edge = np.zeros_like(o)
        edge[1:, :] |= o[:-1, :]; edge[:-1, :] |= o[1:, :]; edge[:, 1:] |= o[:, :-1]; edge[:, :-1] |= o[:, 1:]
        ring = edge & ~o
        out[ring, :3] = outline_rgb
        out[ring, 3] = 255
    return Image.fromarray(out)


def trim_shadow(im: Image.Image, band: float = 0.12) -> Image.Image:
    """Drop the pale, low-saturation cast shadow in the bottom band of the figure's box (keeps eyes/highlights higher up)."""
    a = np.array(im)
    bbox = im.getbbox()
    if bbox is None:
        return im
    x0, y0, x1, y1 = bbox
    top = int(y1 - (y1 - y0) * band)
    rgb_ = a[top:y1, x0:x1, :3].astype(np.float32)
    mx, mn = rgb_.max(-1), rgb_.min(-1)
    pale = (mx > 140) & ((mx - mn) < 0.22 * np.maximum(mx, 1))
    a[top:y1, x0:x1, 3] = np.where(pale, 0, a[top:y1, x0:x1, 3])
    return Image.fromarray(a)


def post_squash(frame: Image.Image, sy: float) -> Image.Image:
    """Nearest-neighbour vertical squash of a finished frame, re-centred (a cheap wing-beat / breathing frame)."""
    w, h = frame.size
    bbox = frame.getbbox()
    if bbox is None:
        return frame
    part = frame.crop(bbox)
    nh = max(1, round(part.height * sy))
    part = part.resize((part.width, nh), Image.NEAREST)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cy = (bbox[1] + bbox[3]) // 2
    out.alpha_composite(part, (bbox[0], max(0, min(h - nh, cy - nh // 2))))
    return out


def is_lamp(rgb: np.ndarray) -> np.ndarray:
    """Warm gold/yellow pixels: the lamp housing and lens."""
    r, g, b = rgb[..., 0].astype(int), rgb[..., 1].astype(int), rgb[..., 2].astype(int)
    return (r > 170) & (g > 110) & (b < 120) & (r >= g) & (g > b + 30)


def is_coat(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[..., 0].astype(int), rgb[..., 1].astype(int), rgb[..., 2].astype(int)
    return (b > r + 10) & (b > 40) & (r < 110)


def fit_normalized(im: Image.Image, fw: int, fh: int, lamp_px: float, pad: int) -> tuple:
    """Scale so the lamp is lamp_px tall (the character-sheet rule), feet on the bottom row, coat centred.
    If that would not fit the frame, shrink just enough to fit and report the lamp size actually used."""
    bbox = im.getbbox()
    if bbox is None:
        raise SystemExit("empty frame after background keying")
    im = im.crop(bbox)
    a = np.asarray(im)
    opaque = a[..., 3] > 0
    lamp = opaque & is_lamp(a[..., :3])
    if lamp.sum() < 10:
        raise SystemExit("no lamp pixels found; cannot normalise this frame")
    ys = np.nonzero(lamp)[0]
    lamp_h = ys.max() - ys.min() + 1
    scale = lamp_px / lamp_h
    scale = min(scale, (fh - pad) / im.height, (fw - 2 * pad) / im.width)
    w, h = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    small = im.resize((w, h), Image.LANCZOS)
    coat = opaque & is_coat(a[..., :3])
    cx = (np.nonzero(coat)[1].mean() if coat.sum() else im.width / 2) * scale
    x = int(round(fw / 2 - cx))
    x = max(pad, min(fw - pad - w, x))
    y = fh - pad // 2 - h
    canvas = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    canvas.alpha_composite(small, (x, max(0, y)))
    return canvas, round(lamp_h * scale, 2)


def recolor(im: Image.Image, mapping: dict) -> Image.Image:
    a = np.array(im)
    for src, dst in mapping.items():
        m = (a[..., 3] == 255) & np.all(a[..., :3] == np.array(rgb(src)), axis=-1)
        a[m, :3] = rgb(dst)
    return Image.fromarray(a)


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    palettes = json.loads((ROOT / "godot/assets/art/palettes.json").read_text())
    palette = [rgb(c) for c in palettes[spec["palette"]]]
    fw, fh = spec["frame"]
    frames, report = [], []
    for f in spec["frames"]:
        src = Image.open(ROOT / f["src"]).convert("RGBA")
        if "box" in f:
            x0, y0, x1, y1 = f["box"]
            m = f.get("margin", 6)
            cell = src.crop((max(0, x0 - m), max(0, y0 - m), min(src.width, x1 + m), min(src.height, y1 + m)))
        elif "grid" in f:
            cell = cut(src, f["grid"], f.get("cell", [0, 0]))
        else:
            cell = src
        cell = key_background(cell, spec.get("bg_threshold", 235))
        if f.get("trim_shadow"):
            cell = trim_shadow(cell)
        if f.get("mirror"):
            cell = cell.transpose(Image.FLIP_LEFT_RIGHT)
        k = spec.get("supersample", 4)
        if spec.get("normalize_lamp_px"):
            cell, lamp = fit_normalized(cell, fw * k, fh * k, spec["normalize_lamp_px"] * k, 2 * k)
            report.append({"name": f.get("name"), "lamp_px": round(lamp / k, 1)})
        else:
            fill = spec.get("fill", 0.95) * (fw - 2) / fw if spec.get("outline") else spec.get("fill", 0.95)
            cell = fit(cell, fw * k, fh * k, fill, spec.get("anchor", "bottom"))
            report.append({"name": f.get("name"), "lamp_px": None})
        locked = lock_palette(cell, palette, rgb("#14121C") if spec.get("outline") else None,
                              spec.get("ink_below_l", 14.0), supersample=k)
        if f.get("recolor"):
            locked = recolor(locked, f["recolor"])
        if f.get("post_squash_y"):
            locked = post_squash(locked, f["post_squash_y"])
        frames.append(locked)
        if f.get("run") and spec.get("asset_id"):
            from common import log_processing
            log_processing(f"gen/log/{spec['asset_id']}/{f['run']}.json", {
                "tool": "gen/art_process.py", "mapping": sys.argv[1], "frame": f.get("name"), "out": spec["out"],
                "index": len(frames) - 1, "mirror": bool(f.get("mirror")), "recolor": f.get("recolor"),
                "trim_shadow": bool(f.get("trim_shadow")), "post_squash_y": f.get("post_squash_y"), "box": f.get("box"),
                "lamp_px": report[-1]["lamp_px"] if report else None, "frame_px": spec["frame"],
                "palette": spec["palette"], "supersample": spec.get("supersample", 4), "outline": bool(spec.get("outline"))})
    strip = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        strip.paste(fr, (i * fw, 0))
    out = ROOT / spec["out"] if not spec["out"].startswith("/") else Path(spec["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out)
    if spec.get("preview"):
        prev = ROOT / spec["preview"] if not spec["preview"].startswith("/") else Path(spec["preview"])
        prev.parent.mkdir(parents=True, exist_ok=True)
        strip.resize((strip.width * 8, strip.height * 8), Image.NEAREST).save(prev)
    print(f"{out}: {len(frames)} frames")
    if report:
        print(json.dumps(report))


if __name__ == "__main__":
    main()
