#!/bin/zsh
# Run 17 (2026-10-13): step(edge, x) at and just below the edge: "below it, zero; at or above it, one". Output: run-17-step-equality.log
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PLUS="$HERE/plus.sh"; SH="$HERE/scratch-shaders"
OUT="$HERE/run-17-step-equality.log"; : > "$OUT"
for v in 0.49 0.4999 0.5 0.5001 0.51; do
  echo "## step(0.5, x) with x = $v" >> "$OUT"
  "$PLUS" $SH/st-equal.gdshader --kind rect --set x=$v --probe 0.5,0.5 >> "$OUT" 2>&1
done
echo "wrote $OUT"
