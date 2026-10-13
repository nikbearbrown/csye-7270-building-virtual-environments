#!/bin/zsh
# make-editor-project.sh <output dir>: builds the scratch pond project for the editor frames E1 and E2 (see make_editor_project.gd).
# Run from anywhere. Needs `godot` on PATH (4.7.2). Writes into <output dir> and a throwaway stage folder next to it (removed at the end);
# use a scratch dir, never a project you work in.
set -eu
OUT="${1:?usage: make-editor-project.sh <output dir>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$(dirname "$OUT")"
STAGE="$(mktemp -d "$(dirname "$OUT")/pondstage.XXXXXX")"   # a throwaway project to run the first script from (next to the output, removed at the end)
printf 'config_version=5\n[application]\nconfig/name="stage"\n' > "$STAGE/project.godot"
cp "$HERE/pond_common.gd" "$HERE/make_editor_project.gd" "$STAGE/"
godot --headless --path "$STAGE" --script res://make_editor_project.gd -- "$OUT" assets
cp "$HERE/pond_common.gd" "$HERE/make_editor_project.gd" "$OUT/"
godot --headless --path "$OUT" --import >/dev/null 2>&1 || true
godot --headless --path "$OUT" --script res://make_editor_project.gd -- "$OUT" scene
rm -f "$OUT/pond_common.gd" "$OUT/make_editor_project.gd"* "$OUT/pond_common.gd"*
rm -rf "$STAGE"
ls -la "$OUT"
