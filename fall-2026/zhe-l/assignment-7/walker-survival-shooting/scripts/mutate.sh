#!/usr/bin/env bash
# Runs one A7 mutation (paths below are for my machine; set REPO, WT and G for yours) in a fresh sparse git worktree, then throws the worktree away.
# Usage: mutate.sh <name> <test.gd> <python-edit-or-"none"> [fresh]
set -u
REPO="${REPO:?set REPO to the course repo root}"
A="fall-2026/zhe-l/assignment-7/walker-survival-shooting"
WT="${WT:-$REPO/../a7-mutate}"
G="${GODOT:-godot}"
name=$1; test=$2; edit=$3; fresh=${4:-}
cd "$REPO"
git worktree remove --force "$WT" >/dev/null 2>&1; git worktree prune
git worktree add --no-checkout "$WT" HEAD >/dev/null 2>&1
cd "$WT"
git sparse-checkout set --cone fall-2026/zhe-l/assignment-7 >/dev/null 2>&1
git checkout -q HEAD
cd "$A"
if [ "$edit" != "none" ]; then python -I -c "$edit" || { echo "EDIT FAILED"; exit 2; }; fi
git -C "$WT" diff --stat | tail -1
if [ -n "$fresh" ]; then rm -rf godot/.godot; fi
timeout 300 "$G" --headless --path godot --import > "logs/mutation_${name}_import.log" 2>&1
GODOT="$G" ./scripts/run-test.sh "$test" 60 > /dev/null 2>&1
status=$?
log="logs/${test%.gd}_60fps.log"
cp "$log" "$REPO/$A/logs/mutation_${name}.log"
echo "MUTATION $name: $test exit=$status pass=$(grep -c '^  PASS' "$log") fail=$(grep -c '^  FAIL' "$log")"
grep -E "^  FAIL" "$log" | head -4
cd "$REPO"; git worktree remove --force "$WT"; git worktree prune
