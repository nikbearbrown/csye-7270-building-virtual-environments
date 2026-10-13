#!/usr/bin/env bash
# Re-creates every piece of Act IV evidence under evidence/act4/out/ (needs Blender 5.1.2 and Godot 4.7.2 on this Mac; ~1 minute).
#   ./reproduce.sh            all of it
# Logs written: out/forms-diff.log  out/probe-nodes-lights.log  out/exporter-labels.log  out/suffix-probe.log  out/lights-probe.log
set -eu
cd "$(dirname "$0")"
BL=/Applications/Blender.app/Contents/MacOS/Blender
mkdir -p _run/tools/blender out
cp ../scratch/tools/blender/build_checkpoint_post.py _run/tools/blender/        # the final agent script, unchanged
# 1. the real post in both glTF forms, then PostMetal's metallic 0.8 -> 0.2 in both  (B33A, B35, B36)
$BL -b --factory-startup --python-exit-code 1 --python export_forms.py >/dev/null 2>&1
cmp out/a_glb/checkpoint_post.glb ../../../../examples/03-blender-mcp-to-godot/checkpoint_post.glb && echo "glb is byte-identical to examples/03's checkpoint_post.glb"
./forms_diff.sh >/dev/null
# 2. does a Blender-only shader node cross?  does a light?  and what does the exporter call the option?  (B36)
$BL -b --factory-startup --python-exit-code 1 --python probe_nodes_lights.py 2>&1 | grep -v "INFO" | grep -E "^export_lights|PROBE_DONE" > out/probe-nodes-lights.log
$BL -b --factory-startup --python-exit-code 1 --python exporter_labels.py 2>&1 | grep -E "^export_|LABELS_DONE" > out/exporter-labels.log
cp out/probe/probe_lights_on.glb out/probe/probe_lights_off.glb lights_probe/
( cd lights_probe && rm -rf .godot && godot --headless --path . --import >/dev/null 2>&1
  godot --headless --path . --script res://print_tree.gd 2>&1 | grep -E "^(==|Node3D|  )" > ../out/lights-probe.log
  godot --headless --path . --script res://classdb.gd 2>&1 | grep exists >> ../out/lights-probe.log )
# 3. one mesh under five suffix names + an empty, imported three ways in Godot 4.7.2  (B38-B41)
$BL -b --factory-startup --python-exit-code 1 --python make_suffix_probe.py >/dev/null 2>&1
./run_suffix_probe.sh > out/suffix-probe.log 2>&1
# 4. the Godot docs pages quoted in the film (text) and the B42 capture (public page, no sign-in; stops if a bot-challenge page is served)
B=https://docs.godotengine.org/en/stable/tutorials
python3 fetch_docs_text.py $B/assets_pipeline/importing_3d_scenes/available_formats.html docs_text/available_formats.txt
python3 fetch_docs_text.py $B/assets_pipeline/importing_3d_scenes/node_type_customization.html docs_text/node_type_customization.txt
python3 fetch_docs_text.py $B/physics/collision_shapes_3d.html docs_text/collision_shapes_3d.txt
python3 capture_collision_page.py /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/lecture-blender-to-godot/a4_collision_shapes_3d.png out/collision-capture.json
python3 crop_pantry.py
echo done
