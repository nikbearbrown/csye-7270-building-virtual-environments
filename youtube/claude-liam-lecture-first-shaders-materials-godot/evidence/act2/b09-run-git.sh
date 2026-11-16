#!/usr/bin/env bash
# B09 evidence: the two READ-ONLY git commands the film replays, run in the instructor example's repository.
# Nothing here writes to walker-claude (GIT_OPTIONAL_LOCKS=0 stops git from even refreshing the index).
# Re-run:  bash <this file>   (prints the output; the film replays b09-git-output.txt line for line)
set -u
export GIT_OPTIONAL_LOCKS=0 GIT_PAGER=cat
cd /Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude || exit 1
echo '$ git show --stat --format='"'"'%h %s'"'"' 93be391'
git show --stat --format='%h %s' 93be391
echo '$ cd assignments/05-shaders-materials'
cd assignments/05-shaders-materials || exit 1
echo '$ git log --reverse --format='"'"'%h %ad  %s'"'"' --date=format:'"'"'%Y-%m-%d %H:%M'"'"' -- CHANGE-BRIEF.md'
git log --reverse --format='%h %ad  %s' --date=format:'%Y-%m-%d %H:%M' -- CHANGE-BRIEF.md
