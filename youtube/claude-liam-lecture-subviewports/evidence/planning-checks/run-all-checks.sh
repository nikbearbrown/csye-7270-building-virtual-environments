#!/bin/zsh
# Re-runs every planning check of the SubViewports film and writes the logs into logs/.
# The scripts need a Godot project to run in: this copies them into a scratch project (default /private/tmp/claude-501/godot-shaders-subviewports/proj-final),
# imports it once, and runs each script in a real window of Godot 4.7.2 with --fixed-fps 30 (every TIME-dependent check reads TIME from the same draw).
# Machine of record: Apple M4 Pro, macOS. Renderers: Forward+ (default) and, where a pixel could differ, Compatibility.
#
# Every script forces one real draw per logical step (RenderingServer.force_draw(false)); see RESULTS.md, "the covered window": a Godot window that other windows cover is drawn on
# only about 4 of 10 frames, so a script that merely waits for frames can read a picture that was never redrawn.
#
# Set SV_SKIP_LAB=1 to skip the Shader Lab batch (run-lab-checks.sh, about 8 minutes, takes the Lab lock). Never stop that batch with `pkill -f`: another film's batch has the same name.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
W="${SV_SCRATCH:-/private/tmp/claude-501/godot-shaders-subviewports/proj-final}"
LOGS="$HERE/logs"; mkdir -p "$LOGS" "$W"
cp "$HERE/scratch-project.godot" "$W/project.godot"
cp "$HERE"/*.gd "$W/"
godot --headless --path "$W" --import >/dev/null 2>&1
RUNFLAGS=()
run() {   # logname script [renderer] [-- args]      (RUNFLAGS: extra engine flags for this run)
  local name="$1"; local script="$2"; shift 2
  local rend=()
  if [ "${1:-}" = "gl_compatibility" ]; then rend=(--rendering-method gl_compatibility); shift; fi
  echo "== $name"
  ( cd "$W" && timeout 590 godot --path . "${rend[@]}" "${RUNFLAGS[@]}" --fixed-fps 30 --script "res://$script" "$@" 2>&1 ) | grep -v "^Godot Engine\|^Metal\|^OpenGL\|^$" > "$LOGS/$name.log"
  grep -c RESULT "$LOGS/$name.log"
}
run run-1-verify1-basics-forward_plus verify1_basics.gd
run run-1b-verify1-basics-gl_compatibility verify1_basics.gd gl_compatibility
run run-2-verify2-two-shaders-forward_plus verify2_two_shaders.gd
run run-2b-verify2-two-shaders-gl_compatibility verify2_two_shaders.gd gl_compatibility
run run-3-verify3-stripes-hue-forward_plus verify3_stripes_hue.gd
run run-3b-verify3-stripes-hue-gl_compatibility verify3_stripes_hue.gd gl_compatibility
run run-4-verify4-mesh-forward_plus verify4_mesh.gd
run run-4b-verify4-mesh-gl_compatibility verify4_mesh.gd gl_compatibility
run run-5-verify5-premultiplied-forward_plus verify5_premultiplied.gd
run run-5b-verify5-premultiplied-gl_compatibility verify5_premultiplied.gd gl_compatibility
run run-6-verify6-chain-resolution-input-forward_plus verify6_chain_resolution_input.gd
run run-8-verify8-your-turn-reference-forward_plus verify8_your_turn_reference.gd
run run-9-verify9-nested-4k-forward_plus verify9_nested_4k.gd
run run-7a-verify7-captures-c01-c08-forward_plus verify7_capture_rehearsal.gd -- c01 c02 c03 c04a c04b c05 c06 c07 c08
run run-7b-verify7-captures-c09-c14-forward_plus verify7_capture_rehearsal.gd -- c09 c10 c11 c12 c13 c14
run run-7c-verify7-captures-c15-c21-forward_plus verify7_capture_rehearsal.gd -- c15 c16 c17 c18 c19 c20 c21
# the covered window (check 10), the Once reading (check 11) and the capture route against scale 1 (check 12)
run run-10-verify10-draws-default-placement verify10_draw_skipping.gd
RUNFLAGS=(--always-on-top); run run-10b-verify10-draws-always-on-top verify10_draw_skipping.gd; RUNFLAGS=()
RUNFLAGS=(--position 0,0); run run-10c-verify10-draws-position-0-0 verify10_draw_skipping.gd; RUNFLAGS=()
run run-11-verify11-once-needs-a-draw-forward_plus verify11_once_needs_a_draw.gd
run run-12-verify12-capture-route-forward_plus verify12_route_equivalence.gd
run run-12b-verify12-capture-route-gl_compatibility verify12_route_equivalence.gd gl_compatibility
# recipe B (check 13): the regular loop never draws, every step is one force_draw(false, 1/30): TIME per step, Update Mode Once, and the 3x route again
run run-16-verify13-time-recipe-A-forward_plus verify13_draw_recipe.gd -- A
run run-16b-verify13-time-recipe-B-forward_plus verify13_draw_recipe.gd -- B
run run-16c-verify13-c21-under-recipe-B-forward_plus verify13_draw_recipe.gd -- c21
export SV_RECIPE=B; run run-12c-verify12-capture-route-recipe-B-forward_plus verify12_route_equivalence.gd; unset SV_RECIPE
if [ "${SV_SKIP_LAB:-0}" != "1" ]; then
  "$HERE/run-lab-checks.sh" > "$LOGS/run-lab-checks.log" 2>&1
fi
echo "done: logs in $LOGS"
