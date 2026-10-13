#!/bin/zsh
# Runs every shader of the film through the series' Shader Lab (real Godot 4.7.2 window) and writes lab-shaders-check.log:
#   * every file in lab-shaders/ must compile and render (exit 0);
#   * the language checks in shaders/err-*.gdshader must FAIL with the compiler messages the film quotes, shaders/ok-*.gdshader must pass.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)/check_shader.sh"
LOG="$HERE/lab-shaders-check.log"; : > "$LOG"
echo "# $(date '+%Y-%m-%d %H:%M')  Godot $(godot --version 2>/dev/null)  (series Shader Lab, Forward+)" >> "$LOG"
for f in "$FILM"/lab-shaders/*.gdshader; do
  out="$("$LAB" "$f" --kind sprite --sprite-scale 1.0 2>&1)"; code=$?
  lines=$(wc -l < "$f" | tr -d ' ')
  echo "[exit $code] lab-shaders/$(basename "$f")  ($lines lines)" >> "$LOG"
  [ $code -ne 0 ] && echo "$out" | head -5 | sed 's/^/    /' >> "$LOG"
done
echo "" >> "$LOG"; echo "# language checks (expected results in brackets)" >> "$LOG"
for f in "$HERE"/shaders/err-*.gdshader "$HERE"/shaders/ok-*.gdshader; do
  out="$("$LAB" "$f" --kind sprite 2>&1)"; code=$?
  echo "[exit $code] shaders/$(basename "$f")" >> "$LOG"
  echo "$out" | grep -E "SHADER ERROR" | head -2 | sed 's/^/    /' >> "$LOG"
done
cat "$LOG"
