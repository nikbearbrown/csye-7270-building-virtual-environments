#!/bin/zsh
# run_compare.sh <out_root>
# Two controlled comparisons, same state scripts, 1920x1080 frames:
#   A. editor settings: factory (popups are separate OS windows, which Movie Maker does not record) vs single-window mode (popups drawn
#      inside the window). The frames without a popup must be pixel-identical, or single-window mode would not be a fair way to record.
#   B. renderer: Forward+ (Godot's default, what every other run uses) vs Compatibility (--rendering-method gl_compatibility).
# Uses pilot-E1 (Sprite2D, dropdowns, dialog, shader editor) and pilot-E2 (ColorRect, Shader Parameters sliders).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$1"
for N in pilot-E1 pilot-E2; do
  echo "=== factory settings: $N"
  "$HERE/capture_editor_states.sh" "$HERE/proj" - "$HERE/state-scripts/final/$N.json" "$OUT/factory/$N" --size 1920x1080 --settings "$HERE/settings/editor_settings-factory-after-first-run.tres" 2>&1 | grep -E "driver log|ERROR|recorded in"
  python3 "$HERE/extract_marks.py" "$OUT/factory/$N/states.json" "$OUT/factory/$N/frames" "$OUT/factory/$N/named" 2>&1 | grep -v -i -E "deprecat|getdata|flattened" | tail -1
  echo "=== Compatibility renderer, single-window settings: $N"
  "$HERE/capture_editor_states.sh" "$HERE/proj" - "$HERE/state-scripts/final/$N.json" "$OUT/compat/$N" --size 1920x1080 --renderer gl_compatibility --settings "$HERE/settings/editor_settings-single-window.tres" 2>&1 | grep -E "driver log|ERROR|recorded in|Compatibility|OpenGL"
  python3 "$HERE/extract_marks.py" "$OUT/compat/$N/states.json" "$OUT/compat/$N/frames" "$OUT/compat/$N/named" 2>&1 | grep -v -i -E "deprecat|getdata|flattened" | tail -1
done
echo COMPAREDONE
