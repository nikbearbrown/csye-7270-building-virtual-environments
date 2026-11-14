"""Phase 2b: build every card slot and fill the Remotion props, using measured narration.

Adapted from the Assignment 6 film's media.py. Images of the game are either frames of the scripted-input capture
(capture/run-02, real engine output) or the author's committed captures in captures/ (fixture captures from capture
harnesses and preview scenes that place the characters; not played gameplay), enlarged with nearest-neighbour scaling.
Figures from captures/figures/ (tools/make_figures.py, drawn from the logs) are scaled to fit. Figures on cards come
from the named source documents and logs; code comes verbatim from the snapshot of the build shown (ad7935f); lines of the author's
documents are checked equal to the files at ad7935f (git show). The
gameplay beats themselves are built by footage.py.
"""
import hashlib
import json

import numpy as np
from PIL import Image, ImageDraw

import cards
from cards import F, wrap, text_block, SAFE_L, SAFE_R, DARK, DARK_TEXT, DARK_MUTED, DARK_HI
from common import (REEL, GAME, A7, CAPS, LOGS, BUILD, BUILD_FULL, CAPTURE, FPS, SNAPSHOT, CAPTURE_FRAMES, INK, INK_SOFT,
                    SPARK, BORDER, run,
                    load_json, save_json, render_frames, source_lines, sha256, capture_rows)

MEDIA = REEL / 'media'
EV = REEL / 'evidence'
SRC = SNAPSHOT or GAME
FIG = CAPS / 'figures'

PLAY = 'Scripted input · real engine output · capture/run-02'
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


def wolf_crop(row, half=140, top=200, bottom=345):
    sx = int(round(row['wx'] - row['cam_x'] + 320))
    return play(row['f']).crop((sx - half, top, sx + half, bottom))


# ---------------------------------------------------------------- documents and source panels
DOCS = {'brief': 'CHANGE-BRIEF.md', 'report': 'TEST-REPORT.md', 'tuning': 'TUNING.md', 'frictional': 'FRICTIONAL.md',
        'readme': 'README.md', 'submission': 'SUBMISSION.md'}
_doc_cache = {}
DOC_DRIFT = {}


def doc_at(name, n, first):
    """Line n of an A7 document as it is at the revision shown (git show BUILD:path). The working tree may have been
    revised since (dated additions by the author); the film quotes the revision it names, and DOC_DRIFT records which
    files differ in the working tree."""
    rel = name if '/' in name else DOCS[name]
    if rel not in _doc_cache:
        tree = (A7 / rel).read_text(encoding='utf-8').splitlines()
        shown = run(['git', '-C', A7, 'show', f'{BUILD_FULL}:fall-2026/zhefan-z/assignment-7/{rel}'],
                    encoding='utf-8').stdout.splitlines()
        if tree != shown:
            DOC_DRIFT[rel] = 'working tree differs from ' + BUILD
        _doc_cache[rel] = shown
    text = _doc_cache[rel][n - 1]
    assert text.startswith(first), f'{rel}:{n} does not start with {first!r}'
    return text


TREE_QUOTES = {}


def doc_tree(name, n, first):
    """Line n of an A7 document as it is in the working tree, for a dated addition the author made after the revision
    shown (quoted only with that label). Asserts the line is not already in the file at BUILD."""
    rel = name if '/' in name else DOCS[name]
    text = (A7 / rel).read_text(encoding='utf-8').splitlines()[n - 1]
    assert text.startswith(first), f'{rel}:{n} (working tree) does not start with {first!r}'
    shown = run(['git', '-C', A7, 'show', f'{BUILD_FULL}:fall-2026/zhefan-z/assignment-7/{rel}'],
                encoding='utf-8').stdout.splitlines()
    assert text not in shown, f'{rel}:{n} is already at {BUILD}; quote it with doc_at'
    TREE_QUOTES[f'{rel}:{n}'] = {'sha256_of_line': hashlib.sha256(text.encode('utf-8')).hexdigest(),
                                 'note': f'working tree, not in {BUILD}'}
    return text


def four_ideas():
    """CHANGE-BRIEF.md:197, the four ideas in the author's words, split into its four sentences."""
    text = doc_at('brief', 197, '**The four ideas** *(mine, translated)*. ')
    body = text[len('**The four ideas** *(mine, translated)*. '):]
    parts = [p if p.endswith('.') else p + '.' for p in body.split('. ')]
    assert len(parts) == 4 and parts[0].startswith('A clip is') and parts[3].startswith('Designing feel'), parts
    return parts


def src_block(d, x, y, w, items, m):
    """items: [(path, [(line number, exact text), ...])]: one dark panel per item, numbered lines; returns bottom y."""
    fm = F('mono', m)
    lh = int(m * 1.32)
    for path, lines in items:
        rows = []
        for n, text in lines:
            parts = wrap(d, text.replace('\t', '    ').rstrip(), fm, w - 80 - int(m * 2.8))
            rows += [(n if j == 0 else None, p) for j, p in enumerate(parts)]
        h = 30 + int(m * 1.2) + 14 + len(rows) * lh + 22
        d.rounded_rectangle([x, y, x + w, y + h], radius=22, fill=DARK)
        d.text((x + 36, y + 22), path, font=F('mono', int(m * 0.9)), fill='#8BC7F3')
        ty = y + 30 + int(m * 1.2) + 14
        for n, p in rows:
            if n is not None:
                d.text((x + 36, ty), f'{n:>3}', font=fm, fill=DARK_MUTED)
            d.text((x + 36 + int(m * 2.8), ty), p, font=fm, fill=DARK_TEXT)
            ty += lh
        y += h + 18
    return y


def quote_block(d, x, y, w, label, text, size):
    """The author's words: a label, then the quote in serif behind an accent bar; returns bottom y."""
    y = text_block(d, x + 40, y, label, F('sans', int(size * 0.62)), w - 40, INK_SOFT, int(size * 0.85)) + 6
    top = y
    y = text_block(d, x + 40, y, f'“{text}”', F('serif', size), w - 40, INK, int(size * 1.22))
    d.rectangle([x, top + 6, x + 12, y - 6], fill=SPARK)
    return y


def snap_lines(rel, numbers, first=None):
    """[(n, exact text)] from the snapshot (checked equal to the working tree by excerpt())."""
    out = []
    for i, n in enumerate(numbers):
        text = excerpt(rel, n, n, (first or {}).get(n, ''))
        out.append((n, text))
    return out


IDEA_LABEL = 'The author’s words · CHANGE-BRIEF.md:197, “The four ideas” (translated from Chinese by the author)'


def idea_card(title, sentence, items, note, src, extra=None, sizes=(84, 78, 72, 68, 64, 60, 56, 52, 48, 46, 44)):
    """Idea card: the author's sentence, the exact lines it points at, a note; `extra(d, y, v)` may add a block."""
    def make(v):
        im, d, y = cards.base(title, SRCVIEW + ' · exact lines at ' + BUILD)
        ty = quote_block(d, SAFE_L, y + 6, SAFE_R - SAFE_L, IDEA_LABEL, sentence, v)
        ty = src_block(d, SAFE_L, ty + 34, SAFE_R - SAFE_L, items, int(v * 0.62))
        if extra:
            ty = extra(d, ty + 10, v)
        ty = text_block(d, SAFE_L, ty + 14, note, F('sans', int(v * 0.66)), SAFE_R - SAFE_L, INK, int(v * 0.88))
        assert ty < 1950, f'{title}: overflows ({ty})'
        cards.footer(d, src)
        return im
    return fit(make, sizes)


# ---------------------------------------------------------------- beats
def build():
    rows = capture_rows()
    ideas = four_ideas()
    remotion('B00')
    remotion('B27')
    remotion('B01')
    remotion('B26', brandLabel='@NikBearBrown', artifactLines=[
        'Built: the run clip (4 cells, 10 fps, step 0.1, LOOP_LINEAR, discrete) and the lunge rig and clip (89 frames, '
        'step 1/60, LOOP_NONE), each owned by one AnimationPlayer on the physics callback; the growl cancel.',
        'Measured: pin 16 / 0 at 30, 60, 144, unchanged by the clips; the change re-pinned after play (ff71bbb); edges '
        '25 / 0 at 30, 60, 144; read-backs 17, 18, 12, 11 / 0; M1–M3 caught, M4 (fresh import) passes.',
        'Judged by the author in play: run r2 kept (r1 rejected), the three phases and an interrupt in each, the 0.2 s '
        'growl window kept.',
        'Open: in-between frames so the planted foot stops sliding; the hitbox read 1/60 s after the clip’s active '
        'section; a fresh clone at the submitted commit.',
        f'The author: clips, rule, verdicts, Gemini sheet · Claude Code: pin, clips, tests, mutations, this film · '
        f'claude.ai: brief and documents · source {BUILD}'])
    BEATS['B28']['shot']['remotion']['props']['durationSeconds'] = nframes('B28') / FPS
    for bid in ('B03', 'B04', 'B05', 'B06', 'B07'):
        BEATS[bid]['shot']['evidence_media'] = f'media/{bid}.mp4'

    # B02 — the game and its two clips (CHANGE-BRIEF revision 2026-11-13, "The two clips").
    now = cap('look/take_lunge_t40_now.png').crop((150, 140, 640, 360))
    doc_at('brief', 148, '| | Clip 1: run cycle | Clip 2: wolf lunge |')
    doc_at('brief', 155, '| Cycle or committing | cycle | committing action |')

    def b02(v):
        im, d, y = cards.base('The game and its two clips', 'Fixture capture (left) · CHANGE-BRIEF.md revision '
                              '2026-11-13, “The two clips” · git log (right)')
        lw = 1470
        pic, k = scaled(now, lw, 1000, pixel=True)
        cards.paste_framed(im, d, pic, SAFE_L, y + 10)
        ty = text_block(d, SAFE_L, y + 10 + pic.height + 20, f'captures/look/take_lunge_t40_now.png, crop, ×{k} '
                        '(fixture: tests/capture_look.gd places the mage and the wolf)', F('sans', 38), lw, INK_SOFT, 50)
        notes_block(d, SAFE_L, ty + 30, lw, [
            ('walker-magic (README.md)', 'a 2D side-scroller: a mage crosses a cave and casts fireballs at a wolf'),
            ('Engine', 'Godot 4.7.2-stable, Forward+, 640×360 at 2×')], int(v * 1.1))
        rx = SAFE_L + lw + 90
        tw = SAFE_R - rx
        cards.table(d, rx, y + 10, [int(tw * 0.22), int(tw * 0.39), tw - int(tw * 0.22) - int(tw * 0.39)],
                    ['', 'Clip 1: run cycle', 'Clip 2: wolf lunge'], [
            ('Object', 'the mage’s Sprite2D (features/player/player.tscn)',
             'the wolf’s rig Facing → Rig → pivots → parts (features/wolf/wolf.tscn)'),
            ('Route', 'Sprite2D + AnimationPlayer frame track',
             'cutout rig keyed as resource text: two region_rects of the A2 wolf_lunge.png'),
            ('Loops or commits', 'loops: LOOP_LINEAR, 4 frames at 10 fps',
             'commits: LOOP_NONE, 89 frames at 60 fps'),
            ('Authority', 'player.gd _set_state() calls play()',
             'wolf.gd _enter() plays on GROWL entry; take_damage() seeks on a growl cancel'),
            ('Commits', 'clips 72e8d21 · wired 33d78ae · r2 sheet 32eed66 · step b1422ca',
             'clips 72e8d21 · wired 33d78ae · growl cancel 72f37b8 · step b1422ca')],
            size=v, head_size=int(v * 0.85), hi_cols=(0,))
        cards.footer(d, f'CHANGE-BRIEF.md:146–155 · README.md · git log · game source {BUILD}')
        return im
    still('B02', fit(b02, (56, 52, 48, 46, 44, 42, 40)), {**caps_prov('look/take_lunge_t40_now.png'),
          'source': 'CHANGE-BRIEF.md:146-155; README.md; git log'})

    # B08 — idea 1: what a clip is.
    ptscn = 'features/player/player.tscn'
    note201 = doc_tree('brief', 201, 'My answer that a track to a missing property "is skipped with no error')
    assert 'is my understanding, not a measurement' in note201 and 'M1 and the earlier a7-4 exit 1' in note201
    doc_tree('brief', 199, '### 2026-11-13 — note on the four ideas')
    m1log = (LOGS / 'mutation-a7-M1-lunge-track-property-renamed_60fps.log').read_text(encoding='utf-8', errors='replace')
    assert 'lunge track 4: FrontPivot has no property rotaton' in m1log

    def note_block(d, y, v):
        return quote_block(d, SAFE_L, y + 6, SAFE_R - SAFE_L, 'The author’s note · CHANGE-BRIEF.md:201, “2026-11-13 — note '
                           f'on the four ideas” (a dated addition in the working tree, after {BUILD})', note201,
                           int(v * 0.74)) + int(v * 0.45)

    still('B08', idea_card('Idea 1 · what a clip is', ideas[0], [
        (ptscn, snap_lines(ptscn, range(95, 100), {95: 'tracks/2/path', 99: '"times"'})),
        ('tests/anim_checks.gd · track_problems(), the published function', snap_lines('tests/anim_checks.gd', [32, 33],
                                                                                         {32: 'if not', 33: 'problems'}))],
        'The run clip’s frame track names its target as the string Sprite2D:frame (line 95). Measured: with a property '
        'misspelt (mutation M1), track_problems() reports “lunge track 4: FrontPivot has no property rotaton”, exit 1 '
        '(logs/mutation-a7-M1-…_60fps.log).',
        'CHANGE-BRIEF.md:197, 201 · features/player/player.tscn:95–99 · tests/anim_checks.gd:32–33 · TEST-REPORT.md → '
        'Mutations', extra=note_block),
        {'card': 'media/B08.png', 'source': 'CHANGE-BRIEF.md:197 (ad7935f) and :201 (working tree, the author’s dated note); '
                                            'player.tscn:95-99; anim_checks.gd:32-33; logs/mutation-a7-M1'})

    # B09 — clip 1: the sheet and its slicing.
    sheet_png = Image.open(SRC / 'assets/sprites/mage/mage_run_cycle_sheet.png').convert('RGBA')
    assert sheet_png.size == (248, 69)
    sheet_img = Image.alpha_composite(Image.new('RGBA', sheet_png.size, (246, 243, 236, 255)), sheet_png).convert('RGB')
    attribution = doc_at('walker-magic-zhefan/assets/sprites/mage/ATTRIBUTION.md', 5, '| `mage_run_cycle_sheet.png`')
    assert '4 Hydrogen' in attribution and 'Generative AI Additional Terms' in attribution
    run_head = snap_lines(ptscn, [64, 65, 66, 67], {64: 'resource_name = "run"', 65: 'length', 66: 'loop_mode', 67: 'step'})
    hfr = snap_lines(ptscn, [83, 90], {83: 'tracks/1/path = NodePath("Sprite2D:hframes")', 90: '"values": [4]'})

    def b09(v):
        im, d, y = cards.base('Clip 1 · the sheet and its slicing', 'assets/sprites/mage/mage_run_cycle_sheet.png · '
                              'cell 62×69 · grid 4 × 1 · CHANGE-BRIEF.md:157')
        lw = 2050
        pic, k = scaled(sheet_img, lw, 760, pixel=True)
        cards.paste_framed(im, d, pic, SAFE_L, y + 10)
        for i, name in enumerate(['0 contact', '1 down', '2 passing', '3 up']):
            x = SAFE_L + i * 62 * k
            if i:
                d.line([x, y + 10, x, y + 10 + pic.height], fill=SPARK, width=6)
            cards.badge(d, x + 16, y + 26, name, size=40)
        ty = text_block(d, SAFE_L, y + 10 + pic.height + 20, f'248×69 = 4 cells of 62×69 in one row: hframes = 4, vframes = '
                        f'1 (not keyed, the Sprite2D default); order 0 contact, 1 down, 2 passing, 3 up · enlarged ×{k}, '
                        'nearest neighbour', F('sans', 40), lw, INK_SOFT, 54)
        notes_block(d, SAFE_L, ty + 30, lw, [
            ('Source (assets/sprites/mage/ATTRIBUTION.md)', 'generated with the Gemini app (model shown as “4 Hydrogen”), '
             '2026-11-12, from prompt v3, with the author’s A2 contact sprite as the only reference; cleaned onto the A2 '
             'palette by tools/clean_run_cycle.py; original as downloaded in design/a7/'),
            ('Terms', 'Google Terms of Service and Generative AI Additional Terms of Service')], v)
        rx = SAFE_L + lw + 90
        by = src_block(d, rx, y + 10, SAFE_R - rx, [(ptscn + ' · the run clip', run_head),
                                                     (ptscn + ' · the hframes track', hfr)], int(v * 0.72))
        text_block(d, rx, by + 10, 'test_clip_run.gd: every frame key < hframes × vframes (4) · run-sheet-hframes-4 · '
                   'every-clip-step-one-frame-period-0.1: PASS', F('sans', 38), SAFE_R - rx, INK_SOFT, 50)
        cards.footer(d, 'CHANGE-BRIEF.md revision 2026-11-13 (“The sheet”) · ATTRIBUTION.md · SOURCES.md · '
                        'logs/test_clip_run_60fps.log')
        return im
    still('B09', fit(b09, (60, 56, 52, 48, 44, 40)), {
        'images': ['assets/sprites/mage/mage_run_cycle_sheet.png'],
        'sha256': {'mage_run_cycle_sheet.png': sha256(SRC / 'assets/sprites/mage/mage_run_cycle_sheet.png')},
        'source': 'player.tscn:64-67, 83, 90; ATTRIBUTION.md:5; CHANGE-BRIEF.md:157'})

    # B10 -> B11: the frame track, then the run cell by cell in the capture.
    workbench('B10', 'Clip 1 · the frame track that reads the sheet', ptscn, 92, 103, 'tracks/2/type', [
        ('Line 67', 'step = 0.1 (one key per frame at 10 fps)'),
        ('Lines 65–66', 'length = 0.4 · loop_mode = 1 (LOOP_LINEAR)')],
        [(0.0, 95, 'Line 95: the track keys Sprite2D:frame'),
         ('cells zero to three', 99, 'Line 99: keys at 0, 0.1, 0.2, 0.3 s'),
         ('Step: point one', 101, 'Line 101: update 1 = discrete'),
         ('No duplicate', 102, 'Line 102: cells 0, 1, 2, 3 — no cell 0 repeated at 0.4')], font=26)
    assert line(ptscn, 67, 'step = 0.1') == 'step = 0.1'
    run_rows = [r for r in rows if 20 <= r['f'] <= 44]
    items = [(mage_crop(r, left=31, right=19), f"f{r['f']} · cell {r['pfr']}", i == 0 or r['pfr'] != run_rows[i - 1]['pfr'])
             for i, r in enumerate(run_rows)]

    def b11(v):
        im, d, y = cards.base('Clip 1 · the run, cell by cell', PLAY + ' · frames 20–44, one per physics tick')
        b1, k = crops_row(im, d, items[:13], SAFE_L, y + 10, SAFE_R - SAFE_L, 470, cap_size=34)
        b2, _ = crops_row(im, d, items[13:], SAFE_L, b1 + 20, int((SAFE_R - SAFE_L) * 12 / 13), 470, cap_size=34)
        ty = text_block(d, SAFE_L, b2 + 10, f'Crops of the 640×360 frames around the mage, enlarged ×{k}, nearest neighbour; '
                        f'outlined in orange: the tick a new cell appears (sheet cell from capture/{CAPTURE}-frames.jsonl)',
                        F('sans', 38), SAFE_R - SAFE_L, INK_SOFT, 50)
        cards.table(d, SAFE_L, ty + 24, [1300, 2156], ['Ticks per cell', ''],
                    [('This capture (frames 20–116)', '0:6, 1:6, 2:6, 3:7 on entry, then 0:5, 1:6, 2:6, 3:7 every loop'),
                     ('captures/run/game-r2-ticks/', '6 / 6 / 6 / 7 on entry, 5 / 6 / 6 / 7 per loop (TUNING.md r2)'),
                     ('test_clip_run.gd', '17 / 0: keys 0, 0.1, 0.2, 0.3 within half a frame; length 0.4; LOOP_LINEAR; '
                                          'discrete; step 0.1; seam')], size=v, head_size=int(v * 0.8))
        cards.footer(d, f'capture/{CAPTURE} (scripted input) · logs/test_clip_run_60fps.log · TUNING.md → Run cycle r2')
        return im
    still('B11', fit(b11, (52, 48, 46, 44, 42, 40)), {'images': [f'capture/{CAPTURE} frames 20-44'],
          'capture_sha256': sha256(REEL / 'capture' / f'{CAPTURE}.mp4'), 'frame_log': f'capture/{CAPTURE}-frames.jsonl'},
          evidence=True)
    # the tick counts quoted on B11, checked against this capture's frame log
    cells = [rows[f]['pfr'] for f in range(20, 117)]
    runs_ = []
    for c in cells:
        if runs_ and runs_[-1][0] == c:
            runs_[-1][1] += 1
        else:
            runs_.append([c, 1])
    assert [n for _, n in runs_[:8]] == [6, 6, 6, 7, 5, 6, 6, 7], runs_

    # B12 — idea 2: one authority.  B13 — land, run, cell zero.
    pgd = 'features/player/player.gd'
    still('B12', idea_card('Idea 2 · one authority', ideas[1], [
        (pgd + ' · _set_state() and _play()', snap_lines(pgd, range(143, 155),
                                                          {147: '_play(CLIPS[next])', 148: 'sprite.flip_h', 153: 'anim.play',
                                                           154: 'anim.seek'})),
        ('tests/test_anim_structure.gd', snap_lines('tests/test_anim_structure.gd', [236],
                                                    {236: 'check("no-game-script-writes-a-keyed-property"'}))],
        'The mage’s AnimationPlayer is the one writer of texture, hframes and frame; the state machine only calls play() '
        'from frame 0 when the state changes, and flip_h stays in code. The structure test scans every game script for '
        'writes to a property a clip keys (and must find a planted one): 11 / 0 (logs/test_anim_structure_60fps.log).',
        'CHANGE-BRIEF.md:197 · features/player/player.gd:143–154 · tests/test_anim_structure.gd:236'),
        {'card': 'media/B12.png', 'source': 'CHANGE-BRIEF.md:197; player.gd:143-154; test_anim_structure.gd:236'})
    land = [r for r in rows if 340 <= r['f'] <= 351]
    assert rows[345]['ps'] == 'FALL' and rows[346]['ps'] == 'RUN' and rows[346]['pfr'] == 0
    items = [(mage_crop(r, top=226, bottom=334, left=31, right=19), f"f{r['f']}" + '\n' + f"{r['ps']} · {r['pfr']}",
              r['f'] == 346) for r in land]

    def b13(v):
        im, d, y = cards.base('Land, run, cell zero', PLAY + ' · frames 340–351')
        b1, k = crops_row(im, d, items, SAFE_L, y + 10, SAFE_R - SAFE_L, 760, cap_size=38)
        ty = text_block(d, SAFE_L, b1 + 10, f'Crops around the mage, enlarged ×{k}, nearest neighbour; state · sheet cell '
                        f'from capture/{CAPTURE}-frames.jsonl; orange: the landing tick (FALL → RUN at frame 346, cell 0)',
                        F('sans', 38), SAFE_R - SAFE_L, INK_SOFT, 50)
        cards.table(d, SAFE_L, ty + 30, [1500, 1956], ['Check', 'Result'],
                    [('test_anim_structure.gd · run-reentry-restarts-at-frame-0', 'PASS · 11 checks / 0 failures'),
                     ('test_anim_edges.gd · run → jump → land → run', 'PASS at 30, 60, 144 · re-entry tick 71, cell 0, clip '
                                                                    'position 0.0')], size=v, head_size=int(v * 0.8))
        cards.footer(d, f'capture/{CAPTURE} · logs/test_anim_structure_60fps.log · logs/test_anim_edges_60fps.log')
        return im
    still('B13', fit(b13, (56, 52, 48, 44, 40)), {'images': [f'capture/{CAPTURE} frames 340-351'],
          'capture_sha256': sha256(REEL / 'capture' / f'{CAPTURE}.mp4')}, evidence=True)

    # B14 — idea 4 and the phase table, beside the key times built from it.
    wolf_tscn = 'features/wolf/wolf.tscn'
    head = doc_at('brief', 163, '| Phase | Frames (begins on) | What the player may do | What the game reads |')
    table_rows = [[c.strip() for c in doc_at('brief', n, '| ').strip('|').split('|')] for n in (165, 166, 167)]
    assert [r[0] for r in table_rows] == ['Startup (GROWL)', 'Active (LUNGE)', 'Recovery (RECOVER)']
    note169 = doc_at('brief', 169, 'A hit on the first tick of a phase')
    step_line = line(wolf_tscn, 64, 'step = 0.016666666666666666')
    times_line = line(wolf_tscn, 108, '"times": PackedFloat32Array(')
    times = [float(t) for t in times_line.split('(')[1].split(')')[0].split(',')]
    frames = [0, 25, 31, 37, 53, 65, 89]
    assert all(abs(t - f / 60) < 1e-6 for t, f in zip(times, frames)) and len(times) == 7

    def b14(v):
        im, d, y = cards.base('Idea 4 · feel designed in frames', 'The author’s words · CHANGE-BRIEF.md:163–169 (the '
                              'phase table, revision 2026-11-13) · key times from features/wolf/wolf.tscn')
        ty = quote_block(d, SAFE_L, y + 6, SAFE_R - SAFE_L, IDEA_LABEL, ideas[3], int(v * 1.05))
        lw = 2380
        hdr = [c.strip().replace('`', '') for c in head.strip('|').split('|')]
        body = [[c.replace('`', '').replace('\\|', '|') for c in r] for r in table_rows]
        tb = cards.table(d, SAFE_L, ty + 34, [430, 400, 900, lw - 1730], hdr, body, size=int(v * 0.8),
                         head_size=int(v * 0.66), hi_cols=(0,))
        tb = text_block(d, SAFE_L, tb + 6, note169, F('sans', int(v * 0.66)), lw, INK_SOFT, int(v * 0.88))
        rx = SAFE_L + lw + 90
        cards.table(d, rx, ty + 34, [380, SAFE_R - rx - 380], ['Key frame', 'Time (frame ÷ 60), line 108'],
                    [(str(f), f'{t:.4f} s') for f, t in zip(frames, times)], size=int(v * 0.8), head_size=int(v * 0.62),
                    hi_cols=(0,))
        assert tb < 1950, f'B14 overflows ({tb})'
        cards.footer(d, f'CHANGE-BRIEF.md:163–169, 197 · {wolf_tscn}:64 ({step_line}) and :108')
        return im
    still('B14', fit(b14, (80, 76, 72, 68, 64, 60, 56, 52, 48, 46, 44)), {'card': 'media/B14.png',
          'source': 'CHANGE-BRIEF.md:163-169,197; wolf.tscn:64,108'})

    # B15 -> B16: the scale track, then each boundary in a fixture strip and in play.
    workbench('B15', 'Clip 2 · the keys built from the phase table', wolf_tscn, 101, 112, 'tracks/3/type', [
        ('Line 64', 'step = 0.016666666666666666 (1/60 s)'),
        ('Key frames ÷ 60 (all four pose tracks)', '0, 25, 31, 37, 53, 65, 89 → 0, 0.4167, 0.5167, 0.6167, 0.8833, '
                                                  '1.0833, 1.4833 s')],
        [(0.0, 104, 'Line 104: the track keys Facing/Rig:scale'),
         ('frames zero', 108, 'Line 108: key times = frame ÷ 60'),
         ('crouch, stretch', 111, 'Line 111: (1.08, 0.86) crouch · (1.22, 0.84) stretch · (0.94, 1.06) overshoot')],
        font=23)
    ticks_fx = {r['since_growl']: r for r in (json.loads(l) for l in
                (CAPS / 'lunge/game-r0/ticks_take_lunge.jsonl').read_text(encoding='utf-8').splitlines())}
    fx_items, play_items = [], []
    play_frames = {0: 880, 31: 911, 53: 933, 89: 969}
    for g, f in play_frames.items():
        fr = ticks_fx[g]
        fx_items.append((cap(f'lunge/game-r0/take_lunge_g+{g:02d}.png').crop((220, 200, 500, 345)),
                         f"g+{g} · {fr['w_state']} · clip {fr['clip']} {fr['clip_frame']}", True))
        r = rows[f]
        assert r['f'] - 880 == g and r['wcf'] == (g if g < 89 else 0), (g, r)
        play_items.append((wolf_crop(r), f"frame {f} · g+{g} · {r['ws']} · clip {r['wclip']} {r['wcf']}", True))
    assert rows[880]['ws'] == 'GROWL' and rows[879]['ws'] == 'PATROL'

    def b16(v):
        im, d, y = cards.base('Each phase boundary, in a strip and in play', 'Fixture capture (top) · ' + PLAY + ' (bottom)'
                              ' · ' + RESULTS)
        d.text((SAFE_L, y), 'Fixture capture · captures/lunge/game-r0/take_lunge_g+00, +31, +53, +89 (the harness places the '
               'characters; its overlay and collision shapes are on)', font=F('sans', 38), fill=INK_SOFT)
        b1, k = crops_row(im, d, fx_items, SAFE_L, y + 60, SAFE_R - SAFE_L, 560, cap_size=40)
        d.text((SAFE_L, b1 + 20), f'{PLAY} · frames 880, 911, 933, 969: the first lunge of B04, g+0 = GROWL entry',
               font=F('sans', 38), fill=INK_SOFT)
        b2, _ = crops_row(im, d, play_items, SAFE_L, b1 + 80, SAFE_R - SAFE_L, 560, cap_size=40)
        ty = text_block(d, SAFE_L, b2 + 16, f'Crops enlarged ×{k}, nearest neighbour; g+n = physics ticks since the growl '
                        'began (clip frame n). test_clip_lunge.gd: 18 checks / 0 failures — every track resolves to a real '
                        'node and property; key times = frames ÷ 60 within half a frame; step 1/60; length 89/60, '
                        'LOOP_NONE; poses match the table.', F('sans', v), SAFE_R - SAFE_L, INK, int(v * 1.25))
        assert ty < 1950, ty
        cards.footer(d, 'captures/lunge/game-r0/ (tests/capture_lunge.gd) · capture/' + CAPTURE +
                     '-frames.jsonl · logs/test_clip_lunge_60fps.log')
        return im
    still('B16', fit(b16, (60, 56, 52, 48, 46, 44, 42, 40, 38)), {
        **caps_prov(*[f'lunge/game-r0/take_lunge_g+{g:02d}.png' for g in play_frames]),
        'capture_frames': list(play_frames.values()), 'capture_sha256': sha256(REEL / 'capture' / f'{CAPTURE}.mp4')},
        evidence=True)

    # B17 — idea 3: the two clocks, measured.
    wgd = 'features/wolf/wolf.gd'
    probes = {}
    for fps in (30, 60, 144):
        for l in (LOGS / f'probe_two_clocks_{fps}fps.log').read_text(encoding='utf-8', errors='replace').splitlines():
            if l.startswith('{'):
                r = json.loads(l)
                probes.setdefault(fps, {})[r['id']] = r.get('observed') or r.get('observation')
    for fps, p in probes.items():
        c = p['clip-time-equals-phase-time-on-every-lunge-clip-tick']
        w = p['lunge-active-window']
        assert c['lunge_clip_ticks'] == 89 and c['largest_abs_difference_s'] < 2e-15, (fps, c)
        assert w['clip_active_section_frames'] == [31, 52] and w['gameplay_reads_hitbox_frames'] == [32, 53]
        assert w['monitoring_on_frames'] == [31, 53] and abs(w['largest_offset_s'] - 1 / 60) < 1e-9

    def clocks_table(d, y, v):
        return cards.table(d, SAFE_L, y, [1250, SAFE_R - SAFE_L - 1250],
                           ['tests/probe_two_clocks.gd at 30, 60 and 144 fps (identical)', 'Measured'], [
            ('Clip time against phase time', 'equal on all 89 lunge-clip ticks; largest difference 1.4e-15 s'),
            ('The hitbox read (LUNGE branch, line 89)', 'clip frames 32–53 against the active section 31–52: '
                                                        'largest disagreement 1/60 s ≈ 0.0167 s'),
            ('monitoring', 'on for frames 31–53: switched off with set_deferred (line 121)'),
            ('The process clock', 'the torch flicker player and the wolf’s removal timer (tick 79 at 60 fps, 80 at 30 and '
                                  '144); gameplay reads neither')], size=int(v * 0.7), head_size=int(v * 0.6), hi_cols=(0,))

    still('B17', idea_card('Idea 3 · two clocks, measured', ideas[2], [
        (wolf_tscn + ' · the AnimationPlayer', snap_lines(wolf_tscn, [251, 252], {251: 'process_physics_priority = -1',
                                                                                   252: 'callback_mode_process = 0'})),
        (wgd + ' · the hitbox, read and switched off', snap_lines(wgd, [89, 121], {89: 'for body in lunge_hitbox',
                                                                                  121: 'lunge_hitbox.set_deferred'}))],
        'callback_mode_process = 0 is ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS. The author’s short answer 5 first said '
        '0 s and was corrected to the probe’s measurement (CHANGE-BRIEF.md:193).',
        'CHANGE-BRIEF.md:183, 193, 197 · logs/probe_two_clocks_30fps.log · _60fps.log · _144fps.log · TEST-REPORT.md → Two clocks',
        extra=clocks_table, sizes=(72, 68, 64, 60, 56, 52, 48, 46, 44, 42, 40)),
        {'card': 'media/B17.png', 'source': 'CHANGE-BRIEF.md:197; wolf.tscn:251-252; wolf.gd:89,121; '
                                            'logs/probe_two_clocks_{30,60,144}fps.log'})

    # B18 -> B19: the change, then what the pin saw.
    workbench('B18', 'The one behaviour change: a growl hit cancels the lunge', wgd, 152, 163, 'func take_damage', [
        ('Line 24', 'const RECOVER_FRAME := 53'),
        ('Lines 164–171', 'the last HP: DEAD in every phase')],
        [(0.0, 158, 'Line 158: only during GROWL'),
         ('sends the wolf to recover', 159, 'Line 159: straight to RECOVER'),
         ('seeks the clip', 162, 'Line 162: seek to frame 52, so the hit tick shows 53'),
         ('Every other phase', 163, 'Line 163: any other phase: HP only')], font=24)
    still('B19', figure_left_notes('What the pin saw', FIGLABEL + ' · logs/pin/hit_growl.json · git log',
        cap('figures/pin_timeline.png'),
        'captures/figures/pin_timeline.png: hit_growl before (a9b4bc1) and after (ff71bbb); one cast at tick 4, the hit '
        'on tick 24', [
            ('Pin first (tests/test_pin_behaviour.gd)', 'a9b4bc1: 8 scenarios, every physics tick, real input, 16 / 0 at '
                                                        '30, 60, 144 · clips 72e8d21 and wired 33d78ae: unchanged'),
            ('The change, 72f37b8', 'hit_growl from tick 24: GROWL → RECOVER, no lunge; kill too (its first hit lands '
                                    'in GROWL), not predicted'),
            ('Played, then re-pinned, ff71bbb', 'only hit_growl.json and kill.json changed; 16 / 0 at 30, 60, 144')],
        'TEST-REPORT.md → Pins · FRICTIONAL.md → Predictions · git show --stat ff71bbb', frac=0.6),
        caps_prov('figures/pin_timeline.png'), evidence=True)

    # B20 — edges before, on and after every boundary (identical at 30, 60, 144).
    edges = {}
    for fps in (30, 60, 144):
        res = {}
        for l in (LOGS / f'test_anim_edges_{fps}fps.log').read_text(encoding='utf-8', errors='replace').splitlines():
            if l.startswith('{"id"'):
                r = json.loads(l)
                res[r['id']] = r
            if l.startswith('WALKER TESTS'):
                res['summary'] = l
        edges[fps] = res
    for fps in (30, 144):
        assert edges[fps]['summary'] == edges[60]['summary'] == 'WALKER TESTS: 25 checks / 0 failures'
    e60 = edges[60]
    bnames = [('growl-start', 0, 'GROWL start'), ('growl-to-lunge', 31, 'GROWL → LUNGE'),
              ('lunge-to-recover', 53, 'LUNGE → RECOVER'), ('recover-to-patrol', 89, 'RECOVER → PATROL')]
    rule = {'cancel': 'cancel', 'no-cancel': 'no cancel', 'hp-only': 'HP only'}
    grid = []
    for key, frame, name in bnames:
        row = [f'{name} (frame {frame})']
        for when in ('before', 'on', 'after'):
            hit = next(v for k, v in e60.items() if k.startswith(f'boundary-{key}-{when}-'))
            assert hit['status'] == 'PASS'
            outcome = rule[hit['id'].split(f'-{when}-')[1]]
            for fps in (30, 144):
                assert edges[fps][hit['id']]['status'] == 'PASS'
            row.append(f"tick {hit['observed']['hit_tick']} · {hit['observed']['expected_phase']}: {outcome}")
        grid.append(row)
    still('B20', table_card('Edges: before, on and after every boundary', RESULTS + ' · tests/test_anim_edges.gd · real '
        'clicks · reference: growl from tick 80', ['Boundary of the lunge clip', 'One tick before', 'On the boundary',
                                                    'One tick after'], grid, [1000, 820, 820, 816],
        'A hit is resolved before the wolf’s update on its tick, so a hit “on” a boundary follows the phase before. Also: '
        'first and last tick of GROWL and LUNGE, first of RECOVER; a killing hit in GROWL, LUNGE and RECOVER (DEAD, dead '
        'clip); a real Esc mid-lunge freezes and resumes aligned; run → jump → land restarts at frame 0; clip frame = '
        'phase tick on 119 ticks. 25 checks / 0 failures at 30, 60 and 144 fps.',
        'logs/test_anim_edges_30fps.log · _60fps.log · _144fps.log (b33642a) · TEST-REPORT.md → Edges', hi_cols=(0,)),
        {'card': 'media/B20.png', 'source': 'logs/test_anim_edges_{30,60,144}fps.log'})

    # B21 — the four published mutations.
    def summary(name):
        return next(l for l in (LOGS / name).read_text(encoding='utf-8', errors='replace').splitlines()
                    if l.startswith('WALKER TESTS')).replace('WALKER TESTS: ', '')
    m1 = (LOGS / 'mutation-a7-M1-lunge-track-property-renamed_60fps.log').read_text(encoding='utf-8', errors='replace')
    assert 'lunge track 4: FrontPivot has no property rotaton' in m1
    m4 = [summary(f'mutation-a7-M4-fresh-import-{n}_60fps.log') for n in ('clip-run', 'clip-lunge', 'clip-flicker',
                                                                          'anim-structure')]
    still('B21', table_card('Broken on purpose: M1 to M4', RESULTS + ' · each from a sparse git worktree of HEAD, '
        'removed after (50aac04)', ['Mutation', 'What the test printed', 'Result'], [
            ('M1 · lunge track subname renamed in the clip only (rotation → rotaton)',
             'track_problems(): “lunge track 4: FrontPivot has no property rotaton”',
             summary('mutation-a7-M1-lunge-track-property-renamed_60fps.log') + ' · exit 1'),
            ('M2 · run loop_mode = LOOP_NONE', 'run-length-0.4-loop-linear and only-run-loops: FAIL (loop_mode 0)',
             summary('mutation-a7-M2-run-loop-none_60fps.log') + ' · exit 1'),
            ('M3 · run frame key = hframes × vframes (4)', 'every frame key < hframes × vframes: FAIL (frame 4, 4 cells '
                                                          'in all)', summary('mutation-a7-M3-run-frame-key-4_60fps.log') +
             ' · exit 1'),
            ('M4 · .godot deleted, --import, every read-back', 'run, lunge, flicker, structure: ' + ', '.join(m4) +
             '; 0 error lines', 'passes: the clips are scene text, not imported — it proves no more than that')],
        [1150, 1450, 856], 'Five earlier mutation logs (logs/mutation-a7-1…5): a Godot 3 loop = true loads as loop_mode 1 '
        'and still loops on 4.7.2 (not caught, harmless); a continuous frame track, a track to a missing node and the '
        'growl cancel removed are caught; a7-3 is the same mutation as M3.',
        'logs/mutation-a7-M*_60fps.log · TEST-REPORT.md → Mutations (exit codes)'),
        {'card': 'media/B21.png', 'source': 'logs/mutation-a7-M1..M4_60fps.log; TEST-REPORT.md:13'})

    # B22 — what the read-backs proved, and what no headless run shows.
    nohead = doc_at('report', 27, 'Whether either motion reads or feels committed')
    rb = [(n, summary(f'test_{n}_60fps.log')) for n in ('clip_run', 'clip_lunge', 'clip_flicker', 'anim_structure')]
    assert [s for _, s in rb] == ['17 checks / 0 failures', '18 checks / 0 failures', '12 checks / 0 failures',
                                  '11 checks / 0 failures'], rb

    def b22(v):
        im, d, y = cards.base('What the read-backs proved, and what they cannot', RESULTS + ' · TEST-REPORT.md:12, 15, 25–27')
        ty = cards.table(d, SAFE_L, y + 10, [900, 650, SAFE_R - SAFE_L - 1550], ['Read-back (60 fps)', 'Log', 'Checks'], [
            ('test_clip_run.gd', rb[0][1], 'track_problems(); keys 0, 0.1, 0.2, 0.3 within half a frame; step 0.1; '
                                           'LOOP_LINEAR; discrete; frame keys < hframes × vframes; seam'),
            ('test_clip_lunge.gd', rb[1][1], 'track_problems(); key times = frames ÷ 60 within half a frame; step 1/60; '
                                             'length 89/60, LOOP_NONE; rig parts and pivots'),
            ('test_clip_flicker.gd', rb[2][1], 'step 0.01; LOOP_LINEAR; continuous energy and size; seam per track'),
            ('test_anim_structure.gd', rb[3][1], 'every state has its clip; play() uses it; autoplay empty; physics '
                                                 'callback; no other writer; one player per sprite')],
            size=int(v * 0.9), head_size=int(v * 0.75), hi_cols=(0,))
        ty = text_block(d, SAFE_L, ty + 30, 'TEST-REPORT.md → What no headless run shows', F('serif_med', int(v * 1.1)),
                        SAFE_R - SAFE_L, SPARK, int(v * 1.4))
        ty = quote_block(d, SAFE_L, ty + 10, SAFE_R - SAFE_L, 'TEST-REPORT.md:27, the author’s words', nohead, int(v * 1.05))
        assert ty < 1950, ty
        cards.footer(d, 'logs/test_clip_run_60fps.log · test_clip_lunge · test_clip_flicker · test_anim_structure · '
                        'TEST-REPORT.md')
        return im
    still('B22', fit(b22, (72, 68, 64, 60, 56, 52, 48, 46, 44, 42)), {'card': 'media/B22.png',
          'source': 'logs/test_clip_*_60fps.log; logs/test_anim_structure_60fps.log; TEST-REPORT.md:27'})

    # B23 — Claude against the author.
    against = doc_at('report', 23, '| **Claude against me** | ')
    slips = doc_at('frictional', 42, '**Process slips.** ')
    assert '2.6–3.3 px' in against and 'I rejected r1 in play' in against and 'not noticeable' in against
    assert 'it still looks like the feet twitch' in doc_at('tuning', 28, '**r1:**')
    r1img = cap('run/analysis/run_r1_beats_vs_r0_6x.png')

    def b23(v):
        im, d, y = cards.base('Claude against the author', FIXTURE + ' · TEST-REPORT.md:23 · TUNING.md · FRICTIONAL.md:42')
        pic, _ = scaled(r1img, SAFE_R - SAFE_L, 560)
        cards.paste_framed(im, d, pic, SAFE_L, y + 10)
        ty = text_block(d, SAFE_L, y + 10 + pic.height + 14, 'captures/run/analysis/run_r1_beats_vs_r0_6x.png: r0 and r1 at '
                        'each of r1’s four beats (game strip, collision shapes on)', F('sans', 38), SAFE_R - SAFE_L,
                        INK_SOFT, 50) + 30
        cw = (SAFE_R - SAFE_L - 90) // 2
        notes_block(d, SAFE_L, ty, cw, [
            ('Waist seam (TEST-REPORT.md:23)', 'Claude estimated a 2.6–3.3 px step; the author saw none, and neither did '
                                               'Claude at 4× in the game strip'),
            ('Run r1 (fc096c9), the strip above', 'hat rows 268 / 270 / 267 / 265 exactly as predicted; in play: “it still '
                                                  'looks like the feet twitch” — reverted (338c8bf)')], v)
        notes_block(d, SAFE_L + cw + 90, ty, cw, [
            ('Visual upgrades r0 (TUNING.md)', 'Claude read them as matching its values; the author: “not noticeable” → '
                                               'r1, then “clearly visible”'),
            ('Process slips the author recorded (FRICTIONAL.md:42)', 'one amended local commit; a temporary backup one '
             'folder above the assignment root for a few seconds; the mutation script run from a temporary folder outside '
             'the repository; nothing left behind')], v)
        cards.footer(d, 'TEST-REPORT.md → Claude against me · TUNING.md (the author’s verdicts, translated) · '
                        'FRICTIONAL.md → Process slips')
        return im
    still('B23', fit(b23, (64, 60, 56, 52, 48, 46, 44, 42)), caps_prov('run/analysis/run_r1_beats_vs_r0_6x.png'))

    # B24 — uncertain, and the next step.
    nxt = doc_at('frictional', 26, '**What I learned:**')
    assert 'The next test is in-betweens for the planted foot, in the final project.' in nxt
    doc_at('readme', 62, '- The growl-cancel window is 0.2 s')
    doc_at('readme', 63, "- The run's planted foot still slides")
    lim = doc_at('submission', 16, 'Known limitations:')
    assert '1/60 s' in lim
    fresh = doc_at('report', 14, '| **Fresh cache** | A clean local clone of HEAD')
    still('B24', columns('Uncertain, and the next step', 'README.md → Known limitations · SUBMISSION.md · FRICTIONAL.md · '
                         'this film', [
        ('Still open in the game', [
            ('', 'The planted foot still slides while a frame is held.'),
            ('', 'The growl window is 0.2 s from sight distance — kept by the author’s decision.'),
            ('', 'The hitbox is read 1/60 s after the clip’s active section begins.')]),
        ('Not confirmed by this film', [
            ('', 'A fresh clone of the submitted commit: it comes after this film (TEST-REPORT.md:14 records a clean '
                 'local clone of HEAD as it was then: import, then 17 / 0 and 18 / 0).'),
            ('', 'A broken track “skipped with no error”: the author’s understanding, not a measurement (the author’s '
                 'note, CHANGE-BRIEF.md:201); no run here played a broken clip.'),
            ('', 'Feel: scripted input here; the verdicts are the author’s, in play.')]),
        ('The next step (FRICTIONAL.md:26)', [
            ('', '“The next test is in-betweens for the planted foot, in the final project.”'),
            ('Also open (FRICTIONAL.md:53)', 'whether the growl window should be wider — a gameplay change with its own '
                                             'pin and re-pin')])],
        'README.md:62–64 · SUBMISSION.md:16 · TEST-REPORT.md:14 · CHANGE-BRIEF.md:201 · FRICTIONAL.md:26, 52–53'),
        {'card': 'media/B24.png', 'source': 'README.md:62-64; SUBMISSION.md:16; TEST-REPORT.md:14; CHANGE-BRIEF.md:201 '
                                            '(working tree); FRICTIONAL.md:26,52-53'})

    # B25 — who did what; the sheet's source and terms; the revision shown.
    doc_at('frictional', 46, '- **Mine:**')
    doc_at('frictional', 47, '- **Claude Code:**')
    doc_at('frictional', 48, '- **claude.ai (chat):**')
    doc_at('submission', 15, 'Summary of my work:')
    still('B25', columns('Who did what', f'FRICTIONAL.md → Human and AI contributions · SUBMISSION.md · ATTRIBUTION.md · '
                         f'game source shown {BUILD}', [
        ('The author', [
            ('', 'Both clips and their look; the per-phase interrupt rule; keeping the 0.2 s window.'),
            ('', 'Every first look and verdict in the running game; the run images in Gemini; the re-pin after play; '
                 'reviews of the agent’s CLAUDE.md draft; the human checks.')]),
        ('Claude Code', [
            ('', 'The pin, clips and rig, read-backs with the published track_problems(), structure and edges tests, '
                 'probes, harnesses, mutations, visual upgrades, figures, measurements; this film.')]),
        ('claude.ai (chat)', [
            ('', 'Planning, commands, the brief and its revisions from the author’s decisions, the Gemini prompts, the '
                 'documents.')]),
        ('The run sheet', [
            ('', 'Gemini app, model shown as “4 Hydrogen”, 2026-11-12, prompt v3; Google Terms of Service and Generative AI '
                 'Additional Terms of Service; original in design/a7/.'),
            ('Revision shown', f'{BUILD} ({BUILD_FULL[:12]}…)')])],
        'FRICTIONAL.md:46–48 · SUBMISSION.md:15 · assets/sprites/mage/ATTRIBUTION.md:5 · git log'),
        {'card': 'media/B25.png', 'source': 'FRICTIONAL.md:46-48; SUBMISSION.md:15; ATTRIBUTION.md:5'})


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
        'note': f'How each non-Remotion slot was made. Gameplay: capture/{CAPTURE} at {BUILD} (scripted input, real '
                'engine output; see CAPTURE.md). Fixtures: the author’s committed captures in captures/ (capture '
                'harnesses that place the characters). Figures: captures/figures/ (tools/make_figures.py). Document '
                f'lines: checked equal to the files at {BUILD} (git show).',
        'documents_quoted_at': BUILD, 'documents_changed_in_working_tree_since': DOC_DRIFT,
        'working_tree_lines_quoted': TREE_QUOTES,
        'beats': {**PROV, **footage}})
    print('media built:', ', '.join(sorted(PROV)), '· documents quoted at', BUILD, '· changed since:', sorted(DOC_DRIFT))


if __name__ == '__main__':
    main()
