#!/bin/zsh
# run_cost_repeats.sh [N]: repeats the wall-clock stress test (verify_g_cost.gd) N more times (default 4) in a throw-away project and saves each run as run-g-repeat-<i>.log.
# The test's absolute times move a little from run to run with what else the Mac is doing (the first valid runs read 10.3 to 10.6 ms for the ten read loop), so the film quotes the
# median of all valid runs. analyze_cost.py reads run-g-verify_g_cost.log and every run-g-repeat-*.log. Keep other windows off the Godot window while this runs.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; FILM="$(cd "$HERE/../.." && pwd)"
SCR="${TMPDIR:-/tmp}/outline-film-cost-project"; rm -rf "$SCR"; mkdir -p "$SCR"
cp "$HERE/project.godot" "$HERE"/ol_lib.gd "$HERE"/verify_g_cost.gd "$SCR"/
export OUTLINE_FILM_DIR="$FILM"
n="${1:-4}"
find "$HERE" -maxdepth 1 -name "run-g-repeat-[0-9].log" -delete
for i in $(seq 1 "$n"); do
  ( cd "$SCR" && godot --path "$SCR" --script res://verify_g_cost.gd -- --out "$HERE/png" ) > "$HERE/run-g-repeat-$i.log" 2>&1
  echo "repeat $i: exit $?  ($(grep -c '^RESULT' "$HERE/run-g-repeat-$i.log") RESULT lines)"
done
