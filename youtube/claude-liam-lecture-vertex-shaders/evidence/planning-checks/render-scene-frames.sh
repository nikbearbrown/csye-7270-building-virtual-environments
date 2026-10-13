#!/bin/zsh
# render-scene-frames.sh: runs every capture scene of scratch-project/capture_scenes.gd in real time and keeps frames (png/scene-<id>-t<time>.png)
# so each planned capture can be LOOKED at before the build session records it offline. D = 12 s unless noted. Re-run: ./render-scene-frames.sh
cd "$(dirname "$0")"
run() { ./run-scene.sh "$1" "$2" --duration 12 | grep -E "ERROR|SCRIPT"; echo "done $1"; }
run slide 1.0,4.0
run local 1.0,8.0
run squash 1.0,6.0
run lean 1.0,10.0
run triptych 0.5,3.0
run tilt 1.0,9.0
run mesh-recipe 1.0,8.5,11.0
run pair 0.5,3.0
run densities 0.5,3.0
run cut-along 0.5,3.0
run polygon 0.5,3.0
run travel 2.0,8.0,8.2,8.4,8.6
run pinned 1.0,1.2,1.4,1.6,6.0,6.2,6.4,6.6
run dials-rest 2.0
run sweeps 1.0,2.0,5.0,8.0
run wind 3.0,11.0
run lit 3.0,10.0
run final 3.0
run flat-mesh 1.0
run stripes 1.0
run flip 3.0,9.0
run vertex-two 1.0,6.0,10.0
run polygon-uv 4.0
run drawing-only 1.0,6.0
run equiv-lit-color 1.5
run polygon-grid 1.0
echo ALLDONE
