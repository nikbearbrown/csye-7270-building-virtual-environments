#!/bin/zsh
# run_water.sh <WxH> <out_root> [script names...]: runs the water state scripts through the series launcher (shared Lab lock inside), extracts the marks
set -u
R=/private/tmp/claude-501/water-editor-capture
SIZE="$1"; OUTROOT="$2"; shift 2
NAMES=("$@"); [ ${#NAMES[@]} -eq 0 ] && NAMES=(water-W water-W3c-colour-picker water-W6-ungrouped-compare)
for N in $NAMES; do
  echo "=== $N ($SIZE) $(date +%T)"
  $R/capture_editor_states.sh $R/waterproj - $R/state-scripts/water/$N.json $OUTROOT/$N --size $SIZE --settings $R/settings/editor_settings-single-window.tres --home $R/home 2>&1 | grep -v -E "^next:"
  python3 $R/extract_marks.py $OUTROOT/$N/states.json $OUTROOT/$N/frames $OUTROOT/$N/named --crop-dock 2>&1 | grep -v -i -E "deprecat|getdata|flattened"
  rm -rf $OUTROOT/$N/frames.keep
done
echo "ALL DONE $(date +%T)"
