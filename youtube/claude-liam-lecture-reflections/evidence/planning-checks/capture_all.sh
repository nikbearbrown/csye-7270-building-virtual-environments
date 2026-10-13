#!/bin/zsh
# capture_all.sh <output dir> [scratch project dir] [--only C07,C08] [--dry-run]
# Records the film's Godot captures, one fresh Godot process each (capture_scene.sh), every clip at the length of the beat that uses it:
# the beat's measured audio length when beat_sheet.json has actual_duration_s (after generate_audio_kokoro.py), else the layout's estimate.
# File names come from the lanes (capture_list.py). <output dir> is normally brutalist.art/runtime/remotion/public/reflections.
# --dry-run prints the plan (capture, file, beat, seconds, source) and records nothing.
# Frames of each clip stay in ${FRAMES_DIR:-${TMPDIR:-/private/tmp}/reflections-capture-frames}/<file>.mp4.frames/ (outside the output folder) until you have
# LOOKED at the video; delete that folder yourself afterwards.
set -eu
POS=(); ONLY=""; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --only) ONLY="${2:?--only needs a list like C07,C08}"; shift 2 ;;
    *) POS+=("$1"); shift ;;
  esac
done
OUT="${POS[1]:?usage: capture_all.sh <output dir> [scratch project dir] [--only C07,C08] [--dry-run]}"
PROJ="${POS[2]:-${TMPDIR:-/private/tmp}/reflections-capture-project}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
PLAN="$(python3 "$HERE/capture_list.py")"
for line in "${(@f)PLAN}"; do
  parts=("${(@s:	:)line}")                       # split on tab
  cid="${parts[1]}"; name="${parts[2]}"; beat="${parts[3]}"; secs="${parts[4]}"; src="${parts[5]}"
  if [ -n "$ONLY" ] && [[ ",$ONLY," != *",$cid,"* ]]; then continue; fi
  echo "$cid  $name  (beat $beat, $secs s, $src)"
  [ "$DRY" = 1 ] && continue
  "$HERE/capture_scene.sh" "$cid" "$OUT/$name" "$PROJ" --length "$secs"
done
