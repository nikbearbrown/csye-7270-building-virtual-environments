#!/bin/zsh
# record_all.sh: records this film's Godot captures (captures.json) as PNG sequences, then MP4s (the one still as a PNG).
# Usage (from anywhere):  record_all.sh [CAPTURE_ID ...]            default: every capture, in order
# Env:  OUT (default /private/tmp/claude-501/ls-capture/out)   WORK (scratch project copy)   MAXFRAMES (smoke test: stop after N frames)
#       PUBLIC (optional: also copy each result into this folder, e.g. <books>/brutalist.art/runtime/remotion/public/godot-shaders)
#       RENDERER (forward_plus is the default; gl_compatibility for the cross-check)   KEEP_FRAMES=1 (keep the PNG sequences)
# It never writes inside the film folder. A capture is offline at a fixed 30 fps tick: it says nothing about real-time frame rate.
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
SHADERS="$FILM/lab-shaders"
CAPS="$HERE/captures.json"
OUT="${OUT:-/private/tmp/claude-501/ls-capture/out}"
WORK="${WORK:-/private/tmp/claude-501/ls-capture/project}"
mkdir -p "$OUT" "$WORK"
cp "$HERE/project.godot" "$HERE/lightlab.gd" "$HERE/light_scene.gd" "$HERE/record_capture.gd" "$WORK/"
IDS=("$@")
if [ ${#IDS[@]} -eq 0 ]; then IDS=($(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1])).keys()))' "$CAPS")); fi
for ID in "${IDS[@]}"; do
  read SECS STILL OUTNAME <<<"$(python3 -c 'import json,sys; c=json.load(open(sys.argv[1]))[sys.argv[2]]; print(c["seconds"], int(bool(c.get("still"))), c.get("out", sys.argv[2] + ".mp4"))' "$CAPS" "$ID")"
  FRAMES=$(python3 -c 'import math,sys; print(int(math.ceil(float(sys.argv[1]) * 30)))' "$SECS")
  [ -n "${MAXFRAMES:-}" ] && FRAMES=$MAXFRAMES
  rm -rf "$OUT/$ID"; mkdir -p "$OUT/$ID"
  RM=(); [ -n "${RENDERER:-}" ] && RM=(--rendering-method "$RENDERER")
  godot --path "$WORK" "${RM[@]}" --fixed-fps 30 --script res://record_capture.gd -- "$ID" "$FRAMES" "$OUT/$ID" "$SHADERS" "$CAPS" | grep RESULT
  if [ "$STILL" = "1" ]; then
    STILLFRAME="$OUT/$ID/$ID-00014.png"                       # frame 14 = t of 0.5 s
    [ -f "$STILLFRAME" ] || STILLFRAME="$(ls "$OUT/$ID"/*.png | tail -1)"
    cp "$STILLFRAME" "$OUT/$OUTNAME"
  else
    ffmpeg -y -loglevel error -framerate 30 -i "$OUT/$ID/$ID-%05d.png" -c:v libx264 -pix_fmt yuv420p -crf 14 "$OUT/$OUTNAME"
  fi
  [ "${KEEP_FRAMES:-0}" = "1" ] || rm -rf "$OUT/$ID"
  if [ -n "${PUBLIC:-}" ]; then mkdir -p "$PUBLIC"; cp "$OUT/$OUTNAME" "$PUBLIC/"; fi
  echo "[$ID] done"
done
