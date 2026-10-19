#!/usr/bin/env python3
"""Generate the circular PLANET EXPRESS logo decal (1024px, transparent PNG).

No bpy dependency - runs under system python (needs Pillow) or Blender's python.
"""
import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))


def make_logo(path=None):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("PIL not available; cannot generate logo")
        return None
    path = path or os.path.join(OUT, "planet_express_logo.png")
    S = 1024
    C = S // 2
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cream = (237, 230, 210, 255)
    ink = (16, 24, 40, 255)
    red = (203, 62, 48, 255)
    reddk = (158, 40, 32, 255)
    teal = (24, 122, 110, 255)

    d.ellipse([C - 500, C - 500, C + 500, C + 500], fill=cream)
    d.ellipse([C - 500, C - 500, C + 500, C + 500], outline=ink, width=12)
    d.ellipse([C - 405, C - 405, C + 405, C + 405], outline=ink, width=7)
    d.ellipse([C - 378, C - 378, C + 378, C + 378], fill=red)
    # planet shading, clipped to the planet disc
    shade = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse([C - 378, C - 150, C + 378, C + 906], fill=reddk)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([C - 378, C - 378, C + 378, C + 378], fill=255)
    shade.putalpha(mask)
    img.alpha_composite(shade)
    d = ImageDraw.Draw(img)
    d.ellipse([C - 378, C - 378, C + 378, C + 378], outline=ink, width=6)
    for (cx, cy, cr) in [(C - 150, C - 120, 46), (C + 170, C - 40, 60), (C + 40, C - 200, 34)]:
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(219, 84, 66, 255))

    # little rocket, nose up
    d.polygon([(C - 62, C - 120), (C + 62, C - 120), (C, C - 218)], fill=teal, outline=ink)
    d.ellipse([C - 62, C - 170, C + 62, C + 40], fill=teal, outline=ink)
    d.polygon([(C - 62, C - 40), (C - 118, C + 66), (C - 62, C + 40)], fill=teal, outline=ink)
    d.polygon([(C + 62, C - 40), (C + 118, C + 66), (C + 62, C + 40)], fill=teal, outline=ink)
    d.ellipse([C - 30, C - 96, C + 30, C - 36], fill=cream, outline=ink, width=4)
    d.polygon([(C - 26, C + 44), (C + 26, C + 44), (C, C + 108)], fill=(242, 178, 52, 255))

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 88)
    except OSError:
        font = ImageFont.load_default()

    def arc_text(text, radius, center_deg, top):
        n = len(text)
        span = 17.0 * n
        for i, ch in enumerate(text):
            a_deg = center_deg - span / 2 + span * (i + 0.5) / n
            a = math.radians(a_deg)
            x = C + radius * math.cos(a)
            y = C + radius * math.sin(a)
            bb = font.getbbox(ch)
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            glyph = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glyph)
            gd.text((10 - bb[0], 10 - bb[1]), ch, font=font, fill=ink)
            rot = a_deg + 90 if top else a_deg - 90
            glyph = glyph.rotate(-rot, expand=True, resample=Image.BICUBIC)
            img.alpha_composite(glyph, (int(x - glyph.width / 2), int(y - glyph.height / 2)))

    arc_text("PLANET", 448, -90, top=True)
    arc_text("EXPRESS", 448, 90, top=False)
    for sx in (-1, 1):
        d.ellipse([C + sx * 448 - 12, C - 12, C + sx * 448 + 12, C + 12], fill=ink)
    img.save(path)
    print("logo written:", path)
    return path


if __name__ == "__main__":
    make_logo()
