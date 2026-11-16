#!/usr/bin/env bash
# preflight.sh <FILM FOLDER> <ACT-NUMBER> <Class> [<Class> ...]
# Assembles shader_kit.py + the film's scenes_act<N>.py into a PRIVATE scratch folder (so parallel builders never collide), then for each class:
#   1. Gate A static check from a folder holding ONLY scenes.py (exactly what `art run`'s Gate A sees)
#   2. manim_layout_audit --curve-strict (Gate B's text/frame audit), warnings printed
#   3. a low-resolution LAST-FRAME still: <scratch>/stills/<Class>.png (LOOK at it before any 4K render)
# Nothing here touches the film's real scenes.py, manim/, or media/. Adapted from the Why Godot film's preflight.sh.
set -u
FILM="$(cd "$1" && pwd)"; shift
ACT="$1"; shift
HERE="$(cd "$(dirname "$0")" && pwd)"
QC=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc
SLUG="$(basename "$FILM")"
SCR="/private/tmp/claude-501/preflight-${SLUG}-act${ACT}"
rm -rf "$SCR"; mkdir -p "$SCR/gateA" "$SCR/stills"
python3 "$HERE/assemble_scenes.py" "$FILM" --out "$SCR" --acts "$ACT" >/dev/null || exit 1
cp "$FILM/beat_sheet.json" "$SCR/"; for d in pantry evidence; do [ -e "$FILM/$d" ] && ln -sfn "$FILM/$d" "$SCR/$d"; done
cp "$SCR/scenes.py" "$SCR/gateA/"
for C in "$@"; do
  echo "=== $C"
  (cd "$SCR/gateA" && python3 "$QC/static_scene_check.py" scenes.py --class "$C" 2>&1 | grep -E "WARN|ERROR|FAIL|clean" | head -6)
  (cd "$SCR" && python3 "$QC/manim_layout_audit.py" scenes.py --class "$C" --curve-strict >/dev/null 2>&1; sed -n '/## /,$p' layout_audit.md | head -14)
  (cd "$SCR" && manim -ql -s --media_dir "$SCR/media" scenes.py "$C" 2>&1 | grep -E "\[pace\]|Traceback|Error|error:" | sed 's/.*\[pace\]/[pace]/' | head -5)
  cp "$SCR/media/images/scenes/${C}_ManimCE_v0.20.1.png" "$SCR/stills/${C}.png" 2>/dev/null || echo "  (no still produced for $C)"
done
echo "stills: $SCR/stills"
