#!/bin/zsh
# Run 1 (2026-10-13): the same blend, written four ways, in three renderers. Reads three pixels of a black-to-white blend.
#   canvas_item or spatial (unshaded)  x  uniforms with source_color or without  x  forward_plus, mobile, gl_compatibility
# Output: run-1-colorspace-matrix.log (one line per run: the Lab's RESULT line). Safe to re-run.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LAB="$(cd "$HERE/../../../_godot-shaders-series/lab" && pwd)"
OUT="$HERE/run-1-colorspace-matrix.log"; : > "$OUT"
for r in forward_plus mobile gl_compatibility; do
  for s in cs-2d-hinted cs-2d-plain; do
    echo "## $s | renderer=$r" >> "$OUT"
    "$LAB/check_shader.sh" "$HERE/scratch-shaders/$s.gdshader" --kind rect --renderer $r --probe 0.1,0.5 --probe 0.5,0.5 --probe 0.9,0.5 >> "$OUT" 2>&1
  done
  for s in cs-3d-hinted cs-3d-plain; do
    echo "## $s | renderer=$r" >> "$OUT"
    "$LAB/check_shader.sh" "$HERE/scratch-shaders/$s.gdshader" --kind quad3d --renderer $r --probe 0.1,0.5 --probe 0.5,0.5 --probe 0.9,0.5 >> "$OUT" 2>&1
  done
done
echo "wrote $OUT"
