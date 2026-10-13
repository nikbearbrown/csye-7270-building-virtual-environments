#!/bin/zsh
# Re-runs every check of this film in order and rewrites the logs and summaries in this folder (about 8 minutes when the Lab is not busy, longer while other sessions hold its lock; needs Godot 4.7.2 and Python with Pillow and numpy; keep other windows off the Godot window while the stress test runs).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
./check_all_shaders.sh > /dev/null
python3 run_lab_checks.py > /dev/null && python3 analyze_lab.py > /dev/null
./run_scratch_checks.sh
./run_cost_repeats.sh 3        # the stress test again, three more times: the film quotes the median of the valid runs
python3 analyze_soft.py > /dev/null; python3 analyze_mascot.py > /dev/null; python3 analyze_crate.py > /dev/null; python3 analyze_filter.py > /dev/null; python3 analyze_cost.py > /dev/null; python3 analyze_subtract.py > /dev/null; python3 analyze_ringconst.py > /dev/null; python3 analyze_padding.py > /dev/null; python3 analyze_bigcopy.py > /dev/null; python3 analyze_sheets.py > /dev/null
python3 make_scenes.py > /dev/null
rm -f png/scenes/*.png
python3 run_scenes.py && python3 analyze_scenes.py > /dev/null
./run_route.sh > /dev/null; python3 analyze_route.py > /dev/null
# the lesson of the audit: a renamed shader file made three checks silently measure the wrong thing, so scan every log for script and shader errors
if grep -l -E "shader not found|SCRIPT ERROR|Parse Error" run-*.log; then echo "WARNING: the logs above hold a script or shader error"; else echo "logs: no script or shader errors"; fi
echo "done: see RESULTS.md for what each log shows"
