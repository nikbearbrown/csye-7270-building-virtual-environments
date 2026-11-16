"""Shared paths, constants and helpers for the Assignment 5 gamedev reel scripts.

Adapted from the Assignment 3 film's scripts (docs/a3/youtube/claude-liam-walker-magic-3d-assets-gamedev/scripts/).
Nothing here edits the game. Paths outside the repository come from the environment, so no
developer-machine path is baked into the reel:
  WALKER_ART_HOME   the Brutalist toolkit (brutalist.art)
  WALKER_SNAPSHOT   a `git archive` of walker-magic-zhefan at the build shown (40c42f5), never run
"""
import hashlib
import json
import math
import os
import re
import subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1]                      # walker-magic-zhefan (project.godot)
A5 = GAME.parent                            # fall-2026/zhefan-z/assignment-5 (the author's documents and captures)
CAPS = A5 / 'captures'
SLUG = REEL.name
TITLE = 'A Red Flash, a Frosted Rock: Two Shaders for a Cave Mage'
BUILD = '40c42f5'                           # game source revision shown (captures and the generated shader)
BUILD_FULL = '40c42f52b7be9964283057ff778b32714fa06340'
FPS = 30
W, H = 3840, 2160

ART = Path(os.environ['WALKER_ART_HOME']) if os.environ.get('WALKER_ART_HOME') else None
SNAPSHOT = Path(os.environ['WALKER_SNAPSHOT']) if os.environ.get('WALKER_SNAPSHOT') else None

PAGE, CARD, BORDER, INK, INK_SOFT, SPARK = '#FAF9F5', '#FFFFFF', '#E5E2D9', '#3D3929', '#73705F', '#D97757'
FONTS = {
    'serif': 'EB_Garamond/static/EBGaramond-Regular.ttf',
    'serif_med': 'EB_Garamond/static/EBGaramond-Medium.ttf',
    'sans': 'Inter/static/Inter_28pt-Regular.ttf',
    'sans_med': 'Inter/static/Inter_28pt-Medium.ttf',
    'mono': 'PT_Mono/PTMono-Regular.ttf',
}


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
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f'command failed ({r.returncode}): {" ".join(map(str, cmd))}\n{r.stderr[-3000:]}')
    return r


def source_lines(root, rel, start, end):
    """Exact one-based inclusive excerpt, newline-joined without a final newline."""
    lines = (Path(root) / rel).read_text(encoding='utf-8').splitlines()
    return '\n'.join(lines[start - 1:end])


def script_narration():
    """Narration per beat, exactly as written in SCRIPT.md."""
    text = (REEL / 'SCRIPT.md').read_text(encoding='utf-8')
    out = {}
    for sec in re.split(r'^## ', text, flags=re.M)[1:]:
        bid = sec[:3]
        if not re.fullmatch(r'B\d\d', bid):
            continue
        spoken = None
        for line in sec.splitlines()[1:]:
            m = re.match(r'\*Narration:\* "(.*)"\s*$', line.strip())
            if m:
                spoken = m.group(1)
                break
        out[bid] = spoken or ''
    return out
