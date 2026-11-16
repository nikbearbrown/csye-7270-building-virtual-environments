#!/usr/bin/env bash
# B09 (Manim version) evidence: three READ-ONLY commands run in the instructor example's repository, in the order the film shows them.
# Shorter than the CCPlainShell version (b09-run-git.sh) because real rows may not be reflowed and the smallest allowed Menlo size (20) fits ~80 characters:
# the log prints hash + date and the stat prints the hash only (no subject lines), so the longest real row is the 79-character stat row. Nothing writes to walker-claude (GIT_OPTIONAL_LOCKS=0).
# Re-run:  bash <this file>   (the film replays b09-git-output-manim.txt line for line)
set -u
export GIT_OPTIONAL_LOCKS=0 GIT_PAGER=cat
cd /Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude || exit 1
echo '$ cd assignments/05-shaders-materials'
cd assignments/05-shaders-materials || exit 1
echo '$ git log --reverse --date=short --format='"'"'%h %ad'"'"' -- CHANGE-BRIEF.md'
git log --reverse --date=short --format='%h %ad' -- CHANGE-BRIEF.md
echo '$ git show --stat --format='"'"'%h'"'"' 93be391'
git show --stat --format='%h' 93be391
