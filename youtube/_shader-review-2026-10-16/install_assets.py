#!/usr/bin/env python3
"""Install only this batch's recorded Godot evidence into Remotion's public assets."""
from pathlib import Path
import hashlib,shutil
from PIL import Image
HERE=Path(__file__).resolve().parent
DEST=HERE.parents[2]/'brutalist.art/runtime/remotion/public/shader-lesson-captures'
def same(a,b):return b.exists() and hashlib.sha256(a.read_bytes()).digest()==hashlib.sha256(b.read_bytes()).digest()
def main():
 DEST.mkdir(parents=True,exist_ok=True)
 for video in sorted((HERE/'captures').glob('*.mp4')):
  frame=HERE/'project-snapshot/evidence/film-frames'/video.stem/'0191.jpg'
  if not same(video,DEST/video.name):shutil.copy2(video,DEST/video.name)
  # The side-by-side still omits the bottom diagnostic caption; the full video retains it at readable size.
  Image.open(frame).crop((0,0,1280,620)).save(DEST/(video.stem+'.jpg'),quality=95)
 print('Installed verified source media:',DEST)
if __name__=='__main__':main()
