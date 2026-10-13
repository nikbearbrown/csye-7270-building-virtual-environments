#!/usr/bin/env bash
# mid.sh <Class> ... : low-res render of the clip (scratch only), then frames at 10/25/50/75/95% -> one contact strip per class
# in /private/tmp/claude-501/lecture-blender-act4/frames/<Class>_strip.png   (LOOK at it: the 50% frame is what GATE T and Gate V sample)
set -u
SCR=/private/tmp/claude-501/lecture-blender-act4
mkdir -p "$SCR/frames"
for C in "$@"; do
  (cd "$SCR" && manim -ql --media_dir "$SCR/media" scenes.py "$C" >/dev/null 2>&1)
  MP4=$(ls "$SCR"/media/videos/scenes/480p15/${C}.mp4 2>/dev/null)
  [ -z "$MP4" ] && { echo "no clip for $C"; continue; }
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MP4")
  rm -f "$SCR"/frames/${C}_f*.png
  i=0
  for P in 0.10 0.25 0.50 0.75 0.95; do
    T=$(python3 -c "print(round($D*$P,3))")
    ffmpeg -v error -y -ss "$T" -i "$MP4" -frames:v 1 "$SCR/frames/${C}_f$i.png"; i=$((i+1))
  done
  python3 - "$SCR" "$C" "$D" <<'PY'
import sys
from PIL import Image, ImageDraw
scr,C,D=sys.argv[1:4]
ims=[Image.open(f"{scr}/frames/{C}_f{i}.png").convert("RGB") for i in range(5)]
w,h=ims[0].size; s=0.62; w2,h2=int(w*s),int(h*s)
S=Image.new("RGB",(w2*3,h2*2),(255,255,255))
for i,im in enumerate(ims):
    S.paste(im.resize((w2,h2)),((i%3)*w2,(i//3)*h2)); ImageDraw.Draw(S).text(((i%3)*w2+4,(i//3)*h2+2),f"{C} {[10,25,50,75,95][i]}% of {float(D):.2f}s",fill=(200,0,0))
S.save(f"{scr}/frames/{C}_strip.png")
PY
  echo "$C clip=${D}s -> $SCR/frames/${C}_strip.png"
done
