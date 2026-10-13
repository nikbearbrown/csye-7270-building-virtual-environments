#!/bin/zsh
# run-checks.sh: re-run any check of this folder in a real window of Godot 4.7.2, serialised with the Shader Lab's lock.
#   ./run-checks.sh verify1 [forward_plus|gl_compatibility]                    one check script (verify1 ... verify10, smoke_compile, scene_frames)
#   ./run-checks.sh scene scene_c02_window 8 0.2,0.5,0.9 [renderer] [runner args]   one capture scene at fractions of its beat (see scene_runner.gd; --route sub4k or native1080)
#   ./run-checks.sh capture scene_c01_pool 13.6 [renderer] [driver args]       one capture scene frame by frame at a fixed 30 fps tick (see scene_capture.gd);
#                                                                              PNGs go to /private/tmp/claude-501/rts-checks/capture/<scene>/ (add --width 960 --height 540 --frames 8 for a quick test;
#                                                                              add --native --width 1920 --height 1080 for C13, the mip-level blur: see verify10.gd and CAPTURE-PLAN.md, Routes)
# It builds a scratch project from this folder (the .gd files, project.godot and ../../lab-shaders as res://lab-shaders/), runs the check there, prints
# the RESULT / NOTE lines and writes the whole log to ./run-logs/<check>-<renderer>.log. Pictures go to /private/tmp/claude-501/rts-checks/.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
W=/private/tmp/claude-501/rts-checks
mkdir -p "$W/proj/lab-shaders" "$W/shots" "$W/frames" "$HERE/run-logs"
rsync -a --include='*.gd' --include='project.godot' --exclude='*' "$HERE/" "$W/proj/"
rsync -a --delete "$FILM/lab-shaders/" "$W/proj/lab-shaders/"
LOCK=/private/tmp/claude-501/shaderlab.lock
mkdir -p /private/tmp/claude-501
for i in $(seq 1 600); do
  if mkdir "$LOCK" 2>/dev/null; then break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
[ -d "$W/proj/.godot" ] || godot --headless --path "$W/proj" --import >/dev/null 2>&1
if [ "$1" = "capture" ]; then
  S="$2"; D="$3"; R="${4:-forward_plus}"; shift 4 2>/dev/null || shift $#
  LOG="$HERE/run-logs/capture-$S-$R.log"
  { echo "# $(date '+%Y-%m-%d %H:%M:%S') godot --path <scratch project> --rendering-method $R --fixed-fps 30 --script res://scene_capture.gd -- --scene res://$S.gd --duration $D --out $W/capture/$S $*"; } > "$LOG"
  rm -rf "$W/capture/$S"
  timeout 600 godot --path "$W/proj" --rendering-method "$R" --fixed-fps 30 --script res://scene_capture.gd -- --scene "res://$S.gd" --duration "$D" --out "$W/capture/$S" "$@" >> "$LOG" 2>&1
elif [ "$1" = "scene" ]; then
  S="$2"; D="$3"; T="$4"; R="${5:-forward_plus}"; shift 5 2>/dev/null || shift $#
  LOG="$HERE/run-logs/$S-$R.log"
  { echo "# $(date '+%Y-%m-%d %H:%M:%S') godot --path <scratch project> --rendering-method $R --script res://scene_runner.gd -- --scene res://$S.gd --duration $D --utimes $T $*"; } > "$LOG"
  timeout 240 godot --path "$W/proj" --rendering-method "$R" --script res://scene_runner.gd -- --scene "res://$S.gd" --duration "$D" --utimes "$T" --shots "$W/shots" "$@" >> "$LOG" 2>&1
else
  N="$1"; R="${2:-forward_plus}"; shift; [ $# -gt 0 ] && shift
  LOG="$HERE/run-logs/$N-$R.log"
  { echo "# $(date '+%Y-%m-%d %H:%M:%S') godot --path <scratch project> --rendering-method $R --script res://$N.gd -- $*"; } > "$LOG"
  timeout 240 godot --path "$W/proj" --rendering-method "$R" --script "res://$N.gd" -- "$@" >> "$LOG" 2>&1
fi
echo "# exit $?" >> "$LOG"
grep -E "^(RESULT|NOTE|# )" "$LOG" | cut -c1-700
grep -E "ERROR|SCRIPT ERROR|Parse Error" "$LOG" | head -20
