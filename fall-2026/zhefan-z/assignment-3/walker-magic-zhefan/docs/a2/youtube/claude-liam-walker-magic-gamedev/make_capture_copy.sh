#!/usr/bin/env bash
# Build the isolated capture copy of the game for the film (Git Bash on Windows).
#   bash make_capture_copy.sh <commit> <dest_dir>
# 1. git archive of the committed game folder at <commit> (no working-tree changes, no .godot cache)
# 2. capture-only display override in the copy's project.godot (disclosed in CAPTURE.md):
#    a 3840x2160 root viewport (stretch mode "viewport" kept); the harness draws the 640x360 game
#    into it at x6 (nearest)
# 3. the harness (capture_main.gd + .tscn) and the input-only driver under res://capture/
# 4. two-step import: the game alone first, then again with res://capture/ present
#    (a first import from an empty cache with the capture scripts present crashed Godot 4.7.2
#    at shutdown, twice; importing the game first avoids it)
set -euo pipefail
COMMIT="$1"; DEST="$2"
GODOT="${GODOT:-/e/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe}"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git -C "$HERE" rev-parse --show-toplevel)"
GAME="fall-2026/zhefan-z/assignment-2/walker-magic-zhefan"

rm -rf "$DEST"; mkdir -p "$DEST"
git -C "$REPO" archive "$COMMIT:$GAME" | tar -x -C "$DEST"

python - "$DEST/project.godot" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
s = s.replace("window/size/viewport_width=640", "window/size/viewport_width=3840")
s = s.replace("window/size/viewport_height=360", "window/size/viewport_height=2160")
s = re.sub(r"window/size/window_(width|height)_override=\d+\n", "", s)
# stretch mode stays "viewport": the root viewport is then a fixed 3840x2160 render target even
# when the OS clamps the window to a smaller screen (seen: 2564x1570), and Movie Maker records it.
# Integer scaling is dropped so the preview window shows the whole 4K root scaled down (with
# integer scaling it showed only the top-left 2564x1570 and the aim cursor was clamped there).
s = s.replace('window/stretch/scale_mode="integer"\n', "")
open(p, "w", encoding="utf-8").write(s)
PY

"$GODOT" --headless --path "$DEST" --import > "$DEST/../import-$COMMIT-game.log" 2>&1
mkdir -p "$DEST/capture"
cp "$HERE/capture_main.gd" "$HERE/capture_driver.gd" "$DEST/capture/"
printf '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://capture/capture_main.gd" id="1"]\n\n[node name="CaptureMain" type="Node"]\nscript = ExtResource("1")\n' > "$DEST/capture/capture_main.tscn"
"$GODOT" --headless --path "$DEST" --import > "$DEST/../import-$COMMIT-capture.log" 2>&1
echo "capture copy ready: $DEST (source $COMMIT)"
