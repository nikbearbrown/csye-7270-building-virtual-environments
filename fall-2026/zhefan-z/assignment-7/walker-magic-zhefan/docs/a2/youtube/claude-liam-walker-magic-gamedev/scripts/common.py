"""Shared paths, constants and helpers for the walker-magic gamedev reel scripts.

Nothing here edits the game. Paths outside the repository come from the
environment so no developer-machine path is baked into the reel:
  WALKER_ART_HOME   the Brutalist toolkit (brutalist.art)
  WALKER_SNAPSHOT   a `git archive` of the game folder at the build shown (74c0443)
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
SLUG = REEL.name
TITLE = 'Her Fire Is the Only Warmth: Building a Cave Mage Slice'
BUILD = '74c0443'                           # tested build shown in the film
CAPTURE_SOURCE = '5266946'                  # capture copy; runtime files identical to BUILD
FPS = 30
SRC_FPS = 60
W, H = 3840, 2160
SAMPLES_PER_SRC_FRAME = 48000 // SRC_FPS    # 800

ART = Path(os.environ['WALKER_ART_HOME']) if os.environ.get('WALKER_ART_HOME') else None
SNAPSHOT = Path(os.environ['WALKER_SNAPSHOT']) if os.environ.get('WALKER_SNAPSHOT') else None

PAGE, CARD, BORDER, INK, INK_SOFT, SPARK = '#FAF9F5', '#FFFFFF', '#E5E2D9', '#3D3929', '#73705F', '#D97757'
FONTS = {
    'serif': 'EB_Garamond/static/EBGaramond-Regular.ttf',
    'serif_med': 'EB_Garamond/static/EBGaramond-Medium.ttf',
    'sans': 'Inter/static/Inter_28pt-Regular.ttf',
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


def probe_frames(path):
    r = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets',
             '-show_entries', 'stream=nb_read_packets,width,height,r_frame_rate', '-of', 'json', path])
    s = json.loads(r.stdout)['streams'][0]
    return int(s['nb_read_packets']), s['width'], s['height'], s['r_frame_rate']


def source_lines(root, rel, start, end):
    """Exact one-based inclusive excerpt, newline-joined without a final newline."""
    lines = (Path(root) / rel).read_text(encoding='utf-8').splitlines()
    return '\n'.join(lines[start - 1:end])


def script_narration():
    """Narration per beat, exactly as approved in SCRIPT.md."""
    text = (REEL / 'SCRIPT.md').read_text(encoding='utf-8')
    out = {}
    for sec in re.split(r'^## ', text, flags=re.M)[1:]:
        bid = sec[:3]
        if not re.fullmatch(r'B\d\d', bid):
            continue
        spoken = None
        for line in sec.splitlines()[1:]:
            line = line.strip()
            m = re.match(r'\*Narration:\* "(.*?)"(?:\s|$)', line)
            if m:
                spoken = m.group(1)
                break
            if line.startswith('"') and line.endswith('"'):
                spoken = line[1:-1]
                break
        out[bid] = spoken or ''
    return out
