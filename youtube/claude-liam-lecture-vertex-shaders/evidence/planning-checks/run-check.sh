#!/bin/zsh
# run-check.sh <script.gd> [renderer]  — runs one planning check windowed in the scratch project (Godot 4.7.2), prints the RESULT lines,
# flags any SHADER/SCRIPT error, and writes the raw log (date, machine, exact command, full output, exit code) to logs/<script>.log
# usage:  ./run-check.sh verify1.gd          ./run-check.sh verify1.gd gl_compatibility
# For the capture scenes:  ./run-scene.sh <scene-id> <comma-separated times> [--duration D]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="$HERE/scratch-project"
mkdir -p "$HERE/logs"
[ -d "$PROJ/.godot" ] || godot --headless --path "$PROJ" --import >/dev/null 2>&1
S="$1"; R="${2:-}"
RM=(); [ -n "$R" ] && RM=(--rendering-method "$R")
LOG="$HERE/logs/${S%.gd}${R:+-$R}.log"
{
  echo "# date: $(date '+%Y-%m-%d %H:%M:%S %Z')   machine: Apple M4 Pro, macOS $(sw_vers -productVersion)"
  echo "# command: godot --path scratch-project ${RM[*]:-} --script res://$S"
  timeout 120 godot --path "$PROJ" "${RM[@]}" --script "res://$S" 2>&1
  echo "# exit: $?"
} > "$LOG"
grep -E "^(RESULT|ERROR|SCRIPT ERROR|SHADER ERROR|Parse Error)" "$LOG" | head -${LINES_MAX:-80}
echo "(log: logs/${S%.gd}${R:+-$R}.log)"
