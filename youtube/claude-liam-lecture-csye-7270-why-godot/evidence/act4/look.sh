#!/usr/bin/env bash
# look.sh <Class> ... — low-res render of each Act IV class (after REEL/preflight.sh 4 assembled the scratch), then stills at 25/50/85/100% of the clip
# into /private/tmp/claude-501/lecture-csye-godot-act4/looks/<Class>_<pct>.png and a contact sheet <Class>_sheet.png
SCR=/private/tmp/claude-501/lecture-csye-godot-act4
mkdir -p "$SCR/looks"
for C in "$@"; do
  (cd "$SCR" && manim -ql --media_dir "$SCR/media" scenes.py "$C" >/dev/null 2>&1)
  MP4="$SCR/media/videos/scenes/480p15/$C.mp4"
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MP4")
  for P in 12 25 50 70 85 98; do
    T=$(python3 -c "print(round($D*$P/100,3))")
    ffmpeg -v error -y -ss "$T" -i "$MP4" -frames:v 1 "$SCR/looks/${C}_${P}.png"
  done
  ffmpeg -v error -y -i "$SCR/looks/${C}_12.png" -i "$SCR/looks/${C}_25.png" -i "$SCR/looks/${C}_50.png" -i "$SCR/looks/${C}_70.png" -i "$SCR/looks/${C}_85.png" -i "$SCR/looks/${C}_98.png" \
    -filter_complex "[0][1][2]hstack=3[a];[3][4][5]hstack=3[b];[a][b]vstack=2" "$SCR/looks/${C}_sheet.png"
  echo "$C  clip=${D}s  $SCR/looks/${C}_sheet.png"
done
