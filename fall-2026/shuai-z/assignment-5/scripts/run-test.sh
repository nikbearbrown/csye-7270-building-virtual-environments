#!/usr/bin/env bash
# scripts/run-test.sh <project> <test-file> <fps>
#
# The course's wrapper (Assignment 5, "Build It"), changed in four places for
# this folder, which holds two Godot projects:
#   - <project> is game (the 2D game, from Assignment 2) or godot (the 3D props
#     scene, from Assignment 3); the course's version always ran --path godot.
#     The log's name starts with it, so the two projects' logs never collide.
#   - A .tscn test runs as the scene, as the 2D game's checks.tscn always has
#     (its script extends Node, so --script cannot run it); a .gd test still
#     runs with --script.
#   - Godot is $GODOT if set, else godot on PATH, else the macOS app's binary.
#   - It runs from this folder's parent wherever it is called from, so the
#     project paths resolve and the logs land in its logs/.
# Unchanged: the timeout (status 124 means the test hung), the pinned frame
# rate, the log, and failing on any SHADER ERROR or SCRIPT ERROR line, because
# exit code 0 does not mean no errors.
set -o pipefail
cd "$(dirname "$0")/.." || exit 2
if [ $# -ne 3 ] || [ ! -f "$1/project.godot" ]; then
	echo "usage: scripts/run-test.sh <game|godot> <test-file> <fps>" >&2
	exit 2
fi
project=$1
test=$2
fps=$3
godot=${GODOT:-$(command -v godot || echo /Applications/Godot.app/Contents/MacOS/Godot)}
if [[ $test == *.tscn ]]; then
	args=(--fixed-fps "$fps" "res://tests/$test")
else
	args=(--script "res://tests/$test" --fixed-fps "$fps")
fi
mkdir -p logs
log="logs/${project}_$(basename "${test%.*}")_${fps}fps.log"
timeout 120 "$godot" --headless --path "$project" "${args[@]}" 2>&1 | tee "$log"
status=$?
if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log"; then status=1; fi
exit $status
