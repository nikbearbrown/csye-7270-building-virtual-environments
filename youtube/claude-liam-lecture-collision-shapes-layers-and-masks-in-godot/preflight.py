#!/usr/bin/env python3
"""Render only low-resolution scene end frames, then Remotion 25/50/95% stills.
Stage-two command: not run during the layout handoff.
"""
from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parent
S=json.loads((R/'beat_sheet.json').read_text())
assert all(b.get('audio_file') and b.get('actual_duration_s',0)>0 for b in S['beats']),'Generate and measure audio first'
for b in S['beats']:
 cls=b.get('shot',{}).get('manim',{}).get('class')
 if cls:
  subprocess.run([sys.executable,'-m','manim','-ql','-s','--disable_caching','--media_dir',str(R/'_qc/preflight/manim'/b['beat_id']),str(R/'scenes.py'),cls],check=True,cwd=R)
script=R.parents[2]/'brutalist.art/runtime/scripts/remotion_scenes.py'
subprocess.run([sys.executable,str(script),str(R),'--stills'],check=True)
print('Inspect all generated PNGs; do not infer visual approval from this exit code.')
