#!/usr/bin/env bash
# Run the course's godot-gamedev checker, unmodified, on game/, the one Godot
# project of Assignment 6. tools/make_evidence.py writes the check folder.
#   tools/check.sh            # from the reel folder; brutalist.art beside course-fork
set -euo pipefail
reel="$(cd "$(dirname "$0")/.." && pwd)"
art="${ART:-$reel/../../../../../../brutalist.art}"
a6="$reel/../.."
echo "== game/"
(cd "$art" && ./art godot-gamedev --check "$reel/checks/game" --game "$a6/game")
