#!/bin/zsh
# Re-runs every scratch GDScript check of the outline film in a throw-away Godot project (never in the film folder), logs each run, and
# then the analysis scripts. Everything runs in a real window (not headless), Godot 4.7.2, Forward+ unless a script says otherwise.
#   ./run_scratch_checks.sh            # all checks
#   ./run_scratch_checks.sh a d        # only verify_a_* and verify_d_*
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
SCR="${TMPDIR:-/tmp}/outline-film-scratch-project"
rm -rf "$SCR"; mkdir -p "$SCR"
cp "$HERE/project.godot" "$HERE"/ol_lib.gd "$HERE"/padding_snippet.gd "$HERE"/verify_*.gd "$SCR"/
export OUTLINE_FILM_DIR="$FILM"
want=("$@")
for f in "$HERE"/verify_*.gd; do
  name="$(basename "$f" .gd)"; id="${name#verify_}"; id="${id%%_*}"
  if [ ${#want[@]} -gt 0 ] && [[ ! " ${want[*]} " == *" $id "* ]]; then continue; fi
  echo "== $name"
  ( cd "$SCR" && godot --path "$SCR" --script "res://$name.gd" -- --out "$HERE/png" ) > "$HERE/run-$id-$name.log" 2>&1
  echo "   exit $?  ->  run-$id-$name.log  ($(grep -c '^RESULT' "$HERE/run-$id-$name.log") RESULT lines, $(grep -c -E 'ERROR|SCRIPT ERROR' "$HERE/run-$id-$name.log") error lines)"
done
