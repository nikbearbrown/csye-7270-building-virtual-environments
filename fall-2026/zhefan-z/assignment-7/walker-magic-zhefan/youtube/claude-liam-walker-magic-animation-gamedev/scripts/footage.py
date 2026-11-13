"""Phase 2a: the three gameplay beats (B03, B04, B05) from capture/run-01, frame-exact.

Adapted from the Assignment 6 film's footage.py. Source: the PNG frames Movie Maker wrote for capture/run-01
(WALKER_CAPTURE), the real 640x360 viewport of the game's main scene at f860fed played by capture/driver.gd
(scripted input). The capture runs at 60 fps, one rendered frame per physics tick; the film runs at 30 fps. Each beat
is built to exactly the number of frames its measured narration gives it, so the compiler neither retimes nor cuts it:
  1. the action at real speed: every second captured frame, in order (60 -> 30 fps; never trimmed to fit);
  2. a labelled replay at x0.25: every captured frame of a part of that action, each shown twice;
  3. the last frame held, labelled, for whatever narration remains.
The game canvas is enlarged x5 with nearest-neighbour scaling (3200x1800) under a header naming the source. A chip in
the ground band under the action reads the state the frame shows from capture/run-01-frames.jsonl (film annotation,
not drawn by the game).
"""
import subprocess

from PIL import Image, ImageDraw

import cards
from common import (REEL, CAPTURE_FRAMES, CAPTURE_FRAMES_TOTAL, FPS, W, H, PAGE, INK, INK_SOFT, SPARK, load_json,
                    save_json, render_frames, sha256, capture_rows)

GAME_X, GAME_Y, K = 320, 250, 5
LABEL = 'Scripted input · real engine output'

# beat: (real-speed frames inclusive, replay frames inclusive, replay caption, chip kind)
PLAN = {
    'B03': ((15, 439), (292, 372), 'the jump and the landing', 'mage'),
    'B04': ((850, 1088), (876, 1062), 'both lunges', 'wolf'),
    'B05': ((1380, 1619), (1518, 1600), 'the cast and the cancel', 'wolf'),
}


def frame_path(n):
    return CAPTURE_FRAMES / f'frame{n:08d}.png'


def header(heading, a, b):
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    d.text((GAME_X, 100), heading, font=cards.F('serif', 76), fill=INK)
    note = (f'capture/run-01 · frames {a}–{b} of {CAPTURE_FRAMES_TOTAL} · 60 fps, one frame per physics tick · '
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
    return (f"frame log · wolf {row['ws']}, tick {ticks[('w', row['f'])]} of the state · {row['wclip']} clip frame "
            f"{row['wcf']} · hitbox {armed} · ghosts {row.get('ghosts', 0)} · frame {row['f']}")


def build(bid, heading, total, rows, ticks):
    (a, b), (ra, rb), what, kind = PLAN[bid]
    real = list(range(a, b + 1, 2))
    assert len(real) <= total, f'{bid}: the real-speed action ({len(real)} frames) is longer than the beat ({total})'
    room = (total - len(real)) // 2
    replay = list(range(ra, rb + 1))[:room]
    assert replay and replay[-1] == rb, f'{bid}: the replay does not fit ({room} of {rb - ra + 1} frames)'
    seq = [(n, 'real') for n in real] + [(n, 'replay') for n in replay for _ in range(2)]
    hold_from = len(seq)
    seq += [(seq[-1][0], 'hold')] * (total - len(seq))
    base = header(heading, a, b)
    chips = {'real': chip('Real speed (every second frame)', False),
             'replay': chip(f'Replay, ×0.25 — {what} (frames {replay[0]}–{replay[-1]})', True),
             'hold': chip('Last frame held', False)}
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
            im.paste(game.resize((640 * K, 360 * K), Image.NEAREST), (GAME_X, GAME_Y))
            c = chips[phase]
            im.paste(c, (GAME_X + 640 * K - c.width - 40, GAME_Y + 40), c)
            s = chip(state_text(rows[n], kind, ticks), False, size=40)
            im.paste(s, (GAME_X + 40, GAME_Y + 360 * K - s.height - 40), s)
            cache[key] = im.tobytes()
        enc.stdin.write(cache[key])
    enc.stdin.close()
    assert enc.wait() == 0, f'{bid}: ffmpeg failed'
    return {'source': 'capture/run-01.mp4 (frames from WALKER_CAPTURE)', 'source_sha256': sha256(REEL / 'capture' / 'run-01.mp4'),
            'input_log': 'capture/run-01-inputs.jsonl', 'frame_log': 'capture/run-01-frames.jsonl',
            'real_speed_frames': [a, b], 'real_speed_method': 'every second captured frame (60 fps capture, 30 fps film)',
            'replay_x0_25_frames': [replay[0], replay[-1]], 'replay_method': 'every captured frame shown twice',
            'hold_starts_at_frame_of_beat': hold_from, 'beat_frames': total, 'scale': 'x5 nearest neighbour',
            'state_chip': 'read from capture/run-01-frames.jsonl, drawn by the film outside the game image',
            'media': f'media/{bid}.mp4', 'media_sha256': sha256(out)}


def main():
    assert CAPTURE_FRAMES and frame_path(0).is_file(), 'set WALKER_CAPTURE to the Movie Maker frames of capture/run-01'
    rows = capture_rows()
    ticks = state_ticks(rows)
    sheet = load_json(REEL / 'beat_sheet.json')
    beats = {b['beat_id']: b for b in sheet['beats']}
    prov = {}
    for bid in PLAN:
        total = render_frames(beats[bid]['actual_duration_s'])
        prov[bid] = build(bid, beats[bid]['heading'], total, rows, ticks)
        print(bid, prov[bid]['beat_frames'], 'frames; hold from', prov[bid]['hold_starts_at_frame_of_beat'])
    save_json(REEL / 'evidence' / 'footage-provenance.json', {
        'note': 'Gameplay beats built by scripts/footage.py from capture/run-01 (scripted input, real engine output, '
                '60 fps). Real-speed interval first (every second frame), then a labelled x0.25 replay (every frame '
                'twice), then a labelled hold.', 'beats': prov})


if __name__ == '__main__':
    main()
