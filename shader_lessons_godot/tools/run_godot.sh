#!/bin/zsh
# run_godot.sh <res://tools/script.gd> <forward_plus|gl_compatibility> <abs log path> [more script args after --]
# Runs one verification script in a real windowed Godot under the series Lab's lock (one windowed Godot at a time on this Mac),
# with a hard timeout. Prints the script's lines and the exit status. Never leaves a Godot behind: `timeout` kills it.
set -u
PROJ="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$1"; RENDERER="$2"; LOGF="$3"; shift 3
LOCK=/private/tmp/claude-501/shaderlab.lock
mkdir -p /private/tmp/claude-501 "$(dirname "$LOGF")"
GOT=0
for i in $(seq 1 3600); do
  if mkdir "$LOCK" 2>/dev/null; then GOT=1; break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
[ "$GOT" = 1 ] || { echo "could not get the Lab lock in 30 minutes"; exit 4; }
( while [ -d "$LOCK" ]; do touch "$LOCK" 2>/dev/null; sleep 20; done ) &
TOUCHER=$!
trap 'kill $TOUCHER 2>/dev/null; rmdir "$LOCK" 2>/dev/null' EXIT
RAW="$(mktemp -t slraw.XXXXXX)"
timeout 240 godot --path "$PROJ" --rendering-method "$RENDERER" --script "$SCRIPT" -- --log "$LOGF" "$@" >"$RAW" 2>&1
CODE=$?
grep -E "^(HEADER|TRAP|CHECK|NOTE|SUMMARY)" "$RAW"
if grep -qE "SHADER ERROR|SCRIPT ERROR|Parse Error|Condition \"|^ERROR:" "$RAW"; then echo "ENGINE_ERRORS (any line starting ERROR: counts; a renamed shader file fails silently otherwise):"; grep -E "SHADER ERROR|SCRIPT ERROR|Parse Error|Condition \"|^ERROR:|^   at:" "$RAW" | head -20; fi
echo "exit $CODE"
cp "$RAW" "${LOGF%.txt}.engine.txt" 2>/dev/null
rm -f "$RAW"
