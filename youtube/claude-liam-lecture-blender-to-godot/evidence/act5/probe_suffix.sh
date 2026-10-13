#!/usr/bin/env bash
# Re-runs the suffix probe on the FIRST agent's own asset: builds the run-1 Blender script (collision BOX) headless, imports the .glb into an
# EMPTY Godot project with Godot's own defaults, prints the imported tree, then flips only nodes/use_node_type_suffixes to false and prints it again.
# Output: probe-suffix-rerun.log (same shape as examples/03-.../logs/probe-suffix-setting.log). Run:  bash probe_suffix.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
EX="$HERE/../../../../examples/03-blender-mcp-to-godot"
T="$(mktemp -d /private/tmp/claude-501/a5_probe.XXXX)"
mkdir -p "$T/tools/blender" "$T/godot"
cp "$EX/scripts/agent/build_checkpoint_post.run1.py" "$T/tools/blender/build_checkpoint_post.py"
printf 'config_version=5\n\n[application]\nconfig/name="a5-probe"\n' > "$T/godot/project.godot"
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python "$T/tools/blender/build_checkpoint_post.py" > "$T/blender.log" 2>&1 || { echo "blender failed"; exit 1; }
cat > "$T/godot/print_tree.gd" <<'GD'
extends SceneTree
func dump(n: Node, d: int) -> void:
	var extra := ""
	if n is CollisionShape3D and n.shape: extra = " shape=" + n.shape.get_class()
	if n is Node3D: extra += " scale=" + str((n as Node3D).scale)
	print("  ".repeat(d), n.get_class(), " [", n.name, "]", extra)
	for c in n.get_children(): dump(c, d + 1)
func _initialize() -> void:
	var inst: Node = (load("res://props/checkpoint_post.glb") as PackedScene).instantiate()
	dump(inst, 0)
	inst.free()
	quit()
GD
{
  godot --headless --path "$T/godot" --import >/dev/null 2>&1
  echo "== fresh import, Godot $(godot --version | cut -d. -f1-3) defaults:"
  grep -E "^nodes/use_(name|node_type)_suffixes" "$T/godot/props/checkpoint_post.glb.import"
  echo
  godot --headless --path "$T/godot" --script res://print_tree.gd 2>&1 | grep -E "^(Node3D|  )"
  sed -i '' 's#^nodes/use_node_type_suffixes=true#nodes/use_node_type_suffixes=false#' "$T/godot/props/checkpoint_post.glb.import"
  rm -rf "$T/godot/.godot/imported"
  godot --headless --path "$T/godot" --import >/dev/null 2>&1
  echo "== same file, nodes/use_node_type_suffixes=false (the demo's setting):"
  grep -E "^nodes/use_(name|node_type)_suffixes" "$T/godot/props/checkpoint_post.glb.import"
  echo
  godot --headless --path "$T/godot" --script res://print_tree.gd 2>&1 | grep -E "^(Node3D|  )"
} > "$HERE/probe-suffix-rerun.log"
cat "$HERE/probe-suffix-rerun.log"
echo "--- dims line from the Blender run:"; grep -E "dims=" "$T/blender.log"
