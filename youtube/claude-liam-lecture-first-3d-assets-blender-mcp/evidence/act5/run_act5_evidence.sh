#!/bin/zsh
# run_act5_evidence.sh - Act V's own evidence (read-only commands; nothing is installed, nothing leaves the machine).
#   1. ls_1.log        the real one-name-per-line listing of the saved sources, Blender's backups and the exports (B49)
#   2. gitignore.log   the real .gitignore of the scratch submission repo (made by ../git/make_repo.sh) and git's view of it (B49)
#   3. prompt.txt      the assignment's plan-first prompt, extracted verbatim from the assignment (B41-B44)
#   4. crop_a5.py      crops the real Blender window shots into pantry/a5_*.png (B46, B47)
HERE="${0:A:h}"
REEL="$HERE/../.."
ASSIGN="$REEL/../../assignments/03-first-3d-assets-with-blender-mcp.md"
{ echo '$ ls -1 *.blend *.blend1 *.glb'; (cd "$HERE/../assets" && ls -1 *.blend *.blend1 *.glb); echo "[exit code $?]"; } > "$HERE/ls_1.log"
REPO=/private/tmp/claude-501/a3film/repo
if [ -d "$REPO" ]; then
  { echo '$ cat .gitignore'; cat "$REPO/.gitignore";
    echo '$ git status --short --ignored'; (cd "$REPO" && GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null git status --short --ignored); echo "[exit code $?]"; } > "$HERE/gitignore.log"
else
  echo "scratch repo missing: run ../git/make_repo.sh first" > "$HERE/gitignore.log"
fi
# the prompt is the first ```text block after the heading "### Build the assets, one at a time"
awk '/^### Build the assets, one at a time/{f=1} f&&/^```text/{p=1;next} p&&/^```/{exit} p{print}' "$ASSIGN" > "$HERE/prompt.txt"
python3 "$HERE/crop_a5.py"
