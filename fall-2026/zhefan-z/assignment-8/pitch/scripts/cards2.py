"""Phase 2a (rebuild from the GDD): every still beat as a 3840x2160 PNG in media/.

Written by Claude Code for the Assignment 8 pitch film, 2026-11-22 (prompt-2-gdd.txt). Reuses cards.py's primitives
and the cards already built and checked in the first cut (why-care, the first sixty seconds, the pin and test table,
the risk drawing, what is new, the dialogue scenes, the outro); the rest is new. Every picture carries its label:
  real (a captured frame or the game's own files, with the revision), generated (the Gemini concept art),
  constructed (drawn here; "Constructed - proposed, not built" for anything not built), figure (from committed logs).
Text comes from GDD.md (version 2.0) and PROJECT-BRIEF.md (revised 2026-11-21).
"""
import io

from PIL import Image, ImageDraw

import cards
from cards import F, chip, page, panel, para, wrap, witch, wolf, fl, arrow, keyed, portrait_box, fit_safe
from common import (REEL, ART_DIR, W, H, TITLE, AUTHOR, PAGE, CARD, BORDER, INK, INK_SOFT, FIRE, FIRE_SOFT, CAVE,
                    CAVE_SOFT, CAVE_DARK, REV_A7, REV_A5, REV_A6, A7_GAME, L_REAL, L_CONSTRUCTED_PROPOSED, L_GENERATED,
                    L_CONSTRUCTED, CAP_840, git_show, sha256, save_json, frame_rows)

P = L_CONSTRUCTED_PROPOSED


def cpage(heading, label=P):
    return page(heading, [(label, 'constructed')])


def game_png(rel):
    return Image.open(io.BytesIO(git_show(f'{REV_A7}:{A7_GAME}/{rel}'))).convert('RGBA')


def a7_png(rel):
    return Image.open(io.BytesIO(git_show(f'{REV_A7}:fall-2026/zhefan-z/assignment-7/{rel}'))).convert('RGB')


def frame840(n):
    rows = frame_rows('run-01')
    return Image.open(CAP_840 / f'frame{n:08d}.png').convert('RGB'), rows[n]


def bullets(d, xy, items, font, fill=INK, gap=1.45, width=None):
    x, y = xy
    for s in items:
        if width:
            for j, line in enumerate(wrap(d, s, font, width)):
                d.text((x + (0 if j == 0 else 44), y), ('· ' if j == 0 else '') + line, font=font, fill=fill)
                y += int(font.size * 1.2)
            y += int(font.size * (gap - 1.2))
        else:
            d.text((x, y), '· ' + s, font=font, fill=fill)
            y += int(font.size * gap)
    return y


# ---------------------------------------------------------------- title, game in brief
def t00():
    im = Image.new('RGB', (W, H), CAVE_DARK)
    d = ImageDraw.Draw(im)
    fl(d, W // 2, 520, 3.4)
    d.text((W // 2, 980), TITLE, font=F('serif_med', 260), fill=PAGE, anchor='mm')
    d.text((W // 2, 1230), 'Final project pitch  ·  ' + AUTHOR, font=F('sans', 84), fill=CAVE_SOFT, anchor='mm')
    d.rounded_rectangle([1020, 1420, 2820, 1640], radius=30, outline=FIRE_SOFT, width=6)
    d.text((W // 2, 1490), 'Game design document (metadata)', font=F('sans_med', 56), fill=FIRE_SOFT, anchor='mm')
    d.text((W // 2, 1580), 'GDD.md  ·  version 2.0  ·  2026-11-21', font=F('mono', 60), fill=PAGE, anchor='mm')
    c = chip(L_CONSTRUCTED + ' · title card', 'constructed')
    im.paste(c, (W - 260 - c.width, 180), c)
    return im


def p01():
    im, d = page('The game in brief', [(L_CONSTRUCTED + ' · card', 'constructed')])
    n = 1544
    g, r = frame840(n)
    assert r['seg'] == 'cancel' and r['ws'] == 'GROWL', 'brief frame: the wolf should be growling'
    k = 4
    im.paste(g.resize((640 * k, 360 * k), Image.NEAREST), (160, 290))
    c = chip(f'{L_REAL} · frame {n} (the fireball in flight, the wolf growling)', 'real', 38)
    im.paste(c, (200, 290 + 1440 - c.height - 30), c)
    p = keyed('witch_fullbody_talk.png')
    ph = 1440
    p = p.resize((int(p.width * ph / p.height), ph), Image.LANCZOS)
    bx = 160 + 2560 + 60
    d.rounded_rectangle([bx, 290, W - 160, 290 + 1440], radius=36, fill=CAVE_DARK, outline=FIRE_SOFT, width=8)
    im.paste(p, (bx + (W - 160 - bx - p.width) // 2, 290), p)
    g1 = chip('Generated (Gemini 4) · concept art', 'generated', 34)
    im.paste(g1, (bx + 20, 290 + 1440 - g1.height - 20), g1)
    para(d, (160, 1790), 'An HD-2D cave action game: you aim fireballs with the mouse to fight through a cold cave. '
         'The goal: reach the bottom and defeat the great wolf that guards it.', F('serif', 68), INK, 3520, 1.2)
    return im


# ---------------------------------------------------------------- GDD sections (constructed)
def g01():
    im, d = cpage('GDD 1 · Design pillars', L_CONSTRUCTED + ' · from GDD.md')
    cols = [(160, 'Your fire is the only warmth', 'A cold cave; only fire, and what fire makes safe, is warm.'),
            (1060, 'Every failure is fair', 'Every danger warns before it strikes.'),
            (1960, 'Readable at a glance, even muted', 'Where she is, what hit her, whether the shot landed.'),
            (2860, 'Small witch, big threat', 'Fragile but capable; the final enemy is far bigger.')]
    for i, (x, t, s) in enumerate(cols):
        panel(d, (x, 320, x + 820, 1980))
        cx = x + 410
        if i == 0:
            d.rectangle([x + 60, 420, x + 760, 1040], fill=CAVE_DARK)
            fl(d, cx, 760, 2.4)
        elif i == 1:
            d.polygon([(cx, 450), (cx + 260, 950), (cx - 260, 950)], outline=FIRE, width=22)
            d.text((cx, 800), '!', font=F('serif_med', 260), fill=FIRE, anchor='mm')
        elif i == 2:
            d.ellipse([cx - 280, 560, cx + 280, 880], outline=INK, width=18)
            d.ellipse([cx - 90, 630, cx + 90, 810], fill=INK)
        else:
            wolf(d, cx - 330, 1000, 1.6, col=CAVE)
            witch(d, cx - 230, 1000, 0.5)
        lines = wrap(d, t, F('serif_med', 72), 700)
        for j, line in enumerate(lines):
            d.text((cx, 1180 + j * 90), line, font=F('serif_med', 72), fill=INK, anchor='mm')
        para(d, (x + 70, 1420), s, F('sans', 52), INK_SOFT, 680, 1.3)
    return im


def g02():
    im, d = cpage('GDD 2 · Core gameplay loop')
    scales = [('Moment to moment', 'move, jump, aim, fire; read a growl: shoot early, or step out of reach', 'built today'),
              ('In one sitting', 'clear a level → campfire and chest → next level → the great wolf', 'will'),
              ('What brings you back', 'a short run: replay for a cleaner one, fewer hits, more lunges cancelled', 'will')]
    cx, cy = 1180, 1160
    for rr, col in ((760, CAVE_SOFT), (520, FIRE_SOFT), (280, FIRE)):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=col, width=26)
    witch(d, cx - 40, cy + 120, 0.8)
    for i, (t, s, tag) in enumerate(scales):
        y = 420 + i * 520
        d.text((2140, y), t, font=F('serif_med', 84), fill=INK)
        para(d, (2140, y + 120), s, F('sans', 56), INK_SOFT, 1540, 1.3)
        c = chip(tag, 'real' if tag == 'built today' else 'constructed', 36)
        im.paste(c, (3680 - c.width, y + 10), c)
    return im


def g03():
    im, d = cpage('GDD 3 · Player experience goals')
    rows = [('small but capable', 'when an early fireball cancels a wolf’s lunge mid-growl'),
            ('safe and warm', 'when she reaches a campfire after a fight'),
            ('tension', 'when the great wolf’s entrance fills the screen'),
            ('relief', 'when the great wolf is beaten and the cave falls quiet')]
    for i, (f, w_) in enumerate(rows):
        y = 380 + i * 400
        panel(d, (160, y, 3680, y + 330))
        x = 260
        if i == 0:
            fl(d, x + 80, y + 180, 1.2); wolf(d, x + 180, y + 280, 0.4, col=CAVE)
        elif i == 1:
            fl(d, x + 160, y + 180, 1.6, FIRE)
        elif i == 2:
            wolf(d, x + 20, y + 300, 0.75, col=INK)
        else:
            d.arc([x + 40, y + 60, x + 300, y + 300], 200, 340, fill=CAVE, width=14)
        d.text((x + 540, y + 70), 'The player should feel', font=F('sans', 50), fill=INK_SOFT)
        d.text((x + 540, y + 140), f, font=F('serif_med', 92), fill=FIRE)
        d.text((x + 1500, y + 175), w_, font=F('sans', 58), fill=INK)
    return im


def g06():
    im, d = cpage('GDD 6 · Progression')
    d.text((160, 290), 'No levelling, no equipment. One change: the heal spell.', font=F('serif', 84), fill=INK)
    xs = [160, 1370, 2580]
    titles = ['Level 1: cave mouth', 'Level 2: deeper tunnels', 'Level 3: the den']
    adds = ['first wolves, easy pits; ends at the campfire and the chest with the heal spell',
            'more wolves; spikes and the rolling boulder (if there are three levels)', 'the great wolf']
    for i, x in enumerate(xs):
        panel(d, (x, 480, x + 1100, 1900), titles[i])
        base = 1400
        d.rectangle([x + 80, base, x + 1020, base + 16], fill=INK)
        for k in range(i + 1 if i < 2 else 0):
            wolf(d, x + 520 + k * 220, base, 0.42, col=CAVE)
        if i == 0:
            d.rounded_rectangle([x + 140, base - 150, x + 330, base], radius=14, fill='#8B6A44', outline=INK, width=6)
            fl(d, x + 410, base - 60, 1.0)
        if i == 1:
            for k in range(4):
                d.polygon([(x + 120 + k * 60, base), (x + 150 + k * 60, base - 80), (x + 180 + k * 60, base)], fill=INK)
            d.ellipse([x + 760, base - 170, x + 930, base], fill=INK_SOFT)
        if i == 2:
            wolf(d, x + 200, base, 1.7, col=INK)
        witch(d, x + 260 if i != 0 else x + 620, base, 0.6)
        para(d, (x + 80, 1500), adds[i], F('sans', 50), INK_SOFT, 940, 1.3)
        if i < 2:
            arrow(d, (x + 1110, 1100), (xs[i + 1] - 10, 1100), FIRE, 14, 40)
    d.text((W // 2, 2000), 'Difficulty rises by level: more wolves, then spikes and the boulder, then the great wolf.',
           font=F('sans_med', 56), fill=FIRE, anchor='mm')
    return im


def g07():
    im, d = cpage('GDD 7 · World and environment')
    d.rounded_rectangle([160, 300, 3680, 1700], radius=60, fill=CAVE_DARK)
    d.polygon([(160, 300), (1900, 300), (1700, 520), (1300, 470), (900, 560), (500, 440), (160, 520)], fill='#2A3A4E')
    levels = [(260, 760, 'cave mouth'), (1300, 1080, 'deeper tunnels (if three)'), (2400, 1400, 'the den')]
    for i, (x, y, t) in enumerate(levels):
        d.rectangle([x, y, x + 1000, y + 22], fill=CAVE_SOFT)
        d.text((x + 20, y + 50), f'{i + 1}. {t}', font=F('sans_med', 56), fill=PAGE)
        if i < 2:
            arrow(d, (x + 1000, y + 10), (levels[i + 1][0] + 60, levels[i + 1][1] - 20), CAVE_SOFT, 12, 36)
    witch(d, 420, 760, 0.55)
    fl(d, 1180, 700, 1.1)
    d.ellipse([1080, 600, 1280, 800], outline=FIRE_SOFT, width=6)
    wolf(d, 2900, 1400, 1.2, col=CAVE)
    d.text((W // 2, 1820), 'One cold cave under a mountain, in two to three short levels.', font=F('serif', 80),
           fill=INK, anchor='mm')
    d.text((W // 2, 1960), 'The one rule: warmth comes only from fire, so lit places are safe places.',
           font=F('sans_med', 60), fill=FIRE, anchor='mm')
    return im


def g08(scenes_png):
    """The four story moments: the three dialogue scenes built for the first cut, and the campfire line (not written)."""
    im, d = cpage('GDD 8 · Narrative: four short, skippable scenes', L_CONSTRUCTED + ' · scenes proposed')
    boxes = [(160, 300), (1960, 300), (160, 1180), (1960, 1180)]
    titles = ['1 · the opening', '2 · at the campfire', '3 · before the boss', '4 · after the boss']
    order = ['B04', None, 'B05', 'B06']
    for (x, y), t, key in zip(boxes, titles, order):
        d.text((x, y), t, font=F('sans_med', 54), fill=INK)
        if key:
            th = scenes_png[key].resize((1720, 968), Image.LANCZOS)
            im.paste(th, (x, y + 80))
        else:
            d.rounded_rectangle([x, y + 80, x + 1720, y + 80 + 760], radius=30, fill=CAVE_DARK)
            fl(d, x + 860, y + 360, 1.8)
            d.text((x + 860, y + 640), 'line not written yet', font=F('serif', 70), fill=CAVE_SOFT, anchor='mm')
    g = chip(L_GENERATED + ' (portraits in the scenes)', 'generated', 38)
    im.paste(g, (160, H - g.height - 40), g)
    return im


def g09():
    im, d = page('GDD 9 · Characters', [(f'Sprites: real game files at {REV_A7}', 'real'),
                                         ('Portraits: ' + L_GENERATED, 'generated')])
    cols = [(160, 'The Little Flame Witch', 'player'), (1400, 'Cave wolves', 'enemies'), (2640, 'The great wolf', 'boss, will')]
    for x, t, role in cols:
        panel(d, (x, 300, x + 1040, 2000))
        d.text((x + 520, 380), t, font=F('serif_med', 76), fill=INK, anchor='mm')
        d.text((x + 520, 470), role, font=F('sans', 50), fill=INK_SOFT, anchor='mm')
    mage = game_png('assets/sprites/mage/mage_idle.png').resize((62 * 8, 69 * 8), Image.NEAREST)
    im.paste(mage, (160 + 520 - mage.width // 2, 560), mage)
    d.text((160 + 520, 1150), 'in play: mage_idle.png (×8)', font=F('mono', 40), fill=INK_SOFT, anchor='mm')
    portrait_box(im, 'curious', (160 + 520 - 330, 1230), 660)
    wr = game_png('assets/sprites/wolf/wolf_run.png').resize((80 * 9, 40 * 9), Image.NEAREST)
    im.paste(wr, (1400 + 520 - wr.width // 2, 640), wr)
    wl = game_png('assets/sprites/wolf/wolf_lunge.png').resize((80 * 9, 40 * 9), Image.NEAREST)
    im.paste(wl, (1400 + 520 - wl.width // 2, 1080), wl)
    d.text((1400 + 520, 1500), 'wolf_run.png, wolf_lunge.png (×9)', font=F('mono', 40), fill=INK_SOFT, anchor='mm')
    para(d, (1480, 1600), 'Grey cave wolves that growl before they lunge.', F('sans', 52), INK, 880, 1.3)
    portrait_box(im, 'snarl', (2640 + 520 - 400, 600), 800)
    para(d, (2720, 1500), 'Much larger, with glowing eyes; it speaks before and after the fight. Only concept art '
         'exists so far.', F('sans', 52), INK, 880, 1.3)
    return im


def g10(look_png):
    im, d = page('GDD 10 · Art direction', [(f'Left: exists (real, {REV_A7})', 'real'), ('Right: ' + P, 'constructed')])
    panel(d, (160, 290, 2020, 2000), 'Exists today')
    panel(d, (2120, 290, 3680, 2000), 'Planned look')
    sheet = game_png('assets/sprites/mage/mage_run_cycle_sheet.png').resize((248 * 3, 69 * 3), Image.NEAREST)
    im.paste(sheet, (240, 440), sheet)
    d.text((240, 670), 'run cycle, 4 cells (A7; Gemini sheet)', font=F('sans', 36), fill=INK_SOFT)
    mage = game_png('assets/sprites/mage/mage_cast.png').resize((62 * 3, 69 * 3), Image.NEAREST)
    im.paste(mage, (1100, 440), mage)
    wolfp = game_png('assets/sprites/wolf/wolf_run.png').resize((80 * 3, 40 * 3), Image.NEAREST)
    im.paste(wolfp, (1340, 520), wolfp)
    d.text((1100, 670), 'sprites (A2)', font=F('sans', 36), fill=INK_SOFT)
    onion = a7_png('captures/figures/lunge_onion.png').crop((300, 200, 960, 500)).resize((860, 391), Image.LANCZOS)
    im.paste(onion, (240, 760))
    d.text((240, 1165), 'lunge rig key poses (figure from the logs, A7)', font=F('sans', 36), fill=INK_SOFT)
    props = Image.open(REEL / 'capture' / 'props-840b501-frame20.png').convert('RGB').crop((40, 60, 600, 300))
    props = props.resize((840, 360), Image.NEAREST)
    im.paste(props, (1140, 760))
    d.text((1140, 1165), '3D props (A3), real render at 840b501', font=F('sans', 36), fill=INK_SOFT)
    g, _ = frame840(15)
    torch = g.crop((0, 40, 320, 340)).resize((640, 600), Image.NEAREST)
    im.paste(torch, (240, 1250))
    d.text((240, 1880), 'cave lights and embers (real frame 15)', font=F('sans', 36), fill=INK_SOFT)
    pt = keyed('witch_fullbody_smile.png')
    pt = pt.resize((int(pt.width * 600 / pt.height), 600), Image.LANCZOS)
    d.rounded_rectangle([960, 1250, 960 + pt.width + 40, 1890], radius=24, fill=CAVE_DARK)
    im.paste(pt, (980, 1270), pt)
    c = chip('Generated (Gemini 4) · concept art', 'generated', 30)
    im.paste(c, (960 + pt.width + 70, 1820), c)
    para(d, (960 + pt.width + 70, 1270), 'Palette from Assignment 2: a cold blue-grey cave; warm colour only on fire '
         'and what fire makes safe.', F('sans', 46), INK, 2000 - (960 + pt.width + 70), 1.3)
    look = look_png.crop((300, 300, 3540, 1760)).resize((1480, 667), Image.LANCZOS)
    im.paste(look, (2160, 420))
    bullets(d, (2200, 1150), ['tilt-shift depth of field, bloom', 'fog and light shafts',
                              'the fireball as a moving light', 'dust, drips, moss, crystal glints',
                              'my Assignment 3 props in the level', 'hit-stop, flash, sparks; a boss title card'],
            F('sans', 50))
    d.text((2200, 1880), 'Techniques from games I played; no assets.', font=F('sans', 44), fill=INK_SOFT)
    return im


def g12():
    im, d = cpage('GDD 12 · Feature list')
    cols = [('Must', ['the 3D cave, sprites in 3D, the HD-2D camera', 'move, jump, aim and cast in 3D',
                      'wolves with growl, lunge and the growl cancel', 'two levels, title screen to end screen',
                      'the great wolf boss', 'HP, fail and restart', 'Windows build + a test report a stranger can rerun']),
            ('Should', ['heal spell, chest and campfire', 'spikes and the rolling boulder', 'the four story scenes',
                        'depth of field, bloom, the fireball as a light', 'sprites lit by the scene']),
            ('Could', ['a third level', 'fog and light shafts', 'dust, drips, moss, crystal glints',
                       'hit-stop, camera shake, impact flash', 'boss title card, lit title screen'])]
    for i, (t, items) in enumerate(cols):
        x = 160 + i * 1190
        panel(d, (x, 300, x + 1130, 1680), t)
        bullets(d, (x + 60, 460), items, F('sans', 50), width=1000)
    d.rounded_rectangle([160, 1760, 3680, 2000], radius=30, fill=CAVE_DARK)
    d.text((240, 1830), 'Smallest playable version:', font=F('sans_med', 56), fill=FIRE_SOFT)
    d.text((1080, 1830), 'one 3D cave room, run, jump and fire at one wolf, my behaviour pin passing',
           font=F('sans', 56), fill=PAGE)
    return im


def g13():
    im, d = cpage('GDD 13 · Out of scope (deliberately)')
    items = ['multiplayer', 'a save system (levels are short; a campfire is a rest and restart point)',
             'levelling, equipment or shops', 'a web export (Windows desktop only)',
             "Assignment 4's later chapters, extra spells, extra bosses"]
    for i, s in enumerate(items):
        y = 380 + i * 320
        panel(d, (160, y, 3680, y + 250))
        d.text((300, y + 125), 'no', font=F('serif_med', 110), fill=FIRE, anchor='lm')
        d.text((560, y + 125), s, font=F('sans', 70), fill=INK, anchor='lm')
        d.line([(560, y + 128), (560 + d.textlength(s, font=F('sans', 70)), y + 128)], fill=FIRE, width=8)
    return im


def g14():
    im, d = cpage('GDD 14 · Technical requirements')
    rows = [('Engine', 'Godot 4.7.2-stable, GDScript, Forward+ (Vulkan)'), ('Export', 'Windows desktop: an .exe in a zip'),
            ('Frame-rate target', '60 fps at 1080p on my RTX 5060 Laptop GPU, measured with the profiler, not claimed'),
            ('Verification', 'pins before every change, edge tests, headless checks, human checks')]
    for i, (k, v) in enumerate(rows):
        y = 320 + i * 170
        d.text((200, y), k, font=F('sans_med', 60), fill=FIRE)
        d.text((900, y), v, font=F('sans', 60), fill=INK)
    d.text((200, 1060), 'From greybox to finished', font=F('serif_med', 80), fill=INK)
    xs = [200, 1400, 2600]
    for i, (x, t) in enumerate(zip(xs, ['grey boxes', 'low-poly Blender pieces (.glb, metres, origin at the base)',
                                        'sprites as camera-facing Sprite3D billboards'])):
        panel(d, (x, 1200, x + 1040, 2000))
        cx = x + 520
        if i == 0:
            for k in range(3):
                d.rectangle([cx - 330 + k * 230, 1520 - k * 60, cx - 150 + k * 230, 1660], fill=BORDER, outline=INK_SOFT, width=6)
        elif i == 1:
            d.polygon([(cx - 300, 1660), (cx - 180, 1420), (cx - 20, 1500), (cx + 120, 1380), (cx + 300, 1660)],
                      fill=CAVE, outline=INK, width=6)
        else:
            d.polygon([(cx - 330, 1680), (cx + 330, 1680), (cx + 230, 1560), (cx - 230, 1560)], fill=CAVE_SOFT)
            d.rectangle([cx - 110, 1330, cx + 110, 1640], fill=CARD, outline=INK, width=6)
            witch(d, cx, 1620, 0.55)
        lines = wrap(d, t, F('sans_med', 46), 960)
        for j, line in enumerate(lines):
            d.text((cx, 1760 + j * 60), line, font=F('sans_med', 46), fill=INK, anchor='mm')
        if i < 2:
            arrow(d, (x + 1050, 1500), (xs[i + 1] - 10, 1500), INK_SOFT, 12, 36)
    return im


def g15(risk_png):
    im, d = cpage('GDD 15 · Risks (also question 6)')
    r = risk_png.crop((0, 260, W, 2060)).resize((2600, 1219), Image.LANCZOS)
    im.paste(r, (160, 300))
    x = 2860
    panel(d, (x, 300, 3680, 1980))
    d.text((x + 410, 400), 'Two more', font=F('serif_med', 76), fill=INK, anchor='mm')
    d.text((x + 60, 520), 'Scope', font=F('sans_med', 58), fill=FIRE)
    para(d, (x + 60, 610), 'three levels may not fit; the plan already allows two', F('sans', 52), INK, 700, 1.3)
    d.text((x + 60, 1000), 'Cost of the look', font=F('sans_med', 58), fill=FIRE)
    para(d, (x + 60, 1090), 'fog and depth of field may miss 60 fps; each is measured, and the costliest is dropped '
         'first', F('sans', 52), INK, 700, 1.3)
    d.text((160, 1620), 'Moving the 2D game into 3D: one room first, judged by my Assignment 7 pin.',
           font=F('sans_med', 56), fill=INK)
    return im


def g16():
    im, d = cpage('GDD 16 · Open questions')
    rows = [('2D gameplay with a 3D backdrop, or 3D bodies held to a plane?', 'the one-room test, judged by my pin'),
            ('Two levels or three?', 'decide after the first level is playable'),
            ('Will the pixel sprites read under depth of field and coloured light?', 'captures from the first room')]
    for i, (q, how) in enumerate(rows):
        y = 360 + i * 560
        panel(d, (160, y, 3680, y + 480))
        d.text((300, y + 240), '?', font=F('serif_med', 300), fill=FIRE, anchor='mm')
        para(d, (520, y + 80), q, F('serif', 80), INK, 3000, 1.2)
        d.text((520, y + 330), 'How I will find out: ' + how, font=F('sans', 58), fill=INK_SOFT)
    return im


# ---------------------------------------------------------------- questions
def q01():
    im, d = cpage('Question 1 · What it is: the artifact and its form')
    d.rounded_rectangle([500, 500, 1300, 1700], radius=40, fill=CAVE, outline=INK, width=14)   # dark enough for Gate V's contrast floor
    d.line([900, 500, 900, 1700], fill=INK, width=16)
    for j in range(8):
        d.rectangle([860, 540 + j * 120, 940, 590 + j * 120], fill=INK)
    d.text((900, 1800), 'a zip', font=F('sans_med', 64), fill=INK, anchor='mm')
    arrow(d, (1400, 1100), (1800, 1100), INK_SOFT, 16, 50)
    items = [('.exe', 'a playable Windows desktop build'), ('2–3 levels', 'a vertical slice, title screen to end screen'),
             ('TEST-REPORT', 'a test report a stranger can rerun')]
    for i, (k, v) in enumerate(items):
        y = 520 + i * 420
        panel(d, (1900, y, 3600, y + 340))
        d.text((2000, y + 170), k, font=F('mono', 80), fill=FIRE, anchor='lm')
        d.text((2600, y + 170), v, font=F('sans', 56), fill=INK, anchor='lm')
    return im


def q05():
    im, d = cpage('Question 5 · What comes first, and how anyone would know it ran')
    x0 = 300
    d.polygon([(x0, 1650), (x0 + 1700, 1650), (x0 + 1450, 1350), (x0 + 250, 1350)], fill=CAVE_SOFT)
    d.rectangle([x0 + 250, 450, x0 + 1450, 1350], fill=CAVE)
    witch(d, x0 + 650, 1520, 1.0)
    wolf(d, x0 + 1050, 1520, 0.8, col=CAVE_DARK)
    for t in range(5):
        fl(d, x0 + 820 + t * 50, 1230 - t * 20, 0.4)
    d.text((x0 + 850, 1780), 'one 3D cave room: run, jump, cast at a wolf', font=F('sans_med', 56), fill=INK, anchor='mm')
    x = 2300
    d.text((x, 450), 'It ran if:', font=F('serif_med', 96), fill=INK)
    panel(d, (x, 620, 3640, 1050))
    d.text((x + 80, 700), '1. my existing behaviour pin', font=F('sans_med', 60), fill=INK)
    d.text((x + 80, 800), 'passes against that room', font=F('sans', 60), fill=INK_SOFT)
    panel(d, (x, 1150, 3640, 1580))
    d.text((x + 80, 1230), '2. a windowed capture of it', font=F('sans_med', 60), fill=INK)
    d.text((x + 80, 1330), 'is labelled with its revision', font=F('sans', 60), fill=INK_SOFT)
    d.text((x, 1700), 'In and out: GDD 12 and 13.', font=F('sans', 52), fill=INK_SOFT)
    return im


# ---------------------------------------------------------------- appendix
def a02():
    im, d = cpage('Appendix · Started, not finished', L_CONSTRUCTED + ' · status card')
    rows = [('The design', 'GDD.md (2.0) and PROJECT-BRIEF.md: written; they will change as I build', 'written'),
            ('The story scenes', 'concept portraits exist; the dialogue box, the lines in the game and the triggers are '
             'not started', 'portraits only'),
            ('The 3D cave', 'nothing started yet', 'not started')]
    for i, (k, v, tag) in enumerate(rows):
        y = 380 + i * 540
        panel(d, (160, y, 3680, y + 460))
        d.text((260, y + 70), k, font=F('serif_med', 90), fill=INK)
        para(d, (260, y + 210), v, F('sans', 60), INK_SOFT, 2600, 1.25)
        c = chip(tag, 'figure' if i == 0 else 'constructed', 44)
        im.paste(c, (3580 - c.width, y + 80), c)
    return im


def a03():
    im, d = cpage('Appendix · Not started: everything here will exist')
    will = ['the two to three 3D cave levels and the HD-2D camera', 'the sprites placed in 3D', 'the look (GDD 10)',
            'the four story scenes in the game', 'the heal spell', 'the great-wolf boss', 'spikes and a rolling boulder',
            'the chest-and-campfire rest point', 'a title and an end screen', 'the Windows export',
            'a test report for the slice']
    for i, s in enumerate(will):
        col, row = divmod(i, 6)
        x, y = 200 + col * 1800, 380 + row * 270
        panel(d, (x, y, x + 1680, y + 210))
        d.text((x + 70, y + 105), s, font=F('sans', 62), fill=INK, anchor='lm')
    return im


def a04():
    im, d = cpage('Appendix · Can one person build this by the final?')
    d.text((160, 300), 'Yes, at the size of the Must and Should columns, with two levels.', font=F('serif', 92), fill=INK)
    d.text((160, 480), 'If I fall behind, I cut in this order:', font=F('sans_med', 64), fill=FIRE)
    cuts = ['the third level', 'the Could items: fog and light shafts, ambient particles, hit-stop and shake, the boss '
            'title card', 'the story scenes']
    for i, s in enumerate(cuts):
        y = 640 + i * 360
        panel(d, (160, y, 3680, y + 300))
        d.text((300, y + 150), str(i + 1), font=F('serif_med', 160), fill=FIRE, anchor='mm')
        para(d, (480, y + 70), s, F('sans', 64), INK, 3100, 1.25)
    d.text((160, 1820), 'Kept whole: the Must column.', font=F('serif_med', 84), fill=INK)
    return im


def a05():
    im, d = page('Appendix · Where every asset comes from', [('From PROJECT-BRIEF.md · ' + L_CONSTRUCTED + ' card', 'constructed')])
    rows = [('Witch and wolf pixel sprites', 'Gemini, my prompts (Assignment 2)', 'generated', "Google's terms"),
            ('Run-cycle sheet', 'Gemini, my prompt (Assignment 7)', 'generated', "Google's terms"),
            ('Wolf lunge rig', 'cut from my Assignment 2 wolf sprite', 'made', 'mine'),
            ('Dialogue portraits', 'Gemini 4, my prompts (ART-PROMPTS.md)', 'generated', "Google's terms"),
            ('Rock, crystal, treasure chest', 'my Blender work via the Blender MCP (A3)', 'made', 'mine'),
            ('Cave pieces, torches, campfire, spikes, boulder', 'my Blender work, same rules', 'will be made', 'mine'),
            ("The great wolf's sprites", 'Gemini, from my wolf sprite', 'will be generated', "Google's terms"),
            ('Cave music', 'Lyria (Assignment 2)', 'generated', "Google's terms"),
            ('Boss and campfire music', 'Lyria', 'will be generated', "Google's terms"),
            ('Sound effects', 'Stable Audio Open 1.0, run locally (A2)', 'generated', "Stability AI's licence"),
            ('Shaders and particle effects', 'my own (Assignments 5 and 6)', 'made', 'mine')]
    xs = [160, 1260, 2500, 3100]
    hdr = ['Asset', 'Where it comes from', 'Made / generated', 'Licence']
    for x, h in zip(xs, hdr):
        d.text((x, 290), h, font=F('sans_med', 52), fill=FIRE)
    d.line([160, 370, 3680, 370], fill=INK, width=4)
    for i, row in enumerate(rows):
        y = 400 + i * 135
        if i % 2 == 0:
            d.rectangle([160, y - 14, 3680, y + 116], fill='#F0EDE4')
        for x, v in zip(xs, row):
            d.text((x + 10, y + 20), v, font=F('sans', 44), fill=INK)
    d.text((160, 1930), 'Nothing bought, no third-party game assets; everything in my public repository and listed in '
           'SOURCES.md.', font=F('sans_med', 52), fill=INK)
    return im


# ---------------------------------------------------------------- build
def main():
    out = REEL / 'media'
    out.mkdir(exist_ok=True)
    reuse = {'Q02': cards.b02(), 'Q03': cards.b07(), 'Q07': cards.b12()}
    q04, table = cards.b09()
    reuse['Q04'] = q04
    look = cards.b03()
    risk = cards.b11()
    sc = cards.scenes()
    sc['B06'] = cards.b06_extras(sc['B06'])
    sc = {k: fit_safe(v.convert('RGB')) for k, v in sc.items()}
    made = {'P01': p01(), 'G01': g01(), 'G02': g02(), 'G03': g03(), 'G06': g06(), 'G07': g07(), 'G08': g08(sc),
            'G09': g09(), 'G10': g10(look), 'G12': g12(), 'G13': g13(), 'G14': g14(), 'G15': g15(risk), 'G16': g16(),
            'Q01': q01(), 'Q05': q05(), 'A02': a02(), 'A03': a03(), 'A04': a04(), 'A05': a05()}
    made.update(reuse)
    prov = {}
    for bid, im in sorted(made.items()):
        assert im.size == (W, H), bid
        im = fit_safe(im.convert('RGB'))
        p = out / f'{bid}.png'
        im.save(p, optimize=True)
        prov[bid] = {'media': f'media/{bid}.png', 'sha256': sha256(p)}
    for bid, im in (('T00', t00()), ('OUT', cards.b17())):   # laid out inside the title-safe area already
        p = out / f'{bid}.png'
        im.convert('RGB').save(p, optimize=True)
        prov[bid] = {'media': f'media/{bid}.png', 'sha256': sha256(p)}
    prov['Q04']['test_table'] = table
    prov['_inputs'] = {f'art/{n}': sha256(ART_DIR / n) for n in
                       ('witch_fullbody_talk.png', 'witch_fullbody_smile.png', 'witch_expressions.png',
                        'wolf_snarl.png', 'wolf_calm.png')}
    prov['_inputs']['capture/props-840b501-frame20.png'] = sha256(REEL / 'capture' / 'props-840b501-frame20.png')
    prov['_reused_from_first_cut'] = {'Q02': 'cards.b02', 'Q03': 'cards.b07', 'Q04': 'cards.b09', 'Q07': 'cards.b12',
                                      'G08': 'cards.scenes (B04-B06)', 'G10': 'cards.b03 (right panel)',
                                      'G15': 'cards.b11 (left panel)', 'OUT': 'cards.b17'}
    save_json(REEL / 'evidence' / 'stills-provenance.json', prov)
    print(len(prov) - 3, 'stills')


if __name__ == '__main__':
    main()
