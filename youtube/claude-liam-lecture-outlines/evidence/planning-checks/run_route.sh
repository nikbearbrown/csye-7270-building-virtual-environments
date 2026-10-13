#!/bin/zsh
# run_route.sh [scene ids...]: plays every scene spec through the 1280 x 720 route and the 3840 x 2160 SubViewport route
# at the film's 50 % and 85 % frames. The big PNGs go to a scratch folder (not the film); analyze_route.py compares them and writes route-summary.txt.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; FILM="$(cd "$HERE/../.." && pwd)"
OUT="${TMPDIR:-/tmp}/outline-film-route-png"; rm -rf "$OUT"; mkdir -p "$OUT"
SCR="${TMPDIR:-/tmp}/outline-film-route-project"; rm -rf "$SCR"; mkdir -p "$SCR"
cp "$HERE/project.godot" "$HERE"/ol_lib.gd "$HERE"/padding_snippet.gd "$HERE"/select_snippet.gd "$HERE"/scene_player.gd "$HERE"/route_check.gd "$SCR"/
cd "$SCR"
for f in "$HERE"/scenes/*.json; do
  id="$(basename "$f" .json)"
  [ $# -gt 0 ] && [[ ! " $* " == *" ${id%%-*} "* ]] && [[ ! " $* " == *" $id "* ]] && continue
  extra=()
  case "$id" in C26-*) extra=(--times 0.05,3.36,6.08);; esac      # scripted keys: before any key, after the first, after the second
  OUTLINE_FILM_DIR="$FILM" timeout 120 godot --path "$SCR" --script res://route_check.gd -- --spec "$f" --out "$OUT" "${extra[@]}" 2>&1 | grep -E "RESULT|SCRIPT ERROR|ERROR: [^1]|Parse Error" | sed "s/^/$id /" | cut -c1-200
done
echo "PNG folder: $OUT"
