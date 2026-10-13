#!/bin/zsh
# Re-creates pantry/a6_bl_file_export.png: Blender 5.1.2's own window (UI scale 2, scratch prefs copied from evidence/blender_config),
# the lantern built by evidence/assets/build_lantern.py, File menu opened by a simulated click on "File", the pointer glides to
# "Export", and the Right-arrow key opens its submenu (glTF 2.0 (.glb/.gltf) is its last row). Nothing is clicked inside the submenu,
# nothing is exported; Blender quits by itself. One Blender window, ~8 s.
HERE="${0:A:h}"
export BLENDER_USER_CONFIG="$HERE/blender_config"
cd "$HERE"
A6_OPEN=click A6_KEYS=RIGHT_ARROW A6_HOVER0=0.6 A6_SNAPWAIT=1.5 \
  timeout 120 /Applications/Blender.app/Contents/MacOS/Blender --enable-event-simulate --python-exit-code 1 \
  --python "$HERE/gui_file_export.py" -- "$HERE/../../pantry/a6_bl_file_export.png" 200 1880 300 738 > "$HERE/gui_file_export.log" 2>&1
echo "exit=$?"
