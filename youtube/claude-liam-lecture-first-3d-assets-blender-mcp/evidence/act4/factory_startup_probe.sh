#!/bin/zsh
# B39A evidence: does --factory-startup skip the user's own PREFERENCES as well as startup.blend?
# Uses a COPY of the reel's scratch Blender config (evidence/blender_config: ui_scale 2.0), never the real user config. Read-only probe.
cd "${0:A:h}"
B=/Applications/Blender.app/Contents/MacOS/Blender
CFG=/private/tmp/claude-501/a4scratch/blender_config_copy
rm -rf $CFG; mkdir -p $CFG; cp ../blender_config/userpref.blend $CFG/
EXPR="import bpy; p=bpy.context.preferences; print('PROBE ui_scale', p.view.ui_scale, '| show_splash', p.view.show_splash)"
{ echo "# user config = a copy of evidence/blender_config (its userpref.blend sets ui_scale 2.0, splash off)"
  echo "\$ BLENDER_USER_CONFIG=<copy> Blender -b --python-expr \"$EXPR\""
  BLENDER_USER_CONFIG=$CFG "$B" -b --python-expr "$EXPR" 2>&1 | grep PROBE
  echo "\$ BLENDER_USER_CONFIG=<copy> Blender -b --factory-startup --python-expr \"$EXPR\""
  BLENDER_USER_CONFIG=$CFG "$B" -b --factory-startup --python-expr "$EXPR" 2>&1 | grep PROBE
} > factory_startup_probe.log
cat factory_startup_probe.log
