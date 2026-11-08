#!/usr/bin/env bash
# scripts/run-test.sh <test-file> <fps|realtime> [timeout-seconds]
#
# The course's Assignment 6 wrapper, changed in four places for this folder:
#   - The project is game/ (the 2D game, from Assignment 2), so it runs
#     --path game; the course's version runs --path godot. Assignment 6 builds
#     in the 2D game only, so this folder holds no other project.
#   - A .tscn test runs as the scene, as the game's checks.tscn always has (its
#     script extends Node, so --script cannot run it); a .gd test still runs
#     with --script. The log is named after the file without its extension.
#   - Godot is $GODOT if set, else godot on PATH, else the macOS app's binary.
#   - It runs from this folder wherever it is called from, so the project path
#     resolves and the logs land in its logs/.
# Unchanged from the course: the realtime mode (no --fixed-fps, for tests that
# wait on audio), the optional timeout (120 s by default; status 124 means the
# test hung), the log name logs/<test>_<fps>fps.log or logs/<test>_realtime.log,
# and failing on any SHADER ERROR or SCRIPT ERROR line, because exit code 0
# does not mean no errors.
set -o pipefail
cd "$(dirname "$0")/.." || exit 2
if [ $# -lt 2 ] || [ $# -gt 3 ] || [ ! -f "game/tests/$1" ]; then
	echo "usage: scripts/run-test.sh <test-file in game/tests/> <fps|realtime> [timeout-seconds]" >&2
	exit 2
fi
godot=${GODOT:-$(command -v godot || echo /Applications/Godot.app/Contents/MacOS/Godot)}
if [ "$2" = "realtime" ]; then
	fps_args=(); tag="realtime"
else
	fps_args=(--fixed-fps "$2"); tag="${2}fps"
fi
if [[ $1 == *.tscn ]]; then
	run_args=("res://tests/$1")
else
	run_args=(--script "res://tests/$1")
fi
mkdir -p logs
log="logs/$(basename "${1%.*}")_${tag}.log"
timeout "${3:-120}" "$godot" --headless "${fps_args[@]}" --path game "${run_args[@]}" 2>&1 | tee "$log"
status=$?
if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log"; then status=1; fi
exit $status
