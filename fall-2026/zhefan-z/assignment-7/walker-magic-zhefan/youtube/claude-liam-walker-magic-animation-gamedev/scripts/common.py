"""Shared paths, constants and helpers for the Assignment 7 gamedev reel scripts.

Adapted from the Assignment 6 film's common.py (docs/a6/youtube/claude-liam-walker-magic-particles-gamedev/scripts/).
Nothing here edits the game. Paths outside the repository come from the environment, so no developer-machine path
is baked into the reel:
  WALKER_ART_HOME   the Brutalist toolkit (brutalist.art)
  WALKER_SNAPSHOT   a `git archive` of walker-magic-zhefan at the build shown (ad7935f), never run
  WALKER_CAPTURE    the PNG frames Movie Maker wrote for capture/run-02 (frame%08d.png), kept outside the repository
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
A7 = GAME.parent                            # fall-2026/zhefan-z/assignment-7 (the author's documents, logs, captures)
CAPS = A7 / 'captures'
LOGS = A7 / 'logs'
SLUG = REEL.name
TITLE = 'Keys on the Tick: A Run Cycle and a Wolf Lunge'
BUILD = 'ad7935f'                           # game source revision shown (snapshot, capture and excerpts)
BUILD_FULL = 'ad7935fab018f8acb1ff8c72b55d6642ff921fa4'
TREE = 'b4ea2c1d78edea5cc546224b241cc9aeaa40ebbe'   # git rev-parse ad7935f:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan
FPS = 30
CAPTURE_FPS = 60                            # capture/run-02: --fixed-fps 60, one rendered frame per physics tick
CAPTURE = 'run-02'                          # capture/run-02 (CAPTURE.md); run-01 was the f860fed film's capture
CAPTURE_FRAMES_TOTAL = 2739
W, H = 3840, 2160

ART = Path(os.environ['WALKER_ART_HOME']) if os.environ.get('WALKER_ART_HOME') else None
SNAPSHOT = Path(os.environ['WALKER_SNAPSHOT']) if os.environ.get('WALKER_SNAPSHOT') else None
CAPTURE_FRAMES = Path(os.environ['WALKER_CAPTURE']) if os.environ.get('WALKER_CAPTURE') else None

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


def capture_rows():
    """capture/run-02-frames.jsonl: one row per rendered frame (row f = Movie Maker PNG frame f)."""
    rows = [json.loads(l) for l in (REEL / 'capture' / f'{CAPTURE}-frames.jsonl').read_text(encoding='utf-8').splitlines()]
    assert [r['f'] for r in rows] == list(range(len(rows))), 'frame log is not one row per frame'
    return rows


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
