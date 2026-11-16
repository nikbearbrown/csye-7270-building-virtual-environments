#!/usr/bin/env bash
# render4k.sh <Class> [extra pct...] : renders one class at 3840x2160/24 into a scratch media dir, runs the toolkit's GATE T functions + Gate V on its 50%/85% frames (+ any extra percentages), then deletes the media.
# Run `REEL/preflight.sh 4 <Class>` first: it assembles kit.py + scenes_act4.py into the scratch scenes.py this script renders. Needs manim 0.20.1, ffmpeg, PIL, numpy, scipy.
HERE="$(cd "$(dirname "$0")" && pwd)"
C="$1"; shift
BID="${C%%_*}"
SCR=/private/tmp/claude-501/lecture-a5shaders-act4
M=/private/tmp/claude-501/lecture-a5shaders-act4-4k/$C
rm -rf "$M"
cd "$SCR" && manim -qk --fps 24 -r 3840,2160 --media_dir "$M" scenes.py "$C" 2>&1 | grep -E "\[pace\]|Traceback|Error" | sed 's/.*\[pace\]/[pace]/'
V=$(find "$M" -name "$C.mp4" | head -1)
if [ -z "$V" ]; then echo "NO VIDEO for $C"; exit 1; fi
ls -la "$V" | awk '{print "mp4 bytes", $5}'
python3 "$HERE/gate_t.py" "$V" "$BID" "$@" 2>&1 | grep -v -i sox
rm -rf "$M"
