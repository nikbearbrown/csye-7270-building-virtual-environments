#!/bin/zsh
# Runs the Godot commands in the film's order, headless, each wrapped in `timeout 120`, and keeps the real stdout in a .log.
# Run ./setup_project.sh first. One Godot at a time.
HERE="${0:A:h}"
PROJ=/private/tmp/claude-501/a3film/godot_proj
cd "$PROJ" || exit 1
run() {   # logname  command...
  local log="$HERE/$1.log"; shift
  { echo "\$ $*"; "$@" 2>&1; echo "[exit code $?]"; } > "$log"
  echo "$(basename $log): $(tail -1 $log)"
}
run import                       godot --headless --path "$PROJ" --import
run check_good                   timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60
run demo_i_lantern_yup_off       timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- lantern=res://variants/lantern_yup_off.glb
run demo_ii_crate_scale_unapplied timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- crate=res://variants/crate_scale_unapplied.glb
run demo_iii_crate_origin_centre timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- crate=res://variants/crate_origin_centre.glb
run demo_iii_crate_origin_centre_lifted timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- crate=res://variants/crate_origin_centre.glb@0,0.4,0
run demo_iii_crate_origin_centre_lifted_origin_check timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- crate=res://variants/crate_origin_centre.glb@0,0.4,0 +origin
run demo_v_check_good_origin_check timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- +origin
run demo_iii_crate_origin_centre_lifted_by_guess timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- crate=res://variants/crate_origin_centre.glb@0,0.5,0
run demo_iv_lantern_x10          timeout 120 godot --headless --path "$PROJ" --script res://tests/check_assets.gd --fixed-fps 60 -- lantern=res://variants/lantern_x10.glb
run colours_good                 timeout 120 godot --headless --path "$PROJ" --script res://tests/check_colours.gd --fixed-fps 60
run colours_viewport_only_variant timeout 120 godot --headless --path "$PROJ" --script res://tests/check_colours.gd --fixed-fps 60 -- res://variants/crate_colour_lost.glb
{ echo '$ python3 glb_colours.py <the three good .glb and the colour_lost variant>'; python3 "$HERE/glb_colours.py" "$PROJ/assets/crate.glb" "$PROJ/assets/lantern.glb" "$PROJ/assets/coin.glb" "$PROJ/variants/crate_colour_lost.glb"; } > "$HERE/glb_colours.log" 2>&1
echo "glb_colours.log written"
