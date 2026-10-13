#!/usr/bin/env zsh
# frames_act2.sh <Class> ... — LOW-RES (480p15) motion check of Act I scenes from the preflight scratch (run REEL/preflight.sh 1 first):
# renders each class, prints its clip length vs audio, and writes frames at 25/50/85/95 % to <scratch>/frames/<Class>_<pct>.png
# plus a per-class strip <scratch>/frames/<Class>_strip.png. One render at a time; never 4K.
SCR=/private/tmp/claude-501/lecture-csye-games-act2
OUT=$SCR/frames; mkdir -p $OUT
for C in "$@"; do
  (cd $SCR && manim -ql --fps 24 --media_dir $SCR/media_ql scenes.py $C >/dev/null 2>&1)
  MP4=$SCR/media_ql/videos/scenes/480p24/$C.mp4
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $MP4)
  for P in 25 50 85 95; do
    T=$(python3 -c "print($D*$P/100)")
    ffmpeg -v error -y -ss $T -i $MP4 -frames:v 1 $OUT/${C}_$P.png
  done
  python3 -c "
from PIL import Image
ims=[Image.open('$OUT/${C}_%d.png'%p) for p in (25,50,85,95)]
w,h=ims[0].size; s=Image.new('RGB',(w*2,h*2))
[s.paste(im,((i%2)*w,(i//2)*h)) for i,im in enumerate(ims)]; s.save('$OUT/${C}_strip.png')"
  B=${C%%_*}
  A=$(python3 -c "import json;print([b['actual_duration_s'] for b in json.load(open('$SCR/beat_sheet.json'))['beats'] if b['beat_id']=='$B'][0])")
  echo "$C clip=${D}s audio=${A}s"
done
