#!/bin/zsh
# record-editor-frames.sh <editor project dir> <node to select> <output dir> [frames]
# Records Godot's OWN editor (4.7.2) for the film's editor frames E1 (Scene dock) and E2 (Inspector of the BackBufferCopy) with Movie Maker.
# The editor opens <editor project dir>/pond.tscn (built by make-editor-project.sh), a scratch plugin selects <node to select>
# (Pond for E1, BackBufferCopy for E2), and PNG frames land in <output dir>. Take a late frame (for example the last) and crop:
#   E1 Scene dock : box (0, 60) to (440, 420) of the 2560 x 1440 frame      E2 Inspector : box (2140, 60) to (2560, 420)
# Why a scratch HOME: the editor's look is a user-level setting. This script gives the process its own HOME with the Light colour preset
# and a 2x UI scale, so frames match the cream palette and your real editor settings are never touched. Nothing else is written outside
# <editor project dir> (the scratch plugin goes into its addons/ folder) and <output dir> and the scratch HOME.
set -eu
PROJ="${1:?editor project dir (from make-editor-project.sh)}"; PICK="${2:?node to select}"; OUT="${3:?output dir}"; FRAMES="${4:-100}"
mkdir -p "$OUT"
SCRATCH_HOME="${SCRATCH_HOME:-$(dirname "$PROJ")/scratch-home}"
SETTINGS="$SCRATCH_HOME/Library/Application Support/Godot"
mkdir -p "$SETTINGS"
cat > "$SETTINGS/editor_settings-4.7.tres" <<'EOT'
[gd_resource type="EditorSettings" format=3]

[resource]
interface/theme/color_preset = "Light"
interface/editor/appearance/display_scale = 7
interface/editor/appearance/custom_display_scale = 2.0
EOT
# the project: 2560 x 1440 window (the movie takes the window size) and the scratch selector plugin
python3 - "$PROJ" <<'EOT'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "project.godot"
s = p.read_text()
s = s.replace("window/size/viewport_width=1280", "window/size/viewport_width=2560").replace("window/size/viewport_height=720", "window/size/viewport_height=1440")
if "[editor_plugins]" not in s:
    s += '\n[editor_plugins]\n\nenabled=PackedStringArray("res://addons/frame_selector/plugin.cfg")\n'
p.write_text(s)
EOT
mkdir -p "$PROJ/addons/frame_selector"
cat > "$PROJ/addons/frame_selector/plugin.cfg" <<'EOT'
[plugin]

name="frame_selector"
description="Scratch helper: selects the node named in PICK_NODE so the Scene dock or Inspector can be recorded. Not part of the film."
author="layout"
version="1.0"
script="plugin.gd"
EOT
cat > "$PROJ/addons/frame_selector/plugin.gd" <<'EOT'
@tool
extends EditorPlugin
var frames := 0
func _enter_tree() -> void:
	set_process(true)
func _process(_delta: float) -> void:
	frames += 1
	if frames == 45:
		var root := EditorInterface.get_edited_scene_root()
		var want := OS.get_environment("PICK_NODE")
		if root != null and want != "":
			var n: Node = root if want == root.name else root.get_node_or_null(want)
			if n != null:
				EditorInterface.get_selection().clear()
				EditorInterface.get_selection().add_node(n)
				EditorInterface.edit_node(n)
				print("RESULT picked ", want)
EOT
HOME="$SCRATCH_HOME" PICK_NODE="$PICK" timeout 240 godot --editor --path "$PROJ" res://pond.tscn --write-movie "$OUT/f.png" --fixed-fps 30 --quit-after "$FRAMES" 2>&1 | grep "RESULT\|Done\|Movie Maker" || true
ls "$OUT" | tail -2
