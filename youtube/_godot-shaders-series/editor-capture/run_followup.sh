#!/bin/zsh
# run_followup.sh <WxH> <run_root>
# The renderer-path follow-up at ONE movie size: editor session, Project Manager session, fresh-HOME session; then extract the named stills.
# Every session takes the shared Lab lock itself (capture_editor_states.sh / run_pm.sh): mkdir, refreshed every 30 s, rmdir in a trap.
#   <run_root>/editor/{frames,states.json,named}   <run_root>/pm/...   <run_root>/fresh/...
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SIZE="$1"; ROOT="$2"
SCRIPTS="$HERE/state-scripts/followup"
mkdir -p "$ROOT"
python3 "$HERE/make_followup_scripts.py" "$SCRIPTS" > /dev/null
EXT() { python3 "$HERE/extract_marks.py" "$1/states.json" "$1/frames" "$1/named" 2>&1 | grep -v -i -E "deprecat|getdata|flattened"; }

echo "=== editor session ($SIZE)"
# a fresh clone every time: Project Settings edits (the script reverts them) can never reach the master scratch project
rsync -a --delete --exclude ".godot/editor" --exclude state_script.json "$HERE/proj/" "$HERE/proj-settings/"
"$HERE/capture_editor_states.sh" proj-settings - "$SCRIPTS/rp-editor.json" "$ROOT/editor" --size "$SIZE" --settings "$HERE/settings/editor_settings-single-window-embedded-menu.tres" 2>&1 | grep -E "lock|godot exit|driver log|ERROR frame"
EXT "$ROOT/editor"

echo "=== Project Manager session ($SIZE)"
"$HERE/run_pm.sh" "$SIZE" "$ROOT/pm" "$SCRIPTS/rp-pm.json" --settings "$HERE/settings/editor_settings-factory-after-first-run.tres" 2>&1 | grep -E "lock|godot exit|frames:|PM_DRIVER ERROR"
EXT "$ROOT/pm"

echo "=== fresh HOME session ($SIZE)"
rm -rf "$HERE/home-fresh"; mkdir -p "$HERE/home-fresh"
"$HERE/capture_editor_states.sh" proj-settings - "$SCRIPTS/rp-fresh.json" "$ROOT/fresh" --size "$SIZE" --home "$HERE/home-fresh" 2>&1 | grep -E "lock|godot exit|driver log|ERROR frame"
EXT "$ROOT/fresh"
cp "$HERE/home-fresh/Library/Application Support/Godot/editor_settings-4.7.tres" "$ROOT/fresh/editor_settings-4.7.written-by-the-editor-on-first-run.tres" 2>/dev/null && echo "copied the settings file the editor wrote in the fresh HOME"
