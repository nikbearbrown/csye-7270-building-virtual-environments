#!/bin/zsh
# Run 6 (2026-10-13): does source_color on a sampler2D matter? (a) a texel colour passed straight through (the four-patch swatches texture),
# (b) a mask: where does step(0.5, r) flip along a grey ramp (value = x / 255)?
# canvas_item and spatial (unshaded); hinted and plain; forward_plus, mobile, gl_compatibility; plus canvas_item with HDR 2D on.
# Probes: the four patch centres; ramp at x = 0.50, 0.60, 0.70, 0.74, 0.78, 0.90.  Output: run-6-sampler-hint-matrix.log
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PLUS="$HERE/plus.sh"; SH="$HERE/scratch-shaders"
OUT="$HERE/run-6-sampler-hint-matrix.log"; : > "$OUT"
run() { echo "## $*" >> "$OUT"; "$PLUS" "$@" >> "$OUT" 2>&1; }
SWP=(--probe 0.25,0.25 --probe 0.75,0.25 --probe 0.25,0.75 --probe 0.75,0.75)
RMP=(--probe 0.50,0.5 --probe 0.60,0.5 --probe 0.70,0.5 --probe 0.74,0.5 --probe 0.78,0.5 --probe 0.90,0.5)
for r in forward_plus mobile gl_compatibility; do
  for sp in 2d 3d; do for h in hinted plain; do
    kind=rect; [ $sp = 3d ] && kind=quad3d
    run $SH/tx-pass-$sp-$h.gdshader --renderer $r --kind $kind --tex tex=swatches "${SWP[@]}"
    run $SH/tx-cut-$sp-$h.gdshader --renderer $r --kind $kind --tex tex=ramp_grey "${RMP[@]}"
  done; done
done
for h in hinted plain; do
  run $SH/tx-pass-2d-$h.gdshader --renderer forward_plus --kind rect --hdr2d --tex tex=swatches "${SWP[@]}"
  run $SH/tx-cut-2d-$h.gdshader --renderer forward_plus --kind rect --hdr2d --tex tex=ramp_grey "${RMP[@]}"
done
echo "wrote $OUT"
