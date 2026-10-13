#!/bin/zsh
# run_scene.sh <scene id or path to a spec> [run_scene.gd options after --]  : copies the player into a throw-away project and plays one spec (timeout 90 s).
#   ./run_scene.sh C13-thickness-steps --times 0.5,3
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; FILM="$(cd "$HERE/../.." && pwd)"
SPEC="$1"; shift
[ -f "$SPEC" ] || SPEC="$HERE/scenes/$SPEC.json"
SCR="${TMPDIR:-/tmp}/outline-film-scene-project"; rm -rf "$SCR"; mkdir -p "$SCR" "$HERE/png/scenes"
cp "$HERE/project.godot" "$HERE"/ol_lib.gd "$HERE"/padding_snippet.gd "$HERE"/select_snippet.gd "$HERE"/scene_player.gd "$HERE"/run_scene.gd "$SCR"/
cd "$SCR" && OUTLINE_FILM_DIR="$FILM" timeout 90 godot --path "$SCR" --script res://run_scene.gd -- --spec "$SPEC" --out "$HERE/png/scenes" "$@" 2>&1 | grep -E "RESULT|SCRIPT ERROR|ERROR: [^1]|Parse Error" 
