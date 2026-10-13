#!/bin/zsh
# capture_scene.sh <capture id, e.g. C08> <output.mp4> [scratch project dir] [--length SECONDS] [--limit N]
# Renders ONE capture of capture_scenes.gd to a 3840 x 2160, 30 fps MP4, in a FRESH Godot process (rect-mode results depend on history).
# Offline fixed tick rate: it says nothing about real-time frame rate.
# Route (CAPTURE-PLAN.md, "Which route each capture uses"):
#   every capture except C08: the 4K route, a 3840 x 2160 SubViewport over the 1280 x 720 canvas (size_2d_override + stretch, scale 3).
#       These shaders read SCREEN_UV (a fraction of the screen), so the route cannot change what they show (run-14: 65 probes, all equal).
#   C08 (the Rect-mode trap): the 1:1 route. A BackBufferCopy's Rect box is measured in RENDER PIXELS (run-13: its default box is 101 px of the
#       render target, which is only 34 canvas units on the 4K route), so C08 is rendered into the 1280 x 720 window itself, where the
#       default box is the 100 px corner a game window gives, and the frames are then enlarged 3x by whole pixels (nearest neighbour:
#       no blur, the scene is flat colour). Same fresh-process rule.
# --length SECONDS  record the clip at that length (the build passes the beat's measured audio length, audio first): every scripted
#                   event keeps its place as a fraction of the clip. Without it the scene's planned length is used (CAPTURE-PLAN.md).
# --limit N         stop after N frames (a short test).
# Frames go to ${FRAMES_DIR:-${TMPDIR:-/private/tmp}/reflections-capture-frames}/<output name>.frames/ (never next to the MP4: the output folder is the
# Remotion public folder and Remotion bundles all of it). They are KEPT so you can look at them; delete that folder yourself afterwards.
# Needs godot 4.7.2 and ffmpeg on PATH. Writes only <output.mp4>, the frames folder above and the scratch project (scripts are copied there).
set -eu
CID="${1:?capture id (C01 ... C19)}"; OUT="${2:?output mp4}"; PROJ="${3:-${TMPDIR:-/private/tmp}/reflections-capture-project}"
EXTRA=()
[ $# -gt 3 ] && EXTRA=("${@:4}")
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$PROJ" "$(dirname "$OUT")"
[ -f "$PROJ/project.godot" ] || cp "$HERE/project.godot" "$PROJ/project.godot"
cp "$HERE"/*.gd "$PROJ/"
FRAMES="${FRAMES_DIR:-${TMPDIR:-/private/tmp}/reflections-capture-frames}/$(basename "$OUT").frames"
mkdir -p "$FRAMES"
if [ "$CID" = "C08" ]; then
  ROUTE=(--route direct --scale 1); VF="scale=3840:2160:flags=neighbor"
else
  ROUTE=(--route sv --scale 3 --full); VF="null"
fi
godot --path "$PROJ" --script res://scene_runner.gd -- --capture "$CID" "${ROUTE[@]}" --all-frames "$FRAMES" "${EXTRA[@]}" 2>&1 | grep "RESULT" | tail -3
ffmpeg -y -loglevel error -framerate 30 -i "$FRAMES/f%05d.png" -vf "$VF" -c:v libx264 -pix_fmt yuv420p -crf 12 -preset medium "$OUT"
echo "wrote $OUT (frames kept in $FRAMES)"
