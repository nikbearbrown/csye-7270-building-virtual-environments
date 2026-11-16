#!/bin/zsh
# capture_shader.sh [options of capture.gd] --name NAME --dest DIR [--renderer R] [--keep-frames]
# Renders a capture with lab/capture.gd under the shared Lab lock (one run at a time), then encodes frames to MP4 (30 fps, h264 crf 14, yuv420p)
# or, with --png, writes one still. Output file: DIR/NAME.mp4 (or DIR/NAME.png). Frames go to a scratch folder and are deleted unless --keep-frames.
# Prints the harness RESULT line. Offline fixed tick rate: Godot runs with --fixed-fps FPS; this proves nothing about real-time frame rate.
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"
NAME=""; DEST=""; RENDERER=""; KEEP=0; FPS=30; PNG=""
ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --name) NAME="$2"; shift 2;;
    --dest) DEST="$2"; shift 2;;
    --renderer) RENDERER="$2"; shift 2;;
    --keep-frames) KEEP=1; shift;;
    --fps) FPS="$2"; ARGS+=("--fps" "$2"); shift 2;;
    --png) PNG="$2"; shift 2;;
    *) ARGS+=("$1"); shift;;
  esac
done
[ -n "$NAME" ] && [ -n "$DEST" ] || { echo "RESULT {\"ok\":false,\"error\":\"need --name and --dest\"}"; exit 2; }
mkdir -p "$DEST"
SCR="/private/tmp/claude-501/capture-frames/$NAME"
rm -rf "$SCR"; mkdir -p "$SCR"
LOCK=/private/tmp/claude-501/shaderlab.lock
mkdir -p /private/tmp/claude-501
GOT=0
for i in $(seq 1 3600); do
  if mkdir "$LOCK" 2>/dev/null; then GOT=1; break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
[ "$GOT" = 1 ] || { echo "RESULT {\"ok\":false,\"error\":\"could not get the Lab lock in 30 minutes\"}"; exit 4; }
# keep the lock fresh: a capture can outlast the 3-minute stale rule
( while [ -d "$LOCK" ]; do touch "$LOCK" 2>/dev/null; sleep 20; done ) &
TOUCHER=$!
trap 'kill $TOUCHER 2>/dev/null; rmdir "$LOCK" 2>/dev/null' EXIT
LOG="$SCR/godot.log"
[ -d "$LAB/.godot" ] || godot --headless --path "$LAB" --import >/dev/null 2>&1
RM=(); [ -n "$RENDERER" ] && RM=(--rendering-method "$RENDERER")
if [ -n "$PNG" ]; then
  timeout 300 godot --path "$LAB" "${RM[@]}" --fixed-fps $FPS --disable-vsync --script res://capture.gd -- "${ARGS[@]}" --png "$DEST/$NAME.png" >"$LOG" 2>&1
else
  timeout 900 godot --path "$LAB" "${RM[@]}" --fixed-fps $FPS --disable-vsync --script res://capture.gd -- "${ARGS[@]}" --out "$SCR/frames" >"$LOG" 2>&1
fi
CODE=$?
grep -E "^RESULT " "$LOG"
if grep -qE "SHADER ERROR|Parse Error|SCRIPT ERROR|Condition \"" "$LOG"; then
  echo "SHADER_OR_SCRIPT_ERROR:"; grep -E "SHADER ERROR|Parse Error|SCRIPT ERROR|Condition \"|ERROR:" "$LOG" | head -12; exit 1
fi
if ! grep -q "^RESULT " "$LOG"; then echo "NO RESULT (engine exit $CODE). Last log lines:"; tail -8 "$LOG"; exit 3; fi
if [ -z "$PNG" ]; then
  ffmpeg -y -loglevel error -framerate $FPS -i "$SCR/frames/frame_%05d.png" -c:v libx264 -preset medium -crf 14 -pix_fmt yuv420p -movflags +faststart "$DEST/$NAME.mp4" || { echo "FFMPEG FAILED"; exit 5; }
  echo "WROTE $DEST/$NAME.mp4"
else
  echo "WROTE $DEST/$NAME.png"
fi
[ "$KEEP" = 1 ] || rm -rf "$SCR/frames"
exit 0
