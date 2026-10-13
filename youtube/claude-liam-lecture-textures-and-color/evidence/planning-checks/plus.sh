#!/bin/zsh
# plus.sh <shader.gdshader> [--renderer R] [runner_plus options]  : like the Lab's check_shader.sh, for the film's planning checks (runner_plus.gd).
# Shares the Lab's lock so two Godot windows never open at once. Prints the RESULT line; prints compiler errors and exits 1 on a shader error.
set -u
PROJ="${PLUS_PROJECT:-/private/tmp/claude-501/godot-shaders-textures-and-color/scratch-proj}"   # a folder holding project.godot + runner_plus.gd (copies are in this folder)
SHADER="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; shift
RENDERER=""; ARGS=()
while [ $# -gt 0 ]; do
  if [ "$1" = "--renderer" ]; then RENDERER="$2"; shift 2
  elif [ "$1" = "--png" ]; then mkdir -p "$(dirname "$2")"; ARGS+=("--png" "$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"); shift 2
  else ARGS+=("$1"); shift; fi
done
LOCK=/private/tmp/claude-501/shaderlab.lock
for i in $(seq 1 360); do
  if mkdir "$LOCK" 2>/dev/null; then break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
LOG="$(mktemp -t plus.XXXXXX)"
RM=(); [ -n "$RENDERER" ] && RM=(--rendering-method "$RENDERER")
timeout 90 godot --path "$PROJ" "${RM[@]}" --script res://runner_plus.gd -- --shader "$SHADER" "${ARGS[@]}" >"$LOG" 2>&1
CODE=$?
grep -E "^RESULT " "$LOG"
if grep -qE "SHADER ERROR|Parse Error|SCRIPT ERROR|Condition \"" "$LOG"; then
  echo "SHADER_OR_SCRIPT_ERROR:"; grep -E "SHADER ERROR|Parse Error|SCRIPT ERROR|Condition \"|ERROR:" "$LOG" | head -12; rm -f "$LOG"; exit 1
fi
if ! grep -q "^RESULT " "$LOG"; then echo "NO RESULT (engine exit $CODE). Last log lines:"; tail -8 "$LOG"; rm -f "$LOG"; exit 3; fi
rm -f "$LOG"; exit 0
