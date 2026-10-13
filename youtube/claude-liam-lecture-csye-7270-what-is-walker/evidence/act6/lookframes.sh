#!/usr/bin/env bash
# lookframes.sh <Class> ... — after REEL/preflight.sh 6: renders each class at -ql --fps 24 (private scratch), prints clip length vs audio, and writes
# frames at 12/30/50/70/92% to /private/tmp/claude-501/lecture-csye-walker-act6/look/<Class>_<pct>.png (LOOK at them; 50% is what GATE T samples).
SCR=/private/tmp/claude-501/lecture-csye-walker-act6; mkdir -p $SCR/look
for C in "$@"; do
  (cd $SCR && manim -ql --fps 24 --disable_caching --media_dir $SCR/medialook scenes.py $C 2>&1 | grep -E "\[pace\]|Traceback|Error" )
  F=$(find $SCR/medialook -name "$C.mp4" | head -1)
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
  echo "$C clip=$D"
  for P in 12 30 50 70 92; do
    T=$(python3 -c "print(round($D*$P/100,3))")
    ffmpeg -v error -y -ss $T -i "$F" -frames:v 1 $SCR/look/${C}_$P.png
  done
done
