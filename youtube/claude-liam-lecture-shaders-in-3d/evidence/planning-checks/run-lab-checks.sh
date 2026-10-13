#!/bin/zsh
# Re-runs every shader this film shows through the Shader Lab (real Godot 4.7.2 window) and records the pixels.
# Output: lab-results.jsonl (one record per check: label, shader, renderer, exit code, the Lab's own output) and png/*.png.
# Safe to re-run; it overwrites its own outputs. Two checks are EXPECTED to fail (the two *-broken shaders): their exit code 1
# and the compiler's message are the evidence.
#   Machine: Apple M4 Pro, Godot 4.7.2 stable (official). Probe positions are normalized 0..1 (x right, y down).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results.jsonl"; : > "$RES"

run() {  # label shader renderer kind [lab args...]
  local label="$1" shader="$2" renderer="$3" kind="$4"; shift 4
  local line code
  line=$("$LAB/check_shader.sh" "$SH/$shader" --kind "$kind" --renderer "$renderer" "$@" --png "$OUT/$label.png" 2>&1)
  code=$?
  python3 -I -c '
import json, sys
label, shader, renderer, code, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.stdin.read().strip()
print(json.dumps({"check": label, "shader": shader, "renderer_requested": renderer, "exit": code, "output": out}))
' "$label" "$shader" "$renderer" "$code" <<<"$line" >> "$RES"
  echo "[$code] $label"
}

FP=forward_plus; GC=gl_compatibility; MB=mobile

# 01 flat teal in 2D (canvas_item on a ColorRect)
run 01-flat-teal-2d-fp          01-flat-teal-2d.gdshader  $FP rect   --probe 0.5,0.5
run 01-flat-teal-2d-gc          01-flat-teal-2d.gdshader  $GC rect   --probe 0.5,0.5
# 02 flat teal in 3D: lit and unshaded give the SAME pixel in the Lab's quad3d scene (white ambient light, energy 1, no lamp)
run 02-flat-teal-3d-fp          02-flat-teal-3d.gdshader  $FP quad3d --probe 0.5,0.5
run 02-flat-teal-3d-gc          02-flat-teal-3d.gdshader  $GC quad3d --probe 0.5,0.5
run 07-flat-teal-3d-unshaded-fp 07-flat-teal-3d-unshaded.gdshader $FP quad3d --probe 0.5,0.5
run 07-flat-teal-3d-unshaded-gc 07-flat-teal-3d-unshaded.gdshader $GC quad3d --probe 0.5,0.5
# 03 the three-function skeleton in spatial (with one dial, as the film draws it): it compiles; an empty fragment() leaves the default white albedo
run 03-skeleton-3d-fp           03-skeleton-3d.gdshader   $FP quad3d --probe 0.5,0.5
# 04 / 05 the two mistakes: EXPECTED to fail with the compiler's message
run 04-color-in-3d-broken-fp    04-color-in-3d-broken.gdshader $FP quad3d --probe 0.5,0.5
run 05-albedo-four-numbers-broken-fp 05-albedo-four-numbers-broken.gdshader $FP quad3d --probe 0.5,0.5
# 06 UV as colour on a QuadMesh seen from the front: corners
run 06-uv-colors-3d-fp          06-uv-colors-3d.gdshader  $FP quad3d --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5
run 06-uv-colors-3d-gc          06-uv-colors-3d.gdshader  $GC quad3d --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5
# 08 empty light() and 09 cull_disabled compile
run 08-empty-light-fp           08-flat-teal-3d-empty-light.gdshader $FP quad3d --probe 0.5,0.5
run 09-two-sided-fp             09-two-sided.gdshader     $FP quad3d --probe 0.5,0.5
# 10 stripes: centres of the first dark and first light stripe (UV.x 0.03125, 0.09375) and the edge probes 0.0625, 0.1875
run 10-stripes-grey-fp          10-stripes-grey.gdshader  $FP quad3d --probe 0.03125,0.5 --probe 0.09375,0.5 --probe 0.0625,0.5 --probe 0.1875,0.5
run 10-stripes-grey-gc          10-stripes-grey.gdshader  $GC quad3d --probe 0.03125,0.5 --probe 0.09375,0.5 --probe 0.0625,0.5 --probe 0.1875,0.5
# 11 mix by a dial: 0, 0.5, 1 in two renderers
#    (the extra probes at the top-left and bottom-right: a uniform is the same for every pixel, so the flat blend reads the same everywhere)
for a in 0.0 0.5 1.0; do
  run 11-mix-dial-fp-$a         11-mix-dial.gdshader      $FP quad3d --set activation=$a --probe 0.5,0.5 --probe 0.1,0.1 --probe 0.9,0.9
  run 11-mix-dial-gc-$a         11-mix-dial.gdshader      $GC quad3d --set activation=$a --probe 0.5,0.5 --probe 0.1,0.1 --probe 0.9,0.9
done
# 12 the real pad shader: five activations, three renderers; dark stripe centre and light stripe centre
for r in $FP $GC $MB; do
  for a in 0.0 0.25 0.5 0.75 1.0; do
    run 12-signal-pad-$r-$a     12-signal-pad.gdshader    $r quad3d --set activation=$a --probe 0.03125,0.5 --probe 0.09375,0.5
  done
done
# the brief's suggested probes (UV.x 0.0625 and 0.1875) at activation 0.5: both land on a dark stripe (labelled in RESULTS.md)
run 12-signal-pad-brief-probes  12-signal-pad.gdshader    $FP quad3d --set activation=0.5 --probe 0.0625,0.5 --probe 0.1875,0.5
# 13 / 14 the same grey 0.5 in 2D (COLOR) and 3D (ALBEDO, unshaded), three renderers
for r in $FP $MB $GC; do
  run 13-grey-2d-$r             13-grey-2d.gdshader       $r rect   --probe 0.5,0.5
  run 14-grey-3d-$r             14-grey-3d.gdshader       $r quad3d --probe 0.5,0.5
  run 15-which-renderer-$r      15-which-renderer.gdshader $r quad3d --probe 0.5,0.5
done
# 17 more render modes on one comma-separated line compile (named in the film, not rendered)
run 17-more-render-modes-fp     17-more-render-modes.gdshader $FP quad3d --probe 0.5,0.5
# 18 / 19 the two-D and the three-D red shaders compile on their own targets (the scene that gives the two-D one to a mesh is verify8)
run 18-two-d-shader-fp          18-two-d-shader-on-a-mesh.gdshader  $FP rect   --probe 0.5,0.5
run 19-three-d-shader-fp        19-three-d-shader-on-a-mesh.gdshader $FP quad3d --probe 0.5,0.5
# 16 all five outputs compile (default values)
run 16-all-outputs-fp           16-all-outputs.gdshader   $FP quad3d --probe 0.5,0.5
echo "wrote $RES"
