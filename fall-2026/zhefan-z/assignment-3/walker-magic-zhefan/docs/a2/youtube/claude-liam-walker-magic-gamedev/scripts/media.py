"""Phase 2: build every non-Remotion slot and fill Remotion props, using measured narration.

Gameplay rule: every clip is cut from a Movie Maker take at normal speed, taking
every second 60 fps source frame for 30 fps output, to exactly the frame count
the compiler will give the beat, so compile.py's retime/slow/center-cut ladder is
never exercised (ratio 1.000000). Any surplus is a labelled final-frame hold.
SLICE AUDIO: the take's own audio, cut sample-exactly to the same interval.
"""
import base64
import io
import json
import shutil
from pathlib import Path

from PIL import Image

import cards
from common import (REEL, GAME, BUILD, CAPTURE_SOURCE, FPS, SRC_FPS, W, H, SAMPLES_PER_SRC_FRAME, SNAPSHOT,
                    load_json, save_json, render_frames, run, probe_frames, source_lines, sha256)

CAP = REEL / 'capture'
MEDIA = REEL / 'media'
WORK = MEDIA / '_work'
AUDIO = REEL / 'audio'
ENC = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-an']
SRC = SNAPSHOT or GAME


# ---------------------------------------------------------------- take facts (from the input logs)
def events(take):
    rows = [json.loads(l) for l in (CAP / f'{take}-inputs.jsonl').read_text(encoding='utf-8').splitlines()]
    return rows


def tick_time(take, event, action=None, attempt=1, nth=0):
    hits = [r for r in events(take) if r['event'] == event and r.get('attempt', 1) == attempt
            and (action is None or r.get('action') == action)]
    return hits[nth]['tick'] / SRC_FPS


R1 = {'jump': tick_time('run-01', 'press', 'jump'), 'stop': tick_time('run-01', 'release', 'move_right'),
      'hurt': tick_time('run-01', 'game:hurt'), 'cast1': tick_time('run-01', 'game:cast'),
      'cast2': tick_time('run-01', 'game:cast', nth=1), 'down': tick_time('run-01', 'game:wolf_down'),
      'clear': tick_time('run-01', 'game:clear')}
# The driver releases "right" 10 ticks after it first reads the wolf in GROWL (capture_driver.gd, run-01),
# so GROWL began about 10 ticks before that release (±1 tick); it lasts GROWL_TIME = 0.5 s (wolf.gd line 21).
R1['growl'] = R1['stop'] - 10 / SRC_FPS
R1['lunge'] = R1['growl'] + 0.5
R1['gone'] = R1['down'] + 0.6                  # DOWN_TIME (wolf.gd line 27)
R2_FAIL = tick_time('run-02', 'game:fail')
TAKE_FRAMES = {t: probe_frames(CAP / f'{t}.avi')[0] for t in ('run-01', 'run-02', 'run-03', 'run-04')}

DISCLOSE = 'Scripted-input capture · {take} · build 74c0443 · real input events, not a person playing'
SLICE = 'SLICE AUDIO — no narration · scripted-input capture · {take} · the game’s own sound'


# ---------------------------------------------------------------- helpers
def nframes(bid):
    return render_frames(BEATS[bid]['actual_duration_s'])


def at(bid, phrase, frames=None):
    """Seconds into the beat where a narration phrase starts (character-proportional estimate)."""
    text = BEATS[bid]['narration_text']
    i = text.index(phrase)
    total = (frames or nframes(bid)) / FPS
    return round(i / len(text) * total, 2)


def label_png(name, items):
    path = WORK / f'label-{name}.png'
    im, boxes = cards.labels(items)
    im.save(path)
    return path, boxes


def src_frames(t0, t1):
    f0 = round(t0 * SRC_FPS)
    f0 -= f0 % 2
    n = round((t1 - t0) * FPS)
    return f0, f0 + 2 * n, n


def footage(take, t0, t1, out, overlays=(), hold=0):
    """Live take interval [t0, t1) at normal speed (+ hold frames), with timed overlays (png, from_s, to_s)."""
    f0, f1, n = src_frames(t0, t1)
    assert f1 <= TAKE_FRAMES[take], f'{take}: interval ends after the take ({f1} > {TAKE_FRAMES[take]})'
    total = n + hold
    graph = (f"[0:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS,select='not(mod(n\\,2))',"
             f"setpts=N/{FPS}/TB" + (f',tpad=stop_mode=clone:stop={hold}' if hold else '') + '[v0]')
    inputs = ['-i', CAP / f'{take}.avi']
    for i, (png, a, b) in enumerate(overlays):
        inputs += ['-i', png]
        graph += f";[v{i}][{i + 1}:v]overlay=0:0:enable='between(t\\,{a:.4f}\\,{b:.4f})'[v{i + 1}]"
    # MJPEG is full-range YUV; convert to the limited range every other slot (and the master) uses.
    graph += f";[v{len(overlays)}]scale=in_range=full:out_range=tv,format=yuv420p[vout]"
    run(['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', graph, '-map', '[vout]',
                                                    '-frames:v', str(total)] + ENC + [out])
    got = probe_frames(out)[0]
    assert got == total, f'{out}: {got} frames, expected {total}'
    return {'take': take, 'src_frame_start': f0, 'src_frame_end': f1, 'take_start_s': f0 / SRC_FPS,
            'take_end_s': f1 / SRC_FPS, 'live_frames': n, 'held_frames': hold}


def still_clip(png, frames, out):
    run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', png, '-frames:v', str(frames)] + ENC + [out])
    assert probe_frames(out)[0] == frames
    return {'still': str(Path(png).relative_to(REEL)).replace('\\', '/'), 'frames': frames}


def concat(parts, out):
    """Join parts frame for frame (concat filter; each part re-timed to the same 30 fps clock)."""
    inputs, graph = [], ''
    for i, p in enumerate(parts):
        inputs += ['-i', p]
        graph += f'[{i}:v]format=yuv420p,setpts=N/{FPS}/TB,setsar=1[p{i}];'
    graph += ''.join(f'[p{i}]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=0[v]'
    expected = sum(probe_frames(p)[0] for p in parts)
    run(['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', graph, '-map', '[v]',
                                                    '-frames:v', str(expected)] + ENC + [out])
    got = probe_frames(out)[0]
    assert got == expected, f'{out}: {got} frames after concat, parts sum to {expected}'
    return got


def take_audio(take, t0, t1, out):
    f0, f1, _ = src_frames(t0, t1)
    s0, s1 = f0 * SAMPLES_PER_SRC_FRAME, f1 * SAMPLES_PER_SRC_FRAME
    run(['ffmpeg', '-y', '-v', 'error', '-i', CAP / f'{take}.avi', '-vn', '-af',
         f'atrim=start_sample={s0}:end_sample={s1},asetpts=PTS-STARTPTS', '-ar', '48000', '-ac', '2',
         '-c:a', 'pcm_s16le', out])
    return {'take': take, 'start_sample': s0, 'end_sample': s1, 'rate': 48000}


def audio_concat(parts, out):
    inputs = []
    for p in parts:
        inputs += ['-i', p]
    graph = ''.join(f'[{i}:a]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=0:a=1[a]'
    run(['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', graph, '-map', '[a]', '-ar', '48000',
                                                    '-ac', '2', '-c:a', 'pcm_s16le', out])


def data_uri(img, fmt='PNG'):
    buf = io.BytesIO()
    img.save(buf, fmt)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(buf.getvalue()).decode()


def take_frame(take, t):
    out = WORK / f'frame-{take}-{t:.2f}.png'
    run(['ffmpeg', '-y', '-v', 'error', '-i', CAP / f'{take}.avi', '-vf', f"select='eq(n\\,{round(t * SRC_FPS)})'",
         '-frames:v', '1', out])
    return Image.open(out).convert('RGB')


def disclosure_qc(boxes, reason):
    regions = [{'label': f'Disclosure label {i + 1}',
                'box': [round((b[0] + 30) / W, 4), round((b[1] + 14) / H, 4), round((b[2] - 30) / W, 4),
                        round((b[3] - 14) / H, 4)]} for i, b in enumerate(boxes)]
    return {'full_bleed': True, 'full_bleed_reason': 'Native 4K Godot capture fills the frame; not a slide.',
            'contrast_reason': reason, 'contrast_regions': regions}


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


def workbench(bid, title, rel, start, end, first, notes, cues, font=30):
    code = excerpt(rel, start, end, first)
    remotion(bid, mode='code', title=title, project='walker-magic', path=rel,
             source=f'Exact source at {BUILD} · lines {start}–{end} · next: the visible result',
             code=code, startLine=start, codeFontSize=font,
             notes=[{'label': k, 'value': v} for k, v in notes],
             output=[f'Godot editor reconstruction · {rel} lines {start}–{end} · build {BUILD}'],
             cues=[{'at': at(bid, p) if isinstance(p, str) else p, 'line': line, 'label': lab} for p, line, lab in cues])
    BEATS[bid]['excerpt'] = {'path': rel, 'start_line': start, 'end_line': end}


# ---------------------------------------------------------------- beats
def build():
    prov = {}

    # B01, B02, B24, B25, B26: library compositions; only the measured duration is added.
    for bid in ('B01', 'B25'):
        remotion(bid)
    BEATS['B02'].pop('lead_silence_s', None)   # not applied by any toolkit step
    remotion('B02', contextTitle='What got built', contextItems=[
        {'label': 'The slice', 'detail': 'Two screens · one mage, one wolf, one pit, one exit'},
        {'label': 'Art', 'detail': 'Gemini app'}, {'label': 'Effects', 'detail': 'Stable Audio Open'},
        {'label': 'Music', 'detail': 'Lyria'}])
    remotion('B24', brandLabel='@NikBearBrown', artifactLines=[
        'Implemented: every state, one wolf, five sounds on real events, a looping track, readable muted.',
        'Limits: no boss yet, and the HUD font is smooth, not pixel.',
        'Limits: the hit box covers her head when she crouches; the defeat image keeps running legs.',
        'Human judgment: six human playtests are where “it feels fair” and “the loop is clean” come from.',
        'Next: the boss arena — the same wolf scene at 2×, 10 HP, a 2-damage lunge.'])
    BEATS['B26']['shot']['remotion']['props']['durationSeconds'] = nframes('B26') / FPS

    # B03 — requirements card (still).
    cards.requirements([
        ('Concept and pillars', 'The idea in plain terms and the four design pillars.'),
        ('One asset, design to game', 'CHAR-IDLE: sheet → prompt → raw output → edits → engine.'),
        ('States and sounds in real play', 'Two or more character states; the five sound events.'),
        ('The slice’s own audio', 'A labelled stretch with no narration over it.'),
        ('A cause and its effect', 'Palette revision 1: a problem, a change, a visible result.'),
        ('An honest accounting', 'Tests, open questions, next step, who made what, the revision.')],
        f'Build shown: {BUILD} · captured from copy {CAPTURE_SOURCE}: identical game files, only a text log differs',
        'Summarised from the film brief the author gave Claude Code (2026-10-07)').save(MEDIA / 'B03.png')
    prov['B03'] = {'card': 'media/B03.png'}

    # B04 — CONCEPT board (Remotion), then P1 in engine (scripted-input capture).
    n = nframes('B04')
    n1 = round(at('B04', 'Watch for the second pillar') * FPS) - 6
    n2 = n - n1
    pitch = excerpt('CONCEPT.md', 7, 7, 'The player is a young fire mage')
    board = {'title': 'Concept and pillars', 'section': 'CONCEPT.md · The game in two sentences', 'excerpt': pitch,
             'source': f'CONCEPT.md lines 7 and 25–29 at {BUILD} · pillar cards are short interpretations',
             'status': 'Design document · four pillars (CONCEPT.md lines 26–29)',
             'visualLabel': 'Next: the first view in engine, where everything is cool except her',
             'layout': 'cards', 'cards': [
                 {'label': '1 · Every failure is fair.', 'text': 'Marked pits, a warning before every attack.'},
                 {'label': '2 · Your fire is the only warmth.', 'text': 'Cool cave; fireball and crystal are the only warm colours.'},
                 {'label': '3 · Readable at a glance, even muted.', 'text': 'White hair brightest; hits flash; failures say why.'},
                 {'label': '4 · Small mage, big threat.', 'text': 'Fragile but capable (the boss is not in this slice).'}],
             'cues': [{'at': at('B04', 'Four pillars'), 'card': 0}, {'at': at('B04', 'Her fire'), 'card': 1},
                      {'at': at('B04', 'You can read'), 'card': 2}, {'at': at('B04', 'Small mage'), 'card': 3}],
             'durationSeconds': n1 / FPS}
    from remotion_win import render_component
    part1, stamp = WORK / 'B04-board.mp4', WORK / 'B04-board.props.json'
    if not (part1.exists() and stamp.exists() and json.loads(stamp.read_text(encoding='utf-8')) == board):
        render_component('GodotDesignBoard', board, part1)
        stamp.write_text(json.dumps(board), encoding='utf-8')
    assert probe_frames(part1)[0] == n1, 'B04 board frame count'
    lab, boxes = label_png('B04', [(DISCLOSE.format(take='run-01'), 'tl', 'disclosure')])
    p2 = footage('run-01', 0.0, n2 / FPS, WORK / 'B04-p1.mp4', [(lab, 0, 99)])
    assert concat([part1, WORK / 'B04-p1.mp4'], MEDIA / 'B04.mp4') == n
    BEATS['B04']['shot'].update({'type': 'VIDEO', 'composite': [
        {'frames': n1, 'remotion': {'pattern': 'GodotDesignBoard', 'props': board}},
        {'frames': n2, 'footage': p2, 'label': DISCLOSE.format(take='run-01')}]})
    BEATS['B04']['shot'].pop('remotion', None)
    BEATS['B04']['qc'] = disclosure_qc(boxes, 'Concept board then dark cave footage; the disclosure label is the stable text in the footage part.')
    prov['B04'] = BEATS['B04']['shot']['composite']

    # B05 — CHARACTER-SHEET excerpt beside the collision check image and the palette.
    sheet_lines = [excerpt('CHARACTER-SHEET.md', a, a, t).replace('**', '').lstrip('- ') for a, t in
                   ((9, '- **On-screen size'), (10, '- **Proportions'), (46, '- Shape: rectangle'))]
    coll = Image.open(GAME / 'design/character/collision.png').convert('RGB')
    cards.design_card('The design: a promise in the character sheet', 'Design document and check image · not gameplay',
                      'CHARACTER-SHEET.md', sheet_lines, coll,
                      'design/character/collision.png · every pose at 64 px with the collision rectangle',
                      [('Hair', '#E8E6F0'), ('Eyes, ribbon, crystal', '#D62839'), ('Hat, capelet', '#3A40A0'),
                       ('Trim, charm', '#D4A63A'), ('Tunic, boots', '#6B5A4E'), ('Skin', '#F5DCCD'), ('Outline', '#1A1420')],
                      [('Size', 'About 64 px tall with the hat; not chibi, 1:3.5'),
                       ('Collision', 'About 14×44 px, feet to chin')],
                      f'Exact excerpts: CHARACTER-SHEET.md lines 9, 10, 46 · palette table lines 51–58 · at {BUILD}').save(MEDIA / 'B05.png')
    BEATS['B05']['shot'] = {**BEATS['B05']['shot'], 'type': 'STILL', 'motion': 'hold'}
    BEATS['B05']['shot'].pop('remotion', None)
    (MEDIA / 'B05.mp4').unlink(missing_ok=True)
    prov['B05'] = {'card': 'media/B05.png'}

    # B06 — three verbatim prompt cards, switched where the narration reaches each one.
    prompts = prompt_texts()
    n = nframes('B06')
    cuts = [0, round(at('B06', 'Then a setup message') * FPS), round(at('B06', 'And then the idle pose') * FPS), n]
    parts = []
    for i, (name, uploaded) in enumerate((('CHAR-REF v1', 'Uploaded with it: nothing'),
                                          ('Setup message', 'Uploaded with it: CHAR-REF v2 + 9 pose sketches; no generation'),
                                          ('CHAR-IDLE v1', 'Sent in the same chat, after the setup message'))):
        png = WORK / f'B06-{i + 1}.png'
        cards.prompt(i + 1, name, prompts[name], uploaded, f'Verbatim from SOURCES.md → Image prompts → {name}').save(png)
        still_clip(png, cuts[i + 1] - cuts[i], WORK / f'B06-{i + 1}.mp4')
        parts.append(WORK / f'B06-{i + 1}.mp4')
    assert concat(parts, MEDIA / 'B06.mp4') == n
    prov['B06'] = {'cards': [f'media/_work/B06-{i}.png' for i in (1, 2, 3)], 'switch_frames': cuts}

    # B07 — the raw Gemini output, never presented as the game.
    raw = Image.open(GAME / 'design/character/generated/CHAR-IDLE-v1.jpg').convert('RGB')
    cards.image_card('What came back', 'RAW GEMINI OUTPUT — not in engine', raw, [
        ('File', 'design/character/generated/CHAR-IDLE-v1.jpg'),
        ('Size', f'{raw.width} × {raw.height} px JPG, on a green screen'),
        ('Made by', 'Gemini app · Gemini 3.8 Flash · prompt CHAR-IDLE v1'),
        ('Watermark', 'Carries Google’s invisible SynthID')],
        'Original download, shown whole and unedited', (2010, 480, 3648, 1900), 192).save(MEDIA / 'B07.png')
    prov['B07'] = {'card': 'media/B07.png', 'image': 'design/character/generated/CHAR-IDLE-v1.jpg'}

    # B08 — Python cleanup tool source view (not a Godot editor view).
    code = excerpt('tools/clean_sprites.py', 442, 459, '# Head size is measured as face width')
    cards.source_view('The edits, as code', 'Source view · Python cleanup tool, run outside Godot',
                      'tools/clean_sprites.py · lines 442–459', 442, code, {442, 443, 456, 457, 459},
                      f'Line 427 runs first: rgb, fg, stats = key_green(a, k) · tools/sprites.json: '
                      f'"idle_height_px": 64 · exact source at {BUILD}').save(MEDIA / 'B08.png')
    BEATS['B08']['shot'].update({'type': 'STILL', 'motion': 'hold'})
    BEATS['B08']['shot'].pop('remotion', None)
    BEATS['B08']['source_view'] = {'path': 'tools/clean_sprites.py', 'start_line': 442, 'end_line': 459}

    # B09 — the cleaned file (asset preview).
    idle = Image.open(GAME / 'assets/sprites/mage/mage_idle.png').convert('RGBA')
    cards.image_card('The cleaned file', 'Asset file preview — not gameplay', idle, [
        ('File', 'assets/sprites/mage/mage_idle.png'),
        ('Size', f'{idle.width} × {idle.height} px canvas · 64 px tall, feet to hat tip'),
        ('Palette', '14 colours used · 0 off-palette pixels · hard alpha'),
        ('Logged', f'assets/sprites/EDIT-LOG.md + edit-log.json · sha256 {sha256(GAME / "assets/sprites/mage/mage_idle.png")[:16]}…')],
        'Shown at 20× with nearest-neighbour scaling on a transparency checker', (192, 480, 1700, 1900), 1900,
        checker=True, scale_nearest=20).save(MEDIA / 'B09.png')
    prov['B09'] = {'card': 'media/B09.png', 'asset': 'assets/sprites/mage/mage_idle.png'}

    # B10 → B11
    workbench('B10', 'One image per state', 'features/player/player.gd', 17, 26, 'const TEXTURES', [
        ('Lines 130–133 · _set_state()', 'sprite.texture = TEXTURES[next]'),
        ('No AnimationPlayer', 'The project has no AnimationPlayer or AnimatedSprite2D node; the swap is the animation.')],
        [(0.0, 17, 'TEXTURES maps each State to one PNG'), ('When the state changes', 20, '_set_state() swaps sprite.texture')])
    n = nframes('B11')
    lab, boxes = label_png('B11', [(DISCLOSE.format(take='run-01'), 'tl', 'disclosure')])
    prov['B11'] = footage('run-01', 0.0, n / FPS, MEDIA / 'B11.mp4', [(lab, 0, 99)])
    BEATS['B11']['qc'] = disclosure_qc(boxes, 'Dark cave footage: the disclosure label is the stable text.')

    # B12 — palette revision 1 rule (Python source view).
    code = excerpt('tools/clean_sprites.py', 130, 151, '# Thick dark regions are fill')
    cards.source_view('Cause and effect: the rule', 'Source view · Python cleanup tool, run outside Godot',
                      'tools/clean_sprites.py · apply_mage_revision() · lines 130–151', 130, code,
                      {138, 139, 145, 146, 149, 150, 151},
                      f'Palette revision 1 (CHARACTER-SHEET.md Revision 3) · exact source at {BUILD}').save(MEDIA / 'B12.png')
    BEATS['B12']['shot'].update({'type': 'STILL', 'motion': 'hold'})
    BEATS['B12']['shot'].pop('remotion', None)
    BEATS['B12']['source_view'] = {'path': 'tools/clean_sprites.py', 'start_line': 130, 'end_line': 151}

    # B13 — before/after contact sheet, then the mage on the dark cave in engine.
    n = nframes('B13')
    n1 = round(at('B13', 'And in the game') * FPS) - 6
    ba = Image.open(GAME / 'design/checks/mage-palette-revision1-before-after.png').convert('RGB')
    png = WORK / 'B13-1.png'
    cards.image_card('Before and after, on the cave tone', 'Contact sheets — not gameplay', ba, [],
                     'design/checks/mage-palette-revision1-before-after.png · darks L* 7.4 → 20.7 / 25.9 / 39.6 · '
                     'cave L* p5 4.7, p50 8.7 (assets/sprites/EDIT-LOG.md)', (192, 480, 3648, 1900), 0).save(png)
    still_clip(png, n1, WORK / 'B13-1.mp4')
    lab, boxes = label_png('B13', [(DISCLOSE.format(take='run-01'), 'tl', 'disclosure')])
    p2 = footage('run-01', 0.0, (n - n1) / FPS, WORK / 'B13-2.mp4', [(lab, 0, 99)])
    assert concat([WORK / 'B13-1.mp4', WORK / 'B13-2.mp4'], MEDIA / 'B13.mp4') == n
    prov['B13'] = [{'card': 'media/_work/B13-1.png', 'frames': n1}, {**p2}]
    BEATS['B13']['qc'] = disclosure_qc(boxes, 'Contact sheet then dark cave footage; the disclosure label is the stable text in the footage part.')

    # B14 → B15
    workbench('B14', 'The cast', 'features/player/player.gd', 101, 112, 'func cast', [
        ('Tuning (tuning.gd line 13)', 'CAST_COOLDOWN := 0.35'),
        ('Lines 212–218 · _read_cast_pressed()', 'return Input.is_action_just_pressed("cast")')],
        [(0.0, 101, 'cast(aim) runs on a click'), ('turns her toward the cursor', 102, 'Face the cursor'),
         ('spawns one fireball', 106, 'One fireball at the staff tip'), ('cooldown', 110, '0.35 s cooldown'),
         ("Holding the button", 110, 'just_pressed: a held button does not repeat')], font=25)
    n = nframes('B15')
    t0 = 4.0
    rel = lambda t: t - t0
    base_lab, boxes = label_png('B15', [(DISCLOSE.format(take='run-01'), 'tl', 'disclosure')])
    ev = [('growl · 0.5 s', R1['growl'], R1['lunge']), ('lunge', R1['lunge'], R1['hurt']),
          ('hit · she takes 1 damage', R1['hurt'], R1['cast1']), ('cast', R1['cast1'], R1['cast2']),
          ('cast · second hit', R1['cast2'], R1['down']), ('wolf down', R1['down'], R1['gone']),
          ('gone', R1['gone'], R1['gone'] + 0.8)]
    overlays = [(base_lab, 0, 99)] + [(label_png(f'B15-{i}', [(t, 'tc2', 'event')])[0], rel(a), rel(b))
                                       for i, (t, a, b) in enumerate(ev)]
    prov['B15'] = footage('run-01', t0, t0 + n / FPS, MEDIA / 'B15.mp4', overlays)
    prov['B15']['event_labels'] = [{'text': t, 'take_from_s': round(a, 4), 'take_to_s': round(b, 4)} for t, a, b in ev]
    BEATS['B15']['qc'] = disclosure_qc(boxes, 'Dark cave footage; the disclosure label is the stable text.')

    # B16 → B17
    workbench('B16', 'Sound listens; it never decides', 'audio/audio_director.gd', 40, 50, 'func connect_game', [
        ('Signals in', 'cast_fired · hurt · failed · cleared · defeated'),
        ('Muted vs unmuted (test_sound_triggers.gd)', 'muted-route-identical: PASS (re-run 2026-10-07)')],
        [(0.0, 40, 'connect_game(): wire signals to sounds'), ('It just announces events', 41, 'cast_fired → SFX-CAST'),
         ('This one node listens', 43, 'failed → stop music, SFX-FAIL'), ('Mute everything', 50, 'defeated → SFX-WOLF-DOWN')], font=25)
    n = nframes('B17')
    a_n, b_n = 78, 72
    c_n = n - a_n - b_n
    segs = []
    for i, (take, t0, k, evl) in enumerate((
            ('run-01', 7.8, a_n, [('SFX-HURT', R1['hurt'], R1['cast1']), ('SFX-CAST ×2', R1['cast1'], R1['down']),
                                  ('SFX-WOLF-DOWN', R1['down'], R1['down'] + 0.9)]),
            ('run-02', 3.8, b_n, [('SFX-FAIL', R2_FAIL, R2_FAIL + 1.0)]),
            ('run-01', 16.5 - c_n / FPS, c_n, [('SFX-CLEAR', R1['clear'], R1['clear'] + 1.2)]))):
        base_lab, boxes = label_png(f'B17-{i}', [(DISCLOSE.format(take=take), 'tl', 'disclosure')])
        ov = [(base_lab, 0, 99)] + [(label_png(f'B17-{i}-{j}', [(t, 'tc2', 'event')])[0], a - t0, b - t0)
                                    for j, (t, a, b) in enumerate(evl)]
        out = WORK / f'B17-{i}.mp4'
        segs.append({**footage(take, t0, t0 + k / FPS, out, ov),
                     'event_labels': [{'text': t, 'take_from_s': round(a, 4)} for t, a, _ in evl]})
    assert concat([WORK / f'B17-{i}.mp4' for i in range(3)], MEDIA / 'B17.mp4') == n
    prov['B17'] = segs
    BEATS['B17']['qc'] = disclosure_qc(boxes, 'Dark cave footage; the disclosure label is the stable text.')

    # B18 — SLICE AUDIO: the takes' own sound, same intervals as the picture, no narration.
    pieces = [('run-01', 7.4, 15.6), ('run-02', 3.6, 6.2)]
    vparts, aparts, segs = [], [], []
    for i, (take, t0, t1) in enumerate(pieces):
        lab, boxes = label_png(f'B18-{i}', [(SLICE.format(take=take), 'tl', 'disclosure')])
        v = footage(take, t0, t1, WORK / f'B18-{i}.mp4', [(lab, 0, 99)])
        a = take_audio(take, t0, t1, WORK / f'B18-{i}.wav')
        assert a['start_sample'] == v['src_frame_start'] * SAMPLES_PER_SRC_FRAME
        segs.append({'video': v, 'audio': a})
        vparts.append(WORK / f'B18-{i}.mp4')
        aparts.append(WORK / f'B18-{i}.wav')
    n = concat(vparts, MEDIA / 'B18.mp4')
    AUDIO.mkdir(exist_ok=True)
    audio_concat(aparts, AUDIO / 'B18.wav')
    BEATS['B18'].update({'audio_file': 'audio/B18.wav', 'actual_duration_s': n / FPS,
                         'slice_audio': {'method': 'Movie Maker take audio (PCM 48 kHz) cut sample-exactly to the '
                                                   'same source interval as the picture; no narration, no added sound',
                                         'approval': 'verbal approval from the instructor the method is acceptable',
                                         'segments': segs}})
    BEATS['B18']['qc'] = disclosure_qc(boxes, 'Dark cave footage; the SLICE AUDIO label is the stable text.')
    prov['B18'] = segs

    # B19 → B20
    workbench('B19', 'Two buses, two keys', 'game/main.gd', 64, 69, '## M / N.', [
        ('session_input.gd lines 11–14', 'mute_music → toggle_mute("Music")\nmute_sfx → toggle_mute("SFX")'),
        ('controls.gd lines 9–10', '"mute_music": [KEY_M] · "mute_sfx": [KEY_N]')],
        [(0.0, 65, 'toggle_mute(bus_name)'), ('M is the music bus', 67, 'Flip the bus mute')])
    narr = REEL / 'mp3' / 'beat-B20.mp3'
    narr_s = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', narr]).stdout)
    n1 = render_frames(narr_s)
    live_end = 3.8
    live_n = round(live_end * FPS)
    hold = n1 - live_n
    assert hold >= 0
    base_lab, boxes = label_png('B20-0', [(DISCLOSE.format(take='run-03'), 'tl', 'disclosure')])
    held_lab, _ = label_png('B20-held', [('Held frame', 'tc2', 'event')])
    v1 = footage('run-03', 0.0, live_end, WORK / 'B20-0a.mp4', [(base_lab, 0, 99)])
    last = WORK / 'B20-last.png'
    run(['ffmpeg', '-y', '-v', 'error', '-i', WORK / 'B20-0a.mp4', '-vf', f"select='eq(n\\,{live_n - 1})'",
         '-frames:v', '1', last])
    frame = Image.open(last).convert('RGBA')
    frame.alpha_composite(Image.open(held_lab))
    frame.convert('RGB').save(WORK / 'B20-held.png')
    still_clip(WORK / 'B20-held.png', hold, WORK / 'B20-0b.mp4')
    concat([WORK / 'B20-0a.mp4', WORK / 'B20-0b.mp4'], WORK / 'B20-0.mp4')
    v1['held_frames'] = hold
    slot_end = 7.8
    lab2, boxes2 = label_png('B20-1', [(SLICE.format(take='run-03'), 'tl', 'disclosure')])
    v2 = footage('run-03', live_end, slot_end, WORK / 'B20-1.mp4', [(lab2, 0, 99)])
    a2 = take_audio('run-03', live_end, slot_end, WORK / 'B20-1.wav')
    n = concat([WORK / 'B20-0.mp4', WORK / 'B20-1.mp4'], MEDIA / 'B20.mp4')
    run(['ffmpeg', '-y', '-v', 'error', '-i', narr, '-i', WORK / 'B20-1.wav', '-filter_complex',
         f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={n1 / FPS:.6f},atrim=0:{n1 / FPS:.6f}[n];'
         f'[1:a]aformat=channel_layouts=stereo[s];[n][s]concat=n=2:v=0:a=1[a]',
         '-map', '[a]', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', AUDIO / 'B20.wav'])
    BEATS['B20'].update({'narration_audio': 'mp3/beat-B20.mp3', 'audio_file': 'audio/B20.wav',
                         'actual_duration_s': n / FPS,
                         'slice_audio': {'method': 'narration over the first part (footage silent, final frame held '
                                                   f'{hold} frames, labelled); then the take audio cut sample-exactly to '
                                                   'the slot interval, no narration',
                                         'approval': 'verbal approval from the instructor the method is acceptable',
                                         'narration_frames': n1, 'slot': {'video': v2, 'audio': a2}}})
    both = [[max(p, q) for p, q in zip(boxes[0][:2], boxes2[0][:2])] + [min(p, q) for p, q in zip(boxes[0][2:], boxes2[0][2:])]]
    BEATS['B20']['qc'] = disclosure_qc(both, 'Dark cave footage; the region is the area both disclosure labels cover.')
    prov['B20'] = {'narrated': v1, 'slot': {'video': v2, 'audio': a2}}

    # B21 → B22
    workbench('B21', 'The check the assignment asks for', 'tests/test_sound_triggers.gd', 118, 123, '# 1. Full scripted route', [
        ('one_per_event() · lines 103–113', 'ok = sounds[id] == events[ev] and sounds[id] == want'),
        ('Runs', 'headless, dummy audio driver: counts play requests')],
        [(0.0, 119, 'One full scripted route, sound on'), ('counts sound requests per event', 121, 'Per sound ID: plays = events = expected')])
    log = (REEL / 'evidence' / 'test_sound_triggers-74c0443.log').read_text(encoding='utf-8').splitlines()
    shown, keep = [], {'route-one-sound-per-event', 'cast-held-2s-plays-once', 'wolf-down-two-fireballs-same-frame'}
    hi = set()
    for line in log:
        if line.startswith('{"id"'):
            rid = json.loads(line)['id']
            if rid in keep:
                hi.add(len(shown))
                shown.append(line)
            else:
                shown.append(f'{{"id":"{rid}", … ,"status":"{json.loads(line)["status"]}"}}')
        elif line.startswith(('SOUND TRIGGERS', 'WALKER TESTS')):
            shown.append(line)
    cards.terminal('Its real output', f'Recorded command output · re-run 2026-10-07 on a fresh copy of {BUILD}',
                   'Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_sound_triggers.gd',
                   shown, hi, 'Limit: headless runs use a dummy audio driver. This proves the triggers, not what you '
                              'hear; that was playtest 5, a person listening.',
                   'Exact output lines; “…” marks fields left out of the eight other results. Full log: evidence/test_sound_triggers-74c0443.log').save(MEDIA / 'B22.png')
    prov['B22'] = {'card': 'media/B22.png', 'log': 'evidence/test_sound_triggers-74c0443.log'}

    # B23 — models, contributions, credits.
    cards.columns('Who made what', None, [
        ('Which model made which asset', [
            ('Gemini app · Gemini 3.8 Flash', 'Every image: mage poses, wolf, fireball and burst, cave background, ground tiles'),
            ('Lyria · Gemini app', 'The music loop, MUS-LOOP'),
            ('Stable Audio Open 1.0 · local, ComfyUI', 'The five effects: cast, hurt, wolf down, fail, clear'),
            ('Drawn in code', 'The exit, the hearts, the crosshair, the dark pit fill')]),
        ('Human and AI contributions', [
            ('The author', 'The design, every accept and reject, the scope, the six playtests'),
            ('Claude', 'Drafted prompts and documents, wrote the code and tools, ran the checks, built this film'),
            ('Narration', 'Kokoro-82M, voice am_onyx, run locally')]),
        ('Credits', [
            ('Sound effects', 'Powered by Stability AI'),
            ('', 'This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI Ltd. All Rights Reserved.'),
            ('Gemini images and Lyria music', 'Carry Google’s invisible SynthID watermark')])],
        'From SOURCES.md and README.md at the branch head · coursework, non-commercial').save(MEDIA / 'B23.png')
    prov['B23'] = {'card': 'media/B23.png'}

    return prov


def prompt_texts():
    """The three B06 prompts, verbatim from SOURCES.md → Image prompts."""
    text = (GAME / 'SOURCES.md').read_text(encoding='utf-8')
    out = {}
    for name, head in (('CHAR-REF v1', '#### CHAR-REF v1\n'),
                       ('Setup message', '#### Setup message (CHAR-REF v2 + 9 pose sketches uploaded, no generation)\n'),
                       ('CHAR-IDLE v1', '#### CHAR-IDLE v1\n')):
        body = text.split(head, 1)[1]
        assert body.startswith('```\n')
        out[name] = body[4:body.index('\n```')]
    return out


def main():
    global BEATS
    MEDIA.mkdir(exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    (REEL / 'evidence').mkdir(exist_ok=True)
    sheet = load_json(REEL / 'beat_sheet.json')
    BEATS = {b['beat_id']: b for b in sheet['beats']}
    prov = build()
    for bid in ('B11', 'B15', 'B17', 'B20'):
        BEATS[bid]['shot']['evidence_media'] = f'media/{bid}.mp4'
    BEATS['B22']['shot']['evidence_media'] = 'media/B22.png'
    save_json(REEL / 'beat_sheet.json', sheet)
    save_json(REEL / 'evidence' / 'media-provenance.json', {
        'note': 'How each non-Remotion slot was made. Times are take seconds; frames are 60 fps source frames.',
        'take_events_s': {'run-01': R1, 'run-02': {'fail': R2_FAIL}}, 'beats': prov})
    print('media built:', ', '.join(sorted(prov)))


if __name__ == '__main__':
    main()
