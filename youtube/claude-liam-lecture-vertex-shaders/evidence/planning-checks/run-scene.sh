#!/bin/zsh
# run-scene.sh <scene-id> <comma-separated times> [--duration D] [--out DIR]
# Runs one capture scene of scratch-project/capture_scenes.gd (real time, planning evidence) and saves frames at the given times to png/scene-<id>-t<time>.png.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="$HERE/scratch-project"
mkdir -p "$HERE/logs"
[ -d "$PROJ/.godot" ] || godot --headless --path "$PROJ" --import >/dev/null 2>&1
SCENE="$1"; TIMES="$2"; shift 2
LOG="$HERE/logs/scene-$SCENE.log"
{
  echo "# date: $(date '+%Y-%m-%d %H:%M:%S %Z')   machine: Apple M4 Pro, macOS $(sw_vers -productVersion)"
  echo "# command: godot --path scratch-project --script res://scene_frames.gd -- --scene $SCENE --times $TIMES $*"
  timeout 120 godot --path "$PROJ" --script res://scene_frames.gd -- --scene "$SCENE" --times "$TIMES" "$@" 2>&1
  echo "# exit: $?"
} > "$LOG"
grep -E "^(RESULT|ERROR|SCRIPT ERROR|SHADER ERROR|Parse Error)" "$LOG" | head -40
