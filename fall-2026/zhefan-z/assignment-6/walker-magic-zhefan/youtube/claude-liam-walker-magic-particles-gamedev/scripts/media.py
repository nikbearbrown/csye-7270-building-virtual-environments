"""Phase 2b: build every card slot and fill the Remotion props, using measured narration.

Adapted from the Assignment 5 film's media.py. Images of the game are either frames of the scripted-input capture
(capture/run-01, real engine output) or the author's committed preview strips in captures/ (fixture captures, not
gameplay), enlarged with nearest-neighbour scaling. Figures on cards come from the named source documents; code comes
verbatim from the snapshot of the build shown (3c37fe0). The gameplay beats themselves are built by footage.py.
"""
from PIL import Image, ImageDraw

import cards
from cards import F, wrap, text_block, SAFE_L, SAFE_R, DARK, DARK_TEXT, DARK_MUTED, DARK_HI
from common import (REEL, GAME, A6, CAPS, BUILD, FPS, SNAPSHOT, CAPTURE_FRAMES, INK, INK_SOFT, SPARK, load_json,
                    save_json, render_frames, source_lines, sha256)

MEDIA = REEL / 'media'
EV = REEL / 'evidence'
SRC = SNAPSHOT or GAME

PLAY = 'Scripted input · real engine output · capture/run-01'
FIXTURE = 'Fixture capture · preview scene strip, not gameplay'
RESULTS = 'Recorded results — not a render'
DOC = 'Document view — reconstruction of the text, not a screenshot'
SRCVIEW = 'Source view — reconstruction, not a screenshot'

IMPACT_CROP = (250, 262, 390, 345)     # the preview impact at screen (320, 327), the pit edge to its right
TRAIL_CROP = (110, 240, 450, 290)      # the preview carrier's path, y 267, x 150 -> 410
PLAY_CROP = (10, 215, 290, 355)         # the first cast of capture/run-01: the mage, the fireball and the impact


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


def strip(folder, n):
    return Image.open(CAPS / folder / f'frame{n:08d}.png').convert('RGB')


def play(n):
    return Image.open(CAPTURE_FRAMES / f'frame{n:08d}.png').convert('RGB')


def strips_prov(*items):
    return {'images': [f'captures/{f}/frame{n:08d}.png' for f, n in items],
            'sha256': {f'{f}/{n}': sha256(CAPS / f / f'frame{n:08d}.png') for f, n in items}}


def workbench(bid, title, rel, start, end, first, notes, cues, font=34):
    code = excerpt(rel, start, end, first)
    remotion(bid, mode='code', title=title, project='walker-magic', path=rel,
             source=f'Exact source at {BUILD} · lines {start}–{end} · next: the visible result',
             code=code, startLine=start, codeFontSize=font,
             notes=[{'label': k, 'value': v} for k, v in notes],
             output=[f'Godot editor reconstruction · {rel} lines {start}–{end} · build {BUILD}'],
             cues=[{'at': at(bid, p) if isinstance(p, str) else p, 'line': ln, 'label': lab} for p, ln, lab in cues])
    BEATS[bid]['excerpt'] = {'path': rel, 'start_line': start, 'end_line': end}


def doc_lines(path, start, end, first=None):
    lines = path.read_text(encoding='utf-8').splitlines()[start - 1:end]
    if first:
        assert lines[0].startswith(first), f'{path.name}:{start} does not start with {first!r}'
    return '\n'.join(lines)


def fit(make, sizes):
    """Largest size whose layout passes its own overflow check (FILL-THE-CANVAS: biggest type that fits)."""
    for size in sizes:
        try:
            return make(size)
        except AssertionError:
            continue
    raise AssertionError('no size fits')


def columns(title, chip, cols, src, value_size=None, label_size=None):
    return fit(lambda v: cards.columns(title, chip, cols, src, value_size=v, label_size=int(v * 0.74)),
               (92, 86, 80, 76, 72, 68, 64, 60, 56))


def table_card(title, chip, header, rows, widths, note, src, size=None):
    def make(v):
        im, d, y = cards.base(title, chip)
        ty = cards.table(d, SAFE_L, y + 10, widths, header, rows, size=v, head_size=int(v * 0.74))
        if note:
            ty = text_block(d, SAFE_L, ty + 24, note, F('sans', int(v * 0.84)), SAFE_R - SAFE_L, INK, int(v * 1.1))
        assert ty < 1960
        cards.footer(d, src)
        return im
    return fit(make, (108, 100, 92, 84, 78, 72, 68, 64, 60, 56, 52, 48))


def _grid(im, d, items, crop, x0, y0, width, height, ncols, cap):
    """Enlarged crops in a grid (largest whole factor that fits), each with a caption under it."""
    gap = 50
    n = len(items)
    nrows = -(-n // ncols)
    cw = (width - gap * (ncols - 1)) // ncols
    cw_px, ch_px = crop[2] - crop[0], crop[3] - crop[1]
    fc = F('sans', cap)
    cap_h = max(len(wrap(d, c, fc, cw)) for _, c in items) * int(cap * 1.28) + 16
    k = max(1, min(cw // cw_px, (height - nrows * (cap_h + gap)) // (nrows * ch_px)))
    for i, (img, c) in enumerate(items):
        r, q = divmod(i, ncols)
        x = x0 + q * (cw + gap) + (cw - cw_px * k) // 2
        y = y0 + r * (ch_px * k + cap_h + gap)
        cards.paste_framed(im, d, img.crop(crop).resize((cw_px * k, ch_px * k), Image.NEAREST), x, y)
        text_block(d, x, y + ch_px * k + 12, c, fc, cw, INK, int(cap * 1.28))
    return k, y0 + nrows * (ch_px * k + cap_h + gap)


def strip_grid(title, chip, items, crop, ncols, src, note=None, cap=56):
    """items: [(image, caption)]; one grid of crops filling the card; an optional note under it."""
    im, d, y = cards.base(title, chip)
    nh = 0
    if note:
        nh = len(wrap(d, note, F('sans', 48), SAFE_R - SAFE_L)) * 64 + 30
    k, bottom = _grid(im, d, items, crop, SAFE_L, y + 10, SAFE_R - SAFE_L, 1940 - (y + 10) - nh, ncols, cap)
    ty = text_block(d, SAFE_L, bottom, (note + ' · ' if note else '') + f'crops enlarged ×{k}, nearest neighbour',
                    F('sans', 48), SAFE_R - SAFE_L, INK_SOFT, 64)
    assert ty < 1960, f'{title}: strip_grid overflows ({ty})'
    cards.footer(d, src)
    return im


def grid_beside_table(title, chip, items, crop, header, rows, fracs, src, note=None):
    """A 2x2 grid of enlarged crops on the left, a table (largest type that fits) on the right."""
    def make(v):
        im, d, y = cards.base(title, chip)
        left = int((SAFE_R - SAFE_L) * 0.5)
        k, bottom = _grid(im, d, items, crop, SAFE_L, y + 10, left, 1940 - (y + 10) - 70, 2, 52)
        d.text((SAFE_L, bottom), f'crops of the 640×360 strips, enlarged ×{k}, nearest neighbour', font=F('sans', 44),
               fill=INK_SOFT)
        rx = SAFE_L + left + 90
        rw = SAFE_R - rx
        ty = cards.table(d, rx, y + 10, [int(rw * f) for f in fracs], header, rows, size=v, head_size=int(v * 0.74))
        if note:
            ty = text_block(d, rx, ty + 20, note, F('sans', int(v * 0.84)), rw, INK, int(v * 1.1))
        assert ty < 1960
        cards.footer(d, src)
        return im
    return fit(make, (72, 66, 62, 58, 54, 50, 46, 42))


def doc_columns(title, chip, panels, note, max_size=64):
    """Dark document/source panels side by side: [(header, start_line, text, highlight_lines, width_fraction)]."""
    im, d, y = cards.base(title, chip)
    top, bottom, gap = y + 10, 1935, 48
    total = SAFE_R - SAFE_L - gap * (len(panels) - 1)
    x0 = SAFE_L
    for head, start, text, hi, frac in panels:
        pw = int(total * frac)
        d.rounded_rectangle([x0, top, x0 + pw, bottom], radius=28, fill=DARK)
        raw = text.split('\n')
        for size in (max_size, 60, 56, 52, 48, 46, 43, 40, 37, 34):
            if size > max_size:
                continue
            f = F('mono', size)
            lh = int(size * 1.36)
            rows = [(start + i, part, j == 0) for i, ln in enumerate(raw)
                    for j, part in enumerate(wrap(d, ln.replace('\t', '    ') or ' ', f, pw - 90 - int(size * 2.9)))]
            if top + 110 + len(rows) * lh <= bottom - 20:
                break
        assert top + 110 + len(rows) * lh <= bottom - 20, f'{title}: panel {head} overflows'
        d.text((x0 + 50, top + 30), head, font=F('mono', 40), fill='#8BC7F3')
        ty = top + 105
        for num, part, firstp in rows:
            if num in hi:
                d.rectangle([x0 + 4, ty - 5, x0 + pw - 4, ty + lh - 5], fill=DARK_HI)
                d.rectangle([x0 + 4, ty - 5, x0 + 14, ty + lh - 5], fill=SPARK)
            if firstp:
                d.text((x0 + 40, ty), f'{num:>4}', font=f, fill=DARK_MUTED)
            d.text((x0 + 50 + int(size * 2.9), ty), part, font=f, fill=DARK_TEXT)
            ty += lh
        x0 += pw + gap
    cards.footer(d, note)
    return im


def line_panels(title, chip, rows, note):
    """rows: [(label, [[(path, n, text), ...], ...], annotation)]: each inner list is one line of side-by-side
    one-line source panels; the annotation follows. Largest type that fits."""
    def make(m):
        im, d, y = cards.base(title, chip)
        ty = y + 10
        fm = F('mono', m)
        lh = int(m * 1.3)
        for label, groups, ann in rows:
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


# ---------------------------------------------------------------- beats
def build():
    remotion('B00')
    remotion('B30')
    remotion('B01')
    remotion('B29', brandLabel='@NikBearBrown', artifactLines=[
        'Built: effects/fireball_impact.tscn (Sparks + Smoke) and effects/fireball_trail.tscn, wired to '
        'Fireball.explode() and the 2.0 s timeout in fireball.gd; every setting in the scene files; tests, previews, '
        'probe and price tools.',
        'Measured: 54 / 0 and 32 / 0 configuration checks; 14 / 0 and 20 / 0 state checks at 30, 60 and 144 fps; both '
        'mutations caught; GPU ≈ 0.02 ms (budget 0.5) and ≈ 0.10 ms (budget 0.3).',
        'Judged by the author: both effects read in play; r1 of each effect kept (smoke fade-in, scale curve 2 → 0).',
        'Unknown: why the trail beads every 8.7 px; why vsync-off FPS stops near 1000; whether a hidden emitter keeps '
        'simulating; the _spent guard, untested.',
        'The author: choices, predictions, verdicts, play, strips, GPU readings · Claude Code: scenes, tests, tools · '
        'claude.ai: planning, documents · source 3c37fe0'])
    BEATS['B31']['shot']['remotion']['props']['durationSeconds'] = nframes('B31') / FPS

    # B02 — the game, the jobs, the event and the condition.
    still('B02', cards.identity('walker-magic: two jobs, one event, one condition',
        f'Game source revision {BUILD} · Godot 4.7.2-stable · Forward+', {
            'img': play(25), 'badge': 'Scripted input · frame 25', 'crop': PLAY_CROP,
            'caption': 'capture/run-01: the first cast, the trail behind the fireball',
            'rows': [('Effect B · the trail', 'Job: shows the fireball’s path and speed, so the player can read where a '
                      'shot is heading. Condition: the fireball exists and has not exploded (fireball.gd _ready to '
                      'explode() or the 2.0 s timeout).')]}, {
            'img': play(32), 'badge': 'Scripted input · frame 32', 'crop': PLAY_CROP,
            'caption': 'capture/run-01: the same shot, three frames after it hit the ground',
            'rows': [('Effect A · the impact', 'Job: tells the player where and when a fireball landed: on a wolf (a '
                      'hit) or on a wall or the ground (a miss). Event: Fireball.explode(), called from '
                      '_on_body_entered.')]},
        'CHANGE-BRIEF.md → Effect A “The job”, Effect B “The job” · capture/run-01 frames 25 and 32'),
        {'images': ['capture/run-01 frame 25', 'capture/run-01 frame 32'],
         'capture_sha256': sha256(REEL / 'capture' / 'run-01.mp4'), 'source': 'CHANGE-BRIEF.md:23-25,78-82'})

    # B03 -> B04: where both effects hook in.
    workbench('B03', 'Where both effects hook in', 'features/fireball/fireball.gd', 43, 49, 'var burst :=', [
        ('fireball.gd lines 61–63, _release_trail()', 'trail.reparent(get_parent(), true) · trail.emitting = false · '
         'create_timer(trail.lifetime, false) → trail.queue_free'),
        ('fireball.gd line 28', 'the 2.0 s timeout calls _release_trail() too')],
        [(0.0, 43, 'Lines 43–45: the A2 flash, exactly as before'),
         ('then instances the new impact', 46, 'Lines 46–48: one new impact per explode(), into Main'),
         ('Then it releases the trail', 49, 'Line 49: release the trail (lines 57–63)')], font=34)
    BEATS['B04']['shot']['evidence_media'] = 'media/B04.mp4'

    # B05 — emission, process, draw.
    imp, gen = 'effects/fireball_impact.tscn', 'shaders/particles_generated.gdshader'
    still('B05', line_panels('Three parts: emission, process, draw', SRCVIEW, [
        ('Emission · how many are born, and when', [[(imp, 80, line(imp, 80, 'amount')), (imp, 83, line(imp, 83, 'one_shot')),
                                                      (imp, 85, line(imp, 85, 'explosiveness'))]],
         'Sparks: 24 particles, one shot, all released at once.'),
        ('Process · how each one moves, every frame, on the GPU', [[(gen, 324, line(gen, 324, 'USERDATA1.xyz += force'))]],
         'In the process shader Godot generates from a ParticleProcessMaterial; the colour ramp is computed here too '
         '(CHANGE-BRIEF.md, short answer 6, corrected).'),
        ('Draw · how they become pixels', [[(imp, 8, line(imp, 8, 'blend_mode')), (imp, 81, line(imp, 81, 'texture'))]],
         'A 4×4 spark texture, drawn with a CanvasItemMaterial in Add mode.')],
        'effects/fireball_impact.tscn · shaders/particles_generated.gdshader · CHANGE-BRIEF.md → Short answers 6'),
        {'card': 'media/B05.png', 'source': 'fireball_impact.tscn:8,80,81,83,85 · particles_generated.gdshader:324'})

    # B06 — why the headless price is near zero.
    still('B06', table_card('Why a GPU effect costs almost nothing headless', RESULTS,
        ['What a headless run reports (Godot 4.7.2, dummy renderer)', 'What that means for this film’s tests'],
        [('0 draw calls; capture_rect() empty; no GPU particle process runs', 'Nothing about the look can be tested headlessly'),
         ('Instance counts, one_shot, amount_ratio and visibility are observable', 'Rules are tested on node state'),
         ('emitting turns false once all particles are emitted, not when they die', 'emitting cannot tell if a burst is alive'),
         ('The finished signal did not fire', 'Aliveness is tested by instance presence'),
         ('CPU time per frame with 6 impacts: 4.6 vs 6.6 µs', 'The headless price is near zero by construction')],
        [1800, 1656], 'Measured in logs/test_fireball_impact_config_60fps.log (2026-11-05).',
        'CLAUDE.md → Headless facts (A6) · TEST-REPORT.md', size=50),
        {'card': 'media/B06.png', 'source': 'CLAUDE.md Headless facts · TEST-REPORT.md:8'})

    # B07 — Effect A intent.
    brief = A6 / 'CHANGE-BRIEF.md'
    still('B07', doc_columns('Effect A · the intent, written first', DOC, [
        ('CHANGE-BRIEF.md · Intent · lines 29–31', 29, doc_lines(brief, 29, 31, '- **Timing phases**'), {29}, 0.5),
        ('CHANGE-BRIEF.md · Observable rules · lines 69–74', 69, doc_lines(brief, 69, 74, '| A1'), set(), 0.5)],
        'CHANGE-BRIEF.md, original version 2026-11-05 · settings came after the intent'),
        {'card': 'media/B07.png', 'source': 'CHANGE-BRIEF.md:29-31,69-74'})

    # B08 -> B09: sparks' process settings, then the first strip.
    workbench('B08', 'Effect A · the sparks’ process settings', imp, 25, 36, 'particle_flag_disable_z', [
        ('CHANGE-BRIEF.md revision 2026-11-05', 'particle_flag_disable_z: without it a 180° spread is a 3D cone'),
        ('Ownership (CLAUDE.md)', 'every effect value lives in the scene file, none in code')],
        [(0.0, 25, 'Line 25: flat in 2D'),
         ('Spread one eighty', 28, 'Line 28: spread 180°, a full circle'),
         ('Initial velocity ninety', 29, 'Lines 29–30: 90 to 160 px/s'),
         ('gravity three hundred down', 31, 'Line 31: gravity (0, 300)'), ('damping forty', 32, 'Lines 32–33: damping 40–60'),
         ('a scale curve', 36, 'Line 36: scale curve 1 → 0')], font=27)
    reading = {10: 'flash and first sparks', 12: 'sparks spreading, still bright', 15: 'flash gone, sparks about half way',
               20: 'sparks orange-red, smoke visible', 30: 'only faint smoke', 50: 'empty'}
    r0 = [10, 12, 15, 20, 30, 50]
    still('B09', strip_grid('Effect A · the first strip, r0', FIXTURE + ' · Movie Maker, 30 fps',
        [(strip('fireball_impact/r0', n), f'frame {n} · t ≈ {(n - 9) / 30:.2f} s · {reading[n]}') for n in r0],
        IMPACT_CROP, 3, 'captures/fireball_impact/r0/ · readings: CHANGE-BRIEF.md line 141 · t ≈ (n − 9)/30 s: '
        'CHANGE-BRIEF.md revision (Effect A r1 kept)'),
        strips_prov(*[('fireball_impact/r0', n) for n in r0]), evidence=True)

    # B10 — r0b: the preview, not the effect.
    still('B10', grid_beside_table('Tuning step r0b · the preview, not the effect', FIXTURE + ' · retrigger: a second impact 6 frames later',
        [(strip('fireball_impact/r0-retrigger', 20), 'r0-retrigger · frame 20'),
         (strip('fireball_impact/r0b-retrigger', 20), 'r0b-retrigger · frame 20'),
         (strip('fireball_impact/r0-retrigger', 30), 'r0-retrigger · frame 30'),
         (strip('fireball_impact/r0b-retrigger', 30), 'r0b-retrigger · frame 30')], IMPACT_CROP,
        ['TUNING.md r0b', ''],
        [('Seen', 'the two impacts looked almost the same, as if stamped'),
         ('Measured', 'second = first scaled by 0.83, mean error 1.6 px; a 15°-rotated control 4.1 px'),
         ('Cause', 'the preview gave the second impact seed + 1'),
         ('Change', 'preview seeds first_seed + 1000 × spawn index (1 and 1001); effect scene unchanged (0069149)'),
         ('Prediction', 'frames 10–15 identical; from frame 20 the second impact no longer lines up'),
         ('Verdict', 'the two impacts now look different. Kept.')], [0.3, 0.7],
        'TUNING.md → Effect A, r0b · captures/fireball_impact/r0-retrigger/, r0b-retrigger/'),
        strips_prov(('fireball_impact/r0-retrigger', 20), ('fireball_impact/r0b-retrigger', 20),
                    ('fireball_impact/r0-retrigger', 30), ('fireball_impact/r0b-retrigger', 30)))

    # B11 -> B12: the smoke colour ramp, then r0 against r1.
    workbench('B11', 'Effect A · r1, the smoke’s colour ramp', imp, 44, 46, '[sub_resource type="Gradient" id="Grad_smoke"]', [
        ('Before r1 (TUNING.md)', 'offsets (0, 1) · grey alpha 0.55 → 0'),
        ('After r1, 35a1f70', 'offsets (0, 0.125, 1) · alpha 0 → 0.55 → 0: a 0.1 s fade-in')],
        [(0.0, 44, 'Grad_smoke: the smoke’s colour over life'),
         ('The change was one setting', 45, 'Line 45: offsets 0, 0.125, 1'),
         ('so the puff now fades in', 46, 'Line 46: alpha 0 → 0.55 → 0')], font=36)
    still('B12', grid_beside_table('Effect A · r0 against r1', FIXTURE + ' · same preview, same seed',
        [(strip('fireball_impact/r0', 10), 'r0 · frame 10'), (strip('fireball_impact/r1', 10), 'r1 · frame 10'),
         (strip('fireball_impact/r0', 12), 'r0 · frame 12'), (strip('fireball_impact/r1', 12), 'r1 · frame 12')], IMPACT_CROP,
        ['', 'Predicted', 'Measured (TUNING.md r1)'],
        [('Frame 10', 'no grey disc; most of the 86 bright pixels back', 'pixels above 200 within 12 px: 86 → 175; centre 144 → 230'),
         ('Frame 12', 'centre about −33 %', 'about −5 %: missed'),
         ('Why', '', 'each frame is one 1/30 s step older: frame n ≈ (n − 9)/30 s'),
         ('Verdict', '', 'running game: the moment of impact is brighter. Kept.')], [0.24, 0.34, 0.42],
        'TUNING.md → Effect A, revision r1 · captures/fireball_impact/r0/, r1/'),
        strips_prov(('fireball_impact/r0', 10), ('fireball_impact/r1', 10), ('fireball_impact/r0', 12), ('fireball_impact/r1', 12)),
        evidence=True)

    BEATS['B13']['shot']['evidence_media'] = 'media/B13.mp4'

    # B14 — Effect B intent and the feature A doesn't use.
    still('B14', doc_columns('Effect B · the intent, and what A doesn’t use', DOC, [
        ('CHANGE-BRIEF.md · Intent · lines 86–88', 86, doc_lines(brief, 86, 88, '- **Timing**'), {86}, 0.5),
        ('CHANGE-BRIEF.md · The job · lines 80–82', 80, doc_lines(brief, 80, 82), {82}, 0.5)],
        'CHANGE-BRIEF.md → Effect B · rules B1–B5 at lines 117–121'),
        {'card': 'media/B14.png', 'source': 'CHANGE-BRIEF.md:80-82,86-88'})

    # B15 -> B16: the trail's process settings, then the first strip.
    trail = 'effects/fireball_trail.tscn'
    workbench('B15', 'Effect B · the trail’s process settings', trail, 25, 38, 'emission_shape = 1', [
        ('Probe e174c96 · brief revision 7957614', 'direction follows the fireball’s rotation; gravity stays world space'),
        ('Lines 39–40', 'turbulence influence 0.1 to 0.2')],
        [(0.0, 25, 'Lines 25–26: a sphere, radius 3 (A emits from a point)'),
         ('Direction minus one', 27, 'Line 27: (−1, 0): behind the fireball'),
         ('while gravity stays', 31, 'Line 31: gravity (0, −30), world space'),
         ('Turbulence is on', 36, 'Lines 36–38: turbulence on, strength 1, scale 2')], font=23)
    reading_b = {10: 'start: one or two particles', 12: 'steady trail', 20: 'steady trail', 30: 'steady trail',
                 40: 'the carrier stops', 45: 'fading where it was', 50: 'gone'}
    tr = [10, 12, 20, 30, 40, 45, 50]
    still('B16', strip_grid('Effect B · the first strip, r0', FIXTURE + ' · a carrier at 260 px/s from frame 10, stopped at 40',
        [(strip('fireball_trail/r0', n), f'frame {n} · {reading_b[n]}') for n in tr], TRAIL_CROP, 2,
        'captures/fireball_trail/r0/ · readings: CHANGE-BRIEF.md line 142 · measurements: TUNING.md → Effect B, revision r1',
        note='Measured at frame 30: about 71 px long (intent 60–80); 4–6 px tall (intent 15–21); dots every 8.7 px with '
             '3–5 px gaps', cap=52),
        strips_prov(*[('fireball_trail/r0', n) for n in tr]), evidence=True)

    # B17 -> B18: the scale curve, then r0 against r1.
    workbench('B17', 'Effect B · r1, the scale curve', trail, 15, 18, '[sub_resource type="Curve" id="Curve_trail_scale"]', [
        ('r1, cc1f2f2 (TUNING.md)', 'linear (0, 1) → (1, 0) became (0, 2) → (1, 0), with max_value = 2.0'),
        ('Not changed', 'the colour ramp (same as Sparks)')],
        [(0.0, 15, 'Curve_trail_scale: size over life'), ('with max value two', 16, 'Line 16: max_value = 2.0'),
         ('from one-to-zero to two-to-zero', 17, 'Line 17: (0, 2) → (1, 0)')], font=40)
    still('B18', grid_beside_table('Effect B · r0 against r1', FIXTURE + ' · same preview, same seed',
        [(strip('fireball_trail/r0', 30), 'r0 · frame 30'), (strip('fireball_trail/r1', 30), 'r1 · frame 30'),
         (strip('fireball_trail/r0', 40), 'r0 · frame 40'), (strip('fireball_trail/r1', 40), 'r1 · frame 40')],
        (250, 245, 430, 290), ['', 'Predicted', 'Measured (TUNING.md r1)'],
        [('Head', '8–12 px', '11–13 px (r0: 4–6); every pixel lit in r0 still lit'),
         ('Strip', 'continuous, the dots overlapping', 'closes only behind the head; 1–3 px gaps further back (r0: 3–5)'),
         ('Lit pixels', 'about 2.5–3×', 'frame 30: 208 → 421; frame 40 (no sprite): ×3.1'),
         ('Verdict', '', 'running game: thicker and brighter. Kept.')], [0.22, 0.33, 0.45],
        'TUNING.md → Effect B, revision r1 · captures/fireball_trail/r0/, r1/'),
        strips_prov(('fireball_trail/r0', 30), ('fireball_trail/r1', 30), ('fireball_trail/r0', 40), ('fireball_trail/r1', 40)),
        evidence=True)

    BEATS['B19']['shot']['evidence_media'] = 'media/B19.mp4'

    # B20 — the generated process shader beside the brief's settings.
    still('B20', line_panels('The process shader Godot writes, beside the brief', SRCVIEW, [
        ('Line 139 · initial velocity from its minimum and maximum',
         [[(gen, 139, line(gen, 139, 'params.initial_velocity_multiplier'))],
          [(imp, 29, line(imp, 29, 'initial_velocity_min')), (imp, 30, line(imp, 30, 'initial_velocity_max'))]],
         'One random value per particle between the two uniforms: the sparks’ 90 and 160 px/s. It becomes a velocity at line 264.'),
        ('Lines 311 and 324 · gravity changes the velocity',
         [[(gen, 311, line(gen, 311, 'force = gravity;')), (gen, 324, line(gen, 324, 'USERDATA1.xyz += force'))],
          [(imp, 31, line(imp, 31, 'gravity'))]],
         'The force starts from the gravity uniform and is added to the velocity every frame, times DELTA: the sparks’ '
         '300 px/s² downward.')],
        'shaders/particles_generated.gdshader (converted by the author in the editor; nothing in the game uses it) · '
        'TEST-REPORT.md → The process shader'),
        {'card': 'media/B20.png', 'source': 'particles_generated.gdshader:139,311,324 · fireball_impact.tscn:29-31'})

    # B21 — what the tests proved.
    still('B21', table_card('What the tests proved', RESULTS + ' · fixed-fps headless, scripts/run-test.sh',
        ['Check', 'Result', 'What it covers'],
        [('Configuration, Effect A', '54 checks / 0 failures', 'every Sparks and Smoke setting read back; no Godot 3 names'),
         ('Configuration, Effect B', '32 checks / 0 failures', 'turbulence, sphere emission, scale curve 2 → 0, defaults written'),
         ('State, Effect A', '14 / 0 at 30, 60 and 144 fps', 'A1–A6: one impact per hit, never otherwise, at the fireball, overlap, outlives it, 0.9 s'),
         ('State, Effect B', '20 / 0 at 30, 60 and 144 fps', 'B1–B5: starts, detaches, stops, freed 0.3 s later, pause, hidden, none on load'),
         ('Nine earlier suites', 'baseline counts, 0 failures', 'after both wirings (f5743f5, e174c96)'),
         ('Not covered', '—', 'the _spent guard; B4 sets visible from the test')], [900, 1000, 1556],
        'Real mouse casts and real Esc presses through the real game loop; aliveness by instance.',
        'TEST-REPORT.md → Machine checks', size=46),
        {'card': 'media/B21.png', 'source': 'TEST-REPORT.md:14-22'})

    # B22 — broken on purpose.
    still('B22', columns('Broken on purpose', RESULTS + ' · ab0784c', [
        ('a1 · a Godot 3 name', [
            ('Mutation', 'Sparks initial_velocity_min = 90.0 renamed to initial_velocity = 90.0'),
            ('Engine', 'no error, no warning: in 4.7.2 initial_velocity is a Vector2 (min, max), so the float is dropped'),
            ('Effect', 'still fires (instances at frames 10 and 16, amount 24), speed 0–160 instead of 90–160'),
            ('Test', 'exit 1, 2 failures: the read-back and the Godot 3 name scan')]),
        ('a2 · drift', [
            ('Mutation', 'Sparks lifetime 0.45 → 0.6, brief unchanged'),
            ('Test', 'exit 1, 1 failure')])],
        'TEST-REPORT.md → Mutation a1, a2 · logs/mutation-a1-*, mutation-a2-*', value_size=56, label_size=42),
        {'card': 'media/B22.png', 'source': 'TEST-REPORT.md:18-19'})

    # B23 — the headless price.
    still('B23', table_card('The headless price, with its control', RESULTS + ' · tests/cost_effects.gd, f7787c4',
        ['Case (3 rounds × 1200 frames, wall time per frame)', 'Mean µs', 'σ'],
        [('control: an empty scene', '3.82', '0.96'), ('game scene, effects off', '240.83', '45.38'),
         ('Effect A, 6 impacts alive', '253.58', '47.54'),
         ('Effect B heaviest (6 flying + 6 fading, +6 refilling)', '296.42', '57.87')], [2300, 600, 556],
        'Each effect’s own price, after subtracting a dry case (the same driver with bare Node2D placeholders): A +8.2 µs, '
        'B +25.1 µs, inside the scene’s frame-to-frame spread (σ 45 µs). Without the dry cases, Effect B’s price would have '
        'doubled. Performance.TIME_PROCESS gave identical values for different cases and is not used.',
        'TEST-REPORT.md → Price', size=56),
        {'card': 'media/B23.png', 'source': 'TEST-REPORT.md:51-60'})

    # B24 — the GPU price.
    still('B24', table_card('The GPU price, against the budget', RESULTS + ' · Visual Profiler, previews/gpu_price.tscn, RTX 5060 Laptop GPU',
        ['', 'Case 1, off', 'Case 2, Effect A ×6', 'Case 3, Effect B heaviest'],
        [('Update GPUParticles (GPU)', 'absent (0)', '0.01 ms', '0.09 ms'),
         ('Render Viewport (GPU)', '0.03 ms', '0.04 ms', '0.04 ms'),
         ('Over case 1', '—', '≈ 0.02 ms', '≈ 0.10 ms'),
         ('Budget (GPU time)', '—', '0.5 ms: within, about 4 %', '0.3 ms: within, about 33 %'),
         ('FPS, vsync on', '160', '161', '167'),
         ('FPS, vsync off (F8)', '995', '999', '985')], [1050, 680, 860, 866],
        'Case 3 carries 18 trails, more than the brief’s 6 + 6, so it is an upper bound. With vsync off the three cases '
        'differ by under 1 %: FPS hides these costs.', 'TEST-REPORT.md → Price', size=50),
        {'card': 'media/B24.png', 'source': 'TEST-REPORT.md:62-73'})

    # B25 — what no headless run shows.
    still('B25', columns('What no headless run shows', 'TEST-REPORT.md · the author’s human checks, translated from Chinese', [
        ('No headless run shows', [
            ('', 'whether either effect is visible or reads well'),
            ('', 'its colour, size and timing on screen'),
            ('', 'whether the GPU keeps simulating a hidden emitter'),
            ('', 'real (not simulated) frame timing')]),
        ('The author saw, in the running game', [
            ('Against the background', 'the pit: Effect A’s smoke clearly visible, Effect B readable; the ground cap: both readable'),
            ('Edge of screen', 'impacts on both walls at the camera limits: no sparks cut off'),
            ('Scene load', 'no trail in the first frames')])],
        'TEST-REPORT.md → What no headless run shows · Human checks', value_size=58, label_size=44),
        {'card': 'media/B25.png', 'source': 'TEST-REPORT.md:34-42,94-96'})

    # B26 — what the agent got wrong.
    still('B26', columns('What the agent got wrong', 'FRICTIONAL.md entries 10, 13 and 14 · agent = Claude Code', [
        ('10 · The smoke prediction', [
            ('The agent', 'assumed frame n shows (n − 10)/30 s; frame 12 missed its prediction.'),
            ('What caught it', 'the spark distances: frame n shows about (n − 9)/30 s.')]),
        ('13 · The trail prediction', [
            ('The agent', 'used the head’s size for the whole trail and predicted a continuous strip.'),
            ('What caught it', 'the r1 strip: 1–3 px gaps remain, because each dot shrinks with age.')]),
        ('14 · The cost script', [
            ('The agent', 'timed its own bookkeeping: +41 / +81 µs.'),
            ('What caught it', 'timing only the frame and adding dry cases: A +8.2 µs, B +25.1 µs.')])],
        'FRICTIONAL.md → Entries', value_size=58, label_size=44),
        {'card': 'media/B26.png', 'source': 'FRICTIONAL.md:25,31,33'})

    # B27 — overruled, uncertain, one next step.
    still('B27', columns('Overruled, uncertain, and one next step', 'TUNING.md r0b · FRICTIONAL.md → Still open · README.md', [
        ('Overruled by the author', [
            ('Claude read', 'frame 20 as sparks too dark too soon (dark-red specks, not orange-red).'),
            ('The author', 'watched in slow motion, judged the darkening rhythm right; nothing changed.')]),
        ('Still open', [
            ('', 'why the trail beads at 8.7 px (a 30 fps simulation is a guess)'),
            ('', 'why vsync-off FPS stops near 1000'),
            ('', 'whether the GPU keeps simulating a hidden emitter'),
            ('', 'the _spent guard: no test exercises it')]),
        ('One next step', [
            ('Proposed by this film', 'a state test that makes one fireball touch two bodies in one physics frame and '
                                      'checks one impact and one detached trail.')])],
        'TUNING.md → r0b · FRICTIONAL.md → Still open · README.md → Known limitations', value_size=58, label_size=44),
        {'card': 'media/B27.png', 'source': 'TUNING.md:23 · FRICTIONAL.md:23,47-48 · README.md:27-31'})

    # B28 — who did what.
    still('B28', columns('Who did what', f'No sourced or model-generated textures · game source revision {BUILD}', [
        ('The author', [
            ('', 'Both effects and their look; every prediction and verdict; approving every tuning change.'),
            ('', 'All play testing and human checks, the strip captures, the GPU readings, the generated-shader '
                 'conversion and the process-versus-draw answer.')]),
        ('Claude Code', [
            ('', 'CLAUDE.md drafts, both effect scenes, the texture-writing script, configuration and state tests, '
                 'previews, mutations, the direction probe, the cost script and the GPU price scene; strip readings, '
                 'predictions and comparisons; this film.')]),
        ('claude.ai (chat)', [
            ('', 'Planning, commands, the setup script, setting values proposed from the author’s choices, compiling '
                 'CHANGE-BRIEF, TUNING, TEST-REPORT and FRICTIONAL; translating the author’s Chinese.'),
            ('Textures', 'spark.png and smoke.png are written by code (tools/write_fx_textures.gd).')])],
        'FRICTIONAL.md → Human and AI contributions · SOURCES.md · assets/textures/fx/ATTRIBUTION.md', value_size=54),
        {'card': 'media/B28.png', 'source': 'FRICTIONAL.md:41-43 · SOURCES.md · ATTRIBUTION.md'})


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
                'output; see CAPTURE.md). Strips: the author’s committed fixture captures in captures/. Both shown '
                'enlarged with nearest-neighbour scaling.',
        'beats': {**PROV, **footage}})
    print('media built:', ', '.join(sorted(PROV)))


if __name__ == '__main__':
    main()
