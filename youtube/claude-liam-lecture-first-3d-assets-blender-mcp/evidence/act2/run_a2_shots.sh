#!/bin/zsh
# Act II's Blender windows (one window at a time; each opens ~16 s, saves one PNG with Blender's own screenshot operator, quits by itself).
# Scratch preferences only (evidence/act2/blender_config, a copy of evidence/blender_config), never the real Blender prefs.
# Run from anywhere:  zsh evidence/act2/run_a2_shots.sh
HERE="${0:A:h}"
export BLENDER_USER_CONFIG="$HERE/blender_config"
PANTRY="$HERE/../../pantry"
run() {   # mode  output-path
  timeout 120 /Applications/Blender.app/Contents/MacOS/Blender --enable-event-simulate --python-exit-code 1 \
    --python "$HERE/gui_shots_a2.py" -- "$2" "$1" > "$HERE/gui_$1.log" 2>&1
  echo "$1 -> ${2:t} exit=$?"
}
# used in the film (Act II)
run sidebar_closed       $PANTRY/a2_bl_sidebar_closed.png        # ev_bl_object_mode.png with the sidebar closed (the act's window)
run parts_closed         $PANTRY/a2_bl_parts_closed.png          # ev_bl_object_mode_parts.png with the sidebar closed (B17)
run orbit1_closed        $PANTRY/a2_bl_orbit1_closed.png         # ev_bl_orbit_1.png with the sidebar closed (front; B15)
run orbit3_closed        $PANTRY/a2_bl_orbit3_closed.png         # ev_bl_orbit_3.png with the sidebar closed (top; B15)
run orbit4_closed        $PANTRY/a2_bl_orbit4_closed.png         # ev_bl_orbit_4.png with the sidebar closed (zoomed in; B15)
run lantern_edit_closed  $PANTRY/a2_bl_lantern_edit_closed.png   # the lantern in Edit Mode, roof selected, sidebar closed (B19)
# auditioned for B19, not used (kept as evidence): the crate in Object Mode / Edit Mode
run crate_object         $HERE/unused/a2_bl_crate_object.png
run crate_object_closed  $HERE/unused/a2_bl_crate_object_closed.png
run edit_closed          $HERE/unused/a2_bl_edit_closed.png
