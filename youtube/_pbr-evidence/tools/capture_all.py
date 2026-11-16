#!/usr/bin/env python3
"""Capture every ShaderLab beat of the PBR reels at its measured duration, encode, install into Remotion public/."""
from pathlib import Path
import json, subprocess, sys, shutil, hashlib
HERE = Path(__file__).resolve().parents[1]
YT = HERE.parent
PUB = HERE.parents[2] / 'brutalist.art/runtime/remotion/public/pbr-captures'
PUB.mkdir(parents=True, exist_ok=True)
(HERE / 'evidence/captures').mkdir(parents=True, exist_ok=True)
FR = HERE / 'evidence/frames'
log = open(HERE / 'evidence/capture-log.txt', 'a')
only = sys.argv[1:]
for slug in ['what-is-pbr', 'why-pbr-matters', 'pbr-textures-are-data']:
    sheet = json.loads((YT / f'claude-liam-lecture-{slug}/beat_sheet.json').read_text())
    for b in sheet['beats']:
        ev = b.get('evidence', {})
        if 'capture_id' not in ev: continue
        name = Path(b['shot']['remotion']['props']['video']).name
        if only and name not in only and ev['capture_id'] not in only: continue
        secs = b['actual_duration_s']
        tag = name[:-4]
        r = subprocess.run(['godot', '--path', str(HERE), '--script', 'res://tools/capture.gd', '--', '--id', ev['capture_id'],
                            '--seconds', f'{secs:.3f}', '--fps', '24', '--out', str(FR / tag)], capture_output=True, text=True, timeout=600)
        line = [l for l in r.stdout.splitlines() if l.startswith('CAPTURE')]
        if r.returncode or not line: sys.exit(f'capture failed for {name}:\n{r.stdout[-800:]}\n{r.stderr[-800:]}')
        out = HERE / 'evidence/captures' / name
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-framerate', '24', '-i', str(FR / tag / ev['capture_id'] / '%04d.jpg'),
                        '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)], check=True)
        shutil.copy2(out, PUB / name)
        shutil.rmtree(FR / tag)
        msg = f'{name}: {line[0]} -> sha256 {hashlib.sha256(out.read_bytes()).hexdigest()[:16]}'
        print(msg); log.write(msg + '\n'); log.flush()
