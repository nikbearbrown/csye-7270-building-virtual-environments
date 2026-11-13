"""Phase 2b: build every card slot and fill the Remotion props, using measured narration.

Adapted from the Assignment 6 film's media.py. Images of the game are either frames of the scripted-input capture
(capture/run-01, real engine output) or the author's committed captures in captures/ (fixture captures from capture
harnesses and preview scenes that place the characters; not played gameplay), enlarged with nearest-neighbour scaling.
Figures from captures/figures/ (tools/make_figures.py, drawn from the logs) are scaled to fit. Figures on cards come
from the named source documents and logs; code comes verbatim from the snapshot of the build shown (f860fed). The
gameplay beats themselves are built by footage.py.
"""
import json

import numpy as np
from PIL import Image, ImageDraw

import cards
from cards import F, wrap, text_block, SAFE_L, SAFE_R, DARK, DARK_TEXT, DARK_MUTED, DARK_HI
from common import (REEL, GAME, A7, CAPS, LOGS, BUILD, FPS, SNAPSHOT, CAPTURE_FRAMES, INK, INK_SOFT, SPARK, BORDER,
                    load_json, save_json, render_frames, source_lines, sha256, capture_rows)

MEDIA = REEL / 'media'
EV = REEL / 'evidence'
SRC = SNAPSHOT or GAME
FIG = CAPS / 'figures'

PLAY = 'Scripted input · real engine output · capture/run-01'
FIXTURE = 'Fixture capture · a capture harness places the characters; not played gameplay'
FIGLABEL = 'Figure from the logs (tools/make_figures.py)'
RESULTS = 'Recorded results — not a render'
SRCVIEW = 'Source view — reconstruction, not a screenshot'
AMBER, RED, GREEN = '#C98A1E', '#C2453A', '#3F8F5F'


# ---------------------------------------------------------------- helpers
def nframes(bid):
    return render_frames(BEATS[bid]['actual_duration_s'])


def at(bid, phrase):
    """Seconds into the beat where a narration phrase starts (character-proportional estimate)."""
    text = BEATS[bid]['narration_text']
    return round(text.index(phrase) / len(text) * nframes(bid) / FPS, 2)


def remotion(bid, **props):
    rem = BEATS[bid]['shot']['remotion']
    rem['props'].update(props)
    rem['props']['durationSeconds'] = nframes(bid) / FPS


def excerpt(rel, start, end, first):
    text = source_lines(SRC, rel, start, end)
    assert text.split('\n')[0].strip().startswith(first), f'{rel}:{start} does not start with {first!r}'
    if SNAPSHOT:
        assert text == source_lines(GAME, rel, start, end), f'{rel}:{start}-{end} differs from the working tree'
    return text


def line(rel, n, first):
    return excerpt(rel, n, n, first)


def still(bid, img, prov, evidence=False):
    img.save(MEDIA / f'{bid}.png')
    BEATS[bid]['shot'].update({'type': 'STILL', 'motion': 'hold'})
    BEATS[bid]['shot'].pop('remotion', None)
    if evidence:
        BEATS[bid]['shot']['evidence_media'] = f'media/{bid}.png'
    PROV[bid] = prov


def cap(rel):
    return Image.open(CAPS / rel).convert('RGB')


def play(n):
    return Image.open(CAPTURE_FRAMES / f'frame{n:08d}.png').convert('RGB')


def caps_prov(*rels):
    return {'images': [f'captures/{r}' for r in rels], 'sha256': {r: sha256(CAPS / r) for r in rels}}


def workbench(bid, title, rel, start, end, first, notes, cues, font=34):
    code = excerpt(rel, start, end, first)
    remotion(bid, mode='code', title=title, project='walker-magic', path=rel,
             source=f'Exact source at {BUILD} · lines {start}–{end} · next: the visible result',
             code=code, startLine=start, codeFontSize=font,
             notes=[{'label': k, 'value': v} for k, v in notes],
             output=[f'Godot editor reconstruction · {rel} lines {start}–{end} · build {BUILD}'],
             cues=[{'at': at(bid, p) if isinstance(p, str) else p, 'line': ln, 'label': lab} for p, ln, lab in cues])
    BEATS[bid]['excerpt'] = {'path': rel, 'start_line': start, 'end_line': end}


def fit(make, sizes):
    """Largest size whose layout passes its own overflow check (FILL-THE-CANVAS: biggest type that fits)."""
    for size in sizes:
        try:
            return make(size)
        except AssertionError:
            continue
    raise AssertionError('no size fits')


def columns(title, chip, cols, src):
    return fit(lambda v: cards.columns(title, chip, cols, src, value_size=v, label_size=int(v * 0.74)),
               (92, 86, 80, 76, 72, 68, 64, 60, 56, 52))


def table_card(title, chip, header, rows, widths, note, src, hi_cols=()):
    def make(v):
        im, d, y = cards.base(title, chip)
        ty = cards.table(d, SAFE_L, y + 10, widths, header, rows, size=v, head_size=int(v * 0.74), hi_cols=hi_cols)
        if note:
            ty = text_block(d, SAFE_L, ty + 24, note, F('sans', int(v * 0.84)), SAFE_R - SAFE_L, INK, int(v * 1.1))
        assert ty < 1960
        cards.footer(d, src)
        return im
    return fit(make, (100, 92, 84, 78, 72, 68, 64, 60, 56, 52, 48, 44))


def scaled(img, box_w, box_h, pixel=False):
    """Fit an image into a box: whole-number nearest-neighbour zoom for pixel art, smooth scaling for figures."""
    if pixel:
        k = max(1, min(box_w // img.width, box_h // img.height))
        return img.resize((img.width * k, img.height * k), Image.NEAREST), k
    r = min(box_w / img.width, box_h / img.height)
    return img.resize((max(1, round(img.width * r)), max(1, round(img.height * r))), Image.LANCZOS), r


def notes_block(d, x, y, w, notes, v, bottom=1950):
    """[(label, value)] in a column: label small and soft, value large; returns the bottom y."""
    for label, value in notes:
        if label:
            y = text_block(d, x, y, label, F('sans', int(v * 0.72)), w, INK_SOFT, int(v * 0.95))
        y = text_block(d, x, y, value, F('serif', v), w, INK, int(v * 1.22)) + int(v * 0.5)
    assert y < bottom, f'notes overflow ({y})'
    return y


def figure_left_notes(title, chip, img, caption, notes, src, frac=0.58, pixel=False, mark=None):
    """One image (figure or capture) on the left, sourced notes on the right; largest note type that fits."""
    def make(v):
        im, d, y = cards.base(title, chip)
        lw = int((SAFE_R - SAFE_L) * frac)
        cap_lines = len(wrap(d, caption, F('sans', 40), lw))
        pic, k = scaled(img, lw, 1930 - (y + 10) - cap_lines * 54 - 30, pixel)
        cards.paste_framed(im, d, pic, SAFE_L, y + 10)
        if mark:
            mark(d, SAFE_L, y + 10, k)
        text_block(d, SAFE_L, y + 10 + pic.height + 22, caption, F('sans', 40), lw, INK_SOFT, 54)
        rx = SAFE_L + lw + 90
        notes_block(d, rx, y + 10, SAFE_R - rx, notes, v)
        cards.footer(d, src)
        return im
    return fit(make, (76, 70, 66, 62, 58, 54, 50, 46, 42))


def crops_row(im, d, items, x0, y0, width, height, cap_size=40):
    """items: [(PIL crop, caption, accent)] in one row, whole zoom that fits; returns the bottom y."""
    n = len(items)
    gap = 24
    cw = (width - gap * (n - 1)) // n
    w0, h0 = items[0][0].size
    k = max(1, min(cw // w0, (height - 2 * int(cap_size * 1.3) - 20) // h0))
    bottom = y0
    for i, (crop, capt, accent) in enumerate(items):
        x = x0 + i * (cw + gap) + (cw - w0 * k) // 2
        pic = crop.resize((w0 * k, h0 * k), Image.NEAREST)
        im.paste(pic, (x, y0))
        d.rectangle([x, y0, x + pic.width, y0 + pic.height], outline=SPARK if accent else BORDER, width=8 if accent else 4)
        ty = text_block(d, x0 + i * (cw + gap), y0 + pic.height + 12, capt, F('sans_med' if accent else 'sans', cap_size),
                        cw, SPARK if accent else INK, int(cap_size * 1.3))
        bottom = max(bottom, ty)
    return bottom, k


def doc_lines(path, start, end, first=None):
    lines = path.read_text(encoding='utf-8').splitlines()[start - 1:end]
    if first:
        assert lines[0].startswith(first), f'{path.name}:{start} does not start with {first!r}'
    return '\n'.join(lines)


def line_panels(title, chip, rows, note):
    """rows: [(label, [[(path, n, text), ...], ...], annotation)]; largest type that fits (Assignment 6 layout)."""
    def make(m):
        im, d, y = cards.base(title, chip)
        ty = y + 10
        fm = F('mono', m)
        lh = int(m * 1.3)
        for label, groups, ann in rows:
            assert d.textlength(label, font=F('serif_med', int(m * 1.25))) <= SAFE_R - SAFE_L, 'label too wide'
            d.text((SAFE_L, ty), label, font=F('serif_med', int(m * 1.25)), fill=SPARK)
            ty += int(m * 1.25 * 1.35)
            for panels in groups:
                gap = 50
                pw = (SAFE_R - SAFE_L - gap * (len(panels) - 1)) // len(panels)
                hmax = 0
                for i, (path, n, text) in enumerate(panels):
                    x0 = SAFE_L + i * (pw + gap)
                    parts = wrap(d, text.replace('\t', '    ').strip(), fm, pw - 60 - int(m * 2.6))
                    h = 82 + len(parts) * lh + 26
                    hmax = max(hmax, h)
                    d.rounded_rectangle([x0, ty, x0 + pw, ty + h], radius=24, fill=DARK)
                    d.text((x0 + 40, ty + 18), path, font=F('mono', 38), fill='#8BC7F3')
                    d.text((x0 + 40, ty + 82), f'{n:>3}', font=fm, fill=DARK_MUTED)
                    for j, part in enumerate(parts):
                        d.text((x0 + 40 + int(m * 2.6), ty + 82 + j * lh), part, font=fm, fill=DARK_TEXT)
                ty += hmax + 20
            ty = text_block(d, SAFE_L, ty, ann, F('sans', int(m * 0.86)), SAFE_R - SAFE_L, INK, int(m * 1.12)) + 40
        assert ty < 1960, f'{title}: line_panels overflows ({ty})'
        cards.footer(d, note)
        return im
    return fit(make, (76, 72, 68, 64, 60, 56, 52, 48))


def mage_crop(row, top=250, bottom=334, left=33, right=33):
    sx = int(round(row['px'] - row['cam_x'] + 320))
    return play(row['f']).crop((sx - left, top, sx + right, bottom))


# ---------------------------------------------------------------- beats
def build():
    rows = capture_rows()
    remotion('B00')
    remotion('B29')
    remotion('B01')
    remotion('B28', brandLabel='@NikBearBrown', artifactLines=[
        'Built: the run clip (4 cells, 10 fps, LOOP_LINEAR, discrete), the lunge rig and clip (89 ticks, LOOP_NONE) and '
        'the torch flicker, each owned by one AnimationPlayer on the physics callback; the growl cancel; embers and the '
        'afterimage; the pin, edges, read-back, structure and afterimage tests.',
        'Measured: pin 16 / 0 at 30, 60, 144 with the clips wired; the change differs only in hit_growl and kill, '
        're-pinned after play (ff71bbb); edges 13 / 0 at 30, 60, 144; mutations a7-2 to a7-5 caught, a7-1 harmless '
        'on 4.7.2.',
        'Judged by the author in play: run r2 kept (r1 rejected), the lunge in both facings, the growl cancel and its '
        '0.2 s window, visual upgrades r1 kept (r0 not noticeable).',
        'Open: in-between frames so the planted foot stops sliding; whether the growl window should be wider.',
        'The author: clips, rule, verdicts, Gemini images · Claude Code: pin, clips, tests, harnesses, upgrades, '
        'figures, this film · claude.ai: brief and documents · source f860fed'])
    BEATS['B30']['shot']['remotion']['props']['durationSeconds'] = nframes('B30') / FPS

    # B02 — before and after at tick 40 (fixture captures of the take_lunge pin scenario).
    still('B02', cards.identity('Before and after: the same tick of the same scripted lunge',
        'Fixture capture · tests/capture_look.gd places the mage (780) and the wolf (860): the pin’s take_lunge, no input', {
            'img': cap('look/take_lunge_t40_before.png'), 'badge': 'Before A7 · 2276069 · tick 40', 'crop': (150, 140, 640, 360),
            'caption': 'captures/look/take_lunge_t40_before.png, crop x 150–640, y 140–360',
            'rows': [('Before', 'one static lunge image, flipped and slid forward; the cave unlit')]}, {
            'img': cap('look/take_lunge_t40_now.png'), 'badge': 'Now · tick 40', 'crop': (150, 140, 640, 360),
            'caption': 'captures/look/take_lunge_t40_now.png, crop x 150–640, y 140–360',
            'rows': [('Now', 'the keyed cutout rig mid-stretch with its afterimage; two flickering torches; embers. '
                             'Gameplay identical on every tick (pin 16 / 0 at 30, 60, 144).')]},
        'captures/look/ (README.md image before_after.png) · tests/capture_look.gd · TEST-REPORT.md → Pin first'),
        caps_prov('look/take_lunge_t40_before.png', 'look/take_lunge_t40_now.png'))

    BEATS['B03']['shot']['evidence_media'] = 'media/B03.mp4'
    BEATS['B04']['shot']['evidence_media'] = 'media/B04.mp4'
    BEATS['B05']['shot']['evidence_media'] = 'media/B05.mp4'

    # B06 — clip 2 route and source: regions and pivots on wolf_lunge.png, beside Muybridge plate 707.
    wolf_png = Image.open(SRC / 'assets/sprites/wolf/wolf_lunge.png').convert('RGBA')
    bg = Image.new('RGBA', wolf_png.size, (246, 243, 236, 255))
    wolf_img = Image.alpha_composite(bg, wolf_png).convert('RGB')
    dog = Image.open(GAME / 'design/a7/reference/Animal_locomotion._Plate_707_(Boston_Public_Library).jpg').convert('RGB')

    def rig_marks(d, ox, oy, k):
        for (x, y, w, h), col, lab, below in (((0, 0, 40, 40), AMBER, 'Rear · Rect2(0, 0, 40, 40)', True),
                                              ((36, 0, 44, 40), RED, 'Front · Rect2(36, 0, 44, 40)', False)):
            d.rectangle([ox + x * k, oy + y * k + (6 if below else 0), ox + (x + w) * k - 1, oy + (y + h) * k - 1 - (0 if below else 6)],
                        outline=col, width=10)
        for (px, py), lab in (((29, 16), 'hip · RearPivot (−11, −22)'), ((55, 16), 'shoulder · FrontPivot (15, −22)')):
            cx, cy = ox + px * k, oy + py * k
            d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=SPARK, outline='#FFFFFF', width=6)
            f = F('sans_med', 44)
            tw = d.textlength(lab, font=f)
            lx = min(cx - tw / 2 - 26, ox + 80 * k - tw - 52)
            d.rounded_rectangle([lx, cy + 40, lx + tw + 52, cy + 116], radius=38, fill=(61, 57, 41))
            d.text((lx + 26, cy + 52), lab, font=f, fill='#FAF9F5')

    def b06(v):
        im, d, y = cards.base('Clip 2 · a cutout rig from the A2 lunge image', 'Route: cutout rig keyed as resource text in '
                              'features/wolf/wolf.tscn · source: assets/sprites/wolf/wolf_lunge.png (A2, unchanged)')
        lw = 2000
        pic, k = scaled(wolf_img, lw, 1000, pixel=True)
        cards.paste_framed(im, d, pic, SAFE_L, y + 10)
        rig_marks(d, SAFE_L, y + 10, k)
        ty = text_block(d, SAFE_L, y + 10 + pic.height + 20, f'wolf_lunge.png, 80×40, enlarged ×{k}, nearest neighbour; '
                        'outlines: the two region_rects (4 px overlap at x 36–40); dots: the pivots in image pixels '
                        '(29, 16) and (55, 16)', F('sans', 38), lw, INK_SOFT, 50)
        notes_block(d, SAFE_L, ty + 30, lw, [
            ('Nodes (wolf.tscn:216–245)', 'Facing → Rig → RearPivot / FrontPivot → Rear / Front'),
            ('Who writes what', 'code: Facing.scale.x = facing · clip: Rig position and scale, pivot rotations')], v)
        rx = SAFE_L + lw + 90
        dp, _ = scaled(dog, SAFE_R - rx, 1050)
        cards.paste_framed(im, d, dp, rx, y + 10)
        text_block(d, rx, y + 10 + dp.height + 20, 'Motion reference: Eadweard Muybridge, Animal Locomotion (1887), plate '
                   '707, dog galloping · public domain · design/a7/reference/ (reference only, nothing drawn from it)',
                   F('sans', 40), SAFE_R - rx, INK_SOFT, 54)
        cards.footer(d, 'features/wolf/wolf.tscn:216–245 · tests/test_clip_lunge.gd (parts-are-regions, pivots-at-measured-'
                        'hip-and-shoulder: PASS) · SOURCES.md')
        return im
    still('B06', fit(b06, (60, 56, 52, 48, 44)), {
        'images': ['assets/sprites/wolf/wolf_lunge.png', 'design/a7/reference/Animal_locomotion._Plate_707_(Boston_Public_Library).jpg'],
        'sha256': {'wolf_lunge.png': sha256(SRC / 'assets/sprites/wolf/wolf_lunge.png'),
                   'plate_707': sha256(GAME / 'design/a7/reference/Animal_locomotion._Plate_707_(Boston_Public_Library).jpg')},
        'source': 'wolf.tscn:216-245; logs/test_clip_lunge_60fps.log lines 16-17'})

    # B07 -> B08: the rig's scale track, then the read-back and the logged poses.
    wolf_tscn = 'features/wolf/wolf.tscn'
    workbench('B07', 'Clip 2 · the phase table becomes keys', wolf_tscn, 99, 110, 'tracks/3/type', [
        ('Measured phase table (CHANGE-BRIEF revision 2026-11-10)', 'GROWL 31 · LUNGE 22 · RECOVER 36 ticks'),
        ('Key frames ÷ 60 (all four pose tracks)', '0, 25, 31, 37, 53, 65, 89 → 0, 0.4167, 0.5167, 0.6167, 0.8833, '
                                                  '1.0833, 1.4833 s')],
        [(0.0, 102, 'Line 102: the track keys Facing/Rig:scale'),
         ('The keys follow it', 106, 'Line 106: key times = frame ÷ 60'),
         ('crouch, stretch', 109, 'Line 109: (1.08, 0.86) crouch · (1.22, 0.84) stretch · (0.94, 1.06) overshoot')],
        font=23)
    lunge_rows = [('every-track-resolves-to-a-real-node-and-property', 'PASS · no problems'),
                  ('lunge-key-times-equal-frames-over-60', 'PASS · frames 0, 25, 31, 37, 53, 65, 89'),
                  ('lunge-length-89-over-60-loop-none', 'PASS · 1.48333 s, loop_mode 0'),
                  ('lunge-poses-match-table', 'PASS'),
                  ('one-animation-player-physics-no-autoplay', 'PASS · callback 0 (physics), autoplay empty'),
                  ('WALKER TESTS', '17 checks / 0 failures')]
    still('B08', figure_left_notes('Clip 2 · read back, and logged in the game', FIXTURE + ' · ' + RESULTS,
        cap('figures/lunge_onion.png'),
        'captures/figures/lunge_onion.png: rig values logged per tick in the game by tests/capture_lunge.gd (fixture: the '
        'harness places the mage), overlaid at the keys 0, 25, 37, 65',
        [(k, v) for k, v in lunge_rows], 'logs/test_clip_lunge_60fps.log · captures/lunge/game-r0/ · TEST-REPORT.md → Clip '
        'read-backs', frac=0.5),
        caps_prov('figures/lunge_onion.png'), evidence=True)

    # B09 — clip 1 route and source: the four-cell sheet beside Muybridge plate 60.
    sheet_png = Image.open(SRC / 'assets/sprites/mage/mage_run_cycle_sheet.png').convert('RGBA')
    sheet_img = Image.alpha_composite(Image.new('RGBA', sheet_png.size, (246, 243, 236, 255)), sheet_png).convert('RGB')
    runner = Image.open(GAME / 'design/a7/reference/Man_in_pelvis_cloth_running_at_a_half-mile_gait_(rbm-QP301M8-1887-060).jpg')
    runner.draft('RGB', (2400, 2000))
    runner = runner.convert('RGB')
    runner.thumbnail((2400, 2400))

    def b09(v):
        im, d, y = cards.base('Clip 1 · four cells on one sheet', 'Route: Sprite2D with an AnimationPlayer frame track · '
                              'source: assets/sprites/mage/mage_run_cycle_sheet.png')
        lw = 2050
        pic, k = scaled(sheet_img, lw, 760, pixel=True)
        cards.paste_framed(im, d, pic, SAFE_L, y + 10)
        for i, name in enumerate(['0 contact', '1 down', '2 passing', '3 up']):
            x = SAFE_L + i * 62 * k
            if i:
                d.line([x, y + 10, x, y + 10 + pic.height], fill=SPARK, width=6)
            cards.badge(d, x + 16, y + 26, name, size=40)
        ty = text_block(d, SAFE_L, y + 10 + pic.height + 20, f'248×69, cells 62×69, hframes 4, enlarged ×{k}, nearest '
                        'neighbour', F('sans', 40), lw, INK_SOFT, 54)
        notes_block(d, SAFE_L, ty + 30, lw, [
            ('Drawn (SOURCES.md)', 'in the Gemini app from the author’s prompt v3, with the A2 contact sprite as the only '
                                   'reference; raw output design/a7/mage_run_cycle_gemini_raw.jpg'),
            ('Cleaned', 'tools/clean_run_cycle.py: onto the A2 palette, at the A2 size, torsos aligned to contact A')], v)
        rx = SAFE_L + lw + 90
        rp, _ = scaled(runner, SAFE_R - rx, 1130)
        cards.paste_framed(im, d, rp, rx, y + 10)
        text_block(d, rx, y + 10 + rp.height + 20, 'Motion reference: Muybridge, Animal Locomotion (1887), plate 60, a man '
                   'running · public domain · design/a7/reference/', F('sans', 40), SAFE_R - rx, INK_SOFT, 54)
        cards.footer(d, 'CHANGE-BRIEF.md revision 2026-11-12 (run cycle replaced) · SOURCES.md · design/a7/reference/SOURCES.md')
        return im
    still('B09', fit(b09, (60, 56, 52, 48, 44)), {
        'images': ['assets/sprites/mage/mage_run_cycle_sheet.png', 'design/a7/reference/Man_in_pelvis_cloth_running_at_a_half-mile_gait_(rbm-QP301M8-1887-060).jpg'],
        'sha256': {'mage_run_cycle_sheet.png': sha256(SRC / 'assets/sprites/mage/mage_run_cycle_sheet.png'),
                   'plate_60': sha256(GAME / 'design/a7/reference/Man_in_pelvis_cloth_running_at_a_half-mile_gait_(rbm-QP301M8-1887-060).jpg')}})

    # B10 -> B11: the run clip's frame track, then the run cell by cell in the capture.
    ptscn = 'features/player/player.tscn'
    workbench('B10', 'Clip 1 · the run clip in the scene file', ptscn, 93, 101, 'tracks/2/path', [
        ('Lines 64–65', 'length = 0.4 · loop_mode = 1 (LOOP_LINEAR)'),
        ('Line 88', 'Sprite2D:hframes = 4 (four cells)')],
        [(0.0, 93, 'Line 93: the track keys Sprite2D:frame'),
         ('cells zero to three', 97, 'Line 97: keys at 0, 0.1, 0.2, 0.3 s'),
         ('No duplicate cell', 100, 'Line 100: cells 0, 1, 2, 3 · line 99: update 1 = discrete')], font=32)
    run_rows = [r for r in rows if 20 <= r['f'] <= 44]
    items = [(mage_crop(r, left=31, right=19), f"f{r['f']} · cell {r['pfr']}", i == 0 or r['pfr'] != run_rows[i - 1]['pfr'])
             for i, r in enumerate(run_rows)]

    def b11(v):
        im, d, y = cards.base('Clip 1 · the run, cell by cell', PLAY + ' · frames 20–44, one per physics tick')
        b1, k = crops_row(im, d, items[:13], SAFE_L, y + 10, SAFE_R - SAFE_L, 470, cap_size=34)
        b2, _ = crops_row(im, d, items[13:], SAFE_L, b1 + 20, int((SAFE_R - SAFE_L) * 12 / 13), 470, cap_size=34)
        ty = text_block(d, SAFE_L, b2 + 10, f'Crops of the 640×360 frames around the mage, enlarged ×{k}, nearest neighbour; '
                        'outlined in orange: the tick a new cell appears (sheet cell from capture/run-01-frames.jsonl)',
                        F('sans', 38), SAFE_R - SAFE_L, INK_SOFT, 50)
        cards.table(d, SAFE_L, ty + 24, [1300, 2156], ['Ticks per cell', ''],
                    [('This capture (frames 20–116)', '0:6, 1:6, 2:6, 3:7 on entry, then 0:5, 1:6, 2:6, 3:7 every loop'),
                     ('captures/run/game-r2-ticks/', '6 / 6 / 6 / 7 on entry, 5 / 6 / 6 / 7 per loop (TUNING.md r2)'),
                     ('test_clip_run.gd', '16 / 0: keys 0, 0.1, 0.2, 0.3; length 0.4; LOOP_LINEAR; discrete')], size=v, head_size=int(v * 0.8))
        cards.footer(d, 'capture/run-01 (scripted input) · logs/test_clip_run_60fps.log · TUNING.md → Run cycle r2')
        return im
    still('B11', fit(b11, (52, 48, 46, 44, 42, 40)), {'images': [f'capture/run-01 frames 20-44'],
          'capture_sha256': sha256(REEL / 'capture' / 'run-01.mp4'), 'frame_log': 'capture/run-01-frames.jsonl'}, evidence=True)

    # B12 -> B13: one authority, then the landing restart in the capture.
    pgd = 'features/player/player.gd'
    workbench('B12', 'One authority: the state machine only calls play()', pgd, 143, 154, 'func _set_state', [
        ('test_anim_structure.gd · 11 / 0', 'no game script writes a property a clip keys'),
        ('player.tscn:416–417', 'process_physics_priority = -1 · callback_mode_process = 0 (physics)')],
        [(0.0, 143, 'Line 143: _set_state(next)'),
         ('a state\'s clip starts', 147, 'Lines 144–147: play only when the state (or clip) changes'),
         ('flip h stays in code', 148, 'Line 148: flip_h stays in code'),
         ('from zero', 154, 'Lines 152–154: play(clip), seek(0.0, true)')], font=25)
    land = [r for r in rows if 340 <= r['f'] <= 351]
    items = [(mage_crop(r, top=226, bottom=334, left=31, right=19), f"f{r['f']}" + '\n' + f"{r['ps']} · {r['pfr']}",
              r['f'] == 346) for r in land]

    def b13(v):
        im, d, y = cards.base('Land, run, cell zero', PLAY + ' · frames 340–351')
        b1, k = crops_row(im, d, items, SAFE_L, y + 10, SAFE_R - SAFE_L, 760, cap_size=38)
        ty = text_block(d, SAFE_L, b1 + 10, f'Crops around the mage, enlarged ×{k}, nearest neighbour; state · sheet cell '
                        'from capture/run-01-frames.jsonl; orange: the landing tick (FALL → RUN at frame 346, cell 0)',
                        F('sans', 38), SAFE_R - SAFE_L, INK_SOFT, 50)
        cards.table(d, SAFE_L, ty + 30, [1500, 1956], ['Check', 'Result'],
                    [('test_anim_structure.gd · run-reentry-restarts-at-frame-0', 'PASS · 11 checks / 0 failures'),
                     ('test_anim_edges.gd · run → jump → land → run', 'PASS at 30, 60, 144 · re-entry tick 71, cell 0, clip '
                                                                    'position 0.0')], size=v, head_size=int(v * 0.8))
        cards.footer(d, 'capture/run-01 · logs/test_anim_structure_60fps.log · logs/test_anim_edges_60fps.log')
        return im
    still('B13', fit(b13, (56, 52, 48, 44, 40)), {'images': ['capture/run-01 frames 340-351'],
          'capture_sha256': sha256(REEL / 'capture' / 'run-01.mp4')}, evidence=True)

    # B14 — pin first: the commit sequence.
    still('B14', table_card('Pin first: record, add, wire, change, play, re-pin', RESULTS + ' · git log · TEST-REPORT.md',
        ['Commit', 'Step', 'Pin (tests/test_pin_behaviour.gd)'],
        [('2276069', 'Baseline: 13 earlier suites', '19 runs, 0 failures'),
         ('a9b4bc1', 'Pin recorded: 8 scenarios, every physics tick, real input', '16 / 0 at 30, 60, 144'),
         ('72e8d21', 'Clips added, not wired', 'unchanged'),
         ('33d78ae', 'Clips wired into both state machines', 'unchanged'),
         ('72f37b8', 'The one change: a growl hit cancels the lunge', 'differs only in hit_growl and kill, from tick 24'),
         ('—', 'Played by the author; accepted', 'TEST-REPORT.md → Human checks'),
         ('ff71bbb', 'Re-pinned, in its own commit', 'hit_growl.json, kill.json changed; 16 / 0 at 30, 60, 144'),
         ('a1b6f44 · 7a9a65e · 272fb39', 'Visual upgrades, alignment fixes', '16 / 0 at 30, 60, 144 after each')],
        [900, 1350, 1206],
        'Recorded per tick: the mage’s state, position and velocity; the wolf’s state, position, HP and hitbox monitoring. '
        'Before the re-pin, 32eed66 (run r2) shows 14 / 16: the two known differences.',
        'git log · logs/pin/*.json · logs/test_pin_behaviour_*fps.log · TEST-REPORT.md → Pin first', hi_cols=(0,)),
        {'card': 'media/B14.png', 'source': 'TEST-REPORT.md:7-21; git log; 32eed66 commit message'})

    # B15 -> B16: the change, then what the pin saw.
    wgd = 'features/wolf/wolf.gd'
    workbench('B15', 'The one behaviour change: a growl hit cancels the lunge', wgd, 152, 163, 'func take_damage', [
        ('Line 24', 'const RECOVER_FRAME := 53'),
        ('Lines 164–171', 'the last HP: DEAD in every phase')],
        [(0.0, 158, 'Line 158: only during GROWL'),
         ('sends the wolf to recover', 159, 'Line 159: straight to RECOVER'),
         ('seeks the clip', 162, 'Line 162: seek to frame 52, so the hit tick shows 53'),
         ('Every other phase', 163, 'Line 163: any other phase: HP only')], font=24)
    still('B16', figure_left_notes('What the pin saw', FIGLABEL + ' · logs/pin/hit_growl.json',
        cap('figures/pin_timeline.png'),
        'captures/figures/pin_timeline.png: hit_growl before (a9b4bc1) and after (ff71bbb); one cast at tick 4, the hit '
        'on tick 24', [
            ('hit_growl', 'from tick 24: GROWL → RECOVER; no lunge, hitbox never armed'),
            ('kill (not predicted)', 'its first hit also lands in GROWL, so its second fireball now misses'),
            ('Re-pin, ff71bbb, after play', 'only hit_growl.json and kill.json changed; the other six byte-identical; '
                                            '16 / 0 at 30, 60, 144')],
        'TEST-REPORT.md → Pin first · FRICTIONAL.md → Predictions · git show --stat ff71bbb', frac=0.68),
        caps_prov('figures/pin_timeline.png'), evidence=True)

    # B17 — edges.
    still('B17', table_card('Edges at the phase boundaries', RESULTS + ' · tests/test_anim_edges.gd · real clicks',
        ['Case (reference: growl from tick 80, lunge 111, recover 133)', 'Result'],
        [('Hit on the first and on the last GROWL tick', 'cancel: RECOVER on the hit tick, clip frame 53, hitbox never armed'),
         ('Hit on the first and on the last LUNGE tick', 'no cancel: states, positions and clip as the unhit run'),
         ('Hit on the first RECOVER tick', 'only HP changes'),
         ('Killing hit in GROWL, LUNGE, RECOVER', 'DEAD, dead clip, hitbox off from the next tick'),
         ('Real Esc mid-lunge', 'position, state and clip freeze on the same tick; resume aligned'),
         ('Run → jump → land → run', 'the cycle restarts at frame 0'),
         ('Clip frame = ticks since the clip began', 'all 119 ticks checked: 89 of one growl-lunge-recover, 30 of the next '
                                                     'growl')],
        [1700, 1756], '13 checks / 0 failures at 30, 60 and 144 fps.',
        'logs/test_anim_edges_30fps.log · _60fps.log · _144fps.log · TEST-REPORT.md → Edges'),
        {'card': 'media/B17.png', 'source': 'logs/test_anim_edges_{30,60,144}fps.log'})

    # B18 — two alignment bugs, with this capture's evidence.
    still('B18', line_panels('Two alignment bugs the read-backs could not see', SRCVIEW + ' · fixes in 272fb39', [
        ('1 · Found by the edges test: a cancel drew clip frame 54 on the hit tick', [[(wgd, 162, line(wgd, 162, 'anim.seek'))]],
         'The hit is handled before the tick’s update, and the clip then advances once: seeking frame 52 makes the hit tick '
         'show 53. In capture/run-01 the cancel tick (frame 1549) shows RECOVER, clip frame 53.'),
        ('2 · Seen in a capture’s tick log: after a one-tick patrol, a growl began at frame 1', [[
            (wolf_tscn, 248, line(wolf_tscn, 248, 'process_physics_priority')),
            (ptscn, 416, line(ptscn, 416, 'process_physics_priority'))]],
         'Spotted in the windowed lunge capture’s tick log; both AnimationPlayers now run before their owner’s script. The '
         'edges check was then extended; with the setting '
         'removed it fails on tick 170. In capture/run-01, PATROL lasts one tick (frame 969) and the growl starts at clip '
         'frame 0 (frame 970).')],
        'CHANGE-BRIEF.md revision 2026-11-12 (two clip-alignment fixes) · TEST-REPORT.md → Edges · capture/run-01-frames.jsonl'),
        {'card': 'media/B18.png', 'source': 'wolf.gd:162; wolf.tscn:248; player.tscn:416; run-01-frames.jsonl 969-970, 1549'})

    # B19 — mutations.
    still('B19', table_card('Broken on purpose', RESULTS + ' · each in a temporary git worktree, removed',
        ['Mutation', 'Caught by', 'Log'],
        [('a7-1 · run clip written with Godot 3 loop = true', 'not caught: 4.7.2 loads it as loop_mode 1, the run still loops '
                                                            '(predicted failure F1 does not occur)', '16 / 0'),
         ('a7-2 · run frame track continuous', 'test_clip_run · every-track-discrete', '1 failure'),
         ('a7-3 · run frame key 4, past the last cell', 'test_clip_run · frame range and frame keys', '2 failures'),
         ('a7-4 · lunge track to a missing node', 'track_problems(): no node at FrontPivotX', '2 failures'),
         ('a7-5 · growl cancel removed', 'test_anim_edges: the lunge continues, hitbox armed 23 ticks', '2 failures')],
        [1300, 1556, 600], 'None printed an error from the game: a7-2 to a7-4 would play silently wrong.',
        'logs/mutation-a7-1-…-5-*_60fps.log · TEST-REPORT.md → Mutations'),
        {'card': 'media/B19.png', 'source': 'logs/mutation-a7-*_60fps.log'})

    # B20 — growl window and two clocks.
    def b20(v):
        im, d, y = cards.base('The growl window, and a second clock', FIGLABEL)
        gw = cap('figures/growl_window.png')
        tc = cap('figures/two_clocks.png')
        lw = 1640
        gp, _ = scaled(gw, lw, 1930 - (y + 10) - 120)
        cards.paste_framed(im, d, gp, SAFE_L, y + 10)
        text_block(d, SAFE_L, y + 10 + gp.height + 16, 'captures/figures/growl_window.png · tests/probe_growl_cancel.gd, '
                   'real clicks', F('sans', 36), lw, INK_SOFT, 46)
        rx = SAFE_L + lw + 80
        tp, _ = scaled(tc, SAFE_R - rx, 900)
        cards.paste_framed(im, d, tp, rx, y + 10)
        ty = text_block(d, rx, y + 10 + tp.height + 16, 'captures/figures/two_clocks.png · pin kill scenario',
                        F('sans', 36), SAFE_R - rx, INK_SOFT, 46)
        notes_block(d, rx, ty + 30, SAFE_R - rx, [
            ('Growl window (kept by the author)', 'from sight distance (dx 118.75) the fireball needs 20 ticks: only casts '
                                                  'in the first 12 of 31 growl ticks (0.2 s) cancel'),
            ('Second clock (kept: gameplay never reads it)', 'removal after death: a create_timer on the frame clock '
                                                            '(wolf.gd:170) — tick 79 at 60 fps, 80 at 30 and 144')], v)
        cards.footer(d, 'TUNING.md · CHANGE-BRIEF.md revisions 2026-11-10 and 2026-11-12 · FRICTIONAL.md')
        return im
    still('B20', fit(b20, (60, 56, 52, 48, 44, 40)), caps_prov('figures/growl_window.png', 'figures/two_clocks.png'))

    # B21 — run r0 and three dead ends.
    rc = cap('figures/run_cycle.png')
    def b21(v):
        im, d, y = cards.base('The run, r0, and three dead ends', FIXTURE + ' · captures/run/')
        r0 = rc.crop((0, 60, 700, 440))
        lw = 1680
        p0, _ = scaled(r0, lw, 820)
        cards.paste_framed(im, d, p0, SAFE_L, y + 10)
        ty = text_block(d, SAFE_L, y + 10 + p0.height + 14, 'captures/figures/run_cycle.png, r0: the two A2 frames at 8 fps, '
                        'ticks per frame 8 8 7 8 7 8 7 8 6 …', F('sans', 36), lw, INK_SOFT, 46)
        notes_block(d, SAFE_L, ty + 26, lw, [
            ('r0 in the game (captures/run/game-r0/)', 'a 1 px hat hop; each pose held 7–8 ticks while the body moves '
                                                        '1.83 px per tick: the planted foot slides 13–15 px, then snaps back')], v)
        rx = SAFE_L + lw + 80
        cb = cap('run/analysis/contact_b_compare_8x.png').crop((0, 0, 2032, 600))
        pc, _ = scaled(cb, SAFE_R - rx, 640)
        cards.paste_framed(im, d, pc, rx, y + 10)
        ty2 = text_block(d, rx, y + 10 + pc.height + 14, 'captures/run/analysis/contact_b_compare_8x.png: Gemini contact B '
                         'against contact A; magenta = the 103 px that differ, all in the trailing leg', F('sans', 36),
                         SAFE_R - rx, INK_SOFT, 46)
        notes_block(d, rx, ty2 + 26, SAFE_R - rx, [
            ('Rejected (TUNING.md, 26932e1)', 'mirroring the leg region: a kick, boots pointing back · Gemini contact B, '
                                              'twice: the same foot forward · darkening the far leg: 19 px, invisible at 2×')], v)
        cards.footer(d, 'TUNING.md → Run cycle r0 · FRICTIONAL.md → Struggle and revision · captures/run/analysis/')
        return im
    still('B21', fit(b21, (60, 56, 52, 48, 44, 40)), caps_prov('figures/run_cycle.png', 'run/analysis/contact_b_compare_8x.png'))

    # B22 — r1 rejected in play, r2 kept.
    def b22(v):
        im, d, y = cards.base('The run: r1 rejected in play, r2 kept', FIXTURE + ' · captures/run/')
        r1 = cap('run/analysis/run_r1_beats_vs_r0_6x.png')
        p1, _ = scaled(r1, SAFE_R - SAFE_L, 470)
        cards.paste_framed(im, d, p1, SAFE_L, y + 10)
        ty = text_block(d, SAFE_L, y + 10 + p1.height + 14, 'captures/run/analysis/run_r1_beats_vs_r0_6x.png: r0 and r1 '
                        'at each of r1’s four beats (game strip, debug collisions on)', F('sans', 36), SAFE_R - SAFE_L,
                        INK_SOFT, 46)
        r2 = rc.crop((0, 480, 1060, 850))
        lw = 1900
        p2, _ = scaled(r2, lw, 1930 - (ty + 30) - 60)
        cards.paste_framed(im, d, p2, SAFE_L, ty + 30)
        text_block(d, SAFE_L, ty + 30 + p2.height + 12, 'captures/figures/run_cycle.png, r2', F('sans', 36), lw, INK_SOFT, 46)
        rx = SAFE_L + lw + 80
        notes_block(d, rx, ty + 30, SAFE_R - rx, [
            ('r1 · fc096c9 → reverted 338c8bf', 'a 2 px sink and lift from the same two frames; hat rows 268 / 270 / 267 / '
                                               '265 exactly as predicted; in play: “still looks like the feet twitch”'),
            ('r2 · 32eed66 · kept', 'a four-frame cycle drawn in one image, cleaned onto the A2 palette, 10 fps: '
                                    '“much better”')], v)
        cards.footer(d, 'TUNING.md → Run cycle r1, r2 (the author’s words, translated from Chinese) · FRICTIONAL.md')
        return im
    still('B22', fit(b22, (60, 56, 52, 48, 44, 40)), caps_prov('run/analysis/run_r1_beats_vs_r0_6x.png', 'figures/run_cycle.png'))

    # B23 -> B24: the flicker clip, then the flicker measured in the capture.
    lights = 'effects/cave_lights.tscn'
    workbench('B23', 'Beyond the requirements: the torch flicker clip', lights, 19, 30, 'tracks/0/type', [
        ('Lines 75–89', 'PointLight2D energy: TorchLeft 1.6 · TorchRight 1.5'),
        ('Lines 16–18', 'flicker · length = 2.4 · loop_mode = 1 (LOOP_LINEAR) · autoplay (line 95)')],
        [(0.0, 22, 'Line 22: the track keys TorchLeft:energy'),
         ('continuous tracks', 23, 'Lines 23 and 28: interp 2, update 0 (continuous)'),
         ('Its seam', 29, 'Line 29: the first and the last value are both 1.6')], font=23)
    pool = []
    for n in range(0, 441):            # frames 441-442 are empty: the scene was freed between segments
        a = np.asarray(play(n)).astype(float)
        pool.append(float(a[110:190, 40:120].mean()))
    T = [0, 0.13, 0.31, 0.47, 0.7, 0.88, 1.07, 1.33, 1.58, 1.81, 2.06, 2.4]
    V = [1.6, 1.2, 1.95, 1.3, 2.08, 1.45, 1.12, 1.85, 1.25, 2.0, 1.35, 1.6]
    best = None
    for off in range(-3, 4):
        e = np.interp(((np.arange(441) - off) / 60.0) % 2.4, T, V)
        c = float(np.corrcoef(pool, e)[0, 1])
        if best is None or c > best[0]:
            best = (c, off, e)
    corr, off, energy = best
    assert corr > 0.9, corr

    def b24(v):
        im, d, y = cards.base('The flicker, measured in the capture', PLAY + ' · frames 0–440')
        x0, y0, pw, ph = SAFE_L + 120, y + 40, 2300, 1050
        d.rectangle([x0, y0, x0 + pw, y0 + ph], outline=BORDER, width=4)
        lo, hi = min(pool), max(pool)
        elo, ehi = 1.1, 2.1
        def px(i):
            return x0 + i / 440 * pw
        pts = [(px(i), y0 + ph - (p - lo) / (hi - lo) * ph * 0.9 - ph * 0.05) for i, p in enumerate(pool)]
        ept = [(px(i), y0 + ph - (e - elo) / (ehi - elo) * ph * 0.9 - ph * 0.05) for i, e in enumerate(energy)]
        d.line(ept, fill=SPARK, width=8)
        d.line(pts, fill=INK, width=5)
        for t in (0, 2.4, 4.8, 7.2):
            xx = px(t * 60)
            if xx <= x0 + pw:
                d.line([xx, y0, xx, y0 + ph], fill=BORDER, width=3)
                d.text((xx - 30, y0 + ph + 14), f'{t:g} s', font=F('sans', 38), fill=INK_SOFT)
        d.text((x0, y0 - 64), f'black: mean brightness of the left torch’s pool (screen x 40–120, y 110–190), {lo:.0f}–{hi:.0f} '
               'of 255 · orange: the clip’s TorchLeft:energy keys, 1.12–2.08 (linear between keys)', font=F('sans', 36),
               fill=INK_SOFT)
        crops = [(play(n).crop((0, 70, 200, 230)), f'frame {n}', False) for n in (int(np.argmin(pool[:150])), int(np.argmax(pool[:150])))]
        rx = x0 + pw + 80
        b, k = crops_row(im, d, crops, rx, y0, SAFE_R - rx, 560, cap_size=38)
        notes_block(d, rx, b + 30, SAFE_R - rx, [
            ('Correlation with the keys', f'{corr:.2f} (best of offsets −3…+3 frames: {off:+d})'),
            ('test_clip_flicker.gd', '11 / 0 · seam: value at 0 = value at 2.4 s on every track')], v)
        cards.footer(d, f'capture/run-01 frames 0–440 · effects/cave_lights.tscn:15–30 · logs/test_clip_flicker_60fps.log · '
                        f'crops enlarged ×{k}')
        return im
    still('B24', fit(b24, (60, 56, 52, 48, 44)), {'images': ['capture/run-01 frames 0-440'],
          'capture_sha256': sha256(REEL / 'capture' / 'run-01.mp4'), 'measure': 'mean RGB of crop (40,110)-(120,190) per frame',
          'correlation': round(corr, 4), 'offset_frames': off}, evidence=True)
    EV.mkdir(exist_ok=True)
    save_json(EV / 'torch-flicker-measurement.json', {
        'source': 'capture/run-01 frames 0-440 (segment "run")', 'region': [40, 110, 120, 190],
        'clip_track': 'effects/cave_lights.tscn TorchLeft:energy (lines 26, 29), linear interpolation between keys',
        'correlation': round(corr, 4), 'best_offset_frames': off, 'mean_brightness': [round(p, 3) for p in pool]})

    # B25 — embers, afterimage, readability.
    ghost_row = rows[926]
    sx = int(round(ghost_row['wx'] - ghost_row['cam_x'] + 320))
    g = play(926).crop((sx - 130, 250, sx + 90, 335))

    def b25(v):
        im, d, y = cards.base('Beyond the requirements: embers, afterimage, readability', PLAY + ' · frame 926')
        lw = 2000
        pg, k = scaled(g, lw, 900, pixel=True)
        cards.paste_framed(im, d, pg, SAFE_L, y + 10)
        ty = text_block(d, SAFE_L, y + 10 + pg.height + 16, f'capture/run-01 frame 926: LUNGE, {ghost_row["ghosts"]} ghosts '
                        f'alive (frame log); enlarged ×{k}, nearest neighbour', F('sans', 38), lw, INK_SOFT, 50)
        full, _ = scaled(play(926), lw, 1930 - (ty + 30))
        cards.paste_framed(im, d, full, SAFE_L, ty + 24)
        rx = SAFE_L + lw + 90
        notes_block(d, rx, y + 10, SAFE_R - rx, [
            ('Afterimage (wolf.tscn:254–259)', 'a ghost every 3 LUNGE ticks, alpha 0.6, life 0.25 s, tint (1, 0.55, 0.2); '
                                              'test_afterimage 6 / 0 at 30, 60, 144'),
            ('Embers (embers.tscn)', '144 particles, lifetime 9 s'),
            ('Readability (TUNING.md)', 'robe-to-cave contrast 2.74 before A7 → 2.57 at r0 → 3.07 at r1'),
            ('The author, in the game', 'r0 “not noticeable” · r1 “clearly visible”: kept'),
            ('Pin after each', '16 / 0 at 30, 60, 144')], v)
        cards.footer(d, 'features/wolf/wolf.tscn · effects/embers.tscn · TUNING.md → Visual upgrades · logs/test_afterimage_*')
        return im
    still('B25', fit(b25, (56, 52, 48, 46, 44, 40)), {'images': ['capture/run-01 frame 926'],
          'capture_sha256': sha256(REEL / 'capture' / 'run-01.mp4')})

    # B26 — limitations.
    still('B26', columns('Limitations', 'README.md → Known limitations · FRICTIONAL.md → Still open · this film', [
        ('In the game', [
            ('', 'The planted foot still slides while a cell is held.'),
            ('', 'The growl window is 0.2 s from sight distance, kept by the author.'),
            ('', 'The wolf’s removal after death runs on the frame clock (gameplay never reads it).')]),
        ('In this film', [
            ('', 'Gameplay is scripted input, not a human playtest.'),
            ('', 'How the clips feel is the author’s judgement in play (TEST-REPORT.md → Human checks).'),
            ('', 'Strips and figures marked “fixture” come from harnesses that place the characters.')])],
        'README.md · FRICTIONAL.md · TEST-REPORT.md'),
        {'card': 'media/B26.png', 'source': 'README.md Known limitations; FRICTIONAL.md Still open'})

    # B27 — who did what.
    still('B27', columns('Who did what', f'FRICTIONAL.md → Human and AI contributions · game source revision {BUILD}', [
        ('The author', [
            ('', 'Both clips and their look; the per-phase interrupt rule; keeping the 0.2 s window.'),
            ('', 'Every first look and verdict in the running game; the run images in Gemini; accepting the re-pin.')]),
        ('Claude Code', [
            ('', 'CLAUDE.md drafts, the pin, the clips and rig, read-backs, structure, edges and afterimage tests, probes, '
                 'capture harnesses, cleanup tools, visual upgrades, mutations, figures, measurements; this film.')]),
        ('claude.ai (chat)', [
            ('', 'Planning, commands, the brief and its revisions from the author’s decisions, the Gemini prompts, the '
                 'documents.')])],
        'FRICTIONAL.md · SOURCES.md'),
        {'card': 'media/B27.png', 'source': 'FRICTIONAL.md Human and AI contributions'})


def main():
    global BEATS, PROV
    assert CAPTURE_FRAMES and (CAPTURE_FRAMES / 'frame00000000.png').is_file(), 'set WALKER_CAPTURE'
    MEDIA.mkdir(exist_ok=True)
    sheet = load_json(REEL / 'beat_sheet.json')
    BEATS = {b['beat_id']: b for b in sheet['beats']}
    PROV = {}
    build()
    save_json(REEL / 'beat_sheet.json', sheet)
    footage = load_json(EV / 'footage-provenance.json')['beats']
    save_json(EV / 'media-provenance.json', {
        'note': f'How each non-Remotion slot was made. Gameplay: capture/run-01 at {BUILD} (scripted input, real engine '
                'output; see CAPTURE.md). Fixtures: the author’s committed captures in captures/ (capture harnesses and '
                'preview scenes that place the characters). Figures: captures/figures/ (tools/make_figures.py).',
        'beats': {**PROV, **footage}})
    print('media built:', ', '.join(sorted(PROV)))


if __name__ == '__main__':
    main()
