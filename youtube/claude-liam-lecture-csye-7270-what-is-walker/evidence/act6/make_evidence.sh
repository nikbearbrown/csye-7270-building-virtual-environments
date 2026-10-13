#!/usr/bin/env bash
# make_evidence.sh — re-runs every read-only check Act VI shows on screen. Output: evidence/act6/*.txt (a plain shell script, not Claude).
# Nothing here writes outside evidence/act6/, calls a model, or touches the network.
HERE="$(cd "$(dirname "$0")" && pwd)"
BOOKS=/Users/bear/Documents/CoWork/bear-textbooks/books
W=$BOOKS/walker; C=$BOOKS/walker-jumpman-clawd
EV=$BOOKS/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/walker-evidence
{
  echo "# B25: does a 'walker gdd' command exist on this Mac? (zsh -c 'walker gdd'; $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  zsh -c 'walker gdd' 2>&1; echo "exit code: $?"
} > "$HERE/walker-gdd-run.txt"
{
  echo "# B25: files in the Walker framework repo (outside games/, godot-demo-projects/, youtube/, .git/) whose name contains test, spec, pytest or gut"
  (cd "$W" && find . -path ./games -prune -o -path ./godot-demo-projects -prune -o -path ./youtube -prune -o -path ./.git -prune -o -type f \( -iname '*test*' -o -iname '*spec*' -o -iname 'pytest*' -o -iname 'gut*' \) -print)
  echo "# the 54 files one publish run installs, matching test/spec (name):"
  grep -E "^[0-9]+ \./" "$EV/installed-tree.txt" | awk 'BEGIN{f=0} /walker-demo-game-codex/{exit} {print}' | grep -i -E "test|spec" || true
  echo "# (a hit named looptest.md is a /gdd command description, not a test runner)"
} > "$HERE/no-test-framework.txt"
{
  echo "# B24: the real design-status file in the Clawd game: mode and gate lines"
  ls -l "$C/design/DESIGN-STATUS.json"
  cat -n "$C/design/DESIGN-STATUS.json" | sed -n 9,14p
  echo "# the starter template the publisher installs (gdd/templates/DESIGN-STATUS.json)"
  cat -n "$W/gdd/templates/DESIGN-STATUS.json" | sed -n 6,11p
  echo "# B24: the sentence, with its real line number (local working copy)"
  grep -n "Gate validation is a convention" "$W/docs/zelda-gdd-workflow.md" | cut -c1-110
  echo "# is that sentence in the committed HEAD (10fedb8) copy of the same file? (0 = no)"
  (cd "$W" && git show HEAD:docs/zelda-gdd-workflow.md | grep -c "Gate validation is a convention")
  echo "# the README line about walker gdd (working copy, then committed)"
  grep -n "walker gdd" "$W/README.md" | cut -c1-120
  (cd "$W" && git show HEAD:README.md | grep -n "walker gdd" | cut -c1-120)
} > "$HERE/gate-status-and-quote.txt"
{
  echo "# B25: public version vs local working copy"
  (cd "$W" && git log -1 --format='HEAD %h %ad %s' --date=short && git status -sb | head -1 && git log origin/main -1 --format='origin/main %h' )
  (cd "$W" && git status --short | head -12)
  echo "# publish run, committed HEAD (publish-committed-HEAD.log):"; cat "$EV/publish-committed-HEAD.log"
  echo "# publish run, working tree (publish.log):"; cat "$EV/publish.log"
  echo "# committed-HEAD install listing (tree.txt) with file counts"
  grep -c "^[0-9]" "$EV/installed/claude-committed-HEAD/tree.txt"
  echo "# working-tree install: asset-gen / gdd / other counts"
  awk '/walker-demo-game  \(agent: claude\)/{f=1;next} /^TOTAL/{f=0} f' "$EV/installed-tree.txt" > "$HERE/_a.tmp"
  echo "asset-gen: $(grep -c 'skills/asset-gen/' "$HERE/_a.tmp")  gdd: $(grep -c 'skills/gdd/' "$HERE/_a.tmp")  root files: $(grep -c -E '^[0-9]+ \./[^/]+$' "$HERE/_a.tmp")  total: $(grep -c -E '^[0-9]+ \./' "$HERE/_a.tmp")"
  rm -f "$HERE/_a.tmp"
  echo "# line counts of the two manifests"
  wc -l < "$EV/installed/claude/CLAUDE.md"; wc -l < "$EV/installed/claude-committed-HEAD/CLAUDE.md"
  echo "# unbuilt list in the workflow doc"
  grep -n "Still unbuilt" "$W/docs/zelda-gdd-workflow.md" | cut -c1-260
} > "$HERE/public-vs-local.txt"
{
  echo "# B26 exhibits"
  echo "## C/CHANGE-BRIEF.md lines 16-21 (the three predictions) and 25-27 (scope)"
  sed -n '16,21p;25,27p' "$C/CHANGE-BRIEF.md" | cut -c1-200
  echo "## C/CLAWD-STATUS.json line 12"; sed -n 12p "$C/CLAWD-STATUS.json"
  echo "## C/FRICTIONAL.md lines 39-44 and 48-50"; sed -n '39,44p;48,50p' "$C/FRICTIONAL.md" | cut -c1-200
  echo "## installed manifest line 10 (judge progress)"; sed -n 10p "$EV/installed/claude/CLAUDE.md" | cut -c1-140
  echo "## C/AGENTS.md lines 11-15 (predict, one change, inspect, never invent, preserve failed receipts)"; sed -n 11,15p "$C/AGENTS.md" | cut -c1-200
} > "$HERE/habit-exhibits.txt"
echo done; ls "$HERE"
