#!/usr/bin/env bash
# gate4k.sh ACT CLASS [CLASS...]  — render each class at 3840x2160 (fps 10, stills only matter), cut frames at 50% / 85% / 95%, run the toolkit's GATE T checks, delete the scratch media.
ACT="$1"; shift
SCR="/private/tmp/claude-501/lecture-a5shaders-act${ACT}"
W=/private/tmp/claude-501/b5work; mkdir -p "$W"
for C in "$@"; do
  M="$W/media4k_$C"; rm -rf "$M"; mkdir -p "$M"
  (cd "$SCR" && manim -r 3840,2160 --fps 10 --media_dir "$M" scenes.py "$C" 2>&1 | grep -E "\[pace\]|Traceback|rror" | head -3)
  V=$(find "$M" -name "$C.mp4" | head -1)
  if [ -z "$V" ]; then echo "$C: no video"; continue; fi
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
  for F in 0.50 0.85 0.95; do
    T=$(python3 -c "print(float('$D')*$F)")
    ffmpeg -y -loglevel error -ss "$T" -i "$V" -frames:v 1 "$W/${C}_f${F}.png"
    echo "--- $C @ $F (t=$T of $D)"
    python3 "$W/gate_t_frame.py" "$W/${C}_f${F}.png" "$C" | tail -9
  done
  rm -rf "$M"
done
