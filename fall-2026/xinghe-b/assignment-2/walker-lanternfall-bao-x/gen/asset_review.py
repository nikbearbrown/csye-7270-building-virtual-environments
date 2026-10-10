#!/usr/bin/env python3
"""Candidate review for a non-character art asset: each candidate's raw thumbnail next to the palette-locked
result at game size (x4) on the ground colour, using the geometry in godot/assets/art/manifest.json.
Multi-frame assets take the N largest figures found by gen/figures.py as their frames.

    gen/.venv-audio/bin/python gen/asset_review.py ART-EN-01     -> gen/rejected/ART-EN-01-review.png
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from art_process import fit, key_background, lock_palette, rgb  # noqa: E402
from figures import find_figures  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "godot" / "assets" / "art"
OUTLINE = {"ART-ENV-01": False, "ART-FX-03": False, "ART-FX-01": False, "ART-ENV-06": False}


def frames_for(raw: Image.Image, n: int) -> list:
    if n == 1:
        return [raw]
    boxes = sorted(find_figures(raw), key=lambda b: -(b[2] - b[0]) * (b[3] - b[1]))[:n]
    boxes.sort(key=lambda b: b[0])
    return [raw.crop(b) for b in boxes]


def preview(asset: str, src: Path, spec: dict, palette) -> Image.Image:
    fw, fh = spec["frame"]
    raw = Image.open(src).convert("RGB")
    if asset == "ART-ENV-01":
        side = min(raw.size)
        tile = raw.crop((0, 0, side, side)).resize((fw, fh), Image.LANCZOS).convert("RGBA")
        one = lock_palette(tile, palette)
        grid = Image.new("RGBA", (fw * 2, fh * 2))
        for x in (0, fw):
            for y in (0, fh):
                grid.paste(one, (x, y))
        return grid
    k = 4
    out = Image.new("RGBA", (fw * spec["frames"], fh), (0, 0, 0, 0))
    for i, fr in enumerate(frames_for(raw, spec["frames"])):
        keyed = key_background(fr.convert("RGBA"), 235)
        cell = fit(keyed, fw * k, fh * k, 0.9, "center")
        locked = lock_palette(cell, palette, rgb("#14121C") if OUTLINE.get(asset, True) else None, 14.0, supersample=k)
        out.paste(locked, (i * fw, 0))
    return out


def main() -> None:
    asset = sys.argv[1]
    manifest = json.loads((ART / "manifest.json").read_text())
    name, spec = next((n, s) for n, s in manifest.items() if s["id"] == asset)
    palette = [rgb(c) for c in json.loads((ART / "palettes.json").read_text())[spec["palette"]]]
    runs = [json.loads(p.read_text()) for p in sorted((ROOT / "gen" / "log" / asset).glob("*.json"))]
    zoom = max(1, min(8, 160 // max(spec["frame"][1], 1)))
    cells = []
    for m in runs:
        p = preview(asset, ROOT / m["raw_outputs"][0], spec, palette)
        ground = Image.new("RGBA", p.size, "#1F2540")
        ground.alpha_composite(p)
        big = ground.convert("RGB").resize((p.width * zoom, p.height * zoom), Image.NEAREST)
        thumb = Image.open(ROOT / m["thumbnail"]).convert("RGB")
        thumb.thumbnail((200, 200))
        cells.append((m, thumb, big))
    w = max(t.width + b.width for _, t, b in cells) + 30
    h = max(max(t.height, b.height) for _, t, b in cells) + 30
    sheet = Image.new("RGB", (w, h * len(cells)), "#0E1020")
    d = ImageDraw.Draw(sheet)
    for r, (m, t, b) in enumerate(cells):
        y = r * h
        sheet.paste(t, (5, y + 5))
        sheet.paste(b, (t.width + 20, y + 5))
        verdict = ((m.get("decision") or {}).get("verdict") or "pending").upper()
        d.text((5, y + h - 18), f"{asset} seed {m['settings']['seed']}  {verdict}  -> {name} {spec['frame']} x{spec['frames']}", fill="#FFF1C9")
    out = ROOT / "gen" / "rejected" / f"{asset}-review.png"
    sheet.save(out, optimize=True)
    print(out)


if __name__ == "__main__":
    main()
