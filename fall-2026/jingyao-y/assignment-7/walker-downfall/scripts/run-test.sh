#!/usr/bin/env bash
# scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]
# The A7 course wrapper, adapted to this repository: the Godot project is the
# repository root (--path .), and Godot is not on PATH here, so GODOT defaults
# to the console build five folders above the project (D:\CSYE 7370).
# It does everything A6's did and adds one thing: a resource-load failure
# ("Failed loading resource") now fails the run. The optional third argument
# sets the timeout; TEST_TIMEOUT is still honoured when it is absent.
set -o pipefail
cd "$(dirname "$0")/.."
GODOT="${GODOT:-$(cd ../../../../.. && pwd)/Godot_v4.7.2-stable_win64_console.exe}"
mkdir -p logs
if [ "$2" = "realtime" ]; then
	fps_args=(); tag="realtime"
else
	fps_args=(--fixed-fps "$2"); tag="${2}fps"
fi
log="logs/$(basename "$1" .gd)_${tag}.log"
timeout "${3:-${TEST_TIMEOUT:-120}}" "$GODOT" --headless "${fps_args[@]}" --path . --script "res://tests/$1" 2>&1 | tee "$log"
status=$?
if grep -qE "SHADER ERROR|SCRIPT ERROR|Failed loading resource" "$log"; then status=1; fi
exit $status
