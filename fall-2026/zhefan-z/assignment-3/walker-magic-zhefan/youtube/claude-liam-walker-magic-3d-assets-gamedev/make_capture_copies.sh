#!/usr/bin/env bash
# Build the three isolated copies of the game for the Assignment 3 film (Git Bash on Windows).
#   bash make_capture_copies.sh <commit> <base_dir>
#
#   <base_dir>/snapshot  git archive of walker-magic-zhefan at <commit>; never run.
#                        The godot-gamedev checker's --game folder (hashes and line numbers).
#   <base_dir>/ref       the same archive, imported; used for the headless check and the .glb read.
#   <base_dir>/capture   the same archive plus two capture-only changes, disclosed in CAPTURE.md:
#                        a 3840x2160 root viewport in project.godot (stretch mode "viewport" kept,
#                        window overrides and integer scaling removed), and the camera harness under
#                        res://capture/. Two-step import, as in Assignment 2: the game first, then
#                        again with res://capture/ present.
#
# Nothing in the repository is changed; the archive is written to a file, not piped.
set -euo pipefail
COMMIT="$1"; BASE="$2"
GODOT="${GODOT:-/e/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe}"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git -C "$HERE" rev-parse --show-toplevel)"
GAME="fall-2026/zhefan-z/assignment-3/walker-magic-zhefan"

for d in snapshot ref capture; do
  if [ -e "$BASE/$d" ]; then echo "refusing: $BASE/$d already exists" >&2; exit 1; fi
done
mkdir -p "$BASE"
TAR="$BASE/walker-magic-zhefan-$COMMIT.tar"
git -C "$REPO" archive -o "$TAR" "$COMMIT:$GAME"
for d in snapshot ref capture; do mkdir "$BASE/$d"; tar -xf "$TAR" -C "$BASE/$d"; done

python - "$BASE/capture/project.godot" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
for old, new in (("window/size/viewport_width=640", "window/size/viewport_width=3840"),
                 ("window/size/viewport_height=360", "window/size/viewport_height=2160")):
    assert s.count(old) == 1, old
    s = s.replace(old, new)
s = re.sub(r"window/size/window_(width|height)_override=\d+\n", "", s)
s = s.replace('window/stretch/scale_mode="integer"\n', "")
open(p, "w", encoding="utf-8").write(s)
PY

"$GODOT" --headless --path "$BASE/ref" --import > "$BASE/import-ref.log" 2>&1
"$GODOT" --headless --path "$BASE/capture" --import > "$BASE/import-capture-game.log" 2>&1
mkdir -p "$BASE/capture/capture"
cp "$HERE/capture_prop_room.gd" "$BASE/capture/capture/"
printf '[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://capture/capture_prop_room.gd" id="1"]\n\n[node name="CapturePropRoom" type="Node3D"]\nscript = ExtResource("1")\n' > "$BASE/capture/capture/capture_prop_room.tscn"
"$GODOT" --headless --path "$BASE/capture" --import > "$BASE/import-capture-harness.log" 2>&1
echo "copies ready in $BASE (source $COMMIT)"
