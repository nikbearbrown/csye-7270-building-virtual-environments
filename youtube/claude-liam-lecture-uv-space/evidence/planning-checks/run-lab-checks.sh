#!/bin/zsh
# Re-runs every shader this film shows (lab-shaders/) and every evidence-only shader (shaders/) through the Shader Lab
# (real Godot 4.7.2 window, series lab/check_shader.sh) and records the pixels.
# Output: lab-results.jsonl (one JSON line per run: label, shader, exit code, the RESULT line or the compiler's message),
#         png/*.png, and (via summarize-lab.py) lab-summary.txt.
# Safe to re-run; it overwrites its own outputs. Two kinds of window:
#   FW  "fill-window": a 256x256 window with the 128 px sprite scaled x2, so the sprite's UV 0..1 is the whole window and a probe
#       position IS a UV value. Used for the arithmetic claims.
#   (default) the Lab's 640x360 window, used for looks and for measuring shapes in pixels with measure.py.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
EV="$HERE/shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results.jsonl"; : > "$RES"
FW=(--kind sprite --size 256x256 --sprite-scale 2.0)

run() {  # label shader-path args...
  local label="$1"; local shader="$2"; shift 2
  local line
  line=$("$LAB/check_shader.sh" "$shader" "$@" --png "$OUT/$label.png" 2>&1)
  local code=$?
  python3 -I -c 'import json,sys; print(json.dumps({"check": sys.argv[1], "shader": sys.argv[2], "exit": int(sys.argv[3]), "output": sys.stdin.read().strip()}))' "$label" "$(basename "$shader")" "$code" <<<"$line" >> "$RES"
  echo "[$code] $label"
}

# ---- 1. UV is the shape's own address, 0..1, y down, whatever the size ------------------------------------------------------
run uv-map-rect-640x360        $SH/02-address-map.gdshader --kind rect --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5
run uv-map-rect-320x180        $SH/02-address-map.gdshader --kind rect --size 320x180 --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5
run uv-map-rect-1280x720       $SH/02-address-map.gdshader --kind rect --size 1280x720 --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5
run uv-map-rect-640x320        $SH/02-address-map.gdshader --kind rect --size 640x320 --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5
run uv-map-sprite-fill         $SH/02-address-map.gdshader $FW --sprite-tex white --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5
run uv-map-sprite-look         $SH/02-address-map.gdshader --kind sprite --sprite-tex white
run uv-write-error-EXPECTED-FAIL $EV/e01-uv-write-error.gdshader --kind sprite
run uv-write-in-vertex-compiles $EV/e16-uv-write-vertex.gdshader $FW --sprite-tex gradient --probe 0.5,0.5 --probe 0.1,0.5
run step-tenth-640x360         $EV/e05-step-tenth.gdshader --kind rect
run step-tenth-640x320         $EV/e05-step-tenth.gdshader --kind rect --size 640x320

# ---- 2. the lookup, unchanged; the template compiles --------------------------------------------------------------------------
run lookup-sprite-fill         $SH/03-lookup.gdshader $FW --sprite-tex sprite --probe 0.5,0.5 --probe 0.4,0.44 --probe 0.6,0.44 --probe 0.05,0.05
run lookup-sprite-look         $SH/03-lookup.gdshader --kind sprite --sprite-tex sprite
run template-copy-bend-look    $SH/04-copy-bend-look.gdshader $FW --sprite-tex sprite --probe 0.5,0.5 --probe 0.4,0.44

# ---- 3. offsets: subtract from the address, the picture moves the other way ------------------------------------------------------
run shift-x-0.25-sprite-fill   $SH/05-shift-x.gdshader $FW --sprite-tex sprite --set amount=0.25 --probe 0.3,0.5 --probe 0.9,0.5 --probe 0.65,0.44 --probe 0.85,0.44 --probe 0.4,0.44
run shift-x-0.25-gradient-fill $SH/05-shift-x.gdshader $FW --sprite-tex gradient --set amount=0.25 --probe 0.5,0.5 --probe 0.1,0.5 --probe 0.9,0.5
run shift-x-0.25-look          $SH/05-shift-x.gdshader --kind sprite --sprite-tex sprite --set amount=0.25
run shift-x-neg0.25-gradient-fill $SH/05-shift-x.gdshader $FW --sprite-tex gradient --set amount=-0.25 --probe 0.5,0.5 --probe 0.9,0.5
run shift-y-0.25-sprite-fill   $SH/06-shift-xy.gdshader $FW --sprite-tex sprite --set shift_y=0.25 --probe 0.4,0.69 --probe 0.6,0.69 --probe 0.4,0.44 --probe 0.5,0.5
run shift-xy-0.25-sprite-fill  $SH/06-shift-xy.gdshader $FW --sprite-tex sprite --set shift_x=0.25 --set shift_y=0.25 --probe 0.65,0.69 --probe 0.85,0.69 --probe 0.4,0.44
run shift-xy-0.25-gradient-fill $SH/06-shift-xy.gdshader $FW --sprite-tex gradient --set shift_x=0.25 --set shift_y=0.25 --probe 0.5,0.5 --probe 0.9,0.9
run shift-y-0.25-look          $SH/06-shift-xy.gdshader --kind sprite --sprite-tex sprite --set shift_y=0.25
run shift-xy-0.25-look         $SH/06-shift-xy.gdshader --kind sprite --sprite-tex sprite --set shift_x=0.25 --set shift_y=0.25
run offset-as-address-colour   $EV/e13-offset-address-color.gdshader $FW --sprite-tex gradient --probe 0.5,0.5 --probe 0.9,0.5

# ---- 4. scale, clamp, repeat -------------------------------------------------------------------------------------------------------
run scale-1-sprite-look        $SH/07-scale.gdshader --kind sprite --sprite-tex sprite --set zoom=1.0
run scale-2-sprite-look        $SH/07-scale.gdshader --kind sprite --sprite-tex sprite --set zoom=2.0
run scale-2-sprite-fill        $SH/07-scale.gdshader $FW --sprite-tex sprite --set zoom=2.0 --probe 0.25,0.25 --probe 0.2,0.22 --probe 0.3,0.22 --probe 0.5,0.5 --probe 0.75,0.25
run scale-2-gradient-fill      $SH/07-scale.gdshader $FW --sprite-tex gradient --set zoom=2.0 --probe 0.25,0.25 --probe 0.75,0.25 --probe 0.9,0.9
run scale-2-checker-look       $SH/07-scale.gdshader --kind sprite --sprite-tex checker --set zoom=2.0
run scale-2-checker-fill       $SH/07-scale.gdshader $FW --sprite-tex checker --set zoom=2.0 --probe 0.25,0.25 --probe 0.6,0.05 --probe 0.9,0.05 --probe 0.9,0.9
run scale-address-as-colour    $EV/e12-scale-address-color.gdshader $FW --sprite-tex white --probe 0.25,0.25 --probe 0.75,0.25 --probe 0.75,0.75
run tile-no-repeat-2-sprite-fill $SH/08-tile-no-repeat.gdshader $FW --sprite-tex white --tex pic=sprite --set zoom=2.0 --probe 0.25,0.25 --probe 0.75,0.25 --probe 0.75,0.75
run tile-no-repeat-2-sprite-look $SH/08-tile-no-repeat.gdshader --kind sprite --sprite-tex white --tex pic=sprite --set zoom=2.0
run tile-no-repeat-2-gradient-fill $SH/08-tile-no-repeat.gdshader $FW --sprite-tex white --tex pic=gradient --set zoom=2.0 --probe 0.25,0.25 --probe 0.627,0.25 --probe 0.9,0.9
run tile-2-sprite-fill         $SH/09-tile.gdshader $FW --sprite-tex white --tex pic=sprite --set zoom=2.0 --probe 0.25,0.25 --probe 0.75,0.25 --probe 0.75,0.75
run tile-3-sprite-fill         $SH/09-tile.gdshader $FW --sprite-tex white --tex pic=sprite --set zoom=3.0 --probe 0.1667,0.1667 --probe 0.5,0.1667 --probe 0.8333,0.1667 --probe 0.1667,0.5 --probe 0.5,0.5 --probe 0.8333,0.5 --probe 0.1667,0.8333 --probe 0.5,0.8333 --probe 0.8333,0.8333 --probe 0.4667,0.48 --probe 0.3333,0.3333
run tile-3-sprite-look         $SH/09-tile.gdshader --kind sprite --sprite-tex white --tex pic=sprite --set zoom=3.0
run tile-2-gradient-fill       $SH/09-tile.gdshader $FW --sprite-tex white --tex pic=gradient --set zoom=2.0 --probe 0.25,0.25 --probe 0.627,0.25 --probe 0.9,0.9

# ---- 5. scroll (compile + two reads; the saved single-process run-3-scroll.log is the one relied on) ---------------------------------
run scroll-gradient-wait0.3    $SH/10-scroll.gdshader $FW --sprite-tex white --tex pic=gradient --wait 0.3 --probe 0.5,0.5
run scroll-gradient-wait1.3    $SH/10-scroll.gdshader $FW --sprite-tex white --tex pic=gradient --wait 1.3 --probe 0.5,0.5
run scroll-sprite-look         $SH/10-scroll.gdshader --kind sprite --sprite-tex white --tex pic=sprite

# ---- 6. centered coordinates, length, abs, flips -------------------------------------------------------------------------------------
run centered-signs             $EV/e02-signs.gdshader --kind rect --probe 0.25,0.25 --probe 0.75,0.25 --probe 0.25,0.75 --probe 0.75,0.75
run centered-range             $EV/e03-centered-range.gdshader --kind rect --probe 0.5,0.5 --probe 0.999,0.5 --probe 0.5,0.999 --probe 0.001,0.001 --probe 0.999,0.999
run length-grey                $EV/e04-length.gdshader --kind rect --probe 0.5,0.5 --probe 0.999,0.5 --probe 0.001,0.001
run zoom-0.5-corner-sprite-fill $SH/07-scale.gdshader $FW --sprite-tex sprite --set zoom=0.5 --probe 0.5,0.5 --probe 0.9,0.9 --probe 0.8,0.88
run zoom-0.5-corner-look       $SH/07-scale.gdshader --kind sprite --sprite-tex sprite --set zoom=0.5
run zoom-0.5-centered-sprite-fill $SH/11-zoom-centered.gdshader $FW --sprite-tex sprite --set zoom=0.5 --probe 0.5,0.5 --probe 0.3,0.38 --probe 0.7,0.38
run zoom-0.5-centered-look     $SH/11-zoom-centered.gdshader --kind sprite --sprite-tex sprite --set zoom=0.5
run zoom-1-centered-sprite-fill $SH/11-zoom-centered.gdshader $FW --sprite-tex sprite --set zoom=1.0 --probe 0.5,0.5 --probe 0.4,0.44
run disc-0.8-sprite-fill       $SH/12-disc.gdshader $FW --sprite-tex white --probe 0.5,0.5 --probe 0.85,0.5 --probe 0.95,0.5 --probe 0.9,0.9
run disc-0.8-sprite-look       $SH/12-disc.gdshader --kind sprite --sprite-tex white
run face-one-eye-fill          $SH/13-face-one-eye.gdshader $FW --sprite-tex white --probe 0.65,0.425 --probe 0.35,0.425 --probe 0.5,0.5
run face-one-eye-look          $SH/13-face-one-eye.gdshader --kind sprite --sprite-tex white
run face-two-eyes-fill         $SH/14-face-two-eyes.gdshader $FW --sprite-tex white --probe 0.65,0.425 --probe 0.35,0.425 --probe 0.5,0.5
run face-two-eyes-look         $SH/14-face-two-eyes.gdshader --kind sprite --sprite-tex white
run face-two-eyes-wide-fill    $SH/14-face-two-eyes.gdshader $FW --sprite-tex white --set eye_x=0.5 --probe 0.75,0.425 --probe 0.25,0.425 --probe 0.65,0.425
run face-one-eye-wide-fill     $SH/13-face-one-eye.gdshader $FW --sprite-tex white --set eye_x=0.5 --probe 0.75,0.425 --probe 0.25,0.425
run abs-fold-red               $EV/e14-abs-fold.gdshader --kind rect --probe 0.2,0.5 --probe 0.8,0.5 --probe 0.5,0.5
run flip-v-1-sprite-fill       $SH/15-flip.gdshader $FW --sprite-tex sprite --set flip=1.0 --probe 0.4,0.44 --probe 0.4,0.56
run flip-v-neg1-sprite-fill    $SH/15-flip.gdshader $FW --sprite-tex sprite --set flip=-1.0 --probe 0.4,0.56 --probe 0.6,0.56 --probe 0.4,0.44
run flip-v-neg1-look           $SH/15-flip.gdshader --kind sprite --sprite-tex sprite --set flip=-1.0
run flip-v-0-look              $SH/15-flip.gdshader --kind sprite --sprite-tex sprite --set flip=0.0
run flip-u-gradient-fill       $EV/e10-flip-u.gdshader $FW --sprite-tex gradient --probe 0.1,0.5 --probe 0.9,0.5

# ---- 7. the squash: a disc on a wide shape, measured in pixels (measure.py bbox on the PNGs) ------------------------------------------
run disc-640x360-oval          $SH/12-disc.gdshader --kind rect --probe 0.5,0.5
run disc-640x320-oval          $SH/12-disc.gdshader --kind rect --size 640x320 --probe 0.5,0.5
run disc-640x640-round         $SH/12-disc.gdshader --kind rect --size 640x640 --probe 0.5,0.5
run disc-aspect-1-640x360      $SH/16-disc-aspect.gdshader --kind rect --set aspect=1.0 --probe 0.5,0.5
run disc-aspect-640x360-round  $SH/16-disc-aspect.gdshader --kind rect --probe 0.5,0.5
run disc-aspect-640x320-round  $SH/16-disc-aspect.gdshader --kind rect --size 640x320 --set aspect=2.0 --probe 0.5,0.5
run disc-screen-pixel-size-640x360 $EV/e06-disc-screen-pixel-size.gdshader --kind rect --probe 0.5,0.5
run disc-texture-pixel-size-640x360 $EV/e07-disc-texture-pixel-size.gdshader --kind rect --probe 0.5,0.5
run pixel-size-probe-640x320   $EV/e08-pixel-size-probe.gdshader --kind rect --size 640x320 --probe 0.5,0.5
# the same shapes in the other renderer (does the geometry depend on it?)
run disc-640x360-oval-COMPAT   $SH/12-disc.gdshader --kind rect --renderer gl_compatibility --probe 0.5,0.5
run disc-aspect-640x360-round-COMPAT $SH/16-disc-aspect.gdshader --kind rect --renderer gl_compatibility --probe 0.5,0.5
run tile-3-sprite-fill-COMPAT  $SH/09-tile.gdshader $FW --sprite-tex white --tex pic=sprite --set zoom=3.0 --renderer gl_compatibility --probe 0.1667,0.1667 --probe 0.5,0.5 --probe 0.4667,0.48 --probe 0.3333,0.3333
run shift-x-0.25-sprite-fill-COMPAT $SH/05-shift-x.gdshader $FW --sprite-tex sprite --set amount=0.25 --renderer gl_compatibility --probe 0.3,0.5 --probe 0.9,0.5 --probe 0.65,0.44
run scale-2-sprite-look-COMPAT $SH/07-scale.gdshader --kind sprite --sprite-tex sprite --set zoom=2.0 --renderer gl_compatibility
run scale-1-sprite-look-COMPAT $SH/07-scale.gdshader --kind sprite --sprite-tex sprite --set zoom=1.0 --renderer gl_compatibility
run uv-map-rect-COMPAT         $SH/02-address-map.gdshader --kind rect --renderer gl_compatibility --probe 0.02,0.02 --probe 0.98,0.98 --probe 0.5,0.5
run face-two-eyes-fill-COMPAT  $SH/14-face-two-eyes.gdshader $FW --sprite-tex white --renderer gl_compatibility --probe 0.65,0.425 --probe 0.35,0.425 --probe 0.5,0.5
run flip-v-neg1-sprite-fill-COMPAT $SH/15-flip.gdshader $FW --sprite-tex sprite --set flip=-1.0 --renderer gl_compatibility --probe 0.4,0.56 --probe 0.6,0.56 --probe 0.4,0.44
run mask-2-checker-fill-COMPAT $SH/17-mask.gdshader $FW --sprite-tex checker --set zoom=2.0 --renderer gl_compatibility --probe 0.25,0.25 --probe 0.75,0.25 --probe 0.9,0.9 --probe 0.495,0.495 --probe 0.505,0.505
run hook-tiled-fill-COMPAT     $SH/01-hook-controls.gdshader $FW --sprite-tex white --tex pic=sprite --set shift=1.0 --set zoom=3.0 --renderer gl_compatibility --probe 0.1667,0.1667 --probe 0.5,0.5 --probe 0.4667,0.48 --probe 0.3333,0.3333
run tile-no-repeat-2-gradient-fill-COMPAT $SH/08-tile-no-repeat.gdshader $FW --sprite-tex white --tex pic=gradient --set zoom=2.0 --renderer gl_compatibility --probe 0.25,0.25 --probe 0.627,0.25
run tile-2-gradient-fill-COMPAT $SH/09-tile.gdshader $FW --sprite-tex white --tex pic=gradient --set zoom=2.0 --renderer gl_compatibility --probe 0.25,0.25 --probe 0.627,0.25

# ---- 8. the mask -----------------------------------------------------------------------------------------------------------------------
run mask-1-checker-fill        $SH/17-mask.gdshader $FW --sprite-tex checker --set zoom=1.0 --probe 0.1,0.1 --probe 0.9,0.9
run mask-2-checker-fill        $SH/17-mask.gdshader $FW --sprite-tex checker --set zoom=2.0 --probe 0.1,0.1 --probe 0.25,0.25 --probe 0.75,0.25 --probe 0.9,0.9 --probe 0.495,0.495 --probe 0.505,0.505
run mask-2-checker-look        $SH/17-mask.gdshader --kind sprite --sprite-tex checker --set zoom=2.0
run step-edge-cases            $EV/e15-step-edge-cases.gdshader --kind rect --probe 0.25,0.5 --probe 0.75,0.5

# ---- 9. the opening shader's states (slide by one whole picture comes back to the start; then a 3 x 3 grid) -----------------------------
run hook-start-fill            $SH/01-hook-controls.gdshader $FW --sprite-tex white --tex pic=sprite --probe 0.5,0.5 --probe 0.4,0.44 --probe 0.05,0.05
run hook-half-slid-fill        $SH/01-hook-controls.gdshader $FW --sprite-tex white --tex pic=sprite --set shift=0.5 --probe 0.2,0.5 --probe 0.5,0.5 --probe 0.8,0.5
run hook-half-slid-look        $SH/01-hook-controls.gdshader --kind sprite --sprite-tex white --tex pic=sprite --set shift=0.5
run hook-one-wrap-fill         $SH/01-hook-controls.gdshader $FW --sprite-tex white --tex pic=sprite --set shift=1.0 --probe 0.5,0.5 --probe 0.4,0.44
run hook-tiled-look            $SH/01-hook-controls.gdshader --kind sprite --sprite-tex white --tex pic=sprite --set shift=1.0 --set zoom=3.0
run hook-tiled-fill            $SH/01-hook-controls.gdshader $FW --sprite-tex white --tex pic=sprite --set shift=1.0 --set zoom=3.0 --probe 0.1667,0.1667 --probe 0.5,0.5 --probe 0.8333,0.8333 --probe 0.4667,0.48 --probe 0.3333,0.3333
echo "wrote $RES"
