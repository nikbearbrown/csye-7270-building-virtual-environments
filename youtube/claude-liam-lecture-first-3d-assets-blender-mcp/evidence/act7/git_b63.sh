#!/bin/zsh
# git_b63.sh — Act VII, B63: the real output shown on screen for "post the source, tag it a3".
# Read-only on the shared scratch repo made by ../git/make_repo.sh: it is COPIED into this builder's own scratch, and only the copy is touched.
# In the copy the existing tag a3 is deleted first, so that `git tag a3` can be run for real, exactly as a student runs it.
# (The copy has the same objects, so the commit ids are the same as in ../git/*.log.)
# Output (each file = the command line, then its real output, then its exit code), run in this order:
#   b63_ls_files_column.log  `git ls-files | column -c 66` (tabs expanded to spaces, as a terminal shows them) -> shown in B63
#   b63_tag.log              `git tag a3` (no output)                                                          -> shown in B63
#   b63_log_decorate.log     `git log --oneline --decorate -1` (proof the tag sits on the submitted commit)    -> NOT shown: B63's terminal holds 13 lines
# No network, no remote, no push.
HERE="${0:A:h}"
SRC=/private/tmp/claude-501/a3film/repo
WORK=/private/tmp/claude-501/a7scratch/repo-copy
[[ -d "$SRC/.git" ]] || { echo "scratch repo missing: run ../git/make_repo.sh first (note: it re-creates the commits, so their ids change)"; exit 1; }
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
rm -rf "$WORK"; mkdir -p "${WORK:h}"; cp -R "$SRC" "$WORK"
cd "$WORK" || exit 1
git tag -d a3 >/dev/null                                   # only in the copy
{ echo '$ git ls-files | column -c 66'; git ls-files | column -c 66 | expand; echo "[exit code $?]"; } > "$HERE/b63_ls_files_column.log"
{ echo '$ git tag a3'; git tag a3; echo "[exit code $?]"; } > "$HERE/b63_tag.log" 2>&1
{ echo '$ git log --oneline --decorate -1'; git log --oneline --decorate -1; echo "[exit code $?]"; } > "$HERE/b63_log_decorate.log" 2>&1
cat "$HERE/b63_ls_files_column.log" "$HERE/b63_tag.log" "$HERE/b63_log_decorate.log"
