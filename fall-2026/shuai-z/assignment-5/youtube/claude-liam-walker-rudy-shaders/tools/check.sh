#!/usr/bin/env bash
# Run the course's godot-gamedev checker, unmodified, once per Godot project.
# The checker takes one folder holding project.godot, and Assignment 5 has two,
# so tools/make_evidence.py writes one check folder for each (see its docstring).
#   tools/check.sh            # from the reel folder; brutalist.art beside course-fork
set -euo pipefail
reel="$(cd "$(dirname "$0")/.." && pwd)"
art="${ART:-$reel/../../../../../../brutalist.art}"
a5="$reel/../.."
status=0
for project in game godot; do
  echo "== $project/"
  (cd "$art" && ./art godot-gamedev --check "$reel/checks/$project" --game "$a5/$project") || status=1
done
exit $status
