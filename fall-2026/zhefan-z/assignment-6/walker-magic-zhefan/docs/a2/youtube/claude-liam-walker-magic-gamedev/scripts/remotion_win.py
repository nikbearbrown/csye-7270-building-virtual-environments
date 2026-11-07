"""Run the toolkit's remotion_scenes.py on Windows, unmodified.

remotion_scenes.py calls subprocess.run(["npx", ...]); on Windows npx is
npx.CMD and CreateProcess does not resolve it (WinError 2), as found in
Assignment 1. This wrapper resolves a bare "npx" with shutil.which in memory
and then runs the toolkit's own main(); the toolkit file is not edited.

  python remotion_win.py <REEL> [remotion_scenes args]     # the wrapper, all Remotion beats
  render_component(pattern, props, out)                    # one composition, same flags
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from common import ART

_real_run = subprocess.run


def _run(cmd, *a, **kw):
    if isinstance(cmd, list) and cmd and cmd[0] == 'npx':
        cmd = [shutil.which('npx')] + cmd[1:]
    return _real_run(cmd, *a, **kw)


subprocess.run = _run
sys.path.insert(0, str(ART / 'runtime' / 'scripts'))


def render_component(pattern, props, out):
    """Same command and flags as remotion_scenes.render_beat (scale 2 -> 3840x2160, PNG frames, crf 16)."""
    project = ART / 'runtime' / 'remotion'
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.remotion-', dir=out.parent) as scratch:
        props_path = Path(scratch) / 'props.json'
        props_path.write_text(json.dumps(props), encoding='utf-8')
        candidate = Path(scratch) / 'render.mp4'
        cmd = ['npx', 'remotion', 'render', 'src/index.ts', pattern, str(candidate), f'--props={props_path}',
               '--concurrency=1', '--scale=2', '--image-format=png', '--crf=16']
        r = subprocess.run(cmd, cwd=project, capture_output=True, text=True)
        if r.returncode != 0 or not candidate.is_file():
            raise RuntimeError(f'Remotion {pattern} failed:\n{r.stderr[-2000:]}')
        os.replace(candidate, out)
    return out


if __name__ == '__main__':
    import remotion_scenes
    sys.argv = ['remotion_scenes.py'] + sys.argv[1:]
    raise SystemExit(remotion_scenes.main())
