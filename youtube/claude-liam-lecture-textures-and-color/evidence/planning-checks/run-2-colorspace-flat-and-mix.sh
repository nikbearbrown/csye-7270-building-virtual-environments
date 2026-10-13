#!/bin/zsh
# Run 2 (2026-10-13): one flat color, and a mid-tone mix at t = 0.5, in canvas_item and spatial (unshaded), uniforms with and without source_color,
# in forward_plus, mobile and gl_compatibility. Centre pixel only. Output: run-2-colorspace-flat-and-mix.log
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LAB="$(cd "$HERE/../../../_godot-shaders-series/lab" && pwd)"
OUT="$HERE/run-2-colorspace-flat-and-mix.log"; : > "$OUT"
for r in forward_plus mobile gl_compatibility; do
  for s in cs2-flat-2d-hinted cs2-flat-2d-plain cs2-mix-2d-hinted cs2-mix-2d-plain; do
    echo "## $s | renderer=$r" >> "$OUT"
    "$LAB/check_shader.sh" "$HERE/scratch-shaders/$s.gdshader" --kind rect --renderer $r --probe 0.5,0.5 >> "$OUT" 2>&1
  done
  for s in cs2-flat-3d-hinted cs2-flat-3d-plain cs2-mix-3d-hinted cs2-mix-3d-plain; do
    echo "## $s | renderer=$r" >> "$OUT"
    "$LAB/check_shader.sh" "$HERE/scratch-shaders/$s.gdshader" --kind quad3d --renderer $r --probe 0.5,0.5 >> "$OUT" 2>&1
  done
done
echo "wrote $OUT"
