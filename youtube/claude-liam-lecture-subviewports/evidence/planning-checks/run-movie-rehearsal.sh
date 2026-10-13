#!/bin/zsh
# SubViewports film: rehearses the RECORDING route (Godot Movie Maker) for this film's capture scenes, in a scratch project (default /private/tmp/claude-501/godot-shaders-subviewports/movie-proj).
# movie_scene.gd is the adapter the build uses: it builds one CaptureScene and steps it by 1/30 s per rendered frame (the scene never reads the wall clock).
#   run-13   scene c21 (Update Mode Once), 400 frames, window ON TOP: left picture follows, right picture freezes at 8.5 s
#   run-13b  the first 8 frames of every scene: frame 0 can lack the pictures
#   run-13d  the pre-roll: with skip=1 the first file is blank and the second already shows the picture at t = 0 (drop the first)
#   run-13c  the same 400 frames three ways: window on top, window at 0,0, default placement. Only the first two are asserted: at default placement a covered window is not drawn
#            on every frame, so the movie holds repeated frames (73 distinct of 400 was seen once, 400 of 400 other times)
# Frames are PNG files in the scratch folder (large); only the numbers are kept in logs/. Needs Pillow and numpy for analyze-movie.py.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
W="${SV_MOVIE_SCRATCH:-/private/tmp/claude-501/godot-shaders-subviewports/movie-proj}"
LOGS="$HERE/logs"; mkdir -p "$LOGS" "$W"
cp "$HERE/capture_scene.gd" "$HERE/common.gd" "$HERE/movie_scene.gd" "$HERE/movie_main.tscn" "$W/"
cp "$HERE/movie-project.godot" "$W/project.godot"
godot --headless --path "$W" --import >/dev/null 2>&1
record() {   # outdir frames scene [engine flags...]      (EXTRA="skip=1 speed=0.95" adds adapter arguments after the scene id)
  local out="$W/$1"; local n="$2"; local scene="$3"; shift 3
  mkdir -p "$out"
  ( cd "$W" && timeout 300 godot --path . "$@" --write-movie "$out/f.png" --fixed-fps 30 --quit-after "$n" -- "$scene" ${=EXTRA:-} 2>&1 ) | grep -E "frames at"
}
echo "== run-13 c21 in Movie Maker, window on top"
record mm-c21 400 c21 --always-on-top > "$LOGS/run-13-movie-maker-c21-on-top.log"
python3 "$HERE/analyze-movie.py" once "$W/mm-c21" >> "$LOGS/run-13-movie-maker-c21-on-top.log"
echo "== run-13b first frames of every scene"
: > "$LOGS/run-13b-movie-maker-first-frames.log"
for sid in c01 c02 c03 c04a c04b c05 c06 c07 c08 c09 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21; do
  record "mm-first-$sid" 10 "$sid" --always-on-top > /dev/null
done
python3 "$HERE/analyze-movie.py" first "$W/mm-first-" c01 c02 c03 c04a c04b c05 c06 c07 c08 c09 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 >> "$LOGS/run-13b-movie-maker-first-frames.log"
echo "== run-13d the pre-roll: skip=1 holds frame 0 at t = 0, so the first kept frame has the picture"
EXTRA="skip=1" record mm-skip-c07 6 c07 --always-on-top > /dev/null
python3 "$HERE/analyze-movie.py" first "$W/mm-skip-" c07 > "$LOGS/run-13d-movie-maker-pre-roll.log"
echo "== run-13c distinct frames by window placement"
: > "$LOGS/run-13c-movie-maker-window-placement.log"
echo "window on top (--always-on-top)" >> "$LOGS/run-13c-movie-maker-window-placement.log"
record mm-top 400 c21 --always-on-top >> "$LOGS/run-13c-movie-maker-window-placement.log"
python3 "$HERE/analyze-movie.py" distinct "$W/mm-top" 400 >> "$LOGS/run-13c-movie-maker-window-placement.log"
echo "window at 0,0 (--position 0,0)" >> "$LOGS/run-13c-movie-maker-window-placement.log"
record mm-pos 400 c21 --position 0,0 >> "$LOGS/run-13c-movie-maker-window-placement.log"
python3 "$HERE/analyze-movie.py" distinct "$W/mm-pos" 400 >> "$LOGS/run-13c-movie-maker-window-placement.log"
echo "default placement (informational, not asserted)" >> "$LOGS/run-13c-movie-maker-window-placement.log"
record mm-default 400 c21 >> "$LOGS/run-13c-movie-maker-window-placement.log"
python3 "$HERE/analyze-movie.py" distinct "$W/mm-default" 400 >> "$LOGS/run-13c-movie-maker-window-placement.log"
echo "done: logs in $LOGS"
