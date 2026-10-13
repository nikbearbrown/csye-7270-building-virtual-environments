#!/bin/zsh
# Saves the engine's FULL log for every expected-to-fail shader (and for two clean ones, to show a clean run prints no warning).
# The Lab's check_shader.sh prints only the "SHADER ERROR" line; the full log also shows the source lines around the error with the
# offending line marked, which is what the film puts on screen (verbatim). Uses a throwaway copy of the Lab project so it does not
# touch the shared Lab or its lock. Output: logs/<shader>.log (first line: the command, second: the date).
# Machine: Apple M4 Pro, Godot 4.7.2, Forward+.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/logs"; mkdir -p "$OUT"
TMP="$(mktemp -d /private/tmp/claude-501/lab-copy.XXXXXX)"
cp "$LAB/project.godot" "$LAB/runner.gd" "$TMP/"
(cd "$TMP" && timeout 120 godot --headless --path . --import >/dev/null 2>&1)
for f in "$SH"/*-err-*.gdshader "$SH/19-float-equals.gdshader" "$SH/05-pastel.gdshader"; do
  b="$(basename "$f" .gdshader)"
  {
    echo "# command: godot --path <copy of lab/> --script res://runner.gd -- --shader lab-shaders/$(basename "$f") --kind rect"
    echo "# date: $(date '+%Y-%m-%d %H:%M:%S')"
    (cd "$TMP" && timeout 60 godot --path . --script res://runner.gd -- --shader "$f" --kind rect 2>&1)
  } > "$OUT/$b.log"
  echo "$b: $(grep -c 'SHADER ERROR' "$OUT/$b.log") shader error line(s), $(grep -ci 'warning' "$OUT/$b.log") warning line(s)"
done
rm -rf "$TMP"
