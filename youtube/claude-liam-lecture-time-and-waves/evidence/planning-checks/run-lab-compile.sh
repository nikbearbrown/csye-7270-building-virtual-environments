#!/bin/zsh
# Compiles and renders every shader this film shows (the real files in ../../lab-shaders/, real TIME) in the Shader Lab, in both renderers.
# Output: lab-compile.txt (one line per file and renderer: exit code and the renderer that ran). A shader error would print SHADER_OR_SCRIPT_ERROR and a non-zero code.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/lab-compile.txt"; : > "$OUT"
run() {  # shader args...
  local shader="$1" r line code
  shift
  for r in forward_plus gl_compatibility; do
    line=$("$LAB/check_shader.sh" "$SH/$shader" "$@" --renderer $r 2>&1)
    code=$?
    echo "[$code] $shader $r :: $(echo "$line" | grep -o '"renderer":"[a-z_]*"' | head -1) $(echo "$line" | grep -E 'SHADER|ERROR' | head -2)" | tee -a "$OUT"
  done
}
run 01-age.gdshader          --kind rect --wait 0.4
run 02-pulse.gdshader        --kind rect --wait 0.4
run 03-dials.gdshader        --kind rect --wait 0.4
run 04-three-shapes.gdshader --kind rect --wait 0.4
run 05-curve-loop.gdshader   --kind rect --tex curve=gradient --wait 0.4
run 06-stripes.gdshader      --kind rect --wait 0.4
run 07-travel.gdshader       --kind rect --wait 0.4
run 08-rings.gdshader        --kind sprite --sprite-tex white --wait 0.4
run 09-ripple.gdshader       --kind sprite --sprite-tex checker --wait 0.4
run 10-flag.gdshader         --kind sprite --sprite-tex checker --wait 0.4
run 11-two-waves.gdshader    --kind sprite --sprite-tex checker --wait 0.4
run 12-breath.gdshader       --kind sprite --sprite-tex sprite --tex curve=gradient --wait 0.4
run 13-banner.gdshader       --kind sprite --sprite-tex checker --set wind=1.0 --wait 0.4
echo "wrote $OUT"
