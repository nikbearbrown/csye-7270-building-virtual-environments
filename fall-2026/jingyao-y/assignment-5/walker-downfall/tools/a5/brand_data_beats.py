"""Add the channel wordmark to the two data-table slots, preserving their clock."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
source_dir=REEL/"source-media";source_dir.mkdir(exist_ok=True)
rows=[]
for bid in ("B18","B19"):
    source=source_dir/(bid+"-original.mp4")
    target=REEL/"media"/(bid+".mp4")
    if not source.exists():shutil.copy2(target,source)
    candidate=target.with_name("_brand-"+target.name)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(source),"-vf","drawtext=fontfile='C\\:/Windows/Fonts/georgia.ttf':text='@NikBearBrown':x=w-tw-210:y=h-155:fontsize=50:fontcolor=0x302d27@0.65","-c:v","libx264","-preset","fast","-threads","4","-crf","16","-pix_fmt","yuv420p","-an",str(candidate)],check=True)
    candidate.replace(target)
    rows.append({"beat":bid,"original_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"branded_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"change":"Channel wordmark only; no retiming or data changes."})
(REEL/"data-branding.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rows,indent=2))
