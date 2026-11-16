#!/usr/bin/env bash
# run4k.sh <ACT> <Class> <BEAT_ID> [pct ...] : assemble, render ONE class at 4K (24 fps) into a private scratch media dir, run GATE T functions on 50/85 % (or given) frames, then delete the media.
set -u
ACT="$1"; CLS="$2"; BID="$3"; shift 3
REEL=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot
SCR=/private/tmp/claude-501/lecture-a5shaders-act${ACT}
python3 $REEL/assemble_scenes.py --out $SCR --acts $ACT >/dev/null
cp $REEL/beat_sheet.json $SCR/
MEDIA=/private/tmp/claude-501/b1scratch/k4/$CLS
rm -rf $MEDIA; mkdir -p $MEDIA
( cd $SCR && manim -r 3840,2160 --fps 24 --media_dir $MEDIA scenes.py $CLS 2>&1 | grep -E "\[pace\]|Traceback|Error" | sed 's/.*\[pace\]/[pace]/' )
V=$(find $MEDIA -name "$CLS.mp4" | head -1)
echo "video: $V"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$V"
python3 /private/tmp/claude-501/b1scratch/gate_t_frame.py "$V" $BID $CLS $SCR "$@" 2>&1 | grep -v SoX
mkdir -p /private/tmp/claude-501/b1scratch/frames
for p in "$@"; do :; done
rm -rf $MEDIA
