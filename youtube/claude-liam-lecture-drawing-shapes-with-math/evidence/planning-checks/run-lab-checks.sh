#!/bin/zsh
# run-lab-checks.sh: every shader this film shows (and every calculator behind a number it says), rendered in the Shader Lab
# (a real, windowed Godot 4.7.2 through ../../../_godot-shaders-series/lab/check_shader.sh), then analysed by the python scripts next to it.
#   ./run-lab-checks.sh        # about 10 minutes; overwrites png/ and lab-results.jsonl, then runs run-calc.py and the four analysis scripts
# Every picture is a SQUARE 480 x 480 view on Forward+ unless the label says otherwise (calculators say their own size).
set -u
source "${0:A:h}/lab-lib.sh"
: > "$RES"
C="$HERE/calc"
S=(--kind rect --size 480x480)
CH=17-crosshair.gdshader

# ---- act I: a circle ------------------------------------------------------------------------------------------------------------
run 01-distance          01-distance.gdshader          "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.2 --probe 0.1,0.5 --probe 0.0,0.0 --probe 0.62,0.66 --probe 0.5,0.9
run 02-circle            02-circle.gdshader            "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.25 --probe 0.5,0.15 --probe 0.9,0.9 --probe 0.62,0.66 --probe 0.5,0.9
run 03-slider-0.1        03-circle-slider.gdshader     "${S[@]}" --set radius=0.1
run 03-slider-0.3        03-circle-slider.gdshader     "${S[@]}" --set radius=0.3
run 03-slider-0.45       03-circle-slider.gdshader     "${S[@]}" --set radius=0.45
# ---- act II: rings and cutouts ---------------------------------------------------------------------------------------------------
run 04-ring              04-ring.gdshader              "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.18 --probe 0.5,0.13 --probe 0.5,0.02
run 05-overlap-sum       05-overlap-sum.gdshader       "${S[@]}" --probe 0.5,0.5 --probe 0.3,0.5 --probe 0.9,0.5
run 06-hole-bug          06-overlap-hole-bug.gdshader  "${S[@]}" --probe 0.5,0.5 --probe 0.3,0.5 --probe 0.5,0.4
run 07-hole-fixed        07-overlap-hole-fixed.gdshader "${S[@]}" --probe 0.5,0.5 --probe 0.3,0.5 --probe 0.5,0.4
run 08-negative-bug      08-negative-eats-dot.gdshader "${S[@]}" --probe 0.88,0.5 --probe 0.7,0.5 --probe 0.4,0.5 --probe 0.9,0.35
run 09-negative-fixed    09-negative-fixed.gdshader    "${S[@]}" --probe 0.88,0.5 --probe 0.7,0.5 --probe 0.4,0.5 --probe 0.9,0.35
# ---- act III: lines and crosses --------------------------------------------------------------------------------------------------
run 10-band              10-band.gdshader              "${S[@]}" --probe 0.5,0.1 --probe 0.7,0.5 --probe 0.5,0.5
run 11-cross             11-cross.gdshader             "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.1 --probe 0.1,0.5 --probe 0.1,0.1
run 12-arm-rectangle     12-arm-rectangle.gdshader     "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.25 --probe 0.5,0.1 --probe 0.6,0.5
run 13-arms-gap          13-arms-gap.gdshader          "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.3 --probe 0.5,0.7 --probe 0.5,0.95 --probe 0.3,0.5
run 14-four-arms         14-four-arms.gdshader         "${S[@]}" --probe 0.5,0.5 --probe 0.3,0.5 --probe 0.7,0.5 --probe 0.5,0.3 --probe 0.5,0.7 --probe 0.3,0.3
# ---- act IV: a tool (the failing shader is EXPECTED to exit 1 with the engine's message) --------------------------------------------
run 15-ring-tool         15-ring-tool.gdshader         "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.18
run 16-uv-in-function    16-uv-inside-function-FAILS.gdshader "${S[@]}"
# ---- act V: the crosshair --------------------------------------------------------------------------------------------------------
run crosshair-default    $CH "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.2 --probe 0.35,0.5
for u in dot_size ring_distance ring_width arm_gap arm_length arm_width; do
  run crosshair-$u-0   $CH "${S[@]}" --set $u=0.0
  run crosshair-$u-1   $CH "${S[@]}" --set $u=1.0
done
run crosshair-arms-only  $CH "${S[@]}" --set dot_size=0.0 --set ring_width=0.0
# the held pairs of the sweep videos (B40 to B42): the first dial of a clip stays at 1 while the second moves, so the 50 % frame shows (first = 1, second = 0) and the 85 % frame (both = 1)
run pair-dot1-ring0      $CH "${S[@]}" --set dot_size=1.0 --set ring_distance=0.0
run pair-dot1-ring1      $CH "${S[@]}" --set dot_size=1.0 --set ring_distance=1.0
run pair-rw1-al0         $CH "${S[@]}" --set ring_width=1.0 --set arm_length=0.0
run pair-rw1-al1         $CH "${S[@]}" --set ring_width=1.0 --set arm_length=1.0
run pair-aw1-ag0         $CH "${S[@]}" --set arm_width=1.0 --set arm_gap=0.0
run pair-aw1-ag1         $CH "${S[@]}" --set arm_width=1.0 --set arm_gap=1.0
run crosshair-all-0      $CH "${S[@]}" --set dot_size=0 --set ring_distance=0 --set ring_width=0 --set arm_gap=0 --set arm_length=0 --set arm_width=0
run crosshair-all-1      $CH "${S[@]}" --set dot_size=1 --set ring_distance=1 --set ring_width=1 --set arm_gap=1 --set arm_length=1 --set arm_width=1
# ---- calculators: claims about the screen, a wide view, argument order, built-ins in functions -------------------------------------
run alpha-clamp-fwd      $C/calc-alpha-clamp.gdshader  --kind rect --size 480x64 --probe 0.125,0.5 --probe 0.375,0.5 --probe 0.625,0.5 --probe 0.875,0.5
run alpha-clamp-compat   $C/calc-alpha-clamp.gdshader  --kind rect --size 480x64 --probe 0.125,0.5 --probe 0.375,0.5 --probe 0.625,0.5 --probe 0.875,0.5 --renderer gl_compatibility
run uv-corners-wide      $C/calc-uv-corners.gdshader   --kind rect --size 640x360 --probe 0.0,0.0 --probe 1.0,0.0 --probe 0.0,1.0 --probe 1.0,1.0
run circle-wide-640x360  02-circle.gdshader            --kind rect --size 640x360
run step-hole            $C/calc-step-hole.gdshader    "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.1
run flip-equals-1minus   $C/calc-flip-equals-one-minus.gdshader "${S[@]}"
run max-equals-capped-sum $C/calc-max-equals-capped-sum.gdshader "${S[@]}"
run vec2-single          $C/calc-vec2-single.gdshader  "${S[@]}"
run builtin-time-in-fn   $C/calc-time-in-function.gdshader   "${S[@]}"
run builtin-color-in-fn  $C/calc-color-in-function-FAILS.gdshader "${S[@]}"
run builtin-uv-passed-in $C/calc-uv-passed-in.gdshader "${S[@]}"
run builtin-uv-in-fn     16-uv-inside-function-FAILS.gdshader "${S[@]}"
run your-turn-reference-default $C/your-turn-reference.gdshader "${S[@]}" --probe 0.5,0.5 --probe 0.5,0.2
run your-turn-reference-thickness-0 $C/your-turn-reference.gdshader "${S[@]}" --set thickness=0.0
run your-turn-reference-thickness-1 $C/your-turn-reference.gdshader "${S[@]}" --set thickness=1.0 --set radius=1.0
run your-turn-reference-wide $C/your-turn-reference.gdshader --kind rect --size 640x360
# ---- the Compatibility renderer, same shaders and view -------------------------------------------------------------------------
R=(--renderer gl_compatibility)
for n in 02-circle 04-ring 05-overlap-sum 06-overlap-hole-bug 07-overlap-hole-fixed 08-negative-eats-dot 09-negative-fixed 10-band 11-cross 12-arm-rectangle 13-arms-gap 14-four-arms 15-ring-tool; do
  run compat-$n $n.gdshader "${S[@]}" "${R[@]}"
done
run compat-17-crosshair-default $CH "${S[@]}" "${R[@]}"
run compat-crosshair-all-1  $CH "${S[@]}" "${R[@]}" --set dot_size=1 --set ring_distance=1 --set ring_width=1 --set arm_gap=1 --set arm_length=1 --set arm_width=1
run compat-01-distance 01-distance.gdshader "${S[@]}" "${R[@]}" --probe 0.62,0.66

# ---- the calculator, the analyses --------------------------------------------------------------------------------------------------
python3 "$HERE/run-calc.py"
python3 "$HERE/analyze-masks.py"
python3 "$HERE/analyze-calcs.py"
python3 "$HERE/analyze-crosshair-and-renderers.py"
python3 "$HERE/analyze-your-turn.py"
echo "done: $RES"
