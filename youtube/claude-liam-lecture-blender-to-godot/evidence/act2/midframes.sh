#!/usr/bin/env bash
# midframes.sh <Class> [pcts...]  — render a scene at 480p15 from the preflight scratch (/private/tmp/claude-501/lecture-blender-act2) and
# write a contact sheet of frames at the given percentages (default 15 30 50 70 95) to <scratch>/sheets/<Class>.png. Look at it.
set -u
C="$1"; shift
PCTS="${*:-15 30 50 70 95}"
SCR=/private/tmp/claude-501/lecture-blender-act2
cd "$SCR" || exit 1
mkdir -p sheets frames
manim -ql --media_dir "$SCR/media_mp4" scenes.py "$C" 2>&1 | grep -E "\[pace\]|Traceback|Error" | sed 's/.*\[pace\]/[pace]/'
MP4=$(ls -t media_mp4/videos/scenes/480p15/${C}.mp4 2>/dev/null | head -1)
[ -z "$MP4" ] && { echo "no mp4"; exit 1; }
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MP4")
echo "clip $DUR s"
rm -f frames/${C}_*.png
i=0
for p in $PCTS; do
  t=$(python3 -c "print(max(0.0, min($DUR-0.05, $DUR*$p/100.0)))")
  ffmpeg -v error -y -ss "$t" -i "$MP4" -frames:v 1 "frames/${C}_$(printf %02d $i)_p${p}.png"
  i=$((i+1))
done
python3 - <<PY
from PIL import Image, ImageDraw
import glob
fs = sorted(glob.glob("frames/${C}_*.png"))
ims = [Image.open(f) for f in fs]
w, h = ims[0].size
cols = 2
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, h * rows), "white")
for k, (f, im) in enumerate(zip(fs, ims)):
    sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    ImageDraw.Draw(sheet).text(((k % cols) * w + 8, (k // cols) * h + 6), f.split("_p")[-1][:-4] + "%", fill=(200, 0, 0))
sheet.save("sheets/${C}.png")
print("sheet: $SCR/sheets/${C}.png")
PY
