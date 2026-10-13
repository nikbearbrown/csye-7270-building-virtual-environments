#!/bin/zsh
# Runs gui_shots.py once per mode (one Blender window at a time, each closes itself) and writes the PNGs into ../../pantry.
# Scratch preferences only: BLENDER_USER_CONFIG points at evidence/blender_config, never at the real Blender prefs.
HERE="${0:A:h}"
export BLENDER_USER_CONFIG="$HERE/../blender_config"
mkdir -p "$BLENDER_USER_CONFIG"
PANTRY="$HERE/../../pantry"
run() {   # mode  png-name
  timeout 120 /Applications/Blender.app/Contents/MacOS/Blender --enable-event-simulate --python-exit-code 1 \
    --python "$HERE/gui_shots.py" -- "$PANTRY/$2" "$1" > "$HERE/gui_$1.log" 2>&1
  echo "$1 -> $2 exit=$?"
}
run object      ev_bl_object_mode.png
run parts       ev_bl_object_mode_parts.png
run edit        ev_bl_edit_mode.png
run stats       ev_bl_status_stats.png
run hand_before ev_bl_hand_edit_before.png
run hand_after  ev_bl_hand_edit_after.png
run orbit1      ev_bl_orbit_1.png
run orbit2      ev_bl_orbit_2.png
run orbit3      ev_bl_orbit_3.png
run orbit4      ev_bl_orbit_4.png
