#!/usr/bin/env bash
# gate4k.sh <ClassName> [fps]   — renders ONE Manim class of the Act IX scratch assembly at 4K (3840x2160), cuts its 50% and 85% frames, runs the toolkit's
# GATE T pixel checks + GATE V on them (evidence/act9/gate_frames.py), then DELETES the scratch media (disk is tight).
# Needs the scratch assembly first:  ./preflight.sh 9 <Class>   (writes /private/tmp/claude-501/lecture-a5shaders-act9/scenes.py)
# The frames are kept in /private/tmp/claude-501/a9-4k-frames/<Class>_{50,85}.png so they can be looked at.
set -u
CLS="$1"; FPS="${2:-8}"
HERE="$(cd "$(dirname "$0")/../.." && pwd)"
SCR=/private/tmp/claude-501/lecture-a5shaders-act9
MED=/private/tmp/claude-501/a9-4k-media
OUT=/private/tmp/claude-501/a9-4k-frames
mkdir -p "$OUT"; rm -rf "$MED"
( cd "$SCR" && manim -qk --fps "$FPS" --media_dir "$MED" scenes.py "$CLS" 2>&1 | grep -E "\[pace\]|Traceback|Error" | sed 's/.*\[pace\]/[pace]/' )
V=$(find "$MED" -name "${CLS}.mp4" | head -1)
if [ -z "$V" ]; then echo "NO VIDEO for $CLS"; exit 1; fi
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
echo "$CLS duration $DUR s ($(du -h "$V" | cut -f1))"
for P in 44 47 50 53 56 85; do
  T=$(python3 -c "print(float('$DUR')*$P/100)")
  ffmpeg -y -loglevel error -ss "$T" -i "$V" -frames:v 1 "$OUT/${CLS}_${P}.png"
done
python3 "$HERE/evidence/act9/gate_frames.py" "$OUT/${CLS}_50.png" "$OUT/${CLS}_85.png" 2>&1 | grep -v "SoX\|sox"
# robustness: GATE T rows only, on frames just either side of the midpoint (the gate samples exactly 50%, but codec noise moves borderline-ink pixels between frames)
echo "-- GATE T around the midpoint (44/47/53/56%): FAIL rows only"
python3 "$HERE/evidence/act9/gate_frames.py" "$OUT/${CLS}_44.png" "$OUT/${CLS}_47.png" "$OUT/${CLS}_53.png" "$OUT/${CLS}_56.png" 2>&1 | grep -E "^==|FAIL" | grep -B1 "FAIL" | grep -v "^--" | sed 's#/private/tmp/claude-501/a9-4k-frames/##'
echo "-- (end)"
rm -rf "$MED"
