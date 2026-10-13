#!/bin/zsh
# ACT III evidence: one real Blender 5.1.2 window (the crate at the world origin, X-ray on), saved by Blender's own
# screenshot operator, then the film's crop. One window, closes itself after ~9 s. Private scratch prefs (a copy).
HERE="${0:A:h}"
export BLENDER_USER_CONFIG="$HERE/blender_config"
PANTRY="$HERE/../../pantry"
timeout 120 /Applications/Blender.app/Contents/MacOS/Blender --enable-event-simulate --python-exit-code 1 \
  --python "$HERE/gui_origin.py" -- "$PANTRY/a3_bl_crate_origin_window.png" > "$HERE/gui_origin.log" 2>&1
echo "gui_origin exit=$?"
grep "^\[gui\]" "$HERE/gui_origin.log"
