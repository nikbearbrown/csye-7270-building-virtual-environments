#!/usr/bin/env bash
# Imports the same GLB three ways in Godot 4.7.2 and prints the imported scene tree each time.
#   A: fresh import (Godot's defaults)   B: only nodes/use_node_type_suffixes=false   C: the demo's enemy.glb.import [params] copied over
set -u
cd "$(dirname "$0")/suffix_probe"
DEMO=/Users/bear/Documents/CoWork/bear-textbooks/books/walker-3d-platformer/godot/enemy/enemy.glb.import
reimport() { rm -rf .godot/imported; godot --headless --path . --import >/dev/null 2>&1; }
dump() { godot --headless --path . --script res://print_tree.gd 2>&1 | grep -v "^Godot Engine\|^$"; }
rm -rf .godot post_suffixes.glb.import
reimport
echo "== A. fresh import (Godot 4.7.2 defaults)"; grep -E "use_name_suffixes|use_node_type_suffixes" post_suffixes.glb.import; dump
sed -i '' 's#^nodes/use_node_type_suffixes=true#nodes/use_node_type_suffixes=false#' post_suffixes.glb.import
reimport
echo; echo "== B. nodes/use_node_type_suffixes=false only"; grep -E "use_name_suffixes|use_node_type_suffixes" post_suffixes.glb.import; dump
# C: keep this file's [remap]/[deps], replace [params] with the demo's [params] verbatim
python3 - "$DEMO" <<'PY'
import sys, re
demo = open(sys.argv[1]).read().split("[params]", 1)[1]
cur = open("post_suffixes.glb.import").read()
head = cur.split("[params]", 1)[0]
open("post_suffixes.glb.import", "w").write(head + "[params]" + demo)
PY
reimport
echo; echo "== C. the demo's enemy.glb.import [params] copied over"; grep -E "use_name_suffixes|use_node_type_suffixes" post_suffixes.glb.import; dump
