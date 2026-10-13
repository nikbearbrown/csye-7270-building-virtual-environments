#!/bin/zsh
# SubViewports film: reads the REAL text of Godot 4.7.2's Inspector for every property the narration and the screen name (Size, Update Mode, Transparent BG, Texture, Material, Filter,
# Blend Mode, Subdivide Width ...), and records editor frames of those states. Always on a scratch copy (editor-scratch/), never on a project Bear works in.
# The driver is addons/shot/plugin.gd (an EditorPlugin): it selects nodes through EditorInterface and prints `SHOT labels[...]` lines (EditorProperty.label) and `SHOT enum ...` lines
# (the option texts the Inspector offers). Movie Maker records the editor window while it does so (frames stay in the scratch folder); each named state is copied from the movie into editor-frames/ as a 1920 x 1080 PNG (the driver prints `SHOT state <name> frame=<n>`).
# Needs the window ON TOP (--always-on-top): a covered Godot window is not drawn on every frame (RESULTS.md).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="${SV_EDITOR_SCRATCH:-/private/tmp/claude-501/godot-shaders-subviewports/edproj-final}"
LOGS="$HERE/logs"; mkdir -p "$LOGS" "$HERE/editor-frames"
STAMP="$(date +%H%M%S)"
shot() {   # mode scene
  local mode="$1"; local scene="$2"
  # a fresh copy of the scratch project for every pass: the editor remembers open scenes and panels, and a stale tab or an open shader editor would show in the frames
  local W="${BASE}-${mode}-${STAMP}"; mkdir -p "$W"
  cp -R "$HERE/editor-scratch/." "$W/"
  godot --headless --path "$W" --import >/dev/null 2>&1
  local out="${W}-movie"; mkdir -p "$out"   # outside the project folder: the editor would otherwise try to preview the movie's .wav file
  echo "== editor, mode $mode"
  ( cd "$W" && SHOT_MODE="$mode" timeout 300 godot --editor --path . --always-on-top "$scene" --write-movie "$out/f.png" --fixed-fps 30 --quit-after 900 2>&1 ) | grep -E "^SHOT|frames at|Movie Maker" > "$LOGS/run-14-editor-labels-$mode.log"
  grep -c "^SHOT" "$LOGS/run-14-editor-labels-$mode.log"
  # copy the movie frame that shows each named state (three frames before the print)
  python3 - "$LOGS/run-14-editor-labels-$mode.log" "$out" "$HERE/editor-frames" <<'PY'
import re, shutil, sys
log, movie, dest = sys.argv[1:4]
for line in open(log):
    m = re.match(r"SHOT state (\S+) frame=(\d+)", line)
    if m:
        k = int(m.group(2)) - 3   # three frames BEFORE the print: the driver changes the next state right after printing, and the state shown has been settled for a second
        shutil.copyfile(f"{movie}/f{k:08d}.png", f"{dest}/{m.group(1)}.png")
        print("frame", m.group(1), "<- movie frame", k)
PY
}
shot default main.tscn
shot shaders shaders.tscn
shot mesh mesh.tscn
echo "done: logs in $LOGS, frames in $HERE/editor-frames"
