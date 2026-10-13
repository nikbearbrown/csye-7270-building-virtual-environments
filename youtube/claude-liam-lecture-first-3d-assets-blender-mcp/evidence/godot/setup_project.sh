#!/bin/zsh
# Builds the scratch Godot project in /private/tmp (not in the repo): the three good .glb, the four wrong ones, the scene, the check.
HERE="${0:A:h}"
ASSETS="$HERE/../assets"
PROJ=/private/tmp/claude-501/a3film/godot_proj
mkdir -p "$PROJ/assets" "$PROJ/variants" "$PROJ/tests"
cp "$HERE/project_src/project.godot" "$PROJ/project.godot"
cp "$HERE/project_src/showcase.tscn" "$PROJ/showcase.tscn"
cp "$HERE/project_src/tests/"*.gd "$PROJ/tests/"
cp "$ASSETS/crate.glb" "$ASSETS/lantern.glb" "$ASSETS/coin.glb" "$PROJ/assets/"
# the four deliberately wrong exports (log kept beside this script)
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python "$HERE/build_variants.py" -- "$PROJ/variants" > "$HERE/build_variants.log" 2>&1
echo "setup: $(ls $PROJ/assets | wc -l | tr -d ' ') good + $(ls $PROJ/variants | wc -l | tr -d ' ') wrong .glb in $PROJ"
