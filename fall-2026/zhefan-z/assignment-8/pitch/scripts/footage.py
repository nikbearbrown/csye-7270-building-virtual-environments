"""Phase 2b: the gameplay beats as media/<beat>.mp4, frame-exact, from real captured play.

Written by Claude Code for the Assignment 8 pitch film; rebuilt 2026-11-22 for the GDD structure (prompt-2-gdd.txt).
The method is the Assignment 7 film's footage.py (840b501):
  1. the action at real speed (60 fps captures: every second captured frame; the 30 fps Assignment 6 capture: every
     frame), never trimmed or retimed to fit;
  2. where named, a replay at x0.25 of part of it, labelled as a slowed replay of the same capture;
  3. the last frame held, labelled, for whatever narration remains.
Each beat is built to exactly the frame count of its measured (padded) narration, so the compiler neither retimes nor
cuts it. The game's 640x360 canvas is enlarged x5 (x3 in the appendix beat, beside the exists-today list) with
nearest-neighbour scaling, under a header that names each capture, its revision and the frames shown. Chips are read
from the captures' frame and input logs and drawn by the film outside the game image; the game frames are untouched.

Sources (each span names its own):
  c840   capture/run-01 (840b501; frames from CAP_840B501)
  cfail  capture/run-02 (840b501, the pit fail; frames from CAP_840B501_FAIL)
  c2b6   capture/a5-run-01 (2b68e0a; frames from CAP_2B68E0A)
  a6     the Assignment 6 film's capture run-01.mp4 (3c37fe0), reused unchanged: A6_RUN01, SHA-256 checked
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

import cards
from common import (REEL, FPS, W, H, PAGE, INK, INK_SOFT, FIRE, REV_A7, REV_A5, REV_A6, REV_A6_CAP, A6_RUN01,
                    A6_RUN01_SHA, CAP_840, CAP_2B6, CAP_FAIL, L_REPLAY, L_HOLD, load_json, save_json, render_frames,
                    sha256, frame_rows, input_rows, run)

SRC = {
    'c840': {'rev': REV_A7, 'fps': 60, 'name': 'capture/run-01', 'log': 'run-01'},
    'cfail': {'rev': REV_A7, 'fps': 60, 'name': 'capture/run-02', 'log': 'run-02'},
    'c2b6': {'rev': REV_A5, 'fps': 60, 'name': 'capture/a5-run-01', 'log': 'a5-run-01', 'note': ' (Assignment 5)'},
    'a6': {'rev': REV_A6_CAP, 'fps': 30, 'name': "the Assignment 6 film's capture/run-01", 'log': None,
           'note': ' (Assignment 6)'},
}

# beat: (layout, [(source, first, last, mode, caption)])   mode 'real' or 'replay' (x0.25: each 60 fps frame twice)
PLAN = {
    'G04': ('full', [('c840', 15, 439, 'real', 'Real speed: run (A/D), stop, run, jump the pit (Space), land'),
                     ('c840', 280, 350, 'replay', 'the jump and the landing'),
                     ('c840', 1500, 1560, 'real', 'Real speed: aim with the mouse, click to cast'),
                     ('cfail', 240, 385, 'real', 'Real speed: no jump, into the pit: the fail and its reason')]),
    'G05': ('full', [('c840', 860, 1088, 'real', 'Real speed: growl, lunge, recover; the second lunge lands'),
                     ('c840', 995, 1015, 'replay', 'the lunge that lands, the hurt tint and blink'),
                     ('c840', 1400, 1619, 'real', 'Real speed: a hit during the growl'),
                     ('c840', 1524, 1560, 'replay', 'the hit during the growl: no lunge'),
                     ('c840', 2040, 2148, 'real', 'Real speed: a hit during the lunge'),
                     ('c840', 2080, 2115, 'replay', 'the hit during the lunge: the dash commits')]),
    'Q07B': ('full', [('c2b6', 420, 560, 'real', 'Real speed: the lunge lands, the hurt tint fades'),
                      ('c2b6', 470, 520, 'replay', 'the hurt tint')]),
    'Q07C': ('full', [('a6', 230, 524, 'real', 'Real speed: impacts on the wolf, the ground, rapid fire')]),
    'Q07D': ('full', [('c840', 140, 439, 'real', 'Real speed: run, stop, run, jump the pit, land')]),
    'A01': ('side', [('c840', 15, 439, 'real', 'Real speed: the run cycle'),
                     ('c840', 990, 1060, 'real', 'Real speed: the lunge rig, the afterimage'),
                     ('c840', 1500, 1600, 'real', 'Real speed: the fireball, its particles, the growl cancel')]),
}
EXISTS = [('The 2D game: mage, wolf, pit, exit', REV_A7), ('Run cycle and the lunge rig', REV_A7),
          ('Impact and trail particles (≈0.02 / 0.10 ms GPU, RTX 5060 Laptop)', REV_A6),
          ('Hurt-tint shader, frosted-rock material', REV_A5), ('3D props: rock, crystal, chest (own scene)', 'Assignment 3'),
          ('Cave lights, embers, afterimage', REV_A7), ('38 headless runs at 30/60/144 fps, passing', REV_A7),
          ('Concept portraits, not in the game', 'pitch/art/')]


def a6_frames(tmp):
    assert A6_RUN01 and A6_RUN01.is_file(), 'set A6_RUN01 to the Assignment 6 capture archive'
    assert sha256(A6_RUN01) == A6_RUN01_SHA, 'A6_RUN01 is not the recorded Assignment 6 capture'
    run(['ffmpeg', '-v', 'error', '-i', A6_RUN01, '-start_number', '0', Path(tmp) / 'frame%08d.png'])
    return Path(tmp)


def label(spans):
    srcs = []
    for s, *_ in spans:
        if s not in srcs:
            srcs.append(s)
    revs = sorted({SRC[s]['rev'] for s in srcs})
    note = SRC[srcs[0]].get('note', '')
    return f"Real capture · scripted input · revision {', '.join(revs)}{note}", srcs


def geometry(layout):
    return (320, 250, 5) if layout == 'full' else (200, 330, 3)


def header(heading, layout, spans):
    """Heading, label and source line, all inside the title-safe inset (x 192-3648, y 108-2052 at 4K)."""
    gx, gy, k = geometry(layout)
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    lab, srcs = label(spans)
    d.text((gx, 102), heading, font=cards.F('serif', 70), fill=INK)
    c = cards.chip(lab, 'real', 42)
    right = gx + 640 * 5 if layout == 'full' else W - 200
    im.paste(c, (right - c.width, 110), c)
    parts = []
    for s in srcs:
        fr = ', '.join(f'{a}–{b}' for ss, a, b, _, _ in spans if ss == s)
        parts.append(f"{SRC[s]['name']} frames {fr}")
    d.text((gx, 196), ' · '.join(parts) + f" · {SRC[srcs[0]]['fps']} fps · 640×360 game canvas, enlarged ×{k}, nearest "
           'neighbour', font=cards.F('sans', 30), fill=INK_SOFT)
    if layout == 'side':
        x0 = gx + 640 * k + 80
        cards.panel(d, (x0, 330, W - 200, 2000), 'Exists today')
        for i, (s, r) in enumerate(EXISTS):
            y = 470 + i * 185
            cards.para(d, (x0 + 50, y), s, cards.F('sans', 46), INK, W - 200 - x0 - 380, 1.2)
            d.text((W - 250, y + 4), r, font=cards.F('mono', 44), fill=INK_SOFT, anchor='ra')
        d.text((gx, gy + 360 * k + 60), 'Everything in this list is in git at the revision shown; '
               'the footage is the game at 840b501.', font=cards.F('sans', 40), fill=INK_SOFT)
    return im


def state_text(src, r, failed):
    if src == 'c840':
        return f"frame log · mage {r.get('ps', '–')} · wolf {r.get('ws', '–')} · wolf HP {r.get('whp', '–')} · frame {r['f']}"
    if src == 'cfail':
        t = f"frame log · mage {r.get('ps', '–')} · HP {r.get('php', '–')} · frame {r['f']}"
        if failed and r['f'] >= failed['frame']:
            t += f" · fail: “{failed['reason']}” (input log, frame {failed['frame']})"
        return t
    if src == 'c2b6':
        return (f"frame log · mage {r.get('ps', '–')} · HP {r.get('php', '–')} · hurt-tint intensity "
                f"{r.get('tint', 0):.2f} (read from the shader) · frame {r['f']}")
    return None


def hit_text(h):
    what = 'no lunge' if h['prev_state'] == 'GROWL' else 'the dash runs on (commits)'
    return (f"hit on frame {h['frame']}: wolf in {h['prev_state']} → {h['state']}, {what} · wolf HP "
            f"{h['hp_before']} → {h['hp_after']}  (input log)")


def build(bid, heading, total, dirs, logs, hits, failed):
    layout, spans = PLAN[bid]
    gx, gy, k = geometry(layout)
    seq = []
    for src, a, b, mode, cap in spans:
        step = 2 if SRC[src]['fps'] == 60 else 1
        if mode == 'real':
            seq += [(src, n, 'real', cap) for n in range(a, b + 1, step)]
        else:
            seq += [(src, n, 'replay', cap) for n in range(a, b + 1) for _ in range(2)]
    assert len(seq) <= total, f'{bid}: action ({len(seq)} frames) is longer than the beat ({total})'
    hold_from = len(seq)
    seq += [(seq[-1][0], seq[-1][1], 'hold', '')] * (total - len(seq))
    base = header(heading, layout, spans)
    out = REEL / 'media' / f'{bid}.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-frames:v', str(total), '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '12', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    small = 40 if layout == 'full' else 30
    last_key, last = None, None
    for src, n, phase, cap in seq:
        key = (src, n, phase, cap)
        if key != last_key:
            im = base.copy()
            game = Image.open(dirs[src] / f'frame{n:08d}.png').convert('RGB')
            assert game.size == (640, 360), f'{bid}: frame {n} is {game.size}'
            lo, hi = game.convert('L').getextrema()
            assert hi - lo > 8, f'{bid}: {src} frame {n} is flat (a gap between segments)'
            im.paste(game.resize((640 * k, 360 * k), Image.NEAREST), (gx, gy))
            text = {'real': cap, 'replay': f'{L_REPLAY} — {cap}', 'hold': L_HOLD}[phase]
            c = cards.chip(text, 'constructed' if phase == 'replay' else 'real', small + 4)
            im.paste(c, (gx + 640 * k - c.width - 30, gy + 30), c)
            rows = logs.get(src)
            if rows is not None:
                r = rows[n]
                assert r['seg'] and r.get('ws') != 'FREED', f'{bid}: {src} frame {n} is between segments'
                s = cards.chip(state_text(src, r, failed), 'figure', small)
                sy = gy + 360 * k - s.height - 30
                im.paste(s, (gx + 30, sy), s)
                h = hits.get(r['seg']) if src == 'c840' else None
                if h and n >= h['frame']:
                    hc = cards.chip(hit_text(h), 'constructed', small)
                    im.paste(hc, (gx + 30, sy - hc.height - 16), hc)
            last, last_key = im.tobytes(), key
        enc.stdin.write(last)
    enc.stdin.close()
    assert enc.wait() == 0, f'{bid}: ffmpeg failed'
    return {'layout': layout, 'label': label(spans)[0],
            'spans': [{'source': SRC[s]['name'], 'revision': SRC[s]['rev'], 'frames': [a, b], 'mode': m,
                       'caption': c} for s, a, b, m, c in spans],
            'real_speed_method': 'every second captured frame (60 fps captures); every frame (30 fps capture)',
            'replay_method': 'every captured frame shown twice (x0.25 of a 60 fps capture at 30 fps)',
            'hold_starts_at_frame_of_beat': hold_from, 'beat_frames': total, 'media': f'media/{bid}.mp4',
            'media_sha256': sha256(out)}


def main():
    sheet = load_json(REEL / 'beat_sheet.json')
    beats = {b['beat_id']: b for b in sheet['beats']}
    assert CAP_840 and CAP_2B6 and CAP_FAIL, 'set CAP_840B501, CAP_840B501_FAIL and CAP_2B68E0A'
    logs = {'c840': frame_rows('run-01'), 'cfail': frame_rows('run-02'), 'c2b6': frame_rows('a5-run-01'), 'a6': None}
    hits = {r['segment']: r for r in input_rows('run-01') if r.get('kind') == 'wolf_hit'}
    failed = next(r for r in input_rows('run-02') if r.get('kind') == 'failed')
    prov = {}
    with tempfile.TemporaryDirectory() as tmp:
        dirs = {'c840': CAP_840, 'cfail': CAP_FAIL, 'c2b6': CAP_2B6, 'a6': a6_frames(tmp)}
        for bid in PLAN:
            total = render_frames(beats[bid]['actual_duration_s'])
            prov[bid] = build(bid, beats[bid]['heading'], total, dirs, logs, hits, failed)
            print(bid, total, 'frames; hold from', prov[bid]['hold_starts_at_frame_of_beat'])
    prov['_a6_capture'] = {'path': 'A6_RUN01 (fall-2026/zhefan-z/assignment-6/walker-magic-zhefan/youtube/'
                                   'claude-liam-walker-magic-particles-gamedev/capture/run-01.mp4, kept out of git)',
                           'sha256': A6_RUN01_SHA, 'revision': REV_A6_CAP,
                           'record': f'CAPTURE.md of the Assignment 6 film at {REV_A6}'}
    save_json(REEL / 'evidence' / 'footage-provenance.json', prov)


if __name__ == '__main__':
    main()
