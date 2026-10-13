#!/bin/zsh
# Re-runs every GDScript check and every Movie Maker scene of "Time and Waves" into a scratch folder (never inside the film folder, so no .godot cache lands here).
# Usage: ./run-all.sh [out_dir]      (default out_dir: /private/tmp/claude-501/godot-shaders-time-and-waves/rerun)
# The Lab-based checks have their own runners: python3 run_twins.py, python3 run_images.py, ./run-lab-compile.sh (set TWIN_RENDERER=gl_compatibility for Compatibility).
# Every Godot window below is started with --always-on-top: TIME only advances while the window is being drawn, so do not cover or minimize it while this runs.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
OUT="${1:-/private/tmp/claude-501/godot-shaders-time-and-waves/rerun}"
mkdir -p "$OUT/gd" "$OUT/scene-project" "$OUT/logs"
cp -R "$HERE/gd/." "$OUT/gd/"
cp -R "$HERE/scene-project/." "$OUT/scene-project/"

cd "$OUT/gd" || exit 1
for n in 1 2 3; do
  godot --path . --always-on-top --script res://verify1_clocks.gd -- --film "$FILM" > "$OUT/logs/clocks-run$n.log" 2>&1
done
godot --path . --always-on-top --script res://verify1c_minimized.gd > "$OUT/logs/minimized.log" 2>&1
godot --path . --always-on-top --script res://verify2_shown_shaders_vs_TIME.gd -- --film "$FILM" > "$OUT/logs/verify2-forward-plus.log" 2>&1
godot --path . --always-on-top --rendering-method gl_compatibility --script res://verify2_shown_shaders_vs_TIME.gd -- --film "$FILM" > "$OUT/logs/verify2-compatibility.log" 2>&1
godot --path . --always-on-top --script res://verify3_curves_breath_wind.gd -- --film "$FILM" > "$OUT/logs/verify3.log" 2>&1
mkdir -p "$OUT/png"
godot --path . --always-on-top --fixed-fps 30 --script res://verify4_click_and_scene.gd -- --film "$FILM" --png "$OUT/png" > "$OUT/logs/verify4.log" 2>&1
godot --path . --always-on-top --script res://verify5_rollover.gd -- --film "$FILM" > "$OUT/logs/verify5.log" 2>&1
godot --headless --path . --script res://default_rollover.gd > "$OUT/logs/default-rollover.log" 2>&1

cd "$OUT/scene-project" || exit 1
# scene name : frames : extra user args (zsh does not split a plain variable, so the extra arguments are an array per entry)
run_scene() {
  local name="$1" frames="$2" tag="$3"
  shift 3
  rm -rf "frames_$tag" && mkdir "frames_$tag"
  godot --path . --always-on-top --write-movie "frames_$tag/f.png" --fixed-fps 30 --quit-after "$frames" "res://scenes/scene_$name.tscn" -- --verify "$@" > "$OUT/logs/scene-$tag.log" 2>&1
}
run_scene c01_late_join 450 c01_late_join
run_scene c03_scale_pause 360 c03_scale_pause
run_scene c07_age 420 c07_age
run_scene c18_rolling_row 360 c18_rolling_row
run_scene c23_curve_loop 360 c23_curve_loop
run_scene c28_travel 390 c28_travel
run_scene c35_together 360 c35_together_together --part together
run_scene c35_together 300 c35_together_logo --part logo
run_scene c35_together 300 c35_together_banner --part banner
run_scene c40_wind_click 420 c40_wind_click
python3 decode_scenes.py > "$OUT/logs/decode-scenes-act1.txt" 2>&1
python3 decode_scenes2.py > "$OUT/logs/decode-scenes-act2-to-5.txt" 2>&1
echo "wrote $OUT/logs (compare with gd/logs and scene-project/logs in the film folder)"
