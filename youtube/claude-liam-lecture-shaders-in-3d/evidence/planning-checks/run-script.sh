#!/bin/zsh
# run-script.sh <script.gd> <log name> [extra godot args, e.g. --rendering-method gl_compatibility]
# Copies project.godot and every verify*.gd into a scratch Godot project (never into a game), runs the script in a real window,
# and writes <log name> next to this file with a header: date, the exact command line, the engine line, then the raw output.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$1"; LOGNAME="$2"; shift 2
PROJ=/private/tmp/claude-501/godot-shaders-shaders-in-3d/checks-project
mkdir -p "$PROJ"
cp "$HERE/project.godot" "$PROJ/"
cp "$HERE"/verify*.gd "$PROJ/" 2>/dev/null
# the GDScript snippets in the film load "res://pad.gdshader": give the scratch project the film's copy of the pad shader under that name
cp "$HERE/../../lab-shaders/12-signal-pad.gdshader" "$PROJ/pad.gdshader"
LOG="$HERE/$LOGNAME"
{
  echo "# date: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "# machine: $(sysctl -n machdep.cpu.brand_string 2>/dev/null), $(uname -sr)"
  echo "# command: godot --path <scratch project> $* --script res://$SCRIPT"
  echo "# ---- raw output follows ----"
} > "$LOG"
timeout 120 godot --path "$PROJ" "$@" --script "res://$SCRIPT" >> "$LOG" 2>&1
echo "exit $?" >> "$LOG"
grep -E "^RESULT|ERROR|exit" "$LOG" | cut -c1-400
