#!/usr/bin/env bash
# Instructor's verification sweep for Chapter 13.
# Runs the agent-written benchmark in fresh processes, 5 times per configuration,
# alternating modes so slow drift on the machine hits both modes equally.
# Usage: bash sweep.sh <project-root-containing-godot/> <out.csv>
set -u
ROOT="$1"; OUT="$2"
echo "run,mode,count,frames,mean_ms,p95_ms,max_ms,object_count,node_count,static_memory_mb" > "$OUT"
for run in 1 2 3 4 5; do
  for count in 500 2000 5000; do
    for mode in servers nodes; do
      line=$(godot --headless --fixed-fps 60 --path "$ROOT/godot" --script res://bench/bench.gd -- --mode=$mode --count=$count --frames=600 2>/dev/null | grep -E "^(servers|nodes),")
      echo "$run,$line" >> "$OUT"
    done
  done
done
