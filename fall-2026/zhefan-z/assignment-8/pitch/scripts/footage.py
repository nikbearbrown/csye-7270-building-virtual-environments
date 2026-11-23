"""Phase 2b: the five gameplay beats as media/Bxx.mp4, frame-exact, from real captured play.

Written by Claude Code for the Assignment 8 pitch film; the method is the Assignment 7 film's footage.py (840b501):
  1. the action at real speed (60 fps captures: every second captured frame; the 30 fps Assignment 6 capture: every
     frame), never trimmed or retimed to fit;
  2. where named, a replay at x0.25 of part of it, labelled as a slowed replay of the same capture;
  3. the last frame held, labelled, for whatever narration remains.
Each beat is built to exactly the frame count of its measured (padded) narration, so the compiler neither retimes nor
cuts it. The game's 640x360 canvas is enlarged x5 with nearest-neighbour scaling (3200x1800) under a header that names
the capture, its revision and the frames shown. Chips under the action are read from the capture's frame log and
drawn by the film outside the game image; the game frames themselves are untouched.

Sources:
  B00, B08, B15  capture/run-01 (840b501, this film's capture; frames from CAP_840B501)
  B13            capture/a5-run-01 (2b68e0a, this film's capture of the Assignment 5 game; frames from CAP_2B68E0A)
  B14            the Assignment 6 film's capture run-01.mp4 (3c37fe0), reused unchanged: A6_RUN01, SHA-256 checked
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

import cards
from common import (REEL, FPS, W, H, PAGE, INK, INK_SOFT, REV_A7, REV_A5, REV_A6_CAP, A6_RUN01, A6_RUN01_SHA, CAP_840,
                    CAP_2B6, L_REPLAY, L_HOLD, load_json, save_json, render_frames, sha256, frame_rows, input_rows, run)

GX, GY, K = 320, 250, 5          # the game canvas ends at y 2050, inside the title-safe bottom (2052)

SRC = {
    'c840': {'rev': REV_A7, 'fps': 60, 'name': 'capture/run-01', 'log': 'run-01',
             'label': f'Real capture · scripted input · revision {REV_A7}'},
    'c2b6': {'rev': REV_A5, 'fps': 60, 'name': 'capture/a5-run-01', 'log': 'a5-run-01',
             'label': f'Real capture · scripted input · revision {REV_A5} (Assignment 5)'},
    'a6': {'rev': REV_A6_CAP, 'fps': 30, 'name': "the Assignment 6 film's capture/run-01", 'log': None,
           'label': f'Real capture · scripted input · revision {REV_A6_CAP} (Assignment 6)'},
}

# beat: (source, [(first, last, mode, caption)], hit-chip segment or None)
#   mode 'real' = real speed, 'replay' = x0.25 (each 60 fps frame twice)
PLAN = {
    'B00': ('c840', [(1380, 1619, 'real', 'Real speed: the cancel segment'),
                     (1520, 1590, 'replay', 'the cast, the hit during the growl')], 'cancel'),
    'B08': ('c840', [(860, 1088, 'real', 'Real speed: the lunge (it lands at frame 1009)'),
                     (1400, 1619, 'real', 'Real speed: the cancel'),
                     (1524, 1560, 'replay', 'the hit during the growl')], 'cancel'),
    'B13': ('c2b6', [(420, 560, 'real', 'Real speed: the lunge lands, the hurt tint fades'),
                     (470, 520, 'replay', 'the hurt tint')], None),
    'B14': ('a6', [(230, 524, 'real', 'Real speed: impacts on the wolf, the ground, rapid fire')], None),
    'B15': ('c840', [(140, 439, 'real', 'Real speed: run, stop, run, jump the pit, land')], None),
}


def a6_frames(tmp):
    assert A6_RUN01 and A6_RUN01.is_file(), 'set A6_RUN01 to the Assignment 6 capture archive'
    assert sha256(A6_RUN01) == A6_RUN01_SHA, 'A6_RUN01 is not the recorded Assignment 6 capture'
    run(['ffmpeg', '-v', 'error', '-i', A6_RUN01, '-start_number', '0', Path(tmp) / 'frame%08d.png'])
    return Path(tmp)


def header(heading, src, spans):
    """Heading, label and source line, all inside the title-safe inset (x 192-3648, y 108-2052 at 4K)."""
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    d.text((GX, 102), heading, font=cards.F('serif', 70), fill=INK)
    c = cards.chip(SRC[src]['label'], 'real', 42)
    im.paste(c, (GX + 640 * K - c.width, 110), c)
    frames = ', '.join(f'{a}–{b}' for a, b, _, _ in spans)
    d.text((GX, 196), f"{SRC[src]['name']} · frames {frames} · {SRC[src]['fps']} fps · 640×360 game canvas, "
           'enlarged ×5, nearest neighbour', font=cards.F('sans', 32), fill=INK_SOFT)
    return im


def state_text(src, r):
    if src == 'c840':
        return f"frame log · mage {r.get('ps', '–')} · wolf {r.get('ws', '–')} · wolf HP {r.get('whp', '–')} · frame {r['f']}"
    if src == 'c2b6':
        return (f"frame log · mage {r.get('ps', '–')} · HP {r.get('php', '–')} · hurt-tint intensity "
                f"{r.get('tint', 0):.2f} (read from the shader) · frame {r['f']}")
    return None


def build(bid, heading, total, frames_dir, rows, hit):
    src, spans, hitseg = PLAN[bid]
    step = 2 if SRC[src]['fps'] == 60 else 1
    seq = []
    for a, b, mode, cap in spans:
        if mode == 'real':
            seq += [(n, 'real', cap) for n in range(a, b + 1, step)]
        else:
            seq += [(n, 'replay', cap) for n in range(a, b + 1) for _ in range(2)]
    assert len(seq) <= total, f'{bid}: action ({len(seq)} frames) is longer than the beat ({total})'
    hold_from = len(seq)
    seq += [(seq[-1][0], 'hold', '')] * (total - len(seq))
    base = header(heading, src, spans)
    out = REEL / 'media' / f'{bid}.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-frames:v', str(total), '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '12', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    last_key, last = None, None
    for n, phase, cap in seq:
        key = (n, phase, cap)
        if key != last_key:
            im = base.copy()
            game = Image.open(frames_dir / f'frame{n:08d}.png').convert('RGB')
            assert game.size == (640, 360), f'{bid}: frame {n} is {game.size}'
            lo, hi = game.convert('L').getextrema()
            assert hi - lo > 8, f'{bid}: frame {n} is flat (a gap between segments)'
            im.paste(game.resize((640 * K, 360 * K), Image.NEAREST), (GX, GY))
            text = {'real': cap, 'replay': f'{L_REPLAY} — {cap}', 'hold': L_HOLD}[phase]
            c = cards.chip(text, 'constructed' if phase == 'replay' else 'real', 44)
            im.paste(c, (GX + 640 * K - c.width - 40, GY + 40), c)
            if rows is not None:
                r = rows[n]
                assert r['seg'] and r.get('ws') != 'FREED', f'{bid}: frame {n} is between segments'
                s = cards.chip(state_text(src, r), 'figure', 40)
                sy = GY + 360 * K - s.height - 40
                im.paste(s, (GX + 40, sy), s)
                if hit and n >= hit['frame'] and rows[n]['seg'] == hit['segment']:
                    t = (f"hit on frame {hit['frame']}: wolf in {hit['prev_state']} → {hit['state']}, "
                         f"no lunge · wolf HP {hit['hp_before']} → {hit['hp_after']}  (input log)")
                    h = cards.chip(t, 'constructed', 40)
                    im.paste(h, (GX + 40, sy - h.height - 20), h)
            last, last_key = im.tobytes(), key
        enc.stdin.write(last)
    enc.stdin.close()
    assert enc.wait() == 0, f'{bid}: ffmpeg failed'
    return {'source': SRC[src]['name'], 'revision': SRC[src]['rev'], 'label': SRC[src]['label'],
            'spans': [{'frames': [a, b], 'mode': m, 'caption': c} for a, b, m, c in spans],
            'real_speed_method': 'every second captured frame' if step == 2 else 'every captured frame',
            'replay_method': 'every captured frame shown twice (x0.25 of a 60 fps capture at 30 fps)',
            'hold_starts_at_frame_of_beat': hold_from, 'beat_frames': total, 'media': f'media/{bid}.mp4',
            'media_sha256': sha256(out)}


def main():
    sheet = load_json(REEL / 'beat_sheet.json')
    beats = {b['beat_id']: b for b in sheet['beats']}
    assert CAP_840 and CAP_2B6, 'set CAP_840B501 and CAP_2B68E0A'
    logs = {'c840': frame_rows('run-01'), 'c2b6': frame_rows('a5-run-01'), 'a6': None}
    hits = {r['segment']: r for r in input_rows('run-01') if r.get('kind') == 'wolf_hit'}
    prov = {}
    with tempfile.TemporaryDirectory() as tmp:
        dirs = {'c840': CAP_840, 'c2b6': CAP_2B6, 'a6': a6_frames(tmp)}
        for bid, (src, spans, hitseg) in PLAN.items():
            total = render_frames(beats[bid]['actual_duration_s'])
            prov[bid] = build(bid, beats[bid]['heading'], total, dirs[src], logs[src], hits.get(hitseg))
            print(bid, total, 'frames; hold from', prov[bid]['hold_starts_at_frame_of_beat'])
    prov['_a6_capture'] = {'path': 'A6_RUN01 (fall-2026/zhefan-z/assignment-6/walker-magic-zhefan/youtube/'
                                   'claude-liam-walker-magic-particles-gamedev/capture/run-01.mp4, kept out of git)',
                           'sha256': A6_RUN01_SHA, 'revision': REV_A6_CAP,
                           'record': 'CAPTURE.md of the Assignment 6 film at 7672d5a'}
    save_json(REEL / 'evidence' / 'footage-provenance.json', prov)


if __name__ == '__main__':
    main()
