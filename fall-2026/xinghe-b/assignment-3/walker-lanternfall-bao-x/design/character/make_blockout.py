#!/usr/bin/env python3
"""Pre-generation character blockout at true game size (32x32), plus silhouette and collision overlays."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
GOLD, CREAM, NAVY, BROWN, INK = "#F2B84B", "#FFF1C9", "#2E3A59", "#8A5A3C", "#14121C"
POSES = ["turn_front", "turn_side", "turn_back", "idle", "walk_contact", "walk_passing",
         "cast", "hurt", "levelup", "sunflare", "defeat", "victory"]
# per pose: head offset, torso lean (px), legs [(hip_dx, foot_dx, foot_y)], arms [(dx, dy) from the front shoulder],
# satchel visible, glow radius (0 = none). Arms are drawn outside the torso so they read in silhouette.
SPEC = {
    "turn_front":   dict(head=(0, 0), lean=0, legs=[(-3, -4, 31), (3, 4, 31)], arms=[(-8, 8), (8, 8)], bag=False, glow=0, front=True),
    "turn_side":    dict(head=(1, 0), lean=0, legs=[(0, 0, 31)], arms=[], bag=True, glow=0),
    "turn_back":    dict(head=(0, 0), lean=0, legs=[(-3, -4, 31), (3, 4, 31)], arms=[(-8, 8), (8, 8)], bag=True, glow=0, back=True),
    "idle":         dict(head=(1, 0), lean=0, legs=[(-2, -3, 31), (2, 3, 31)], arms=[(3, 9)], bag=True, glow=10),
    "walk_contact": dict(head=(1, 1), lean=1, legs=[(-2, -7, 31), (2, 7, 31)], arms=[(7, 6)], bag=True, glow=10),
    "walk_passing": dict(head=(1, -1), lean=0, legs=[(0, 0, 31), (2, 6, 27)], arms=[(2, 9)], bag=True, glow=10),
    "cast":         dict(head=(2, 0), lean=2, legs=[(-2, -5, 31), (2, 5, 31)], arms=[(12, 0)], bag=True, glow=10),
    "hurt":         dict(head=(-4, 2), lean=-3, legs=[(-2, -6, 31), (2, 5, 28)], arms=[(-6, -9)], bag=True, glow=0),
    "levelup":      dict(head=(0, -2), lean=0, legs=[(-2, -3, 31), (2, 3, 31)], arms=[(-5, -12), (5, -12)], bag=True, glow=10, both=True),
    "sunflare":     dict(head=(0, -1), lean=0, legs=[(-3, -6, 31), (3, 6, 31)], arms=[(-12, -2), (12, -2)], bag=True, glow=14, both=True),
    "defeat":       dict(down=True),
    "victory":      dict(head=(1, -2), lean=0, legs=[(-3, -7, 31), (3, 7, 31)], arms=[(8, -13), (6, 4)], bag=True, glow=10),
}

def pose(name: str, silhouette: bool = False) -> Image.Image:
    s = SPEC[name]
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = (lambda col: INK) if silhouette else (lambda col: col)
    if s.get("down"):
        d.rectangle([9, 24, 27, 29], fill=c(NAVY), outline=INK)
        d.rectangle([22, 21, 26, 24], fill=c(BROWN), outline=INK)
        d.ellipse([1, 21, 11, 31], fill=c(NAVY), outline=INK)
        d.line([27, 26, 31, 28], fill=INK, width=2)
        return im
    hx, hy = 16 + s["head"][0], 8 + s["head"][1]
    if s["glow"] and not silhouette:
        r = s["glow"]
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(255, 241, 201, 90))
    for hip, foot, fy in s["legs"]:
        d.line([16 + hip, 26, 16 + foot, fy], fill=INK, width=2)
    tx = 16 + s["lean"]
    d.rectangle([tx - 5, 14, tx + 5, 26], fill=c(NAVY), outline=INK)
    if s["bag"]:
        d.rectangle([tx - 9, 18, tx - 5, 23], fill=c(BROWN), outline=INK)
    for i, (ax, ay) in enumerate(s["arms"]):
        sx = tx + (5 if (ax >= 0 and not (s.get("front") or s.get("back") or s.get("both"))) else (5 if ax >= 0 else -5))
        d.line([sx, 16, sx + ax, 16 + ay], fill=INK, width=2)
    d.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=c(NAVY if s.get("back") else GOLD), outline=INK)
    if not s.get("back") and not silhouette:
        lx = hx if s.get("front") else hx + 2
        d.rectangle([lx - 2, hy - 2, lx + 2, hy + 2], fill=CREAM)
    return im

def label(im: Image.Image, text: str) -> Image.Image:
    out = Image.new("RGBA", (im.width, im.height + 28), "#C7D0E0")
    out.paste(im, (0, 0))
    ImageDraw.Draw(out).text((6, im.height + 6), text, fill=INK, font=ImageFont.load_default())
    return out

def x8(im): return im.resize((im.width * 8, im.height * 8), Image.NEAREST)

tiles = [label(x8(pose(p)), f"{i+1:02d} {p}") for i, p in enumerate(POSES)]
sheet = Image.new("RGBA", (256 * 6, tiles[0].height * 2), "#C7D0E0")
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % 6) * 256, (i // 6) * t.height))
sheet.save(OUT / "blockout-poses-x8.png")

sil = Image.new("RGBA", (32 * 12 + 11 * 4, 32), "#C7D0E0")
for i, p in enumerate(POSES):
    sil.paste(pose(p, silhouette=True), (i * 36, 0), pose(p, silhouette=True))
Image.Image.resize(sil, (sil.width * 3, sil.height * 3), Image.NEAREST).save(OUT / "silhouette-32.png")
sil.save(OUT / "silhouette-32-actual-size.png")

ov = x8(pose("idle"))
d = ImageDraw.Draw(ov)
d.rectangle([0, 0, 255, 255], outline="#00FF99", width=2)
d.ellipse([(16 - 10) * 8, (20 - 10) * 8, (16 + 10) * 8, (20 + 10) * 8], outline="#FF3366", width=4)
d.line([16 * 8, 0, 16 * 8, 255], fill="#FF3366", width=1)
d.line([0, 20 * 8, 255, 20 * 8], fill="#FF3366", width=1)
ov.save(OUT / "collision-overlay-x8.png")

pal = Image.new("RGB", (5 * 120, 120))
for i, col in enumerate([GOLD, CREAM, NAVY, BROWN, INK]):
    ImageDraw.Draw(pal).rectangle([i * 120, 0, i * 120 + 119, 119], fill=col)
pal.save(OUT / "palette.png")
print("wrote blockout, silhouettes, collision overlay, palette")
