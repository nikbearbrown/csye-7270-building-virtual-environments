"""Phase 2a: every still beat as a 3840x2160 PNG in media/ (the compiler holds each one for its narration).

Written by Claude Code for the Assignment 8 pitch film. Four kinds of picture, each labelled on screen:
  - constructed drawings (simple line pictures drawn here with Pillow) for everything not built yet:
    "Constructed - proposed, not built";
  - the author's Gemini concept art, shown in framed boxes: "Generated (Gemini 4) · concept art, not in the game".
    The files in art/ are read, never changed; in the film their flat green background is keyed to the dark frame;
  - the title card and dialogue scenes that use them: "Constructed";
  - evidence from Assignment 7 read at its revision with `git show 840b501:...` (a figure drawn from the logs, the
    committed test logs) and one real captured frame of the cave (capture/run-01, 840b501).
No footage, screenshot, logo or likeness of any other game is drawn; the comparable games are named in text only.
"""
import io
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from common import (REEL, ART_DIR, W, H, TITLE, AUTHOR, PAGE, CARD, BORDER, INK, INK_SOFT, FIRE, FIRE_SOFT, CAVE,
                    CAVE_SOFT, CAVE_DARK, REV_A7, REV_A5, REV_A6, A7_GAME, L_REAL, L_CONSTRUCTED_PROPOSED, L_GENERATED,
                    L_CONSTRUCTED, CAP_840, font_path, git_show, sha256, save_json, frame_rows)

_fonts = {}


def F(name, size):
    k = (name, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(str(font_path(name)), size)
    return _fonts[k]


def rgb(hexstr, a=255):
    h = hexstr.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


# ---------------------------------------------------------------- labels and page furniture
CHIP = {'real': INK, 'generated': CAVE, 'constructed': FIRE, 'figure': INK_SOFT}


def chip(text, kind, size=46):
    f = F('sans_med', size)
    tw = int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(text, font=f))
    h = int(size * 1.9)
    im = Image.new('RGBA', (tw + 2 * int(size * 0.75), h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, h - 1], radius=h // 2, fill=rgb(CHIP[kind]))
    d.text((int(size * 0.75), int(size * 0.36)), text, font=f, fill=rgb(PAGE))
    return im


def page(heading, chips=(), bg=PAGE):
    """A page with the beat heading top left and its label chips top right (stacked right to left)."""
    im = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(im)
    d.text((160, 96), heading, font=F('serif', 92), fill=INK if bg == PAGE else PAGE)
    x = W - 160
    for text, kind in chips:
        c = chip(text, kind)
        x -= c.width
        im.paste(c, (x, 110), c)
        x -= 30
    return im, d


def text_center(d, xy, text, font, fill, anchor='mm'):
    d.text(xy, text, font=font, fill=fill, anchor=anchor)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, font, fill, width, gap=1.3):
    x, y = xy
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += int(font.size * gap)
    return y


# ---------------------------------------------------------------- the author's concept art
def keyed(name, box=None):
    """An art/ image with its flat green background made transparent (display only; the file is not changed)."""
    im = Image.open(ART_DIR / name).convert('RGB')
    if box:
        im = im.crop(box)
    a = np.asarray(im).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    green = g - np.maximum(r, b)
    alpha = np.clip(1.0 - (green - 40) / 90.0, 0.0, 1.0)
    spill = green > 0
    g2 = np.where(spill, np.minimum(g, np.maximum(r, b) + 10), g)
    out = np.dstack([r, g2, b, (alpha * 255)]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


# crops of the art (pixel boxes in the original files)
CROP = {
    'curious': ('witch_expressions.png', (40, 0, 1000, 960)),
    'determined': ('witch_expressions.png', (1010, 0, 1970, 960)),
    'victory': ('witch_expressions.png', (40, 1010, 1000, 1970)),
    'sad': ('witch_expressions.png', (1010, 1010, 1970, 1970)),
    'snarl': ('wolf_snarl.png', (170, 560, 1010, 1400)),
    'calm': ('wolf_calm.png', (130, 250, 970, 1090)),
}


def portrait_box(im, key, xy, size, mirror=False):
    """A framed portrait box: dark cave panel, the keyed portrait, a fire-coloured inner rule."""
    name, box = CROP[key]
    p = keyed(name, box).resize((size - 40, size - 40), Image.LANCZOS)
    if mirror:
        p = p.transpose(Image.FLIP_LEFT_RIGHT)
    x, y = xy
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + size, y + size], radius=36, fill=CAVE_DARK, outline=FIRE_SOFT, width=10)
    im.paste(p, (x + 20, y + 20), p)
    d.rounded_rectangle([x, y, x + size, y + size], radius=36, outline=FIRE_SOFT, width=10)


def dialogue_box(im, xy, wh, name, line):
    x, y = xy
    w, h = wh
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + w, y + h], radius=40, fill=(24, 31, 42), outline=CAVE_SOFT, width=6)
    f = F('sans_med', 56)
    tw = d.textlength(name, font=f)
    d.rounded_rectangle([x + 60, y - 50, x + 60 + tw + 90, y + 50], radius=50, fill=FIRE)
    d.text((x + 105, y - 33), name, font=f, fill=PAGE)
    para(d, (x + 80, y + 110), '“' + line + '”', F('serif', 92), PAGE, w - 160, 1.25)


def dark_page(heading, chips):
    im, d = page(heading, chips, bg=CAVE_DARK)
    return im, d


def scene(bid, heading, rows):
    """A constructed dialogue scene: one row per line, the speaker's portrait framed beside a dialogue box."""
    im, d = dark_page(heading, [(L_CONSTRUCTED + ' · dialogue scene, proposed', 'constructed')])
    n = len(rows)
    size = 760 if n == 2 else 1080
    top = 330 if n == 2 else 460
    gap = 90
    for i, (key, name, line, left) in enumerate(rows):
        y = top + i * (size + gap)
        if left:
            portrait_box(im, key, (200, y), size)
            dialogue_box(im, (200 + size + 80, y + size - 560), (W - 200 - (200 + size + 80), 520), name, line)
        else:
            portrait_box(im, key, (W - 200 - size, y), size)
            dialogue_box(im, (200, y + size - 560), (W - 200 - size - 80 - 200, 520), name, line)
    g = chip(L_GENERATED + ' (portraits)', 'generated', 42)
    im.paste(g, (200, H - g.height - 60), g)
    return im


# ---------------------------------------------------------------- simple drawn figures (constructed)
def witch(d, x, y, s=1.0, flame=True):
    """A stick-simple witch: hat, head, cloak, staff with a flame. (x, y) = feet."""
    k = lambda v: int(v * s)
    d.polygon([(x - k(70), y), (x + k(70), y), (x + k(40), y - k(170)), (x - k(40), y - k(170))], fill=CAVE)
    d.ellipse([x - k(38), y - k(250), x + k(38), y - k(174)], fill=PAGE, outline=INK, width=max(3, k(6)))
    d.polygon([(x - k(80), y - k(225)), (x + k(80), y - k(225)), (x + k(10), y - k(380))], fill=INK)
    d.line([(x + k(80), y), (x + k(110), y - k(260))], fill=INK, width=max(4, k(12)))
    if flame:
        fl(d, x + k(112), y - k(270), s * 0.8)


def fl(d, x, y, s=1.0, col=FIRE):
    k = lambda v: int(v * s)
    d.polygon([(x, y - k(70)), (x + k(30), y - k(15)), (x + k(22), y + k(15)), (x, y + k(25)),
               (x - k(22), y + k(15)), (x - k(30), y - k(15))], fill=col)
    d.ellipse([x - k(12), y - k(5), x + k(12), y + k(19)], fill=FIRE_SOFT)


def wolf(d, x, y, s=1.0, col=INK_SOFT):
    """A simple wolf silhouette facing left. (x, y) = feet line, x = nose."""
    k = lambda v: int(v * s)
    pts = [(x, y - k(120)), (x + k(60), y - k(150)), (x + k(80), y - k(200)), (x + k(110), y - k(160)),
           (x + k(320), y - k(150)), (x + k(420), y - k(190)), (x + k(390), y - k(130)), (x + k(360), y - k(100)),
           (x + k(350), y), (x + k(310), y), (x + k(300), y - k(70)), (x + k(150), y - k(70)), (x + k(140), y),
           (x + k(100), y), (x + k(95), y - k(90)), (x + k(30), y - k(95))]
    d.polygon(pts, fill=col)


def arrow(d, a, b, col=INK, width=14, head=40):
    import math
    d.line([a, b], fill=col, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45))
    p2 = (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))
    d.polygon([b, p1, p2], fill=col)


def panel(d, box, title=None, fill=CARD):
    d.rounded_rectangle(box, radius=40, fill=fill, outline=BORDER, width=6)
    if title:
        d.text(((box[0] + box[2]) // 2, box[1] + 90), title, font=F('serif_med', 84), fill=INK, anchor='mm')


def constructed_page(heading):
    return page(heading, [(L_CONSTRUCTED_PROPOSED, 'constructed')])


def b02():
    im, d = constructed_page('Why anyone would care')
    y0, y1 = 330, 1500
    boxes = [(160, y0, 1260, y1), (1370, y0, 2470, y1), (2580, y0, 3680, y1)]
    titles = ['HD-2D look', 'Side-scrolling shooting', 'Mouse-aimed fireball']
    for b, t in zip(boxes, titles):
        panel(d, b, t)
    # 1: a flat sprite standing in a lit 3D box
    x0, yb = 260, 1380
    d.polygon([(x0, yb), (x0 + 900, yb), (x0 + 760, yb - 260), (x0 + 140, yb - 260)], fill=CAVE_SOFT)
    d.polygon([(x0 + 140, yb - 260), (x0 + 760, yb - 260), (x0 + 760, yb - 860), (x0 + 140, yb - 860)], fill=CAVE)
    d.polygon([(x0, yb), (x0 + 140, yb - 260), (x0 + 140, yb - 860), (x0, yb - 1000)], fill='#6C86A3')
    d.polygon([(x0 + 900, yb), (x0 + 760, yb - 260), (x0 + 760, yb - 860), (x0 + 900, yb - 1000)], fill='#6C86A3')
    d.polygon([(x0 + 560, yb - 860), (x0 + 640, yb - 860), (x0 + 520, yb - 150), (x0 + 330, yb - 150)], fill=FIRE_SOFT)
    witch(d, x0 + 430, yb - 120, 0.9)
    # 2: a scrolling corridor with shots
    x0 = 1470
    d.rectangle([x0, 1280, x0 + 900, 1300], fill=INK)
    witch(d, x0 + 160, 1280, 0.8, flame=False)
    for i in range(3):
        fl(d, x0 + 360 + i * 140, 1100, 0.6)
    wolf(d, x0 + 640, 1280, 0.62)
    arrow(d, (x0 + 120, 560), (x0 + 780, 560), INK_SOFT)
    d.text((x0 + 450, 640), 'the screen scrolls', font=F('sans', 50), fill=INK_SOFT, anchor='mm')
    # 3: aim with the mouse
    x0 = 2680
    witch(d, x0 + 160, 1380, 0.8, flame=False)
    cx, cy = x0 + 760, 720
    d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline=INK, width=10)
    d.line([cx - 110, cy, cx + 110, cy], fill=INK, width=8)
    d.line([cx, cy - 110, cx, cy + 110], fill=INK, width=8)
    for t in range(6):
        px = x0 + 270 + t * 75
        py = 1090 - t * 62
        fl(d, px, py, 0.35 + t * 0.06)
    d.text((cx, cy + 180), 'aim anywhere', font=F('sans', 50), fill=INK_SOFT, anchor='mm')
    # the comparison, in text only
    d.text((160, 1590), 'Named in text only (no footage, art or logos):', font=F('sans_med', 52), fill=INK)
    rows = ['Octopath Traveler: the HD-2D look, but turn-based',
            'Metal Slug: side-scrolling shooting, fixed-direction shots',
            'Hollow Knight: a large cave to explore, with progression']
    for i, r in enumerate(rows):
        d.text((160, 1680 + i * 90), '· ' + r, font=F('sans', 54), fill=INK_SOFT)
    d.text((W - 160, 1770), 'This: a short action run, a few minutes, no levelling', font=F('serif_med', 70),
           fill=FIRE, anchor='rm')
    return im


def b03():
    im, d = constructed_page('The look (planned)')
    # a cave cross-section seen by a tilted camera
    L, T, R, B = 360, 340, 3480, 1700
    d.rounded_rectangle([L, T, R, B], radius=60, fill=CAVE_DARK)
    # blurred near and far bands (tilt-shift)
    band = Image.new('RGBA', (R - L, 230), rgb(CAVE, 170))
    im.paste(band, (L, T), band)
    im.paste(band, (L, B - 230), band)
    d.text((L + 60, T + 70), 'blurred', font=F('sans', 54), fill=CAVE_SOFT)
    d.text((L + 60, B - 160), 'blurred', font=F('sans', 54), fill=CAVE_SOFT)
    # light shafts from cracks
    for cx in (1300, 2500):
        shaft = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shaft)
        sd.polygon([(cx - 40, T + 230), (cx + 40, T + 230), (cx + 260, B - 230), (cx - 120, B - 230)], fill=rgb(CAVE_SOFT, 90))
        im.paste(shaft, (0, 0), shaft)
        d.line([(cx - 60, T + 230), (cx, T + 200), (cx + 50, T + 235)], fill=PAGE, width=10)
    d = ImageDraw.Draw(im)
    ground = B - 330
    d.rectangle([L, ground, R, ground + 18], fill=CAVE_SOFT)
    witch(d, 1000, ground, 1.0)
    wolf(d, 2750, ground, 0.9, col=CAVE_SOFT)
    # the fireball as a moving light: warm glow on the wall around it
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([1600, 700, 2300, 1400], fill=rgb(FIRE, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    im.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(im)
    fl(d, 1950, 1060, 1.3)
    arrow(d, (1500, 1080), (1830, 1065), FIRE_SOFT, 10, 34)
    notes = [('tilt-shift depth of field', 160, 1790), ('cold blue cave; only fire is warm', 1180, 1790),
             ('light shafts through fog', 2380, 1790)]
    for t, x, y in notes:
        d.text((x, y), t, font=F('sans_med', 56), fill=INK)
    d.text((160, 1890), 'the fireball as a moving light  ·  hit-stop, flash and sparks  ·  a boss title card  ·  '
           'dust, drips, moss, crystals', font=F('sans', 52), fill=INK_SOFT)
    d.text((160, 1985), 'Godot renderer features only; visual only — my behaviour pin will still pass after each one',
           font=F('sans', 52), fill=INK_SOFT)
    return im


def b07():
    im, d = constructed_page('Who opens it, and the first sixty seconds')
    d.text((160, 280), 'Target role: gameplay programmer   ·   Reader: a hiring manager or lead gameplay programmer',
           font=F('sans_med', 60), fill=INK)
    y0, y1 = 500, 1500
    xs = [160, 1080, 2000, 2920]
    w = 760
    steps = ['download the zip', 'unzip, double-click the .exe', 'title screen shows the controls',
             'playing; one key skips the opening line']
    for i, (x, s) in enumerate(zip(xs, steps)):
        panel(d, (x, y0, x + w, y1))
        cx = x + w // 2
        if i == 0:
            d.rounded_rectangle([cx - 200, 760, cx + 200, 1160], radius=30, fill=CAVE_SOFT, outline=INK, width=10)
            d.line([cx, 760, cx, 1160], fill=INK, width=12)
            for j in range(5):
                d.rectangle([cx - 24, 790 + j * 70, cx + 24, 820 + j * 70], fill=INK)
        elif i == 1:
            d.rounded_rectangle([cx - 230, 760, cx + 230, 1160], radius=20, fill=CARD, outline=INK, width=10)
            d.text((cx, 960), '.exe', font=F('mono', 130), fill=INK, anchor='mm')
            arrow(d, (cx + 120, 1260), (cx + 20, 1150), FIRE, 12, 40)
        elif i == 2:
            d.rectangle([cx - 300, 720, cx + 300, 1120], fill=CAVE_DARK)
            d.text((cx, 840), TITLE, font=F('serif', 56), fill=PAGE, anchor='mm')
            for j, c in enumerate(['A / D  move', 'Space  jump', 'mouse  aim & cast']):
                d.text((cx, 940 + j * 56), c, font=F('mono', 40), fill=CAVE_SOFT, anchor='mm')
            d.rectangle([cx - 30, 1120, cx + 30, 1200], fill=INK)
            d.rectangle([cx - 140, 1200, cx + 140, 1220], fill=INK)
        else:
            d.rectangle([cx - 300, 720, cx + 300, 1120], fill=CAVE_DARK)
            witch(ImageDraw.Draw(im), cx - 150, 1080, 0.55)
            wolf(d, cx + 60, 1080, 0.45, col=CAVE_SOFT)
            d.rectangle([cx - 30, 1120, cx + 30, 1200], fill=INK)
            d.rectangle([cx - 140, 1200, cx + 140, 1220], fill=INK)
        lines = wrap(d, s, F('sans_med', 56), w - 100)
        for j, line in enumerate(lines):
            d.text((cx, 1300 + j * 70), line, font=F('sans_med', 56), fill=INK, anchor='mm')
        if i < 3:
            arrow(d, (x + w + 20, 1000), (xs[i + 1] - 20, 1000), INK_SOFT, 12, 36)
    d.line([160, 1640, 3680, 1640], fill=FIRE, width=12)
    d.line([160, 1610, 160, 1670], fill=FIRE, width=12)
    d.line([3680, 1610, 3680, 1670], fill=FIRE, width=12)
    d.text((W // 2, 1740), 'under a minute, without reading anything else', font=F('serif_med', 80), fill=FIRE,
           anchor='mm')
    return im


def b10():
    im, d = constructed_page('In, out, first')
    cols = [(160, 'In'), (1370, 'Out (deliberately)'), (2580, 'First')]
    for x, t in cols:
        panel(d, (x, 300, x + 1100, 2000), t)
    ins = ['one cave level, title to end screen', "the mage's run, jump, aimed fireball", 'a heal spell',
           'wolves and the great-wolf boss', 'spikes and a rolling boulder', 'a chest and a campfire rest point',
           'four story moments with portraits', 'a Windows build']
    for i, s in enumerate(ins):
        d.text((240, 470 + i * 150), '· ' + s, font=F('sans', 58), fill=INK)
    d.text((1370 + 550, 900), 'no multiplayer', font=F('serif_med', 110), fill=INK, anchor='mm')
    for k in range(4):
        cx = 1600 + k * 210
        d.ellipse([cx - 60, 1150, cx + 60, 1270], outline=INK_SOFT, width=10)
        d.line([cx - 90, 1400, cx - 60, 1290, cx + 60, 1290, cx + 90, 1400], fill=INK_SOFT, width=10)
    d.line([1500, 1120, 2240, 1460], fill=FIRE, width=18)
    # first: one 3D room with the core loop
    x0 = 2660
    d.polygon([(x0 + 40, 1250), (x0 + 900, 1250), (x0 + 780, 1080), (x0 + 160, 1080)], fill=CAVE_SOFT)
    d.rectangle([x0 + 160, 560, x0 + 780, 1080], fill=CAVE)
    witch(d, x0 + 330, 1180, 0.6)
    wolf(d, x0 + 560, 1180, 0.5, col=CAVE_DARK)
    d.text((x0 + 470, 1340), 'the core loop in one 3D cave room', font=F('sans_med', 50), fill=INK, anchor='mm')
    d.text((x0 + 470, 1410), 'run · jump · cast at a wolf · HD-2D framing', font=F('sans', 46), fill=INK_SOFT, anchor='mm')
    d.text((x0 + 70, 1530), 'How anyone would know it ran:', font=F('sans_med', 52), fill=FIRE)
    para(d, (x0 + 70, 1610), 'my existing behaviour pin passes against that room, and a windowed capture of it is '
         'labelled with its revision', F('sans', 50), INK, 960, 1.3)
    return im


def b11():
    im, d = constructed_page('The risk: 2D into 3D, and the pin as its test')
    para(d, (160, 290), 'Moving the 2D game into a 3D scene could break the movement, collision and state machines '
         'that already work.', F('serif', 76), INK, 3500, 1.2)
    panel(d, (160, 620, 1700, 1560), 'A: keep the 2D gameplay layer')
    panel(d, (2140, 620, 3680, 1560), 'B: 3D bodies held to a plane')
    # A: flat layer in front of a 3D backdrop
    d.rectangle([430, 830, 1430, 1290], fill=CAVE)
    d.rectangle([330, 930, 1330, 1390], outline=INK, width=10)
    witch(d, 620, 1360, 0.6)
    wolf(d, 900, 1360, 0.5)
    d.text((930, 1480), 'the 3D cave renders behind it', font=F('sans', 50), fill=INK_SOFT, anchor='mm')
    # B: bodies on a plane in a 3D room
    x0 = 2300
    d.polygon([(x0, 1380), (x0 + 1220, 1380), (x0 + 1060, 1180), (x0 + 160, 1180)], fill=CAVE_SOFT)
    d.rectangle([x0 + 160, 800, x0 + 1060, 1180], fill=CAVE)
    d.line([(x0 + 80, 1290), (x0 + 1140, 1290)], fill=FIRE, width=8)
    witch(d, x0 + 400, 1290, 0.6)
    wolf(d, x0 + 680, 1290, 0.5, col=CAVE_DARK)
    d.text((x0 + 610, 1480), 'the characters move on one plane', font=F('sans', 50), fill=INK_SOFT, anchor='mm')
    # the test
    arrow(d, (930, 1580), (1700, 1760), INK_SOFT)
    arrow(d, (2910, 1580), (2140, 1760), INK_SOFT)
    d.rounded_rectangle([1700, 1700, 2140, 1900], radius=30, fill=INK)
    d.text((1920, 1800), 'one-room spike', font=F('sans_med', 52), fill=PAGE, anchor='mm')
    d.text((W // 2, 2000), 'The test: does my Assignment 7 pin still pass there?  If not, the 2D layer stays and the '
           '3D becomes the backdrop.', font=F('sans_med', 54), fill=FIRE, anchor='mm')
    return im


def b12():
    im, d = constructed_page('Why this project: half new, half existing')
    panel(d, (160, 320, 1800, 1980), 'New to me')
    panel(d, (2040, 320, 3680, 1980), 'Already have, with evidence')
    # new: a flat sprite card standing in a lit 3D cave
    x0 = 300
    d.polygon([(x0, 1500), (x0 + 1360, 1500), (x0 + 1160, 1240), (x0 + 200, 1240)], fill=CAVE_SOFT)
    d.rectangle([x0 + 200, 560, x0 + 1160, 1240], fill=CAVE)
    d.polygon([(x0 + 820, 560), (x0 + 900, 560), (x0 + 760, 1300), (x0 + 560, 1300)], fill=FIRE_SOFT)
    d.polygon([(x0 + 500, 1420), (x0 + 760, 1420), (x0 + 780, 980), (x0 + 520, 980)], fill=CARD, outline=INK)
    witch(d, x0 + 640, 1400, 0.85)
    # 2026-11-22: wording from the corrected PROJECT-BRIEF.md question 7 (770a2aaf)
    for i, s in enumerate(['a whole 3D cave level, its lighting and camera',
                           '2D sprites that run and fight in it (A3: one static billboard)']):
        d.text((300, 1640 + i * 100), '· ' + s, font=F('sans_med', 48), fill=INK)
    rows = [('Shaders and materials', 'Assignment 5', REV_A5), ('Particles, GPU time measured', 'Assignment 6', REV_A6),
            ('Animation, state machines, pins, edge tests, mutations', 'Assignment 7', REV_A7)]
    for i, (s, a, r) in enumerate(rows):
        y = 540 + i * 230
        d.text((2140, y), s, font=F('sans_med', 58), fill=INK)
        d.text((2140, y + 85), f'{a} · {r}', font=F('mono', 50), fill=INK_SOFT)
    d.text((2140, 1320), 'Real footage of each follows, labelled with', font=F('sans', 56), fill=INK_SOFT)
    d.text((2140, 1400), 'the revision it was captured at.', font=F('sans', 56), fill=INK_SOFT)
    return im


# ---------------------------------------------------------------- title, evidence, exists/will, outro
def b01():
    rows = frame_rows('run-01')
    n = 15
    assert rows[n]['seg'] == 'run' and rows[n]['ps'] == 'IDLE', 'title backdrop: frame 15 should be the idle mage'
    g = Image.open(CAP_840 / f'frame{n:08d}.png').convert('RGB').resize((W, H), Image.NEAREST)
    shade = Image.new('RGB', (W, H), CAVE_DARK)
    im = Image.blend(g, shade, 0.45)
    d = ImageDraw.Draw(im)
    # framed portrait on the right
    p = keyed('witch_fullbody_talk.png')
    ph = 1600
    p = p.resize((int(p.width * ph / p.height), ph), Image.LANCZOS)
    bx, by = 2330, 200
    bw, bh = p.width + 80, ph + 80
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=48, fill=CAVE_DARK, outline=FIRE_SOFT, width=12)
    im.paste(p, (bx + 40, by + 40), p)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=48, outline=FIRE_SOFT, width=12)
    g1 = chip(L_GENERATED, 'generated', 40)
    im.paste(g1, (bx + bw - g1.width - 30, by + bh - g1.height - 30), g1)
    d.text((200, 640), TITLE, font=F('serif_med', 190), fill=PAGE)
    d.text((210, 900), 'An HD-2D cave adventure shooter', font=F('serif', 100), fill=FIRE_SOFT)
    d.text((210, 1060), 'Final project pitch  ·  ' + AUTHOR, font=F('sans', 64), fill=CAVE_SOFT)
    d.text((210, 1160), 'Proposed: a playable Windows build of one vertical slice', font=F('sans', 60), fill=CAVE_SOFT)
    c = chip(L_CONSTRUCTED + ' · title card', 'constructed')
    im.paste(c, (220, 150), c)
    b = chip(f'Background: {L_REAL} · frame {n}', 'real', 40)
    im.paste(b, (220, H - b.height - 140), b)
    return im


def scenes():
    return {
        'B04': scene('B04', 'Story moment 1 of 4: the opening', [
            ('curious', 'The witch', 'The fire in my staff is the only warm thing down here. Let’s see where this cave goes.', True)]),
        'B05': scene('B05', 'Story moment: before the boss', [
            ('snarl', 'The great wolf', 'Turn back, little flame. This cave is mine.', True),
            ('determined', 'The witch', 'Then I’ll light my own way.', False)]),
        'B06': b06(),
    }


def b06():
    return scene('B06', 'Story moment: after the boss', [
        ('calm', 'The great wolf', 'Your fire burns brighter than I thought. Go on.', True),
        ('victory', 'The witch', 'We did it!', False)])


def b06_extras(im):
    """Also planned: the campfire line and the sad portrait for a defeat."""
    d = ImageDraw.Draw(im)
    s = 180
    x, y = 1150, 1190
    portrait_box(im, 'sad', (x, y), s)
    d.text((x + s + 40, y + 30), 'Also planned: a line at the campfire after the first fight,', font=F('sans', 48),
           fill=CAVE_SOFT)
    d.text((x + s + 40, y + 100), 'and this sad portrait for a defeat.', font=F('sans', 48), fill=CAVE_SOFT)
    return im


def test_table():
    """(suite, rates, checks) from the committed test logs at 840b501 (the 38 runs: 35 test suites and 3 probe runs)."""
    names = git_show(f'{REV_A7}:fall-2026/zhefan-z/assignment-7/logs/').decode()   # tree listing
    logs = [l.strip() for l in names.splitlines() if l.strip().endswith('.log') and
            (l.startswith('test_') or l.startswith('probe_two_clocks'))]
    out = {}
    for name in logs:
        text = git_show(f'{REV_A7}:fall-2026/zhefan-z/assignment-7/logs/{name}').decode('utf-8', 'replace')
        last = [l for l in text.splitlines() if 'checks /' in l or 'failures' in l]
        suite, fps = name[:-4].rsplit('_', 1)
        out.setdefault(suite, []).append((int(fps.replace('fps', '')), last[-1].strip() if last else '?'))
    return out


def b09():
    im, d = page('What it proves: pinned before the change, tested after',
                 [(f'Figure from the logs · Assignment 7 · {REV_A7}', 'figure')])
    fig = Image.open(io.BytesIO(git_show(f'{REV_A7}:fall-2026/zhefan-z/assignment-7/captures/figures/pin_timeline.png')))
    fig = fig.convert('RGB')
    fw = 2260
    fig = fig.resize((fw, int(fig.height * fw / fig.width)), Image.LANCZOS)
    im.paste(fig, (160, 330))
    y = para(d, (160, 330 + fig.height + 30), 'captures/figures/pin_timeline.png at 840b501: the pin, every physics '
             'tick, before (a9b4bc1) and after (ff71bbb) the growl cancel. Only hit_growl and kill changed.',
             F('sans', 44), INK_SOFT, fw, 1.3)
    para(d, (160, y + 80), 'Measured cost (Assignment 6, RTX 5060 Laptop GPU): impact and trail particles about 0.02 '
         'and 0.10 ms of GPU time. Planned: frame time for the slice, measured on the same GPU.', F('sans', 52), INK,
         fw, 1.3)
    tab = test_table()
    runs = sum(len(v) for v in tab.values())
    fails = [s for s, v in tab.items() for _, line in v if '/ 0 failures' not in line]
    assert runs == 38 and not fails, f'expected 38 passing runs in logs/ at 840b501, got {runs}, failing {fails}'
    x0 = 2560
    d.text((x0, 330), f'{runs} headless runs, 0 failures', font=F('serif_med', 76), fill=INK)
    d.text((x0, 430), f'committed test logs, logs/ at {REV_A7}', font=F('sans', 44), fill=INK_SOFT)
    three = sorted([s for s, v in tab.items() if len(v) == 3])
    one = sorted([s for s, v in tab.items() if len(v) == 1])
    y = 530
    d.text((x0, y), 'at 30, 60 and 144 fps:', font=F('sans_med', 48), fill=FIRE)
    y += 70
    for s in three:
        n = tab[s][0][1].split(':')[-1].split('/')[0].replace('checks', '').strip()
        d.text((x0, y), f'{s.replace("test_", "")}', font=F('mono', 40), fill=INK)
        d.text((W - 160, y), f'{n} checks ×3', font=F('mono', 40), fill=INK_SOFT, anchor='ra')
        y += 54
    y += 24
    d.text((x0, y), 'at 60 fps:', font=F('sans_med', 48), fill=FIRE)
    y += 70
    for s in one:
        n = tab[s][0][1].split(':')[-1].split('/')[0].replace('checks', '').strip()
        d.text((x0, y), f'{s.replace("test_", "")}', font=F('mono', 40), fill=INK)
        d.text((W - 160, y), f'{n} checks', font=F('mono', 40), fill=INK_SOFT, anchor='ra')
        y += 54
    assert y < H - 60, f'test table overflows ({y})'
    return im, {'runs': runs, 'suites_three_rates': three, 'suites_60': one}


def b16():
    im, d = page('Exists today, and what will exist', [('Will exist: ' + L_CONSTRUCTED_PROPOSED.split(' - ')[1], 'constructed'),
                                                       ('Exists: in git at the revision shown', 'real')])
    panel(d, (160, 300, 2260, 2000), 'Exists today')
    panel(d, (2400, 300, 3680, 2000), 'Will exist')
    rows = [('The 2D game: mage, wolf, pit, exit', REV_A7), ('Run cycle and the lunge rig', REV_A7),
            ('Impact and trail particles (≈0.02 / 0.10 ms GPU)', REV_A6), ('Hurt-tint shader, frosted-rock material', REV_A5),
            ('3D props: rock, crystal, chest (own scene)', 'Assignment 3'), ('Cave lights, embers, afterimage', REV_A7),
            ('38 headless runs at 30/60/144 fps, passing', REV_A7), ('Concept portraits, not in the game', 'pitch/art/')]
    for i, (s, r) in enumerate(rows):
        y = 470 + i * 180
        d.text((240, y), s, font=F('sans', 56), fill=INK)
        d.text((2180, y + 5), r, font=F('mono', 52), fill=INK_SOFT, anchor='ra')
    will = ['the 3D cave level and its camera', 'sprites placed in 3D', 'the HD-2D look', 'four story moments in the game',
            'the heal spell', 'the great-wolf boss', 'spikes and a rolling boulder', 'the chest and campfire rest point',
            'title and end screens', 'the Windows export', 'a test report for the slice']
    for i, s in enumerate(will):
        d.text((2480, 470 + i * 135), '· ' + s, font=F('sans', 56), fill=INK)
    return im


def b17():
    """Silent outro: the title and the author's name only (no channel handle, persona or credit line)."""
    im = Image.new('RGB', (W, H), CAVE_DARK)
    d = ImageDraw.Draw(im)
    fl(d, W // 2, 560, 4.0)
    d.text((W // 2, 1060), TITLE, font=F('serif_med', 290), fill=PAGE, anchor='mm')
    d.text((W // 2, 1380), AUTHOR + '  ·  final project pitch', font=F('sans', 96), fill=CAVE_SOFT, anchor='mm')
    d.line([420, 1700, W - 420, 1700], fill=FIRE, width=14)
    return im


def fit_safe(im):
    """Scale a composed page to 90% and centre it on its own background colour, so every mark sits inside the
    toolkit's title-safe inset (final_frame_check.py: x 192-3648, y 108-2052 at 4K)."""
    bg = im.getpixel((2, 2))
    s = im.resize((int(W * 0.9), int(H * 0.9)), Image.LANCZOS)
    out = Image.new('RGB', (W, H), bg)
    out.paste(s, ((W - s.width) // 2, (H - s.height) // 2))
    return out


def main_first_cut():
    """The first cut's stills (B01-B17), kept for the record; the rebuilt film uses cards2.main()."""
    out = REEL / 'media'
    out.mkdir(exist_ok=True)
    made = {'B01': b01(), 'B02': b02(), 'B03': b03(), 'B07': b07(), 'B10': b10(), 'B11': b11(), 'B12': b12(),
            'B16': b16(), 'B17': b17()}
    s = scenes()
    s['B06'] = b06_extras(s['B06'])
    made.update(s)
    im9, table = b09()
    made['B09'] = im9
    prov = {}
    for bid, im in sorted(made.items()):
        assert im.size == (W, H), bid
        if bid not in ('B01', 'B17'):      # B01 is a full-bleed plate (qc.full_bleed); B17 is laid out inside safe
            im = fit_safe(im.convert('RGB'))
        p = out / f'{bid}.png'
        im.convert('RGB').save(p, optimize=True)
        prov[bid] = {'media': f'media/{bid}.png', 'sha256': sha256(p)}
        print(bid, 'ok')
    prov['B09']['test_table'] = table
    prov['_inputs'] = {f'art/{n}': sha256(ART_DIR / n) for n in
                       ('witch_fullbody_talk.png', 'witch_expressions.png', 'wolf_snarl.png', 'wolf_calm.png')}
    save_json(REEL / 'evidence' / 'stills-provenance.json', prov)


if __name__ == '__main__':
    import cards2
    cards2.main()
