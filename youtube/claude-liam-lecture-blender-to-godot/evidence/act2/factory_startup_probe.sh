#!/usr/bin/env bash
# Act II, B14 evidence: does --factory-startup really skip personal settings (not only startup.blend)?
# Make a private config dir with a saved user preference (UI scale 1.5), then read the preference with and without --factory-startup.
# The private dir is created under the scratch area and removed; the user's real Blender config is never touched (BLENDER_USER_CONFIG points elsewhere).
set -u
B=/Applications/Blender.app/Contents/MacOS/Blender
CFG=$(mktemp -d /private/tmp/claude-501/blender-cfg.XXXXXX)
export BLENDER_USER_CONFIG="$CFG"
{
  echo "# Blender $($B --version | head -1 | sed 's/Blender //')"
  echo "# 1. save a personal setting (UI scale 1.5) into a private config dir"
  $B -b --python-expr "import bpy; bpy.context.preferences.view.ui_scale = 1.5; bpy.ops.wm.save_userpref(); print('SAVED ui_scale', bpy.context.preferences.view.ui_scale)" 2>&1 | grep -E "SAVED|Error"
  echo "# 2. a normal start reads it back"
  $B -b --python-expr "import bpy; print('ui_scale', bpy.context.preferences.view.ui_scale)" 2>&1 | grep -E "^ui_scale"
  echo "# 3. with --factory-startup the saved setting is skipped"
  $B -b --factory-startup --python-expr "import bpy; print('ui_scale', bpy.context.preferences.view.ui_scale)" 2>&1 | grep -E "^ui_scale"
} | tee factory_startup_transcript.txt
rm -rf "$CFG"
