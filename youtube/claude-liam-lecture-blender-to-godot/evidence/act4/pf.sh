#!/usr/bin/env bash
# pf.sh <Class> ...  : like preflight.sh 4 but KEEPS the scratch (so stills accumulate while iterating). Final proof still uses ./preflight.sh 4 <all classes>.
set -u
HERE="$(cd "$(dirname "$0")/../.." && pwd)"
QC=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc
SCR="/private/tmp/claude-501/lecture-blender-act4"
mkdir -p "$SCR/gateA" "$SCR/stills"
python3 "$HERE/assemble_scenes.py" --out "$SCR" --acts 4 >/dev/null || exit 1
cp "$HERE/beat_sheet.json" "$SCR/"; ln -sfn "$HERE/pantry" "$SCR/pantry"; ln -sfn "$HERE/evidence" "$SCR/evidence"
cp "$SCR/scenes.py" "$SCR/gateA/"
for C in "$@"; do
  echo "=== $C"
  (cd "$SCR/gateA" && python3 "$QC/static_scene_check.py" scenes.py --class "$C" 2>&1 | grep -E "WARN|ERROR|FAIL" | head -6)
  (cd "$SCR" && python3 "$QC/manim_layout_audit.py" scenes.py --class "$C" --curve-strict >/dev/null 2>&1; sed -n '/## /,$p' layout_audit.md | head -14)
  (cd "$SCR" && manim -ql -s --media_dir "$SCR/media" scenes.py "$C" 2>&1 | grep -E "\[pace\]|Traceback|Error|error:" | sed 's/.*\[pace\]/[pace]/' | head -5)
  cp "$SCR/media/images/scenes/${C}_ManimCE_v0.20.1.png" "$SCR/stills/${C}.png" 2>/dev/null || echo "  (no still produced for $C)"
done
