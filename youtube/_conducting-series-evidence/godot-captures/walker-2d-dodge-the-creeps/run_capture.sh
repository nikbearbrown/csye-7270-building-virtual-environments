#!/bin/zsh
# Generic Walker capture: scratch copy -> autoload driver -> windowed Movie Maker run -> PNG shots + H.264 clip.
# usage: run_capture.sh <name> <plan.json> <clip_start_frame> <clip_frames> [res://scene.tscn]
# The SOURCE project (books/<name>/godot) is only READ (rsync). All edits happen in the scratch copy.
set -eu
NAME=$1; PLAN=$2; CLIP_START=$3; CLIP_FRAMES=$4; SCENE=${5:-}
WIN_W=${WIN_W:-1920}; WIN_H=${WIN_H:-1080}   # window = Movie Maker size; set to the game aspect for non-16:9 games
SRC=/Users/bear/Documents/CoWork/bear-textbooks/books/$NAME/godot
WORK=/private/tmp/claude-501/capture-work/$NAME
COPY=$WORK/godot
OUT="/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/$NAME"
SHARED=/private/tmp/claude-501/capture-work/_shared
GODOT=/opt/homebrew/bin/godot
mkdir -p "$WORK" "$OUT"
rm -f "$OUT"/*.png "$OUT"/*.mp4(N)
printf '#!/bin/zsh\n# Exact command used for this capture (generic runner + this plan):\nWIN_W=%s WIN_H=%s /private/tmp/claude-501/capture-work/_shared/run_capture.sh %s %s %s %s %s\n# copies of run_capture.sh, capture_driver.gd and plan.json sit beside this file\n' $WIN_W $WIN_H $NAME $PLAN $CLIP_START $CLIP_FRAMES "$SCENE" > "$OUT/capture.sh"

# 1) fresh scratch copy (no .godot / evidence / youtube)
rm -rf "$COPY"
rsync -a --exclude .godot --exclude evidence --exclude youtube "$SRC/" "$COPY/"

# 2) copy-only edits: capture driver autoload + 1920x1080 window so Movie Maker records 1080p
mkdir -p "$COPY/_capture"
cp "$SHARED/capture_driver.gd" "$COPY/_capture/capture_driver.gd"
/usr/bin/python3 -I - "$COPY/project.godot" $WIN_W $WIN_H <<'PY'
import re, sys
p = sys.argv[1]; s = open(p).read()
s = re.sub(r'^window/size/window_(width|height)_override=.*\n', '', s, flags=re.M)
add = 'window/size/window_width_override=%s\nwindow/size/window_height_override=%s\n' % (sys.argv[2], sys.argv[3])
if re.search(r'^\[display\]\n', s, flags=re.M):
    s = re.sub(r'^\[display\]\n', '[display]\n\n' + add, s, count=1, flags=re.M)
else:
    s += '\n[display]\n\n' + add
line = 'CaptureDriver="*res://_capture/capture_driver.gd"\n'
if re.search(r'^\[autoload\]\n', s, flags=re.M):
    s = re.sub(r'^\[autoload\]\n', '[autoload]\n\n' + line, s, count=1, flags=re.M)
else:
    s += '\n[autoload]\n\n' + line
open(p, 'w').write(s)
PY

# 3) import once (output goes to the copy's .godot)
$GODOT --headless --path "$COPY" --import > "$WORK/import.log" 2>&1 || true

# 4) windowed Movie Maker run, fixed 30 fps, always-on-top (an occluded window stops drawing)
rm -rf "$WORK/frames"; mkdir -p "$WORK/frames"
cp "$PLAN" "$OUT/plan.json"
$GODOT --path "$COPY" --write-movie "$WORK/frames/f.png" --fixed-fps 30 --resolution ${WIN_W}x${WIN_H} --always-on-top \
  $SCENE -- --plan="$PLAN" --out="$OUT" > "$OUT/raw-log.txt" 2>&1 || echo "GODOT EXIT $?" >> "$OUT/raw-log.txt"
pkill -f "$COPY" 2>/dev/null || true

# 5) H.264 1080p 30 fps clip
# Game audio recorded by Movie Maker (f.wav) is muxed in, cut to the same window, unless AUDIO=0.
AUDIO_ARGS=(-an)
if [[ "${AUDIO:-1}" == "1" && -f "$WORK/frames/f.wav" ]]; then
  AUDIO_ARGS=(-ss $(( CLIP_START / 30.0 )) -t $(( CLIP_FRAMES / 30.0 )) -i "$WORK/frames/f.wav" -map 0:v -map 1:a -c:a aac -b:a 192k -shortest)
fi
ffmpeg -y -loglevel error -framerate 30 -start_number $CLIP_START -i "$WORK/frames/f%08d.png" "${AUDIO_ARGS[@]}" -frames:v $CLIP_FRAMES \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -pix_fmt yuv420p -crf 16 -preset slow -r 30 "$OUT/$NAME-clip.mp4"
ffmpeg -hide_banner -i "$OUT/$NAME-clip.mp4" -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume" | sed 's/^/AUDIO /' >> "$OUT/raw-log.txt" || true
ffmpeg -y -loglevel error -i "$OUT/$NAME-clip.mp4" -vf "fps=1,scale=640:-1,tile=4x2" -frames:v 1 "$OUT/contact-sheet-clip.png"

# 6) sanity: distinct movie frames (frozen frames = window was not drawing)
echo "DISTINCT frames: $(md5 -q "$WORK"/frames/*.png | sort -u | wc -l) of $(ls "$WORK"/frames/*.png | wc -l)" | tee -a "$OUT/raw-log.txt"
cp "$SHARED/capture_driver.gd" "$SHARED/run_capture.sh" "$OUT/"
grep -E "SHOT|INPUT|CALL|ERROR|SCRIPT ERROR|frames at|recording movie" "$OUT/raw-log.txt" | head -60
