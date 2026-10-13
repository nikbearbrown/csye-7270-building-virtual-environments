#!/bin/zsh
# run_all.sh <size WxH> <out_root> [script names...]
# Runs every final state script (or only the named ones) through capture_editor_states.sh, then extracts the named stills.
# Settings: all scripts run with the single-window settings (popups are drawn inside the window, so Movie Maker records them);
# tc-E3 also shows the renderer selector. Compare runs with the factory settings: see run_factory_compare.sh.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SIZE="$1"; OUTROOT="$2"; shift 2
NAMES=("$@")
[ ${#NAMES[@]} -eq 0 ] && NAMES=(pilot-E1 pilot-E2 pilot-E3 drawing-shapes-E1-default-width drawing-shapes-E1-wide-inspector local-world-E1-clean-root local-world-E1-plan-exact-root-is-Parent tc-E1 tc-E2 tc-E3)
for N in $NAMES; do
  SET="$HERE/settings/editor_settings-single-window.tres"
  [ "$N" = "tc-E3" ] && SET="$HERE/settings/editor_settings-single-window-renderer-selector.tres"
  SC="$(python3 -c "import json,sys;d=json.load(open('$HERE/state-scripts/final/$N.json'));print({'pilot-E1':'e1_sprite'}.get('$N',''))")"
  echo "=== $N ($SIZE)"
  "$HERE/capture_editor_states.sh" "$HERE/proj" - "$HERE/state-scripts/final/$N.json" "$OUTROOT/$N" --size "$SIZE" --settings "$SET" 2>&1 | grep -v -E "^next:" 
  python3 "$HERE/extract_marks.py" "$OUTROOT/$N/states.json" "$OUTROOT/$N/frames" "$OUTROOT/$N/named" --crop-dock 2>&1 | grep -v -i -E "deprecat|getdata|flattened"
done
