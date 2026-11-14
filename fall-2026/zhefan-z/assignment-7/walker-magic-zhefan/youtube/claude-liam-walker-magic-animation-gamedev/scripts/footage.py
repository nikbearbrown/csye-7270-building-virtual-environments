"""Phase 2a: the five gameplay beats (B03-B07) from capture/run-02, frame-exact.

Adapted from the Assignment 6 film's footage.py. Source: the PNG frames Movie Maker wrote for capture/run-02
(WALKER_CAPTURE), the real 640x360 viewport of the game's main scene at ad7935f played by capture/driver.gd
(scripted input). The capture runs at 60 fps, one rendered frame per physics tick; the film runs at 30 fps. Each beat
is built to exactly the number of frames its measured narration gives it, so the compiler neither retimes nor cuts it:
  1. the action at real speed: every second captured frame, in order (60 -> 30 fps; never trimmed to fit);
  2. a labelled replay at x0.25: every captured frame of a part of that action, each shown twice;
  3. the last frame held, labelled, for whatever narration remains.
The game canvas is enlarged x5 with nearest-neighbour scaling (3200x1800) under a header naming the source. A chip in
the ground band under the action reads the state the frame shows from capture/run-02-frames.jsonl (film annotation,
not drawn by the game). In the three interrupt beats a second chip, from the hit frame on, gives the hit as the
driver logged it (capture/run-02-inputs.jsonl, "wolf_hit"): the state the wolf ended the previous tick in (the phase
that counts, because a hit is resolved before the wolf's own update), the state and clip frame on the hit tick, HP.
"""
import json
import subprocess

from PIL import Image, ImageDraw

import cards
from common import (REEL, CAPTURE, CAPTURE_FRAMES, CAPTURE_FRAMES_TOTAL, FPS, W, H, PAGE, INK, INK_SOFT, SPARK,
                    load_json, save_json, render_frames, sha256, capture_rows)

GAME_X, GAME_Y, K = 320, 250, 5
LABEL = 'Scripted input · real engine output'

# beat: (real-speed frames inclusive, replay frames inclusive, replay caption, chip kind, segment with a wolf hit)
PLAN = {
    'B03': ((15, 439), (292, 372), 'the jump and the landing', 'mage', None),
    'B04': ((860, 1088), (876, 1030), 'both lunges', 'wolf', None),
    'B05': ((1380, 1619), (1518, 1600), 'the cast and the cancel', 'hit', 'cancel'),
    'B06': ((1930, 2148), (2058, 2148), 'the cast, the hit in LUNGE, the full dash', 'hit', 'lunge_hit'),
    'B07': ((2500, 2706), (2616, 2706), 'the cast, the hit in RECOVER', 'hit', 'recover_hit'),
}


def frame_path(n):
    return CAPTURE_FRAMES / f'frame{n:08d}.png'


def header(heading, a, b):
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    d.text((GAME_X, 100), heading, font=cards.F('serif', 76), fill=INK)
    note = (f'capture/{CAPTURE} · frames {a}–{b} of {CAPTURE_FRAMES_TOTAL} · 60 fps, one frame per physics tick · '
            '640×360 game canvas, enlarged ×5, nearest neighbour')
    f = cards.F('sans', 40)
    tw = d.textlength(LABEL, font=f)
    x = W - GAME_X - tw - 64
    d.rounded_rectangle([x, 104, W - GAME_X, 174], radius=35, fill=INK)
    d.text((x + 32, 116), LABEL, font=f, fill=PAGE)
    d.text((GAME_X, 198), note, font=cards.F('sans', 38), fill=INK_SOFT)
    return im


def chip(text, accent, size=48):
    f = cards.F('sans_med', size)
    probe = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    tw = int(probe.textlength(text, font=f))
    h = int(size * 1.9)
    im = Image.new('RGBA', (tw + 72, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, tw + 71, h - 1], radius=h // 2, fill=SPARK if accent else (61, 57, 41, 235))
    d.text((36, int(size * 0.33)), text, font=f, fill=PAGE)
    return im


def state_ticks(rows):
    """Ticks since the wolf's (and the mage's) current state began, per frame, within a segment."""
    out = {}
    last = {}
    for r in rows:
        for who, key in (('w', 'ws'), ('p', 'ps')):
            s = r.get(key)
            k = (r['seg'], s)
            if s is None:
                continue
            if last.get(who, (None, None))[0] != k:
                last[who] = (k, r['f'])
            out[(who, r['f'])] = r['f'] - last[who][1]
    return out


def state_text(row, kind, ticks):
    if kind == 'mage':
        return (f"frame log · mage {row['ps']} · {row['pclip']} clip, sheet cell {row['pfr']} · "
                f"tick {ticks[('p', row['f'])]} of the state · frame {row['f']}")
    armed = 'armed' if row.get('mon') else 'off'
    tail = f"ghosts {row.get('ghosts', 0)}" if kind == 'wolf' else f"wolf HP {row.get('whp', '–')}"
    return (f"frame log · wolf {row['ws']}, tick {ticks[('w', row['f'])]} of the state · {row['wclip']} clip frame "
            f"{row['wcf']} · hitbox {armed} · {tail} · frame {row['f']}")


def wolf_hits():
    out = {}
    for line in (REEL / 'capture' / f'{CAPTURE}-inputs.jsonl').read_text(encoding='utf-8').splitlines():
        r = json.loads(line)
        if r.get('kind') == 'wolf_hit':
            out[r['segment']] = r
    return out


def hit_text(h):
    return (f"hit on frame {h['frame']} ({h['since_growl']} ticks after the growl began): phase that counts "
            f"{h['prev_state']} (the tick before) → {h['state']} on the hit tick, clip frame {h['clip_frame']}, "
            f"HP {h['hp_before']} → {h['hp_after']}")


def build(bid, heading, total, rows, ticks, hits):
    (a, b), (ra, rb), what, kind, seg = PLAN[bid]
    real = list(range(a, b + 1, 2))
    assert len(real) <= total, f'{bid}: the real-speed action ({len(real)} frames) is longer than the beat ({total})'
    room = (total - len(real)) // 2
    replay = list(range(ra, rb + 1))[:room]
    assert replay and replay[-1] == rb, f'{bid}: the replay does not fit ({room} of {rb - ra + 1} frames)'
    for n in range(a, b + 1):
        assert rows[n]['seg'] != '' and 'ws' in rows[n] and rows[n]['ws'] != 'FREED', f'{bid}: frame {n} is empty'
    seq = [(n, 'real') for n in real] + [(n, 'replay') for n in replay for _ in range(2)]
    hold_from = len(seq)
    seq += [(seq[-1][0], 'hold')] * (total - len(seq))
    base = header(heading, a, b)
    chips = {'real': chip('Real speed (every second frame)', False),
             'replay': chip(f'Replay, ×0.25 — {what} (frames {replay[0]}–{replay[-1]})', True),
             'hold': chip('Last frame held', False)}
    h = hits.get(seg) if seg else None
    if seg:
        assert h and h['segment'] == seg and a <= h['frame'] <= b, f'{bid}: no logged hit in {a}-{b}'
        assert rows[h['frame'] - 1]['ws'] == h['prev_state'] and rows[h['frame']]['ws'] == h['state'], f'{bid}: hit row'
        assert rows[h['frame']]['wcf'] == h['clip_frame'] and rows[h['frame']]['whp'] == h['hp_after'], f'{bid}: hit row'
        hchip = chip(hit_text(h), True, size=40)
    out = REEL / 'media' / f'{bid}.mp4'
    out.parent.mkdir(exist_ok=True)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-frames:v', str(total), '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '10', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    cache = {}
    for n, phase in seq:
        key = (n, phase)
        if key not in cache:
            cache.clear()
            im = base.copy()
            game = Image.open(frame_path(n)).convert('RGB')
            assert game.size == (640, 360), f'{frame_path(n)} is {game.size}'
            lo, hi = game.convert('L').getextrema()
            assert hi - lo > 8, f'{bid}: frame {n} is empty (the scene was freed between segments)'
            im.paste(game.resize((640 * K, 360 * K), Image.NEAREST), (GAME_X, GAME_Y))
            c = chips[phase]
            im.paste(c, (GAME_X + 640 * K - c.width - 40, GAME_Y + 40), c)
            s = chip(state_text(rows[n], kind, ticks), False, size=40)
            sy = GAME_Y + 360 * K - s.height - 40
            im.paste(s, (GAME_X + 40, sy), s)
            if h and n >= h['frame']:
                im.paste(hchip, (GAME_X + 40, sy - hchip.height - 20), hchip)
            cache[key] = im.tobytes()
        enc.stdin.write(cache[key])
    enc.stdin.close()
    assert enc.wait() == 0, f'{bid}: ffmpeg failed'
    p = {'source': f'capture/{CAPTURE}.mp4 (frames from WALKER_CAPTURE)',
         'source_sha256': sha256(REEL / 'capture' / f'{CAPTURE}.mp4'),
         'input_log': f'capture/{CAPTURE}-inputs.jsonl', 'frame_log': f'capture/{CAPTURE}-frames.jsonl',
         'real_speed_frames': [a, b], 'real_speed_method': 'every second captured frame (60 fps capture, 30 fps film)',
         'replay_x0_25_frames': [replay[0], replay[-1]], 'replay_method': 'every captured frame shown twice',
         'hold_starts_at_frame_of_beat': hold_from, 'beat_frames': total, 'scale': 'x5 nearest neighbour',
         'state_chip': f'read from capture/{CAPTURE}-frames.jsonl, drawn by the film outside the game image',
         'media': f'media/{bid}.mp4', 'media_sha256': sha256(out)}
    if h:
        p['wolf_hit'] = {k: h[k] for k in ('frame', 'segment', 'prev_state', 'state', 'clip_frame', 'since_growl',
                                           'hp_before', 'hp_after', 'monitoring')}
    return p


def main():
    assert CAPTURE_FRAMES and frame_path(0).is_file(), f'set WALKER_CAPTURE to the Movie Maker frames of capture/{CAPTURE}'
    rows = capture_rows()
    assert len(rows) == CAPTURE_FRAMES_TOTAL
    ticks = state_ticks(rows)
    hits = wolf_hits()
    sheet = load_json(REEL / 'beat_sheet.json')
    beats = {b['beat_id']: b for b in sheet['beats']}
    prov = {}
    for bid in PLAN:
        total = render_frames(beats[bid]['actual_duration_s'])
        prov[bid] = build(bid, beats[bid]['heading'], total, rows, ticks, hits)
        print(bid, prov[bid]['beat_frames'], 'frames; hold from', prov[bid]['hold_starts_at_frame_of_beat'])
    save_json(REEL / 'evidence' / 'footage-provenance.json', {
        'note': f'Gameplay beats built by scripts/footage.py from capture/{CAPTURE} (scripted input, real engine output, '
                '60 fps). Real-speed interval first (every second frame), then a labelled x0.25 replay (every frame '
                'twice), then a labelled hold.', 'beats': prov})


if __name__ == '__main__':
    main()
