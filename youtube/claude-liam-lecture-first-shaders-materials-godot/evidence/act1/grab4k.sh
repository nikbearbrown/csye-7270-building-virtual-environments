#!/usr/bin/env bash
# grab4k.sh <ACT> <Class> : render one class at 4K/24fps in a private media dir, save PNG frames at 50 % and 85 % into frames50/ and frames85/, delete the media.
set -u
ACT="$1"; CLS="$2"
REEL=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot
SCR=/private/tmp/claude-501/lecture-a5shaders-act${ACT}
B=/private/tmp/claude-501/b1scratch
python3 $REEL/assemble_scenes.py --out $SCR --acts $ACT >/dev/null
cp $REEL/beat_sheet.json $SCR/
MEDIA=$B/k4/$CLS; rm -rf $MEDIA; mkdir -p $MEDIA $B/frames50 $B/frames85
( cd $SCR && manim -r 3840,2160 --fps 24 --media_dir $MEDIA scenes.py $CLS 2>&1 | grep -E "\[pace\]|Traceback|Error" | sed 's/.*\[pace\]/[pace]/' )
V=$(find $MEDIA -name "$CLS.mp4" | head -1)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
python3 - "$V" "$D" "$CLS" <<'PY'
import sys, subprocess
v, d, c = sys.argv[1], float(sys.argv[2]), sys.argv[3]
B = "/private/tmp/claude-501/b1scratch"
for pct, folder in ((50, "frames50"), (85, "frames85")):
    t = min(d * pct / 100.0, d - 0.05)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", v, "-frames:v", "1", f"{B}/{folder}/{c}.png"], check=True)
print(c, "dur", round(d, 2))
PY
rm -rf $MEDIA
