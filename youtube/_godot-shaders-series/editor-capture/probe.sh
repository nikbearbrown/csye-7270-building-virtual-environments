#!/bin/zsh
# probe.sh <state_script.json> <out_dir> [--size WxH] [--settings FILE]
# One exploratory run on a FRESH clone of the master scratch project (proj -> proj-settings), so Project Settings edits never persist.
# Runs the launcher (shared Lab lock inside), extracts the named stills, prints the driver notes and errors.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$1"; OUT="$2"; shift 2
SIZE=1920x1080; SETTINGS="$HERE/settings/editor_settings-single-window-embedded-menu.tres"
while [ $# -gt 0 ]; do
  case "$1" in
    --size) SIZE="$2"; shift 2;;
    --settings) SETTINGS="$2"; shift 2;;
    *) echo "unknown option $1"; exit 2;;
  esac
done
rsync -a --delete --exclude ".godot/editor" --exclude state_script.json "$HERE/proj/" "$HERE/proj-settings/"
rm -rf "$OUT"
"$HERE/capture_editor_states.sh" proj-settings - "$SCRIPT" "$OUT" --size "$SIZE" --settings "$SETTINGS" 2>&1 | grep -E "driver log|ERROR|lock" | cut -c1-200
python3 "$HERE/extract_marks.py" "$OUT/states.json" "$OUT/frames" "$OUT/named" 2>&1 | grep -v -i -E "deprecat|getdata|flattened" | tail -n +1 | cut -c1-200
