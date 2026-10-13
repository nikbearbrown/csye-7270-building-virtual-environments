#!/usr/bin/env zsh
# midframes.sh <Class> ... — low-res (480p24) render of each act-4 scene from the preflight scratch, frames at 25/50/95 % of the clip.
# Run REEL/preflight.sh 4 <Classes> first (it builds /private/tmp/claude-501/lecture-a3assets-act4/scenes.py). One render at a time.
SCR=/private/tmp/claude-501/lecture-a3assets-act4
mkdir -p $SCR/mid
for C in "$@"; do
  (cd $SCR && manim -ql --fps 24 --media_dir $SCR/media_mid scenes.py $C >/dev/null 2>&1)
  MP4=$SCR/media_mid/videos/scenes/480p24/$C.mp4
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $MP4)
  for P in 25 50 95; do
    T=$(python3 -c "print($D*$P/100)")
    ffmpeg -v error -y -ss $T -i $MP4 -frames:v 1 $SCR/mid/${C}_$P.png
  done
  echo "$C duration=$D"
done
