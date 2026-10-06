#!/usr/bin/env bash
# Runs every test and benchmark in the correct order.
# Usage:  bash run_bench.sh [path-to-godot-binary]
# Default binary: /Applications/Godot.app/Contents/MacOS/Godot

set -euo pipefail

GODOT="${1:-/Applications/Godot.app/Contents/MacOS/Godot}"
PROJ="$(cd "$(dirname "$0")/godot" && pwd)"

run() {
    local label="$1"; shift
    echo ""
    echo "=== $label ==="
    "$GODOT" --headless "$@" --path "$PROJ" 2>&1
    echo "(exit $?)"
}

echo "Godot: $GODOT"
echo "Project: $PROJ"

# Import so the new bench/ scripts appear in the UID cache.
echo ""
echo "=== IMPORT ==="
"$GODOT" --headless --import --path "$PROJ" 2>&1

# ---- Three existing tests (servers / original scene) ----
run "test_mouse_input"    --script res://test_mouse_input.gd
run "test_collision_input" --script res://test_collision_input.gd
run "test_motion"          --script res://test_motion.gd

# ---- Parity test: node-based baseline must behave like the original ----
run "test_nodes_parity count=500"  --script res://bench/test_nodes_parity.gd -- --count=500
run "test_nodes_parity count=5000" --script res://bench/test_nodes_parity.gd -- --count=5000

# ---- Benchmark ----
run "bench servers count=500"  --fixed-fps 60 --script res://bench/bench.gd -- --mode=servers --count=500  --frames=600
run "bench servers count=5000" --fixed-fps 60 --script res://bench/bench.gd -- --mode=servers --count=5000 --frames=600
run "bench nodes count=500"    --fixed-fps 60 --script res://bench/bench.gd -- --mode=nodes   --count=500  --frames=600
run "bench nodes count=5000"   --fixed-fps 60 --script res://bench/bench.gd -- --mode=nodes   --count=5000 --frames=600

echo ""
echo "All done."
