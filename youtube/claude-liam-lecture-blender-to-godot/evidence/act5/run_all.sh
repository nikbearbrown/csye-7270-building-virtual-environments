#!/usr/bin/env bash
# Reproduces everything Act V part 1 (B45-B58) shows that is not typed by hand. Run from anywhere:  bash evidence/act5/run_all.sh
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
SCR=/private/tmp/claude-501/a5_render; mkdir -p "$SCR"
# 1. the real Blender render of the post (first agent's own run-1 script, collision BOX) + camera-projected anchors -> pantry/a5_*.png
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python "$HERE/render_a5.py" -- "$SCR"
python3 "$HERE/crop_a5.py" "$SCR"                    # writes ../../pantry/a5_post.png, a5_box.png, a5_boxopaque.png and post_anchors.json
# 2. the suffix probe re-run on that same asset in an empty Godot project (default import vs use_node_type_suffixes=false)
bash "$HERE/probe_suffix.sh"                          # writes probe-suffix-rerun.log
# 3. every session number recomputed from the recorded transcript and logs
bash "$HERE/transcript_facts.sh"                      # writes transcript-facts.log
# 4. the lane file (Claude Code session blocks; cues in frames at 30 fps from the measured audio)
python3 "$HERE/make_lanes_act5.py"                    # writes ../../lanes/act5.json
