#!/usr/bin/env bash
# ============================================================
# About: the test wrapper A6 asks for (the template in the A6 brief, "2. Build It", with two changes for this repository's folders)
# ============================================================
# Usage: ./scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]
# Examples: ./scripts/run-test.sh a3_asset_check.gd 60
#           ./scripts/run-test.sh cost_effects.gd 60 300
# It does five things:
#   1. Wraps Godot in timeout: if a test script errors before quit(), headless Godot keeps running; it is killed when the time is up (exit code 124 = hung)
#   2. When the second argument is a frame rate, pins it with --fixed-fps: every frame's delta is 1/fps, whatever the machine's speed
#      When the second argument is realtime, the frame rate is not pinned: for tests that wait on audio (timers follow game time, audio follows the real clock)
#   3. An optional third argument sets the timeout in seconds (120 when left out), for the long-running cost script
#   4. Keeps a copy of the output as a log in logs/
#   5. Fails when the log contains SHADER ERROR or SCRIPT ERROR (Godot can exit 0 even after such errors)

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
# Choose the frame-rate mode: a pinned frame rate, or realtime
# ============================================================
if [ "$2" = "realtime" ]; then
	fps_args=()  # If it is realtime, we add no --fixed-fps and let the game run on real time
	tag="realtime"  # The log name says realtime
else
	fps_args=(--fixed-fps "$2")  # Otherwise, we pin every frame's time to the given frame rate
	tag="${2}fps"  # The log name says the frame rate, e.g. 60fps
fi

# ============================================================
# Run the test, keep the log, check for error lines
# ============================================================
mkdir -p logs
log="logs/$(basename "$1" .gd)_${tag}.log"  # Log file name: <test name>_<mode>.log, e.g. logs/a3_asset_check_60fps.log
timeout "${3:-120}" "$GODOT" --headless "${fps_args[@]}" --path "$project" --script "res://tests/$1" 2>&1 | tee "$log"
status=$?  # Exit code of the pipeline above: 0 = success, 124 = timed out (hung), anything else = failure
if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log"; then status=1; fi
exit $status
