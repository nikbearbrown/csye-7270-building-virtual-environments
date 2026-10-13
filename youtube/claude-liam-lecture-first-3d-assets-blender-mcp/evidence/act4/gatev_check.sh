#!/usr/bin/env zsh
# gatev_check.sh <Class> ... — 1080p24 render of act-4 scenes from the preflight scratch (run REEL/preflight.sh 4 <Classes> first),
# frames at 50 % and 85 % of each clip (where Gate V samples a beat), then the REAL Gate V code in test mode
# (TK/runtime/qc/final_frame_check.py --frames-dir) and the GATE T approximation (evidence/act4/gate_t_probe.py, frames upscaled to 4K).
# One render at a time; never 4K.
HERE=${0:A:h}
SCR=/private/tmp/claude-501/lecture-a3assets-act4
QC=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc
OUT=$SCR/gatev; rm -rf $OUT; mkdir -p $OUT
for C in "$@"; do
  (cd $SCR && manim -r 1920,1080 --fps 24 --media_dir $SCR/media_1080 scenes.py $C >/dev/null 2>&1)
  MP4=$SCR/media_1080/videos/scenes/1080p24/$C.mp4
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $MP4)
  for P in 50 85; do
    T=$(python3 -c "print($D*$P/100)")
    ffmpeg -v error -y -ss $T -i $MP4 -frames:v 1 $OUT/${C}_$P.png
  done
  echo "$C clip=${D}s"
done
python3 $QC/final_frame_check.py --frames-dir $OUT 2>&1 | tail -40
python3 $HERE/gate_t_probe.py $OUT/*_50.png 2>&1 | grep -v "^   PASS"
