#!/bin/zsh
# SubViewports film: records the film's editor frames with the SERIES' editor driver (../../_godot-shaders-series/editor-capture/README.md): the whole editor
# (the driver sizes the window to 3456 x 1944, Movie Maker resamples it to 1920 x 1080, so the title bar and the bottom strip are in the frame), popups included
# (Single Window Mode on), under the shared Lab lock. The state scripts are editor-driver/state-scripts/subviewports-E1.json (B04), -E4 (B12 and B10), -E3 (B32), and the same three with -wide (the Inspector dock widened so long labels read in full).
# One difference from the series' own runs: a `godot` wrapper puts --always-on-top on every Godot process this script starts, because a covered window is not drawn on
# every frame (RESULTS.md, the covered window). Nothing in the series folder is edited; the driver plugin is copied into a scratch project.
# Output: editor-frames/series-driver/<mark>.png (1920 x 1080) and logs/run-15-series-driver-*.log. About three minutes, longer if the lock is held.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
SER="$(cd "$FILM/../_godot-shaders-series" && pwd)"
EC="$SER/editor-capture"
SCR="/private/tmp/claude-501/godot-shaders-subviewports"
LOGS="$HERE/logs"; DEST="$HERE/editor-frames/series-driver"; mkdir -p "$LOGS" "$DEST"
STAMP="$(date +%H%M%S)"
# the wrapper: the same Godot with --always-on-top
REAL="$(command -v godot)"; REAL="${REAL:A}"
WRAP="$SCR/godot-on-top"; mkdir -p "$WRAP"
printf '#!/bin/zsh\nexec "%s" --always-on-top "$@"\n' "$REAL" > "$WRAP/godot"; chmod +x "$WRAP/godot"
for name in subviewports-E1 subviewports-E4 subviewports-E3 subviewports-E1-wide subviewports-E4-wide subviewports-E3-wide; do
  PROJ="$SCR/sv-editor-driver-$name-$STAMP"; OUT="$SCR/sv-editor-driver-out-$name-$STAMP"
  mkdir -p "$PROJ/addons"
  cp -R "$HERE/editor-driver/." "$PROJ/"
  cp -R "$EC/proj/addons/driver" "$PROJ/addons/"
  echo "== $name"
  PATH="$WRAP:$PATH" "$EC/capture_editor_states.sh" "$PROJ" - "$PROJ/state-scripts/$name.json" "$OUT" --size 1920x1080 --home "$SCR/editor-home" --settings "$EC/settings/editor_settings-single-window.tres" > "$LOGS/run-15-series-driver-$name.log" 2>&1
  python3 "$EC/extract_marks.py" "$OUT/states.json" "$OUT/frames" "$OUT/named" >> "$LOGS/run-15-series-driver-$name.log" 2>&1
  cp "$OUT/named/"*.png "$DEST/" 2>/dev/null
  tail -4 "$LOGS/run-15-series-driver-$name.log" | cut -c1-200
done
echo "done: frames in $DEST"
