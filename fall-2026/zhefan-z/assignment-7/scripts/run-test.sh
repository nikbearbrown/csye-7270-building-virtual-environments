#!/usr/bin/env bash
# scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]
# Run from fall-2026/zhefan-z/assignment-6/ in Git Bash.
set -o pipefail
GODOT="/e/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe"
mkdir -p logs
if [ "$2" = "realtime" ]; then
	fps_args=(); tag="realtime"
else
	fps_args=(--fixed-fps "$2"); tag="${2}fps"
fi
log="logs/$(basename "$1" .gd)_${tag}.log"
timeout "${3:-120}" "$GODOT" --headless "${fps_args[@]}" --path walker-magic-zhefan --script "res://tests/$1" 2>&1 | tee "$log"
status=$?
if grep -qE "SHADER ERROR|SCRIPT ERROR|Failed loading resource|Failed to load resource|Parse Error" "$log"; then status=1; fi
exit $status
