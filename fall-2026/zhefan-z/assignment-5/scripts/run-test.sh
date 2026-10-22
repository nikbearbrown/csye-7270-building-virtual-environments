#!/usr/bin/env bash
# scripts/run-test.sh <test-file.gd> <fps>
# Run from fall-2026/zhefan-z/assignment-5/ in Git Bash.
set -o pipefail
GODOT="/e/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe"
mkdir -p logs
log="logs/$(basename "$1" .gd)_${2}fps.log"
timeout 120 "$GODOT" --headless --path walker-magic-zhefan --script "res://tests/$1" --fixed-fps "$2" 2>&1 | tee "$log"
status=$?
if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log"; then status=1; fi
exit $status
