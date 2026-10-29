#!/usr/bin/env bash
# ============================================================
# About: the test wrapper A5 asks for (the template from the assignment brief, with two changes for this repository's folders)
# ============================================================
# Usage: ./scripts/run-test.sh <test-file.gd> <fps>
# Example: ./scripts/run-test.sh a3_asset_check.gd 60
# It does four things:
#   1. Wraps Godot in timeout: if a test script errors before quit(), headless Godot keeps running; it is killed after 120 s (exit code 124 = hung)
#   2. Pins the frame rate with --fixed-fps: every frame's delta is 1/fps, whatever the machine's speed
#   3. Keeps a copy of the output as a log in logs/
#   4. Fails when the log contains SHADER ERROR or SCRIPT ERROR (Godot can exit 0 even after such errors)

# ============================================================
# Setting: a pipeline fails if any command in it fails (otherwise only the final tee counts, and tee always succeeds)
# ============================================================
set -o pipefail

# ============================================================
# The two changes from the template
# ============================================================
# 1. Godot project folder: godot/ in this repository, project-survival-shooting/ in my local working folder. Use whichever exists
if [ -f godot/project.godot ]; then
	project="godot"
else
	project="project-survival-shooting"
fi
# 2. Godot program: can be set with the GODOT environment variable; if unset, use the console build godot_console when it exists (Windows), otherwise godot
#    (on Windows the GUI build godot.exe does not send its output into a pipe, so the console build comes first)
if [ -z "$GODOT" ]; then
	if command -v godot_console > /dev/null; then
		GODOT="godot_console"
	else
		GODOT="godot"
	fi
fi

# ============================================================
# Run the test, keep the log, check for error lines
# ============================================================
mkdir -p logs
log="logs/$(basename "$1" .gd)_${2}fps.log"  # Log file name: <test name>_<fps>fps.log, e.g. logs/a3_asset_check_60fps.log
timeout 120 "$GODOT" --headless --path "$project" --script "res://tests/$1" --fixed-fps "$2" 2>&1 | tee "$log"
status=$?  # Exit code of the pipeline above: 0 = success, 124 = timed out (hung), anything else = failure
if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log"; then status=1; fi
exit $status
