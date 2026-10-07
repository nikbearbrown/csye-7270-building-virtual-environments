#!/usr/bin/env python3
"""Draw walker-rudy's design-v1 blockouts: the storyboard thumbnails and the character-sheet images.

Code-drawn by Claude Code (route B, chosen by Shuai Zhang on 2026-09-30). These are blockouts made
of simple shapes; they are not generative-model outputs. Run from the repository root:

    python3 design/tools/make_blockouts.py
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SB_DIR = ROOT / "design" / "storyboard"
CH_DIR = ROOT / "design" / "character"
SS = 3  # supersampling factor

# Rudy's palette (CHARACTER-SHEET.md)
HAIR, EYES, ROBE, SKIN, BOOTS, LINE = "#C2954E", "#3E8E5E", "#5A606B", "#F2D6BD", "#6A4A33", "#3A2A24"
HAIR_DARK, HAIR_LIGHT = "#8A6633", "#DDBF8C"  # strand lines and the highlight band
# Planned Level 1 colors
WHEAT, MEADOW, SKY, CASTLE, PATH = "#D8B858", "#8FA85E", "#CFE0E6", "#A3ABB5", "#9C8463"
GRASS = "#7E9A4E"
STEEL, WOOD, IRON = "#C9CED6", "#9A6B3F", "#8E949C"
GOBLIN, TUNIC = "#8FA07A", "#7A5A3C"
CAP, STEM, SPORE = "#C2652B", "#E8DCC4", "#8A5BB0"
GOLD, HEART = "#F3E2A0", "#C84B4B"
OUTLINE_GP = 4.0  # the outer outline, in game pixels; added in-engine in the real game
INNER_GP = 1.5  # inner lines, in game pixels
TAG = "blockout · code-drawn by Claude · not a generative-model output"


# ── helpers ────────────────────────────────────────────────────────────────────

def rgb(c, a=255):
    if isinstance(c, tuple):
        return c if len(c) == 4 else (*c, a)
    r, g, b = ImageColor.getrgb(c)[:3]
    return (r, g, b, a)


def shade(c, f):
    r, g, b = ImageColor.getrgb(c)[:3]
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))


def font(size, bold=True):
    names = ["Arial Bold.ttf" if bold else "Arial.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{n}", size)
        except OSError:
            pass
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except OSError:
        return ImageFont.load_default()


def rot(v, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)


def add(*vs):
    return (sum(v[0] for v in vs), sum(v[1] for v in vs))


def mul(v, s):
    return (v[0] * s, v[1] * s)


def ldir(a):
    """Limb direction: 0 = straight down, +90 = forward (+x), 180 = straight up."""
    r = math.radians(a)
    return (math.sin(r), -math.cos(r))


def arc(c, r, a0, a1, n=24, ry=None):
    ry = r if ry is None else ry
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def composite(dst, src, x, y):
    """Alpha-composite src onto dst with its top-left at (x, y), clipping at the edges."""
    x, y = int(round(x)), int(round(y))
    l, t = max(0, x), max(0, y)
    r, b = min(dst.width, x + src.width), min(dst.height, y + src.height)
    if r <= l or b <= t:
        return
    dst.alpha_composite(src.crop((l - x, t - y, r - x, b - y)), (l, t))


def outline_under(img, n_px, color=LINE):
    """Return img with a uniform outer outline of about n_px pixels added underneath."""
    a = img.getchannel("A")
    mask = a.filter(ImageFilter.GaussianBlur(n_px / 1.87)).point(lambda v: 255 if v > 8 else 0)
    base = Image.new("RGBA", img.size, rgb(color))
    base.putalpha(mask)
    return Image.alpha_composite(base, img)


class Pen:
    """Draws in game-pixel coordinates (x forward, y up) onto a supersampled RGBA layer."""

    def __init__(self, img, ox, oy, k, flip=False):
        self.img, self.d = img, ImageDraw.Draw(img)
        self.ox, self.oy, self.k, self.flip = ox, oy, k, flip

    def p(self, pt):
        x, y = pt
        return (self.ox + (-x if self.flip else x) * self.k, self.oy - y * self.k)

    def w(self, gp):
        return max(1, int(round(gp * self.k)))

    def poly(self, pts, fill, line=LINE, lw=INNER_GP):
        q = [self.p(pt) for pt in pts]
        self.d.polygon(q, fill=rgb(fill))
        if line and lw:
            self.d.line(q + [q[0], q[1]], fill=rgb(line), width=self.w(lw), joint="curve")

    def ellipse(self, c, rx, ry, fill, line=LINE, lw=INNER_GP):
        x, y = self.p(c)
        bb = [x - rx * self.k, y - ry * self.k, x + rx * self.k, y + ry * self.k]
        self.d.ellipse(bb, fill=rgb(fill) if fill else None,
                       outline=rgb(line) if line and lw else None, width=self.w(lw) if line and lw else 0)

    def seg(self, a, b, width, fill, line=LINE, lw=INNER_GP):
        passes = ((line, width + 2 * lw), (fill, width)) if line and lw else ((fill, width),)
        pa, pb = self.p(a), self.p(b)
        for col, wd in passes:
            r = wd * self.k / 2
            self.d.line([pa, pb], fill=rgb(col), width=max(1, int(round(wd * self.k))))
            for q in (pa, pb):
                self.d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=rgb(col))

    def line(self, pts, col=LINE, lw=INNER_GP):
        self.d.line([self.p(pt) for pt in pts], fill=rgb(col), width=self.w(lw), joint="curve")


def render(draw_fn, scale, bounds=(-130, 130, -60, 220), outline=True, mode="color", ghost=1.0, after=None):
    """Render a sprite drawn by draw_fn(pen) in game pixels. Returns (image, origin_px).

    mode: "color", "silhouette" (solid black) or "flash" (blended toward white)."""
    x0, x1, y0, y1 = bounds
    k = scale * SS
    img = Image.new("RGBA", (int((x1 - x0) * k), int((y1 - y0) * k)), (0, 0, 0, 0))
    origin = (-x0 * k, y1 * k)
    draw_fn(Pen(img, origin[0], origin[1], k))
    if outline:
        img = outline_under(img, OUTLINE_GP * k)
    if after:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        after(Pen(layer, origin[0], origin[1], k))
        img = Image.alpha_composite(img, layer)
    if mode == "silhouette":
        a = img.getchannel("A")
        img = Image.new("RGBA", img.size, (0, 0, 0, 255))
        img.putalpha(a)
    elif mode == "flash":
        white = Image.new("RGBA", img.size, (255, 255, 255, 255))
        white.putalpha(img.getchannel("A"))
        img = Image.blend(img, white, 0.45)
    if ghost < 1.0:
        a = img.getchannel("A").point(lambda v: int(v * ghost))
        img.putalpha(a)
    return img, origin


def flip_h(img, origin):
    return ImageOps.mirror(img), (img.width - origin[0], origin[1])


# ── Rudy: side view, facing right ──────────────────────────────────────────────

HIP_Y, THIGH, SHIN, UPPER, FORE, R = 36, 17, 15, 15, 13, 30

POSES = {
    "idle": dict(lean=3, legs=((6, -4), (-6, -3)), arms=((10, 18), (-12, 14)), eye="open", mouth="smile"),
    "run_contact": dict(lean=14, legs=((42, -12), (-38, -48)), arms=((-45, 70), (40, 60)),
                        eye="open", mouth="smile", flare=(4, 4, 6, 6)),
    "run_passing": dict(lean=14, legs=((4, -6), (28, -105)), arms=((18, 55), (-20, 55)),
                        eye="open", mouth="smile", flare=(2, 2, 3, 3)),
    "rise": dict(lean=6, legs=((55, -105), (25, -115)), arms=((118, 20), (-45, 10)), eye="open", mouth="big",
                 air=48, grounded=False, flare=(-2, -3, -2, -3), cowlick=-14),
    "fall": dict(lean=-4, legs=((18, -6), (-12, -10)), arms=((105, 10), (-100, -10)), eye="open", mouth="o",
                 air=22, grounded=False, flare=(6, 10, 6, 10), cowlick=12),
    "hurt": dict(lean=-20, legs=((25, -12), (-18, -18)), arms=((125, 0), (-110, 0)), eye="squeeze", mouth="o",
                 air=8, grounded=False, tilt=-8),
    "defeat": dict(lean=-8, sit=True, legs=((88, -4), (80, -8)), arms=((35, 25), (-25, 30)), eye="dizzy",
                   mouth="small", flare=(10, 9, 4, 9)),
    "respawn": dict(lean=14, kneel=True, legs=((80, -80), (-10, -80)), arms=((55, 35), (-15, 25)), eye="open",
                    mouth="grit"),
    "celebrate": dict(lean=2, legs=((28, -45), (-14, -50)), arms=((70, 70), (-125, 0)), eye="happy", mouth="big",
                      air=10, grounded=False),
    "sword_idle": dict(lean=6, legs=((24, -14), (-20, -12)), arms=((40, 25), (25, 70)), eye="open", mouth="smile",
                       sword=70, shield="back"),
    "slash": dict(lean=16, legs=((48, -22), (-36, -14)), arms=((90, 0), (25, 95)), eye="open", mouth="grit",
                  sword=92, shield="back", swoosh=True),
    "block": dict(lean=8, legs=((26, -28), (-26, -24)), arms=((-35, 40), (55, 75)), eye="open", mouth="grit",
                  sword=-55, shield="front"),
}


def skeleton(pose, air=True):
    lean = pose.get("lean", 0)
    hip = (0, HIP_Y + (pose.get("air", 0) if air else 0))
    legs = []
    for i, (a, knee) in enumerate(pose["legs"]):  # 0 = near, 1 = far
        h = add(hip, (2 if i == 0 else -2, 3))
        k = add(h, mul(ldir(a), THIGH))
        ank = add(k, mul(ldir(a + knee), SHIN))
        legs.append((h, k, ank, a + knee))
    contacts = []
    for h, k, ank, sa in legs:
        contacts.append(ank[1] - 4)
        if pose.get("kneel"):
            contacts.append(k[1] - 5)
    if pose.get("sit"):
        contacts.append(hip[1] - 8)
    dy = 0.0
    if pose.get("grounded", True):
        dy = -min(contacts)
    hip = add(hip, (0, dy))
    legs = [(add(h, (0, dy)), add(k, (0, dy)), add(a, (0, dy)), sa) for h, k, a, sa in legs]
    body = lambda p: add(hip, rot(p, -lean))  # torso-local → world
    arms = []
    for i, (a, el) in enumerate(pose["arms"]):
        s = body((1 if i == 0 else -1, 46))
        e = add(s, mul(ldir(a), UPPER))
        hand = add(e, mul(ldir(a + el), FORE))
        arms.append((s, e, hand))
    neck = body((0, 54))
    head_rot = -(lean + pose.get("tilt", 0))
    head_c = add(neck, rot((0, R), head_rot))
    return dict(hip=hip, legs=legs, arms=arms, body=body, head_c=head_c, head_rot=head_rot)


def draw_leg(pen, leg, col):
    h, k, ank, sa = leg
    pen.seg(h, k, 11, col)
    pen.seg(k, ank, 10, col)
    toe = add(ank, mul(ldir(sa + 90), 10))
    pen.seg(ank, toe, 8, col)


def draw_arm(pen, arm, sleeve, hand_col=SKIN):
    s, e, hand = arm
    pen.seg(s, e, 11, sleeve)
    pen.seg(e, hand, 10, sleeve)
    pen.ellipse(hand, 5.2, 5.2, hand_col)


def draw_sword(pen, hand, a):
    d = ldir(a)
    n = ldir(a + 90)
    guard = add(hand, mul(d, 4))
    tip = add(hand, mul(d, 36))
    pen.seg(add(hand, mul(d, -6)), guard, 3.4, BOOTS)
    pen.poly([add(guard, mul(n, 1.9)), add(tip, mul(d, -3), mul(n, 1.9)), tip,
              add(tip, mul(d, -3), mul(n, -1.9)), add(guard, mul(n, -1.9))], STEEL)
    pen.seg(add(guard, mul(n, 6)), add(guard, mul(n, -6)), 2.6, IRON)
    pen.ellipse(add(hand, mul(d, -7)), 2.4, 2.4, IRON)


def draw_shield(pen, c, rx=14, ry=17):
    pen.ellipse(c, rx, ry, IRON)
    pen.ellipse(c, rx - 2.6, ry - 2.6, WOOD)
    pen.ellipse(c, 2.8, 2.8, IRON)


def draw_head(pen, sk, pose):
    c, hr = sk["head_c"], sk["head_rot"]
    H = lambda p: add(c, rot(p, hr))
    pen.ellipse(c, R, R, SKIN)
    hair = arc((0, 0), R + 2, 25, 205, 30)
    hair += [(-0.86 * R, -0.62 * R), (-0.62 * R, -1.0 * R), (-0.38 * R, -0.78 * R), (0.10 * R, -0.55 * R),
             (0.20 * R, -0.15 * R), (0.30 * R, 0.24 * R), (0.46 * R, 0.40 * R), (0.60 * R, 0.27 * R),
             (0.76 * R, 0.36 * R), (0.90 * R, 0.30 * R)]
    pen.poly([H(p) for p in hair], HAIR)
    band = arc((0, 0), 0.84 * R, 70, 140, 12) + arc((0, 0), 0.70 * R, 140, 70, 12)
    pen.poly([H(p) for p in band], HAIR_LIGHT, lw=0)
    for r0, a0, a1 in ((0.92, 95, 200), (0.62, 105, 195), (0.36, 120, 185)):
        pen.line([H(p) for p in arc((0, 0), r0 * R, a0, a1, 14)], HAIR_DARK, 1.0)
    for strand in (((0.40, 0.84), (0.48, 0.60), (0.52, 0.40)), ((0.60, 0.74), (0.70, 0.54), (0.76, 0.40))):
        pen.line([H((x * R, y * R)) for x, y in strand], HAIR_DARK, 1.0)
    ca = pose.get("cowlick", 0)
    cow = [(-3, 29), (-4.5, 33.5), (-2.5, 38), (2, 40), (0.5, 37), (-1, 34), (1.2, 29.4)]
    base = (-1, 29)
    pen.poly([H(add(base, rot((p[0] - base[0], p[1] - base[1]), ca))) for p in cow], HAIR)
    e = (0.42 * R, 0.02 * R)
    st = pose.get("eye", "open")
    if st == "open":
        pen.ellipse(H(e), 4.3, 6.2, EYES)
        pen.ellipse(H(add(e, (0.9, -0.5))), 2.2, 3.4, LINE, lw=0)
        pen.ellipse(H(add(e, (-0.9, 2.3))), 1.3, 1.3, "#FFFFFF", lw=0)
    elif st == "happy":
        pen.line([H(add(e, (-4, -1))), H(add(e, (0, 2.2))), H(add(e, (4, -1)))], LINE, 1.6)
    elif st == "squeeze":
        pen.line([H(add(e, (-3.5, 3))), H(add(e, (2.5, 0))), H(add(e, (-3.5, -3)))], LINE, 1.6)
    elif st == "dizzy":
        pen.ellipse(H(e), 4, 4, None, LINE, 1.2)
        pen.ellipse(H(e), 1.8, 1.8, None, LINE, 1.2)
    m = (0.62 * R, -0.42 * R)
    ms = pose.get("mouth", "smile")
    if ms == "smile":
        pen.line([H(add(m, (-3, 1))), H(add(m, (0, -1.2))), H(add(m, (3, 1)))], LINE, 1.3)
    elif ms == "big":
        pen.ellipse(H(m), 3.2, 2.6, "#7A3B2E", LINE, 1.0)
    elif ms == "o":
        pen.ellipse(H(m), 1.8, 2.2, "#7A3B2E", LINE, 1.0)
    elif ms == "small":
        pen.line([H(add(m, (-2.5, -0.8))), H(add(m, (0, 0.6))), H(add(m, (2.5, -0.8)))], LINE, 1.2)
    elif ms == "grit":
        pen.line([H(add(m, (-2.8, 0))), H(add(m, (2.8, 0.4)))], LINE, 1.3)


def draw_rudy(pen, pose_name, air=True):
    pose = POSES[pose_name]
    sk = skeleton(pose, air)
    body = sk["body"]
    fl = pose.get("flare", (0, 0, 0, 0))
    far_sleeve, far_boot = shade(ROBE, 0.82), shade(BOOTS, 0.82)
    draw_arm(pen, sk["arms"][1], far_sleeve, shade(SKIN, 0.9))
    if pose.get("shield") == "back":
        draw_shield(pen, add(sk["arms"][1][2], (1, 2)))
    draw_leg(pen, sk["legs"][1], far_boot)
    draw_leg(pen, sk["legs"][0], BOOTS)
    robe = [(-14, 50), (12, 50), (15, 30), (22 + fl[0], -16 + fl[1]), (6, -19 + (fl[1] + fl[3]) / 2),
            (-20 - fl[2], -16 + fl[3]), (-16, 30)]
    pen.poly([body(p) for p in robe], ROBE)
    pen.poly([body(p) for p in [(-17.5, 20), (16, 20), (16.6, 14.5), (-18.2, 14.5)]], BOOTS)
    pen.poly([body(p) for p in [(-4, 51), (-14, 54), (-24, 48), (-28, 37), (-23, 26), (-12, 23), (-6, 33)]],
             shade(ROBE, 0.9))
    pen.line([body(p) for p in [(-8, 47), (-15, 40), (-20, 31)]], LINE, 1.0)
    draw_head(pen, sk, pose)
    near = sk["arms"][0]
    if "sword" in pose:
        s, e, hand = near
        pen.seg(s, e, 11, ROBE)
        pen.seg(e, hand, 10, ROBE)
        draw_sword(pen, hand, pose["sword"])
        pen.ellipse(hand, 5.2, 5.2, SKIN)
    else:
        draw_arm(pen, near, ROBE)
    if pose.get("shield") == "front":
        draw_shield(pen, add(sk["arms"][1][2], (5, 0)), rx=10, ry=18)


def swoosh_after(pose_name, air=True):
    if not POSES[pose_name].get("swoosh"):
        return None
    sk = skeleton(POSES[pose_name], air)

    def after(pen):
        s = add(sk["arms"][0][0], (8, -8))
        outer = arc(s, 54, 55, -50, 30)
        inner = arc(s, 44, -50, 55, 30)
        pen.d.polygon([pen.p(p) for p in outer + inner], fill=(255, 255, 255, 150))
    return after


def rudy(pose_name, scale, air=True, **kw):
    return render(lambda pen: draw_rudy(pen, pose_name, air), scale, after=swoosh_after(pose_name, air), **kw)


# ── Rudy: front, three-quarter and back views for the turnaround ───────────────

def draw_rudy_view(pen, view):
    sx = 0.86 if view == "3q" else 1.0
    X = lambda p: (p[0] * sx, p[1])
    for bx in (-8, 8):
        pen.seg(X((bx, 20)), X((bx, 5)), 10, BOOTS)
        pen.seg(X((bx, 4)), X((bx + (3 if view == "3q" else 0), 4)), 10, BOOTS)
    for side in (-1, 1):
        pen.seg(X((16 * side, 84)), X((22 * side, 64)), 11, ROBE if view != "back" else shade(ROBE, 0.95))
        pen.seg(X((22 * side, 64)), X((23 * side, 50)), 10, ROBE)
        pen.ellipse(X((23.5 * side, 46)), 5.2, 5.2, SKIN)
    robe = [(-15, 88), (15, 88), (16, 60), (26, 20), (0, 17), (-26, 20), (-16, 60)]
    pen.poly([X(p) for p in robe], ROBE)
    pen.poly([X(p) for p in [(-17.5, 57), (17.5, 57), (18.2, 51.5), (-18.2, 51.5)]], BOOTS)
    if view == "back":
        pen.poly([X(p) for p in [(-22, 92), (22, 92), (27, 72), (14, 58), (0, 54), (-14, 58), (-27, 72)]],
                 shade(ROBE, 0.9))
        pen.line([X((-12, 82)), X((0, 64)), X((12, 82))], LINE, 1.2)
    else:
        pen.ellipse(X((0, 86)), 26, 10, shade(ROBE, 0.9))
    c = (0, 120)
    if view == "back":
        pen.ellipse(c, R + 2, R + 2, HAIR)
        nape = [(-26, 106), (-14, 93), (0, 97), (14, 93), (26, 106)]
        pen.poly(nape + [(20, 112), (-20, 112)], HAIR, lw=0)
        pen.line(nape, LINE, INNER_GP)
        pen.poly(arc(c, 0.84 * R, 50, 130, 12) + arc(c, 0.70 * R, 130, 50, 12), HAIR_LIGHT, lw=0)
        for ex in (-0.7, -0.3, 0.3, 0.7):
            pen.line([(0, 120 + 0.95 * R), (ex * 0.6 * R, 120 + 0.3 * R), (ex * R, 120 - 0.62 * R)], HAIR_DARK, 1.0)
    else:
        pen.ellipse(X(c), R, R, SKIN)
        off = 5 if view == "3q" else 0
        hair = arc(c, R + 2, -28, 208, 34)
        hair += [(-0.92 * R, 120 - 0.62 * R), (-0.72 * R, 120 - 0.10 * R), (-0.60 * R + off, 120 + 0.30 * R),
                 (-0.40 * R + off, 120 + 0.44 * R), (-0.18 * R + off, 120 + 0.62 * R), (off, 120 + 0.72 * R),
                 (0.18 * R + off, 120 + 0.62 * R), (0.40 * R + off, 120 + 0.44 * R), (0.60 * R + off, 120 + 0.30 * R),
                 (0.72 * R, 120 - 0.10 * R), (0.92 * R, 120 - 0.62 * R)]
        pen.poly([X(p) for p in hair], HAIR)
        for a0, a1 in ((100, 150), (30, 80)):
            pen.poly([X(p) for p in arc(c, 0.86 * R, a0, a1, 10) + arc(c, 0.72 * R, a1, a0, 10)], HAIR_LIGHT, lw=0)
        pen.line([X((off, 120 + 0.72 * R)), X((off * 0.5, 120 + 1.0 * R))], HAIR_DARK, 1.1)
        for sgn in (-1, 1):
            for pts in (((0.06, 0.98), (0.45, 0.82), (0.78, 0.45), (0.88, -0.10)),
                        ((0.10, 0.84), (0.38, 0.70), (0.60, 0.44))):
                pen.line([X((sgn * x * R + off * (1 - x), 120 + y * R)) for x, y in pts], HAIR_DARK, 1.0)
        eyes = [(-11, 118, 4.3), (11, 118, 4.3)] if view == "front" else [(3, 118, 3.4), (18, 118, 4.3)]
        for ex, ey, rx in eyes:
            pen.ellipse(X((ex, ey)), rx, 6.2, EYES)
            pen.ellipse(X((ex + 0.4, ey - 0.5)), rx * 0.5, 3.4, LINE, lw=0)
            pen.ellipse(X((ex - 0.9, ey + 2.3)), 1.2, 1.2, "#FFFFFF", lw=0)
        mx = 0 if view == "front" else 11
        pen.line([X((mx - 3, 105)), X((mx, 103.6)), X((mx + 3, 105))], LINE, 1.3)
    cow = [(-3, 149), (-4.5, 153.5), (-2.5, 158), (2, 160), (0.5, 157), (-1, 154), (1.2, 149.4)]
    pen.poly([X(p) for p in cow], HAIR)


def rudy_view(view, scale):
    if view == "side":
        return rudy("idle", scale)
    return render(lambda pen: draw_rudy_view(pen, view), scale)


# ── Enemies, props and hazards ─────────────────────────────────────────────────

def draw_goblin(pen, state="walk", step=0):
    if state == "squash":
        pen.ellipse((0, 10), 40, 11, GOBLIN)
        pen.ellipse((-30, 16), 12, 6, GOBLIN)
        pen.line([(10, 10), (16, 16)], LINE, 1.6)
        pen.line([(10, 16), (16, 10)], LINE, 1.6)
        return
    sw = 18 if step == 0 else -18
    for i, a in enumerate((sw, -sw)):
        col = GOBLIN if i == 0 else shade(GOBLIN, 0.85)
        pen.seg((0, 30), add((0, 30), mul(ldir(a), 26)), 9, col)
    pen.poly([(-15, 62), (13, 62), (19, 24), (-21, 24)], TUNIC)
    pen.seg((2, 56), add((2, 56), mul(ldir(-sw * 1.3), 20)), 8, GOBLIN)
    c = (2, 88)
    pen.poly([(-18, 98), (-46, 116), (-22, 86)], GOBLIN)
    pen.ellipse(c, 27, 25, GOBLIN)
    pen.ellipse((27, 84), 8, 6, shade(GOBLIN, 0.92))
    pen.ellipse((13, 94), 3.4, 4.4, LINE, lw=0)
    pen.ellipse((12.2, 95.6), 1.1, 1.1, "#FFFFFF", lw=0)
    pen.line([(6, 74), (14, 71), (22, 75)], LINE, 1.4)


def goblin(scale, state="walk", step=0, **kw):
    return render(lambda pen: draw_goblin(pen, state, step), scale, **kw)


def draw_mushroom(pen, state="idle"):
    if state == "squash":
        pen.ellipse((0, 9), 34, 9, STEM)
        pen.ellipse((0, 22), 56, 12, CAP)
        return
    for x in (-14, -4, 9):
        pen.line([(x, 2), (x - 4, -6)], BOOTS, 2.2)
    pen.poly([(-19, 0), (19, 0), (17, 30), (15, 66), (-13, 66), (-17, 30)], STEM)
    pen.ellipse((8, 48), 3.0, 4.2, LINE, lw=0)
    pen.ellipse((17, 46), 2.4, 3.6, LINE, lw=0)
    if state == "attack":
        pen.ellipse((14, 28), 5.5, 6.5, "#5E2A22")
        cap = arc((0, 66), 58, 0, 180, 30, ry=28) + [(-60, 60), (60, 60)]
    else:
        pen.ellipse((14, 28), 3.6, 4.2, "#5E2A22")
        cap = arc((0, 66), 52, 0, 180, 30, ry=38) + [(-55, 56), (55, 56)]
    pen.poly(cap[:-2] + [cap[-1], cap[-2]][::-1], CAP)
    pen.poly([(-50, 62), (50, 62), (46, 57), (-46, 57)], "#EAD9B8")
    for sx, sy in ((-24, 84), (6, 96), (28, 80)):
        pen.ellipse((sx, sy if state != "attack" else sy - 8), 5, 3.5, "#9C4A1E", lw=0)


def mushroom(scale, state="idle", **kw):
    return render(lambda pen: draw_mushroom(pen, state), scale, **kw)


def draw_waystone(pen, lit=False):
    pen.poly([(-22, 0), (22, 0), (21, 52), (14, 68), (0, 72), (-14, 68), (-21, 52)], "#9AA0A8")
    rune = "#CFEAFF" if lit else "#5C6168"
    pen.line([(0, 18), (0, 54)], rune, 3)
    pen.line([(-9, 46), (0, 38), (9, 46)], rune, 3)
    pen.line([(-8, 26), (8, 26)], rune, 3)
    for x in (-16, -4, 12):
        pen.ellipse((x, 3), 8, 4, MEADOW, lw=0)


def waystone(scale, lit=False, **kw):
    def after(pen):
        if lit:
            for r, a in ((34, 60), (24, 70)):
                x, y = pen.p((0, 36))
                rr = r * pen.k
                pen.d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(207, 234, 255, a))
    return render(lambda pen: draw_waystone(pen, lit), scale, after=after, **kw)


def draw_gear(pen):
    draw_shield(pen, (-6, 0))
    draw_sword(pen, (6, -14), 145)


def gear(scale, **kw):
    return render(draw_gear, scale, bounds=(-40, 40, -40, 45), **kw)


# ── Storyboard frames ──────────────────────────────────────────────────────────

class Frame:
    def __init__(self, w=1280, h=720):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w * SS, h * SS), (255, 255, 255, 255))
        self.d = ImageDraw.Draw(self.img)
        self.labels = []

    def P(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def poly(self, pts, fill, line=None, lw=0):
        self.d.polygon(self.P(pts), fill=rgb(fill))
        if line:
            q = self.P(pts)
            self.d.line(q + [q[0]], fill=rgb(line), width=int(lw * SS))

    def rect(self, x0, y0, x1, y1, fill):
        self.d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=rgb(fill))

    def tpoly(self, pts, fill_rgba):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon(self.P(pts), fill=fill_rgba)
        self.img = Image.alpha_composite(self.img, layer)
        self.d = ImageDraw.Draw(self.img)

    def tellipse(self, cx, cy, rx, ry, fill_rgba, line=None, lw=0):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS],
                                      fill=fill_rgba, outline=rgb(line) if line else None, width=int(lw * SS))
        self.img = Image.alpha_composite(self.img, layer)
        self.d = ImageDraw.Draw(self.img)

    def line(self, pts, col, lw, dash=None):
        q = self.P(pts)
        if not dash:
            self.d.line(q, fill=rgb(col), width=int(lw * SS), joint="curve")
            return
        on, off = dash[0] * SS, dash[1] * SS
        acc, draw_on = 0.0, True
        for (x0, y0), (x1, y1) in zip(q, q[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            t = 0.0
            while t < L:
                step = min((on if draw_on else off) - acc, L - t)
                if draw_on:
                    a, b = t / L, (t + step) / L
                    self.d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)],
                                fill=rgb(col), width=int(lw * SS))
                t += step
                acc += step
                if acc >= (on if draw_on else off) - 1e-6:
                    acc, draw_on = 0.0, not draw_on

    def arrow(self, pts, col=LINE, lw=4, dash=None, head=16):
        self.line(pts, col, lw, dash)
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        a = math.atan2(y1 - y0, x1 - x0)
        tip = (x1, y1)
        left = (x1 - head * math.cos(a - 0.45), y1 - head * math.sin(a - 0.45))
        right = (x1 - head * math.cos(a + 0.45), y1 - head * math.sin(a + 0.45))
        self.poly([tip, left, right], col)

    def gradient(self, y0, y1, c0, c1):
        a, b = ImageColor.getrgb(c0), ImageColor.getrgb(c1)
        for y in range(int(y0 * SS), int(y1 * SS)):
            t = (y - y0 * SS) / max(1, (y1 - y0) * SS)
            col = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
            self.d.line([(0, y), (self.w * SS, y)], fill=col)

    def sprite(self, made, x, y_base, flip=False):
        img, origin = made
        if flip:
            img, origin = flip_h(img, origin)
        composite(self.img, img, x * SS - origin[0], y_base * SS - origin[1])
        self.d = ImageDraw.Draw(self.img)

    def label(self, xy, text, size=22, fg="#FFFFFF", bg=(40, 30, 26, 200), pad=8):
        self.labels.append((xy, text, size, fg, bg, pad))

    def save(self, path, header):
        out = self.img.resize((self.w, self.h), Image.LANCZOS)
        d = ImageDraw.Draw(out, "RGBA")
        self.labels.insert(0, ((14, 12), header, 24, "#FFFFFF", (40, 30, 26, 215), 10))
        for (x, y), text, size, fg, bg, pad in self.labels:
            f = font(size)
            bb = d.textbbox((x, y), text, font=f)
            d.rounded_rectangle([bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad], radius=6, fill=bg)
            d.text((x, y), text, font=f, fill=rgb(fg))
        f = font(15, bold=False)
        bb = d.textbbox((0, 0), TAG, font=f)
        d.text((self.w - (bb[2] - bb[0]) - 12, self.h - 26), TAG, font=f, fill=(60, 50, 45, 220))
        d.rectangle([0, 0, self.w - 1, self.h - 1], outline=rgb(LINE), width=3)
        out.convert("RGB").save(path)


def hills_y(x, horizon):
    return horizon - 18 * math.sin(x / 140) - 10 * math.sin(x / 57 + 1)


def castle(f, cx, by, s=1.0):
    col, roof = CASTLE, shade(CASTLE, 0.86)
    f.rect(cx - 22 * s, by - 48 * s, cx + 22 * s, by, col)
    for dx in (-27, 27):
        f.rect(cx + (dx - 7) * s, by - 64 * s, cx + (dx + 7) * s, by, col)
        f.poly([(cx + (dx - 9) * s, by - 64 * s), (cx + dx * s, by - 84 * s), (cx + (dx + 9) * s, by - 64 * s)], roof)
    for i in range(5):
        x = cx - 20 * s + i * 9 * s
        f.rect(x, by - 54 * s, x + 5 * s, by - 48 * s, col)
    f.poly([(cx - 7 * s, by), (cx - 7 * s, by - 14 * s), (cx, by - 20 * s), (cx + 7 * s, by - 14 * s), (cx + 7 * s, by)],
           shade(CASTLE, 0.7))


def heart(f, x, y, full=True, s=1.0):
    pts = [(x, y + 9 * s)] + [(x - 13 * s * math.sin(t) ** 3, y - (11 * math.cos(t) - 4 * math.cos(2 * t) - 1.6 * math.cos(3 * t)
            - math.cos(4 * t)) * s) for t in [i * 2 * math.pi / 40 for i in range(41)]]
    f.poly(pts, HEART if full else (255, 255, 255, 0), LINE, 2.2)


def hearts(f, n_full=3, total=3, x=46, y=86):
    for i in range(total):
        heart(f, x + i * 38, y, full=i < n_full)


def spikes(f, x0, gy, n=5, s=1.0):
    w = 20 * s
    f.poly([(x0 - 4, gy), (x0 + n * w + 4, gy), (x0 + n * w + 4, gy - 10 * s), (x0 - 4, gy - 10 * s)], WOOD, LINE, 2)
    for i in range(n):
        f.poly([(x0 + i * w, gy - 10 * s), (x0 + i * w + w / 2, gy - 42 * s), (x0 + (i + 1) * w, gy - 10 * s)], IRON,
               LINE, 2)


def spore(f, x, y, r=11, alpha=255):
    f.tellipse(x, y, r + 3, r + 3, (138, 91, 176, int(alpha * 0.35)))
    f.tellipse(x, y, r, r, (138, 91, 176, alpha), LINE, 2)
    f.tellipse(x - 2, y - 2, r * 0.4, r * 0.4, (205, 180, 230, alpha))


def burst(f, x, y, r=26, col=(255, 248, 225, 255)):
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    f.poly(pts, col, LINE, 2)


def gameplay_bg(f, ground_y=560, gaps=(), horizon=330, castle_x=930, castle_s=0.8):
    f.gradient(0, horizon + 60, "#BCD6E6", "#EEF3F0")
    hills = [(x, hills_y(x, horizon)) for x in range(0, f.w + 21, 20)]
    f.poly(hills + [(f.w, horizon + 140), (0, horizon + 140)], "#A9BFB2")
    castle(f, castle_x, hills_y(castle_x, horizon) + 4, castle_s)
    mead = [(x, horizon + 34 - 14 * math.sin(x / 190 + 2)) for x in range(0, f.w + 21, 20)]
    f.poly(mead + [(f.w, ground_y), (0, ground_y)], MEADOW)
    wh = [(x, horizon + 92 - 16 * math.sin(x / 160 + 0.5)) for x in range(0, f.w + 21, 20)]
    f.poly(wh + [(f.w, ground_y), (0, ground_y)], WHEAT)
    for x in range(6, f.w, 13):
        top = horizon + 92 - 16 * math.sin(x / 160 + 0.5)
        f.line([(x, top + 6), (x + 3, top + 26)], "#C29E45", 2)
    edges = [0] + [v for g in gaps for v in g] + [f.w]
    for x0, x1 in zip(edges[0::2], edges[1::2]):
        f.rect(x0, ground_y, x1, f.h, PATH)
        f.rect(x0, ground_y, x1, ground_y + 12, GRASS)
        f.line([(x0, ground_y), (x1, ground_y)], LINE, 3)
        for x in (x0, x1):
            if 0 < x < f.w:
                f.line([(x, ground_y), (x, f.h)], LINE, 3)
    for x0, x1 in gaps:
        f.rect(x0 + 1.5, ground_y + 1.5, x1 - 1.5, f.h, "#5A4E44")


K = 720 / 1080  # gameplay: frame px per game px (1920×1080 view drawn at 1280×720)


def panel_1():
    f = Frame()
    gy = 560
    gameplay_bg(f, gy)
    f.sprite(rudy("idle", K), 250, gy)
    f.tpoly([(390, 118), (890, 118), (890, 232), (390, 232)], (255, 255, 255, 205))
    f.line([(390, 118), (890, 118), (890, 232), (390, 232), (390, 118)], LINE, 3)
    f.label((516, 150), "GAME TITLE", 40, "#3A2A24", (255, 255, 255, 0), 0)
    f.label((536, 262), "press Enter to start", 20, "#3A2A24", (255, 255, 255, 200), 8)
    f.label((120, 600), "Rudy at the start of Level 1, idle", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((842, 300), "castle far away", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((560, 610), "Enter: the title fades and play starts on this same screen.", 17, "#FFFFFF",
            (40, 30, 26, 200), 6)
    f.label((560, 642), "No loading, no scene change; the hearts appear.", 17, "#FFFFFF", (40, 30, 26, 200), 6)
    f.save(SB_DIR / "01-first-sight.png", "1  FIRST SIGHT · MEDIUM · EYE LEVEL · GAMEPLAY VIEW, TITLE ON TOP")


def panel_2():
    f = Frame()
    gy = 560
    gameplay_bg(f, gy)
    spikes(f, 560, gy, 5, 0.95)
    f.sprite(goblin(K), 806, gy, flip=True)
    f.sprite(rudy("run_contact", K, ghost=0.4), 330, gy)
    f.sprite(rudy("rise", K, ghost=0.45), 560, gy - 120)
    q = [((1 - t) ** 2 * 360 + 2 * (1 - t) * t * 560 + t * t * 792, (1 - t) ** 2 * (gy - 6) + 2 * (1 - t) * t * (gy - 380)
          + t * t * (gy - 112)) for t in [i / 30 for i in range(31)]]
    f.arrow(q, LINE, 4, dash=(16, 10))
    f.sprite(rudy("fall", K), 796, gy - 66)
    burst(f, 812, gy - 80, 22)
    f.arrow([(846, gy - 110), (872, gy - 182)], LINE, 4)
    hearts(f)
    f.label((860, 336), "bounce", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((520, 586), "spikes", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((740, 586), "patrolling goblin", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((360, 210), "jump arc over the spikes, stomp", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((960, 60), "CAMERA FOLLOWS RUDY →", 18, "#FFFFFF", (40, 30, 26, 200), 6)
    f.save(SB_DIR / "02-core-action.png", "2  CORE ACTION · MEDIUM · EYE LEVEL · GAMEPLAY")


def panel_3():
    f = Frame()
    f.gradient(0, 720, "#A9C6DC", "#F2E9D8")
    vp = (640, -1400)
    for x in (-200, 120, 1160, 1480):
        f.line([(x, 720), (vp[0] + (x - vp[0]) * 0.55, 0)], (255, 255, 255, 255), 2)
    f.sprite(rudy("sword_idle", 5.0), 560, 920)
    for x in range(0, 1281, 9):
        h = 40 + 30 * math.sin(x / 23) ** 2
        f.line([(x, 720), (x + 6, 720 - h)], "#C29E45" if x % 2 else WHEAT, 5)
    for (x, y, r) in ((780, 470, 14), (840, 410, 9), (720, 560, 10), (870, 520, 7), (650, 420, 6)):
        f.tellipse(x, y, r * 2.2, r * 2.2, (255, 240, 200, 90))
        burst(f, x, y, r, (255, 250, 230, 255))
    f.label((900, 300), "glow fading as the pickup is taken", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((40, 640), "LOW ANGLE: the camera is below Rudy, looking up", 18, "#FFFFFF", (40, 30, 26, 200), 6)
    f.label((900, 600), "hand closes on the hilt;\nshield on the other arm", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.save(SB_DIR / "03-success.png", "3  SUCCESS · CLOSE-UP · LOW ANGLE · DESIGN VIEW (in play: the medium gameplay shot)")


def panel_4():
    f = Frame()
    gy = 560
    gameplay_bg(f, gy)
    f.sprite(mushroom(K, "attack"), 200, gy)
    spore(f, 236, gy - 22, 11, 230)
    f.line([(246, gy - 26), (380, gy - 44), (500, gy - 54), (600, gy - 56)], SPORE, 4, dash=(14, 10))
    for x, y, a in ((330, gy - 38, 90), (430, gy - 50, 140), (520, gy - 55, 190)):
        spore(f, x, y, 9, a)
    f.sprite(rudy("block", K, ghost=0.35), 650, gy)
    f.sprite(rudy("hurt", K), 690, gy, flip=True)
    spore(f, 610, gy - 58, 11)
    burst(f, 616, gy - 58, 30)
    f.arrow([(722, gy - 150), (822, gy - 150)], LINE, 5)
    f.sprite(gear(K * 1.4, ghost=0.85), 790, gy - 196)
    f.line([(728, gy - 196), (756, gy - 210)], LINE, 3)
    f.line([(732, gy - 178), (760, gy - 188)], LINE, 3)
    f.sprite(goblin(K), 1000, gy, flip=True)
    for (x, y) in ((24, 160), (1256, 160), (24, 690), (1256, 690)):
        f.line([(x - 10, y - 18), (x + 8, y - 6), (x - 8, y + 6), (x + 10, y + 18)], LINE, 3)
    hearts(f)
    f.label((40, 440), "mushroom attacks: cap squeezes, spore puffs out", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((836, 398), "knockback", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((836, 330), "sword and shield knocked away", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((470, 586), "spore hits his back: the shield covers only the front", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((46, 118), "hearts stay at 3: the gear took the hit", 16, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((960, 60), "CAMERA SHAKE ON IMPACT", 18, "#FFFFFF", (40, 30, 26, 200), 6)
    f.save(SB_DIR / "04-failure.png", "4  FAILURE · MEDIUM · EYE LEVEL · GAMEPLAY")


def panel_5():
    f = Frame()
    gy = 560
    gameplay_bg(f, gy, gaps=((800, 1030),))
    f.sprite(waystone(K * 1.35, lit=True), 210, gy)
    f.sprite(rudy("respawn", K, mode="flash"), 320, gy)
    f.sprite(rudy("fall", K), 912, gy + 120)
    f.arrow([(970, gy - 150), (970, gy + 130)], LINE, 5)
    q = [((1 - t) ** 2 * 880 + 2 * (1 - t) * t * 640 + t * t * 344, (1 - t) ** 2 * (gy + 40) + 2 * (1 - t) * t * (gy - 560)
          + t * t * (gy - 150)) for t in [i / 30 for i in range(31)]]
    f.arrow(q, LINE, 4, dash=(16, 10))
    f.tpoly([(560, gy - 420), (700, gy - 420), (700, gy - 360), (560, gy - 360)], (20, 20, 24, 200))
    hearts(f)
    f.label((584, gy - 406), "FADE", 22, "#FFFFFF", (0, 0, 0, 0), 0)
    f.label((720, gy - 410), "after a short fade: respawn at the waystone with 3 hearts", 16, "#FFFFFF",
            (40, 30, 26, 190), 6)
    f.label((120, 586), "waystone (lit)", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((260, 618), "flashing: invulnerable", 16, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((1040, 470), "misjudged jump:\nfalls into the cliff", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.save(SB_DIR / "05-recovery.png", "5  RECOVERY · MEDIUM · EYE LEVEL · GAMEPLAY")


def panel_6():
    f = Frame()
    gy = 610
    gameplay_bg(f, gy, horizon=360, castle_x=1060, castle_s=1.25)
    k = K * 0.62
    cx = 900
    for i in range(6):
        w = 120 - i * 14
        f.tpoly([(cx - w, gy - 6), (cx + w, gy - 6), (cx + w * 0.8, 120), (cx - w * 0.8, 120)], (255, 236, 170, 26))
    f.tellipse(cx, gy - 6, 120, 24, (243, 226, 160, 255), LINE, 3)
    f.tellipse(cx, gy - 6, 88, 16, (255, 246, 210, 255), "#C9A94E", 3)
    f.tellipse(cx, gy - 6, 50, 9, (243, 226, 160, 255), "#C9A94E", 2)
    for (x, y, r) in ((860, 470, 5), (930, 420, 4), (890, 360, 6), (950, 300, 4), (870, 250, 3)):
        f.tellipse(x, y, r, r, (255, 250, 220, 230))
    f.sprite(rudy("run_contact", k, ghost=0.4), 640, gy)
    f.arrow([(670, gy - 30), (830, gy - 30)], LINE, 5)
    f.sprite(rudy("celebrate", k), cx, gy - 6)
    f.line([(330, 190), (1010, 190), (1010, 570), (330, 570), (330, 190)], LINE, 3, dash=(14, 10))
    for (x0, y0, x1, y1) in ((330, 190, 230, 120), (1010, 190, 1110, 120), (330, 570, 230, 650), (1010, 570, 1110, 650)):
        f.arrow([(x0, y0), (x1, y1)], LINE, 4, head=14)
    hearts(f)
    f.label((350, 210), "start of the shot: normal gameplay framing", 16, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((440, 650), "CAMERA ZOOMS OUT", 18, "#FFFFFF", (40, 30, 26, 200), 6)
    f.label((900, 60), "then fades to the end card (panel 7)", 18, "#FFFFFF", (40, 30, 26, 200), 6)
    f.label((700, 640), "teleport circle: light rises", 16, "#FFFFFF", (40, 30, 26, 190), 6)
    f.save(SB_DIR / "06-teleport-circle.png", "6  THE END · WIDE · EYE LEVEL · GAMEPLAY → TRANSITION")


def panel_7():
    f = Frame()
    f.gradient(0, 230, "#BCD6E6", "#EEF3F0")
    horizon = 196
    hills = [(x, horizon - 8 * math.sin(x / 120) - 5 * math.sin(x / 47 + 1)) for x in range(0, f.w + 21, 20)]
    f.poly(hills + [(f.w, f.h), (0, f.h)], "#A9BFB2")
    castle(f, 1010, horizon - 8 * math.sin(1010 / 120) - 5 * math.sin(1010 / 47 + 1) + 3, 0.42)
    f.poly([(0, 226), (1280, 214), (1280, 720), (0, 720)], MEADOW)
    for poly in ([(0, 300), (430, 262), (560, 720), (0, 720)], [(640, 232), (1280, 244), (1280, 720), (860, 720)],
                 [(330, 236), (600, 228), (640, 330), (420, 360)]):
        f.poly(poly, WHEAT)
    vp = (1000, 190)
    for x in range(-600, 1900, 60):
        f.line([(x, 720), (vp[0] + (x - vp[0]) * 0.18, 260)], "#C29E45", 2)
    centre = [(250, 730), (330, 610), (520, 480), (700, 380), (850, 292), (960, 222), (1000, 200)]
    widths = [120, 100, 70, 46, 26, 12, 4]
    left, right = [], []
    for i, (x, y) in enumerate(centre):
        x2, y2 = centre[min(i + 1, len(centre) - 1)]
        x1, y1 = centre[max(i - 1, 0)]
        a = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
        left.append((x + math.cos(a) * widths[i] / 2, y + math.sin(a) * widths[i] / 2))
        right.append((x - math.cos(a) * widths[i] / 2, y - math.sin(a) * widths[i] / 2))
    f.poly(left + right[::-1], "#B9A27E", LINE, 2)
    f.tellipse(318, 628, 64, 18, (243, 226, 160, 235), LINE, 3)
    f.tellipse(318, 628, 40, 11, (255, 246, 210, 235), "#C9A94E", 2)
    for (x, y, r) in ((300, 600, 4), (336, 580, 3), (318, 556, 4), (346, 536, 2)):
        f.tellipse(x, y, r, r, (255, 250, 220, 230))
    f.tpoly([(440, 68), (840, 68), (840, 140), (440, 140)], (255, 255, 255, 190))
    f.line([(440, 68), (840, 68), (840, 140), (440, 140), (440, 68)], LINE, 3)
    f.label((497, 89), "LEVEL COMPLETE", 30, "#3A2A24", (255, 255, 255, 0), 0)
    f.label((560, 420), "the road ahead, to the castle", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((390, 650), "the teleport circle Rudy just used", 17, "#FFFFFF", (40, 30, 26, 190), 6)
    f.label((860, 600), "silent card: the music has faded out", 17, "#FFFFFF", (40, 30, 26, 200), 6)
    f.label((860, 632), "Enter: play Level 1 again", 17, "#FFFFFF", (40, 30, 26, 200), 6)
    f.save(SB_DIR / "07-level-complete.png", "7  LEVEL COMPLETE · WIDE · HIGH ANGLE · DESIGN VIEW (end card)")


# ── Character-sheet images ─────────────────────────────────────────────────────

def canvas(w, h, bg="#F4F1EA"):
    img = Image.new("RGBA", (w * SS, h * SS), rgb(bg))
    return img


def place(img, made, x, y_base, flip=False):
    sp, origin = made
    if flip:
        sp, origin = flip_h(sp, origin)
    composite(img, sp, x * SS - origin[0], y_base * SS - origin[1])


def finish(img, w, h, texts, path, tag=True):
    out = img.resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(out, "RGBA")
    for (x, y), text, size, col, bold in texts:
        d.text((x, y), text, font=font(size, bold), fill=rgb(col))
    if tag:
        f = font(15, bold=False)
        bb = d.textbbox((0, 0), TAG, font=f)
        d.text((w - (bb[2] - bb[0]) - 12, h - 26), TAG, font=f, fill=(60, 50, 45, 220))
    out.convert("RGB").save(path)


def turnaround():
    W, H, s = 1800, 900, 2.6
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    base = 760
    xs = {"front": 520, "3q": 880, "side": 1220, "back": 1560}
    for gy_gp, col in ((0, LINE), (90, "#8C7F74"), (150, "#8C7F74"), (160, "#B0A496")):
        y = (base - gy_gp * s) * SS
        for x in range(370 * SS, (W - 60) * SS, 30 * SS):
            d.line([(x, y), (x + 16 * SS, y)], fill=rgb(col), width=2 * SS)
    for v, x in xs.items():
        place(img, rudy_view(v, s), x, base)
    bx = 345
    d.line([(bx * SS, base * SS), (bx * SS, (base - 160 * s) * SS)], fill=rgb(LINE), width=5 * SS)
    for gy_gp in (0, 30, 60, 90, 120, 150, 160):
        y = (base - gy_gp * s) * SS
        d.line([((bx - 14) * SS, y), ((bx + 14) * SS, y)], fill=rgb(LINE), width=3 * SS)
    texts = [((40, 30), "Rudy — turnaround reference (front, three-quarter, side facing right, back)", 30, LINE, True),
             ((40, 74), "Drawn at 2.6× game size. At game size he is 160 px tall to the cowlick tip; the head is 60 px.",
              20, LINE, False)]
    for gy_gp, t in ((160, "160 px · cowlick tip = game height"), (150, "150 · top of head = 2.5 heads"),
                     (90, "90 · chin = 1.5 heads"), (0, "0 · soles")):
        texts.append(((40, base - gy_gp * s - 12), t, 17, LINE, False))
    for v, x in xs.items():
        name = {"front": "FRONT", "3q": "THREE-QUARTER", "side": "SIDE (FACING RIGHT)", "back": "BACK"}[v]
        texts.append(((x - 9 * len(name) // 2 - 10, base + 30), name, 20, LINE, True))
    finish(img, W, H, texts, CH_DIR / "turnaround.png")


POSE_LIST = [
    ("idle", "#2 Idle", "standing still · loop · default"),
    ("run_contact", "#3 Run: contact", "running · loop · default"),
    ("run_passing", "#4 Run: passing", "running · loop · default"),
    ("rise", "#5 Rising", "jump, going up · single"),
    ("fall", "#6 Falling", "coming down; also the stomp · single"),
    ("hurt", "#7 Hurt", "took a hit; gear flies off separately · single"),
    ("defeat", "#8 Defeat", "zero hearts · single"),
    ("respawn", "#9 Respawn", "reappearing at a waystone · single"),
    ("celebrate", "#10 Celebrate", "on the teleport circle · loop"),
    ("sword_idle", "#11 Sword idle", "prop callout · loop · sword form"),
    ("slash", "#12 Slash", "attack · single · sword form"),
    ("block", "#13 Block", "shield up, front only · hold · sword form"),
]


def poses_sheet():
    cols, cw, chh = 4, 430, 470
    W, H = cols * cw, 4 * chh + 120
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    texts = [((30, 26), "Rudy — 13 poses (side view, facing right; facing left is a runtime flip)", 30, LINE, True),
             ((30, 68), "Drawn at 1.6× game size. Sword-form run, rise and fall reuse poses 3–6 with the props added.",
              19, LINE, False)]
    cells = [("turnaround", "#1 Turnaround", "reference only · see turnaround.png")] + POSE_LIST
    for i, (key, title, sub) in enumerate(cells):
        cx, cy = (i % cols) * cw, 120 + (i // cols) * chh
        d.rounded_rectangle([(cx + 10) * SS, (cy + 10) * SS, (cx + cw - 10) * SS, (cy + chh - 10) * SS],
                            radius=12 * SS, fill=rgb("#FFFFFF"), outline=rgb("#D8D0C4"), width=2 * SS)
        base = cy + 370
        d.line([((cx + 40) * SS, base * SS), ((cx + cw - 40) * SS, base * SS)], fill=rgb("#B9AEA0"), width=2 * SS)
        if key == "turnaround":
            for j, v in enumerate(("front", "3q", "side", "back")):
                place(img, rudy_view(v, 0.95), cx + 70 + j * 96, base)
        else:
            place(img, rudy(key, 1.6), cx + cw / 2 - 10, base)
        texts.append(((cx + 26, cy + 388), title, 21, LINE, True))
        texts.append(((cx + 26, cy + 420), sub, 16, LINE, False))
    legend_y = 120 + 3 * chh + 30
    for j, t in enumerate(["Every pose: 2.5 heads; one cowlick; green eyes; grey robe with the hood down;",
                           "brown belt and boots; dark-brown 4 px outer outline (added in-engine).",
                           "Blockout of shapes only: proportions and poses, not final art."]):
        texts.append(((cw + 30, legend_y + 40 + j * 30), t, 18, LINE, False))
    finish(img, W, H, texts, CH_DIR / "poses.png")


def silhouette_sheet():
    W, H = 1920, 1080
    img = canvas(W, H, "#FFFFFF")
    d = ImageDraw.Draw(img)
    base = 700
    for key, x in (("idle", 780), ("run_contact", 940), ("sword_idle", 1100), ("block", 1260)):
        place(img, rudy(key, 1.0, mode="silhouette"), x, base)
    d.line([(560 * SS, base * SS), (1400 * SS, base * SS)], fill=rgb("#B0B0B0"), width=2 * SS)
    d.line([(660 * SS, base * SS), (660 * SS, (base - 160) * SS)], fill=rgb(LINE), width=3 * SS)
    for y in (base, base - 160):
        d.line([(650 * SS, y * SS), (670 * SS, y * SS)], fill=rgb(LINE), width=3 * SS)
    texts = [((60, 50), "Silhouette test at game size: a 1920×1080 frame, Rudy 160 px tall (+4 px outer outline)", 30,
              LINE, True),
             ((60, 96), "Idle · run (contact) · sword idle · block. At this size it must still read: big round head, "
                        "cowlick, the large hood on his back, robe flaring at the knees, round shield, line of the blade.", 20,
              LINE, False),
             ((560, base - 92), "160 px", 18, LINE, True)]
    finish(img, W, H, texts, CH_DIR / "silhouette.png")


def collision_sheet():
    cols, cw, chh, s = 4, 430, 500, 2.0
    W, H = cols * cw, 3 * chh + 170
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    texts = [((30, 26), "Collision overlay: every pose with the body capsule at the same scale (2× game size)", 30, LINE,
              True),
             ((30, 68), "Red: body capsule 64×136 px. Orange: sword hitbox (slash only). Blue: shield block zone "
                        "(front only). Only the capsule can be hurt.", 19, LINE, False),
             ((30, 98), "Art beyond the capsule (cowlick and top of the hair, about 24 px; the robe flare; the sword and "
                        "shield) never makes Rudy easier to hit. Airborne poses sit in the same frame as idle; during "
                        "defeat and respawn he cannot be hit.", 17, LINE, False)]
    for i, (key, title, sub) in enumerate(POSE_LIST):
        cx, cy = (i % cols) * cw, 150 + (i // cols) * chh
        d.rounded_rectangle([(cx + 10) * SS, (cy + 10) * SS, (cx + cw - 10) * SS, (cy + chh - 10) * SS],
                            radius=12 * SS, fill=rgb("#FFFFFF"), outline=rgb("#D8D0C4"), width=2 * SS)
        base, mx = cy + 420, cx + cw / 2 - 10
        d.line([((cx + 40) * SS, base * SS), ((cx + cw - 40) * SS, base * SS)], fill=rgb("#B9AEA0"), width=2 * SS)
        place(img, rudy(key, s, air=False), mx, base)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        r = 32 * s
        box = [(mx - r) * SS, (base - 136 * s) * SS, (mx + r) * SS, base * SS]
        ld.rounded_rectangle(box, radius=r * SS, fill=(220, 50, 50, 55), outline=(200, 30, 30, 255), width=3 * SS)
        if key == "slash":
            ld.rectangle([(mx + 22 * s) * SS, (base - 112 * s) * SS, (mx + 78 * s) * SS, (base - 40 * s) * SS],
                         fill=(240, 150, 40, 60), outline=(220, 120, 20, 255), width=3 * SS)
        if key == "block":
            ld.rectangle([(mx + 30 * s) * SS, (base - 120 * s) * SS, (mx + 44 * s) * SS, (base - 30 * s) * SS],
                         fill=(60, 120, 220, 70), outline=(40, 90, 200, 255), width=3 * SS)
        img.alpha_composite(layer)
        d = ImageDraw.Draw(img)
        texts.append(((cx + 26, cy + 436), title, 21, LINE, True))
    finish(img, W, H, texts, CH_DIR / "collision.png")


def palette_sheet():
    W, H = 1600, 980
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    rudy_cols = [("hair", HAIR), ("eyes", EYES), ("robe", ROBE), ("skin", SKIN), ("belt, boots", BOOTS),
                 ("outline", LINE)]
    env_cols = [("wheat", WHEAT), ("meadow", MEADOW), ("sky", SKY), ("castle", CASTLE), ("path", PATH)]
    texts = [((30, 26), "Palette check: Rudy at game size against the planned Level 1 colors", 30, LINE, True)]
    for row, (cols, y, title) in enumerate(((rudy_cols, 110, "Rudy"), (env_cols, 230, "Level 1 (planned)"))):
        texts.append(((30, y + 30), title, 20, LINE, True))
        for i, (name, c) in enumerate(cols):
            x = 230 + i * 200
            d.rounded_rectangle([x * SS, y * SS, (x + 170) * SS, (y + 70) * SS], radius=8 * SS, fill=rgb(c),
                                outline=rgb(LINE), width=2 * SS)
            texts.append(((x, y + 76), f"{name} {c}", 16, LINE, False))
    tiles = [("wheat", WHEAT), ("meadow", MEADOW), ("sky", SKY), ("path", PATH)]
    for row, gray in enumerate((False, True)):
        for i, (name, c) in enumerate(tiles):
            x, y = 40 + i * 390, 380 + row * 290
            tile = Image.new("RGBA", (360 * SS, 260 * SS), rgb(c))
            place(tile, rudy("idle", 1.0), 180, 220)
            if gray:
                tile = ImageOps.grayscale(tile.convert("RGB")).convert("RGBA")
            composite(img, tile, x * SS, y * SS)
            texts.append(((x, y - 28), f"{name}{' (grayscale)' if gray else ''}", 18, LINE, True))
    texts.append(((40, H - 50), "The fills alone barely separate from the background (hair against wheat 1.42, "
                                "against meadow 1.03); the 4 px dark outer outline is what keeps Rudy readable.", 18,
                  LINE, False))
    finish(img, W, H, texts, CH_DIR / "palette.png")


def main():
    SB_DIR.mkdir(parents=True, exist_ok=True)
    CH_DIR.mkdir(parents=True, exist_ok=True)
    for fn in (panel_1, panel_2, panel_3, panel_4, panel_5, panel_6, panel_7, turnaround, poses_sheet, silhouette_sheet,
               collision_sheet, palette_sheet):
        fn()
        print("drew", fn.__name__)


if __name__ == "__main__":
    main()
