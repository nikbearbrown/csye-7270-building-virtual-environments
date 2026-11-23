"""GDD 11 (G11): the game's own music and sound effects, played after the narration, with a picture timed to them.

Written by Claude Code for the Assignment 8 pitch film. The audio is read from the game's files at 840b501
(`git show 840b501:<game>/assets/audio/...`); those six files are byte-identical to Assignment 2's (same git blobs).
Nothing is regenerated or edited except: the music excerpt is the loop's first 1.5 s with 0.25 s fades (6 s and
0.4 s before the 2026-11-22 tightening), played at -8 dB
(the game's own Music bus level, default_bus_layout.tres); each effect is played whole, at its file level.

    python audio.py     # after generate_audio_kokoro.py and sheet.py --pad: writes mp3/beat-G11.mp3, media/G11.mp4,
                        # evidence/audio-excerpts.json, and sets G11's actual_duration_s
"""
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import cards
from common import (REEL, FPS, W, H, PAGE, INK, INK_SOFT, FIRE, FIRE_SOFT, CAVE, CAVE_SOFT, REV_A7, A7_GAME,
                    load_json, save_json, sha256, git_show, run, render_frames)

GAME_AUDIO = f'{REV_A7}:{A7_GAME}/assets/audio'
STABILITY = ('This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI '
             'Ltd. All Rights Reserved.  Powered by Stability AI.')
# file, what it is, how it was made (Assignment 2 SOURCES.md), length to play (None = whole file)
CLIPS = [
    ('music/MUS-LOOP.ogg', "MUS-LOOP · the cave theme (the loop's first 1.5 s)",
     'Lyria in the Gemini app, from my prompt; cut into a 54.6 s crossfaded loop · Google Terms of Service and '
     'Generative AI Additional Terms · carries SynthID', 1.5),
    ('sfx/SFX-CAST.ogg', 'SFX-CAST · a fireball is cast', 'Stable Audio Open 1.0, run locally in ComfyUI; seed 3, trimmed to 0.4 s', None),
    ('sfx/SFX-HURT.ogg', 'SFX-HURT · the witch is hit', 'Stable Audio Open 1.0, run locally in ComfyUI; seed 3, trimmed to 0.3 s', None),
    ('sfx/SFX-WOLF-DOWN.ogg', 'SFX-WOLF-DOWN · a wolf is defeated', 'Stable Audio Open 1.0, run locally in ComfyUI; seed 1, trimmed to 0.6 s', None),
    ('sfx/SFX-FAIL.ogg', 'SFX-FAIL · a fail (pit or 0 HP)', 'Stable Audio Open 1.0, run locally in ComfyUI; seed 2, trimmed to 1.0 s', None),
    ('sfx/SFX-CLEAR.ogg', 'SFX-CLEAR · the level is cleared', 'Stable Audio Open 1.0, run locally in ComfyUI; seed 3, trimmed to 1.2 s', None),
]
GAP_AFTER_VOICE, GAP, TAIL = 0.3, 0.2, 0.4      # 2026-11-22 tightened cut (was 0.6, 0.8, 1.0)
MUSIC_DB = -8.0
SR = 48000


def probe(path):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path])
                 .stdout.decode().strip())


def pcm(path, sr=SR):
    raw = run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(sr), '-']).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def build_audio(tmp):
    voice = pcm(REEL / 'mp3' / 'beat-G11.mp3')           # Kokoro's measured narration, unpadded
    lead = int(0.3 * SR)
    parts = [np.zeros((lead, 2), np.float32), voice, np.zeros((int(GAP_AFTER_VOICE * SR), 2), np.float32)]
    t = (lead + len(voice)) / SR + GAP_AFTER_VOICE
    timeline = []
    for i, (rel, what, how, length) in enumerate(CLIPS):
        src = Path(tmp) / Path(rel).name
        src.write_bytes(git_show(f'{GAME_AUDIO}/{rel}'))
        a = pcm(src)
        if length:
            a = a[:int(length * SR)]
            n = int(0.25 * SR)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            a[:n] *= ramp
            a[-n:] *= ramp[::-1]
            a *= 10 ** (MUSIC_DB / 20)
        dur = len(a) / SR
        timeline.append({'file': f'assets/audio/{rel}', 'what': what, 'how': how, 'start_s': round(t, 3),
                         'dur_s': round(dur, 3), 'git_blob': run(['git', '-C', REEL.parents[3], 'rev-parse',
                                                                  f'{GAME_AUDIO}/{rel}']).stdout.decode().strip(),
                         'level': f'{MUSIC_DB:+.0f} dB (the game\'s Music bus)' if length else 'file level'})
        parts += [a, np.zeros((int((GAP if i < len(CLIPS) - 1 else TAIL) * SR), 2), np.float32)]
        t += dur + (GAP if i < len(CLIPS) - 1 else TAIL)
    mix = np.clip(np.concatenate(parts), -1.0, 1.0)
    wav = Path(tmp) / 'g11.wav'
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-', wav],
        input=mix.tobytes())
    out = REEL / 'mp3' / 'beat-G11.mp3'
    voice_s = probe(out)
    run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', out])
    return timeline, voice_s, probe(out)


def waveform(path, w, h):
    a = pcm(path, 8000).mean(axis=1)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if len(a) == 0:
        return im
    cols = np.array_split(np.abs(a), w)
    peak = max(1e-6, float(np.abs(a).max()))
    for x, c in enumerate(cols):
        v = float(c.max()) / peak if len(c) else 0
        y = int(v * (h / 2 - 2))
        d.line([(x, h // 2 - y), (x, h // 2 + y)], fill=(61, 57, 41, 255))
    return im


def build_video(timeline, total_s, tmp):
    base, d = cards.page('GDD 11 · Sound and music', [(f'Real audio · the game\'s own files at {REV_A7} (made in '
                                                       'Assignment 2)', 'real')])
    x0, y0, rowh, ww = 240, 330, 250, 900
    waves = []
    for i, c in enumerate(timeline):
        y = y0 + i * rowh
        src = Path(tmp) / Path(c['file']).name
        wv = waveform(src, ww, 150)
        waves.append(wv)
        d.text((x0 + ww + 80, y + 10), c['what'], font=cards.F('sans_med', 56), fill=INK)
        cards.para(d, (x0 + ww + 80, y + 90), c['how'], cards.F('sans', 42), INK_SOFT, 2300, 1.25)
    d.text((x0, y0 + 6 * rowh + 10), 'Effects: ' + STABILITY, font=cards.F('sans', 36), fill=INK_SOFT)
    d.text((x0, y0 + 6 * rowh + 70), 'Music: generated with Lyria in the Gemini app; audio made with Lyria carries '
           "Google's SynthID watermark.  Planned, not made yet: a boss theme, a campfire theme, the great wolf's growl, "
           'the boulder, a campfire crackle.', font=cards.F('sans', 36), fill=INK_SOFT)
    total = render_frames(total_s)
    out = REEL / 'media' / 'G11.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-frames:v', str(total), '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '14', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    last_key, last = None, None
    for f in range(total):
        t = f / FPS
        cur = next((i for i, c in enumerate(timeline) if c['start_s'] <= t < c['start_s'] + c['dur_s'] + 0.25), None)
        prog = None
        if cur is not None:
            c = timeline[cur]
            prog = min(1.0, (t - c['start_s']) / c['dur_s'])
            prog = round(prog * 60) / 60
        key = (cur, prog)
        if key != last_key:
            im = base.copy()
            dd = ImageDraw.Draw(im)
            for i, wv in enumerate(waves):
                y = y0 + i * rowh
                fill = FIRE_SOFT if i == cur else '#F0EDE4'
                dd.rounded_rectangle([x0 - 20, y - 10, x0 + ww + 20, y + 170], radius=24, fill=fill)
                im.paste(wv, (x0, y + 10), wv)
                if i == cur:
                    px = x0 + int(prog * ww)
                    dd.line([(px, y - 10), (px, y + 170)], fill=FIRE, width=8)
                    dd.text((x0 + ww + 80, y - 40), '▶ playing', font=cards.F('sans_med', 36), fill=FIRE)
            last, last_key = cards.fit_safe(im).tobytes(), key
        enc.stdin.write(last)
    enc.stdin.close()
    assert enc.wait() == 0
    return out


def main():
    sheet = load_json(REEL / 'beat_sheet.json')
    b = next(x for x in sheet['beats'] if x['beat_id'] == 'G11')
    assert not b.get('audio_mix'), 'G11 is already mixed: regenerate its narration first'
    with tempfile.TemporaryDirectory() as tmp:
        timeline, voice_s, total_s = build_audio(tmp)
        b['voice_s'] = round(voice_s, 3)
        b['actual_duration_s'] = round(total_s, 2)
        b['audio_mix'] = 'narration (lead 0.3 s), then the six excerpts in evidence/audio-excerpts.json'
        out = build_video(timeline, b['actual_duration_s'], tmp)
    save_json(REEL / 'beat_sheet.json', sheet)
    save_json(REEL / 'evidence' / 'audio-excerpts.json', {
        'beat': 'G11', 'source': f'git show {GAME_AUDIO}/... (byte-identical to Assignment 2)', 'excerpts': timeline,
        'track': 'mp3/beat-G11.mp3', 'track_sha256': sha256(REEL / 'mp3' / 'beat-G11.mp3'),
        'media': 'media/G11.mp4', 'media_sha256': sha256(out), 'stability_notice': STABILITY})
    print('G11', b['actual_duration_s'], 's;', [(c['file'], c['start_s']) for c in timeline])


if __name__ == '__main__':
    main()
