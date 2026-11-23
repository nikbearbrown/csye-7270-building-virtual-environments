"""Shared paths, constants and helpers for the Assignment 8 pitch film (The Little Flame Witch).

Written by Claude Code for this film; the frame-log and hashing helpers follow the Assignment 7 film's common.py
(fall-2026/zhefan-z/assignment-7/walker-magic-zhefan/youtube/claude-liam-walker-magic-animation-gamedev/scripts/ at
840b501). Nothing here edits a game. Paths outside the repository come from the environment, so no developer-machine
path is baked into the reel:
  BRUTALIST_HOME   the Brutalist toolkit checkout (brutalist.art): fonts, Kokoro, compiler, gates
  CAP_840B501      PNG frames Movie Maker wrote for capture/run-01 (the game at 840b501), frame%08d.png
  CAP_840B501_FAIL PNG frames Movie Maker wrote for capture/run-02 (the pit fail, 840b501)
  CAP_2B68E0A      PNG frames Movie Maker wrote for capture/a5-run-01 (the Assignment 5 game at 2b68e0a)
  A6_RUN01         the Assignment 6 film's capture archive run-01.mp4 (game at 3c37fe0), checked by SHA-256
"""
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]          # fall-2026/zhefan-z/assignment-8/pitch
REPO = REEL.parents[3]                               # the course repository
ART_DIR = REEL / 'art'
SLUG = 'zhefan-z-little-flame-witch-pitch'
TITLE = 'The Little Flame Witch'
AUTHOR = 'Zhefan Zhang'
FPS = 30
W, H = 3840, 2160

# Revisions shown (all verified against git in Part 1 of the session)
REV_A7 = '840b501'          # the game today (Assignment 7 tip); the new capture
REV_A7_FULL = '840b501d645178013115beb0883764d69e5e9552'
A7_GAME = 'fall-2026/zhefan-z/assignment-7/walker-magic-zhefan'
REV_A5 = '2b68e0a'          # Assignment 5 tip: hurt tint
REV_A5_FULL = '2b68e0ac04fa1259ef1a77bf314205bc7bc3146e'
A5_GAME = 'fall-2026/zhefan-z/assignment-5/walker-magic-zhefan'
REV_A6_CAP = '3c37fe0'      # the Assignment 6 film's capture revision (no game file changed from it to 7672d5a)
REV_A6 = '7672d5a'
A6_RUN01_SHA = '81f207048bb51d6370cc461ba0c00b4c4a4c37d60ca1fac6e240403c23322e80'

ART = Path(os.environ['BRUTALIST_HOME']) if os.environ.get('BRUTALIST_HOME') else None
CAP_840 = Path(os.environ['CAP_840B501']) if os.environ.get('CAP_840B501') else None
CAP_2B6 = Path(os.environ['CAP_2B68E0A']) if os.environ.get('CAP_2B68E0A') else None
CAP_FAIL = Path(os.environ['CAP_840B501_FAIL']) if os.environ.get('CAP_840B501_FAIL') else None
A6_RUN01 = Path(os.environ['A6_RUN01']) if os.environ.get('A6_RUN01') else None

# Palette: the toolkit's cream page and ink, a cold cave blue and the one warm colour, fire.
PAGE, CARD, BORDER, INK, INK_SOFT = '#FAF9F5', '#FFFFFF', '#E5E2D9', '#3D3929', '#73705F'
FIRE, FIRE_SOFT, CAVE, CAVE_SOFT, CAVE_DARK = '#D97757', '#F3C9A8', '#4F6D8F', '#C9D6E3', '#1F2A38'
FONTS = {
    'serif': 'EB_Garamond/static/EBGaramond-Regular.ttf',
    'serif_med': 'EB_Garamond/static/EBGaramond-Medium.ttf',
    'sans': 'Inter/static/Inter_28pt-Regular.ttf',
    'sans_med': 'Inter/static/Inter_28pt-Medium.ttf',
    'mono': 'PT_Mono/PTMono-Regular.ttf',
}

# On-screen labels (the exact wording the author asked for)
L_REAL = f'Real capture · scripted input · revision {REV_A7}'
L_REPLAY = 'Slowed replay ×0.25 of the same capture'
L_HOLD = 'Last frame held'
L_CONSTRUCTED_PROPOSED = 'Constructed - proposed, not built'
L_GENERATED = 'Generated (Gemini 4) · concept art, not in the game'
L_CONSTRUCTED = 'Constructed'


def font_path(name):
    return ART / 'runtime' / 'fonts' / FONTS[name]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def render_frames(seconds):
    """Frames the compiler gives a beat: it pads, never truncates (compile.prepare_timeline)."""
    return math.ceil(seconds * FPS - 1e-8)


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, **kw)
    if r.returncode != 0:
        err = r.stderr.decode('utf-8', 'replace') if isinstance(r.stderr, bytes) else r.stderr
        raise RuntimeError(f'command failed ({r.returncode}): {" ".join(map(str, cmd))}\n{err[-3000:]}')
    return r


def git_show(rev_path):
    """Bytes of a committed file (`<rev>:<path>`), so committed evidence is read at its revision, never the tree."""
    return run(['git', '-C', REPO, 'show', rev_path]).stdout


def frame_rows(name):
    """capture/<name>-frames.jsonl: one row per rendered frame (row f = Movie Maker PNG frame f)."""
    rows = [json.loads(l) for l in (REEL / 'capture' / f'{name}-frames.jsonl').read_text(encoding='utf-8').splitlines()]
    assert [r['f'] for r in rows] == list(range(len(rows))), f'{name}: frame log is not one row per frame'
    return rows


def input_rows(name):
    return [json.loads(l) for l in (REEL / 'capture' / f'{name}-inputs.jsonl').read_text(encoding='utf-8').splitlines()]
