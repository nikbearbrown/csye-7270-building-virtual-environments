#!/bin/zsh
# Run 15 (2026-10-13): does the source_color hint touch alpha? The shader outputs a.a = 0.5 as a gray value (a : source_color, alpha 0.5).
# If alpha were converted to light (0.214) the shown value would be 0.5 in the linear pipelines; untouched (0.5) it shows encode(0.5) = 0.7354 there.
# Output: run-15-alpha-untouched.log
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PLUS="$HERE/plus.sh"; SH="$HERE/scratch-shaders"
OUT="$HERE/run-15-alpha-untouched.log"; : > "$OUT"
run() { echo "## $*" >> "$OUT"; "$PLUS" "$@" >> "$OUT" 2>&1; }
run $SH/al-alpha-3d.gdshader --kind quad3d --renderer forward_plus --probe 0.5,0.5
run $SH/al-alpha-3d.gdshader --kind quad3d --renderer gl_compatibility --probe 0.5,0.5
run $SH/al-alpha-2d.gdshader --kind rect --renderer forward_plus --hdr2d --probe 0.5,0.5
run $SH/al-alpha-2d.gdshader --kind rect --renderer forward_plus --probe 0.5,0.5
echo "wrote $OUT"
