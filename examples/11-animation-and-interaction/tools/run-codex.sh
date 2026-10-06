#!/bin/bash
# usage: run-codex.sh <repo-dir> <prompt-file> <log-prefix>
cd "$1" || exit 2
date -u +"%Y-%m-%dT%H:%M:%SZ start" > "$3.time"
codex exec --sandbox workspace-write --json -o "$3-last.txt" "$(cat "$2")" < /dev/null > "$3.jsonl" 2> "$3.stderr"
echo "exit $?" >> "$3.time"
date -u +"%Y-%m-%dT%H:%M:%SZ end" >> "$3.time"
