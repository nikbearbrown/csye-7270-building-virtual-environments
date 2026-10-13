#!/usr/bin/env bash
# midframes.sh <Class> <t1> <t2> ... — low-res full render of one Act V class from preflight's scratch + frames at the given seconds,
# and the clip length against the audio.  (run ./preflight.sh 5 <Class> first)  frames -> /private/tmp/claude-501/lecture-csye-games-act5-frames/
SCR=/private/tmp/claude-501/lecture-csye-games-act5; C="$1"; shift
FR=/private/tmp/claude-501/lecture-csye-games-act5-frames; mkdir -p "$FR"
(cd "$SCR" && rm -rf media/videos && manim -ql --fps 24 --disable_caching --media_dir "$SCR/media" scenes.py "$C" 2>&1 | grep -E "\[pace\]|Traceback|Error" | sed 's/.*\[pace\]/[pace]/')
V=$(ls "$SCR"/media/videos/scenes/480p24/$C.mp4); ffprobe -v error -show_entries format=duration -of csv=p=0 "$V"
for t in "$@"; do ffmpeg -v error -y -ss "$t" -i "$V" -frames:v 1 "$FR/${C}_$t.png"; done
