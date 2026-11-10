"""Phase 2a: the three gameplay beats (B04, B13, B19) from capture/run-01, frame-exact.

Source: the PNG frames Movie Maker wrote for capture/run-01 (WALKER_CAPTURE), the real 640x360 viewport of the
game's main scene at 3c37fe0 played by capture/driver.gd (scripted input). Each beat is built to exactly the
number of frames its measured narration gives it, so the compiler neither retimes nor cuts it:
  1. the action at real speed: every captured frame once, in order (never trimmed to fit);
  2. a labelled replay at x0.25 (each frame shown four times) of a part of that action, shortened if needed;
  3. the last frame held, labelled, for whatever narration remains.
The game canvas is enlarged x5 with nearest-neighbour scaling (3200x1800) under a header naming the source.
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import cards
from common import REEL, CAPTURE_FRAMES, FPS, W, H, PAGE, INK, INK_SOFT, SPARK, load_json, render_frames, sha256

GAME_X, GAME_Y, K = 320, 250, 5
LABEL = 'Scripted input · real engine output'

# beat: (real-speed frames inclusive, replay frames inclusive, replay caption)
PLAN = {
    'B04': ((6, 70), (10, 70), 'the same second'),
    'B13': ((72, 527), (302, 340), 'the two hits on the wolf'),
    'B19': ((531, 907), (700, 745), 'the shot to the left'),
}


def frame_path(n):
    return CAPTURE_FRAMES / f'frame{n:08d}.png'


def header(heading, a, b):
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    d.text((GAME_X, 100), heading, font=cards.F('serif', 76), fill=INK)
    note = f'capture/run-01 · frames {a}–{b} of 909 · 640×360 game canvas, enlarged ×5, nearest neighbour'
    f = cards.F('sans', 40)
    tw = d.textlength(LABEL, font=f)
    x = W - GAME_X - tw - 64
    d.rounded_rectangle([x, 104, W - GAME_X, 174], radius=35, fill=INK)
    d.text((x + 32, 116), LABEL, font=f, fill=PAGE)
    d.text((GAME_X, 198), note, font=cards.F('sans', 42), fill=INK_SOFT)
    return im


def chip(text, accent):
    f = cards.F('sans_med', 48)
    probe = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    tw = int(probe.textlength(text, font=f))
    im = Image.new('RGBA', (tw + 72, 92), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, tw + 71, 91], radius=46, fill=SPARK if accent else (61, 57, 41, 235))
    d.text((36, 16), text, font=f, fill=PAGE)
    return im


def build(bid, heading, total):
    (a, b), (ra, rb), what = PLAN[bid]
    real = list(range(a, b + 1))
    assert len(real) <= total, f'{bid}: the real-speed action ({len(real)} frames) is longer than the beat ({total})'
    room = (total - len(real)) // 4
    replay = list(range(ra, rb + 1))[:room]
    seq = [(n, 'real') for n in real] + [(n, 'replay') for n in replay for _ in range(4)]
    hold_from = len(seq)
    seq += [(seq[-1][0], 'hold')] * (total - len(seq))
    base = header(heading, a, b)
    chips = {'real': chip('Real speed, 30 fps', False),
             'replay': chip(f'Replay, ×0.25 — {what} (frames {replay[0]}–{replay[-1]})' if replay else '', True),
             'hold': chip('Last frame held', False)}
    out = REEL / 'media' / f'{bid}.mp4'
    out.parent.mkdir(exist_ok=True)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-frames:v', str(total), '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '10', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    cache = {}
    for i, (n, phase) in enumerate(seq):
        key = (n, phase)
        if key not in cache:
            cache.clear()
            im = base.copy()
            game = Image.open(frame_path(n)).convert('RGB')
            assert game.size == (640, 360), f'{frame_path(n)} is {game.size}'
            im.paste(game.resize((640 * K, 360 * K), Image.NEAREST), (GAME_X, GAME_Y))
            c = chips[phase]
            im.paste(c, (GAME_X + 640 * K - c.width - 40, GAME_Y + 40), c)
            cache[key] = im.tobytes()
        enc.stdin.write(cache[key])
    enc.stdin.close()
    assert enc.wait() == 0, f'{bid}: ffmpeg failed'
    return {'source': 'capture/run-01.mp4 (frames from WALKER_CAPTURE)', 'source_sha256': sha256(REEL / 'capture' / 'run-01.mp4'),
            'input_log': 'capture/run-01-inputs.jsonl', 'real_speed_frames': [a, b], 'replay_x0_25_frames': [replay[0], replay[-1]] if replay else [],
            'hold_starts_at_frame_of_beat': hold_from, 'beat_frames': total, 'scale': 'x5 nearest neighbour',
            'media': f'media/{bid}.mp4', 'media_sha256': sha256(out)}


def main():
    assert CAPTURE_FRAMES and frame_path(0).is_file(), 'set WALKER_CAPTURE to the Movie Maker frames of capture/run-01'
    sheet = load_json(REEL / 'beat_sheet.json')
    beats = {b['beat_id']: b for b in sheet['beats']}
    prov = {}
    for bid in PLAN:
        total = render_frames(beats[bid]['actual_duration_s'])
        prov[bid] = build(bid, beats[bid]['heading'], total)
        print(bid, prov[bid]['beat_frames'], 'frames; hold from', prov[bid]['hold_starts_at_frame_of_beat'])
    path = REEL / 'evidence' / 'footage-provenance.json'
    from common import save_json
    save_json(path, {'note': 'Gameplay beats built by scripts/footage.py from capture/run-01 (scripted input, real engine '
                             'output). Real-speed interval first, then a labelled x0.25 replay, then a labelled hold.',
                     'beats': prov})


if __name__ == '__main__':
    main()
