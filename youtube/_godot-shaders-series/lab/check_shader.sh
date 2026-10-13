#!/bin/zsh
# check_shader.sh <shader.gdshader> [runner options]   (see runner.gd for the options)
# Renders the shader in a real Godot window, prints one RESULT line, exits 1 on any shader error.
# Extra option handled here: --renderer forward_plus | mobile | gl_compatibility  (default: Godot's default for a new project, forward_plus).
# The RESULT line reports the renderer that actually ran. The same shader can read different pixels in different renderers.
# Example:
#   check_shader.sh /abs/path/red.gdshader --kind rect --probe 0.5,0.5 --png /abs/out/red.png
#   check_shader.sh /abs/path/pad.gdshader --kind quad3d --set activation=0.5 --probe 0.22,0.5
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"
SHADER="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; shift
RENDERER=""
ARGS=()
while [ $# -gt 0 ]; do
  if [ "$1" = "--renderer" ]; then RENDERER="$2"; shift 2
  elif [ "$1" = "--png" ]; then mkdir -p "$(dirname "$2")"; ARGS+=("--png" "$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"); shift 2
  else ARGS+=("$1"); shift; fi
done
[ -f "$SHADER" ] || { echo "RESULT {\"ok\":false,\"error\":\"no such shader $SHADER\"}"; exit 2; }
# One Lab run at a time (many writers share this project's cache). Waits up to 30 minutes and NEVER runs without the lock;
# a lock directory older than 3 minutes is stale (a run takes seconds) and is cleared.
LOCK=/private/tmp/claude-501/shaderlab.lock
mkdir -p /private/tmp/claude-501
GOT=0
for i in $(seq 1 3600); do
  if mkdir "$LOCK" 2>/dev/null; then GOT=1; break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
[ "$GOT" = 1 ] || { echo "RESULT {\"ok\":false,\"error\":\"could not get the Lab lock in 30 minutes\"}"; exit 4; }
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
LOG="$(mktemp -t shaderlab.XXXXXX)"
[ -d "$LAB/.godot" ] || godot --headless --path "$LAB" --import >/dev/null 2>&1
RM=(); [ -n "$RENDERER" ] && RM=(--rendering-method "$RENDERER")
timeout 60 godot --path "$LAB" "${RM[@]}" --script res://runner.gd -- --shader "$SHADER" "${ARGS[@]}" >"$LOG" 2>&1
CODE=$?
grep -E "^RESULT " "$LOG"
if grep -qE "SHADER ERROR|Parse Error|SCRIPT ERROR|Condition \"" "$LOG"; then
  echo "SHADER_OR_SCRIPT_ERROR:"; grep -E "SHADER ERROR|Parse Error|SCRIPT ERROR|Condition \"|ERROR:" "$LOG" | head -12
  rm -f "$LOG"; exit 1
fi
if ! grep -q "^RESULT " "$LOG"; then echo "NO RESULT (engine exit $CODE). Last log lines:"; tail -8 "$LOG"; rm -f "$LOG"; exit 3; fi
rm -f "$LOG"; exit 0
