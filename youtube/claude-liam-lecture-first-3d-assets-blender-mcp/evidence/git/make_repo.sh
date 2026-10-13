#!/bin/zsh
# E10 - a tiny scratch repository that has the SHAPE of a student's Assignment 3 submission, then the real git commands of the
# ship-it beats (tag a3, log, status, clone, checkout, ls-files). Local only: no remote, no push, no network.
# Nothing here is a student's work: the .md files are one-line placeholders and say so.
HERE="${0:A:h}"
ASSETS="$HERE/../assets"
GODOT="$HERE/../godot"
ROOT=/private/tmp/claude-501/a3film
REPO="$ROOT/repo"
rm -rf "$REPO" "$ROOT/a3-check"
mkdir -p "$REPO/godot/assets" "$REPO/godot/tests" "$REPO/art/3d" "$REPO/tools/blender"
cd "$REPO" || exit 1
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null       # never read or write the real git config
git init -q -b main
git config user.name "Example Student"
git config user.email "student@example.invalid"
cat > .gitignore <<'EOG'
# Godot's import cache and Blender's automatic backups stay out of the repository
.godot/
*.blend1
EOG
# --- commit 1: the brief, written before building
for f in CHANGE-BRIEF.md; do :; done
echo "Placeholder for the film's scratch repo: the real file names the three assets, their sizes in metres, origin, look, triangle budget and three predicted failures, with the check for each." > CHANGE-BRIEF.md
echo "Placeholder for the film's scratch repo: the real file names the six parts of Blender's window in the student's own words." > BLENDER-NOTES.md
git add .gitignore CHANGE-BRIEF.md BLENDER-NOTES.md
git commit -q -m "Add CHANGE-BRIEF.md and BLENDER-NOTES.md before building" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
# --- commit 2: scripts, sources, exports
cp "$ASSETS"/build_crate.py "$ASSETS"/build_lantern.py "$ASSETS"/build_coin.py tools/blender/
cp "$ASSETS"/crate.blend "$ASSETS"/lantern.blend "$ASSETS"/coin.blend art/3d/
cp "$ASSETS"/crate.blend1 "$ASSETS"/lantern.blend1 "$ASSETS"/coin.blend1 art/3d/        # Blender's own backups sit beside the sources
cp "$ASSETS"/crate.glb "$ASSETS"/lantern.glb "$ASSETS"/coin.glb godot/assets/
cp /private/tmp/claude-501/a3film/godot_proj/assets/*.import godot/assets/
echo "Placeholder for the film's scratch repo: the real file lists every tool and version (Blender 5.1.2, Godot 4.7.2, Claude Code) and what the AI did." > SOURCES.md
git add -A
git commit -q -m "Add build scripts, .blend sources and .glb exports for crate, lantern and coin" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
# --- commit 3: Godot project, scene, check, reports
cp "$GODOT/project_src/project.godot" "$GODOT/project_src/showcase.tscn" godot/
cp "$GODOT/project_src/tests/check_assets.gd" godot/tests/
cp -R /private/tmp/claude-501/a3film/godot_proj/.godot godot/.godot                     # the import cache exists on disk, and is ignored
echo "Placeholder for the film's scratch repo: the real file records each check's command and result, with Blender and Godot versions." > TEST-REPORT.md
echo "Placeholder for the film's scratch repo: the real file is the student's honest log of attempts, errors and who did what." > FRICTIONAL.md
echo "Scratch repository made for the film's ship-it beats. It has the shape of an Assignment 3 submission; it is not a student's work. Check: timeout 120 godot --headless --path godot --script res://tests/check_assets.gd --fixed-fps 60" > README.md
git add -A
git commit -q -m "Add Godot showcase scene, headless check, README and reports" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"

LOG="$HERE"
step() {   # logname  command...   (run inside the repo; the log keeps the command and its real output)
  local name="$1"; shift
  { echo "\$ $*"; "$@" 2>&1; echo "[exit code $?]"; } > "$LOG/$name.log"
  echo "== $name"; cat "$LOG/$name.log"
}
step git_tag            git tag a3
step git_log            git log --oneline --decorate
step git_status         git status --short
step git_status_ignored git status --short --ignored
step git_ls_files       git ls-files
cd "$ROOT" || exit 1
{ echo "\$ git clone $REPO ../a3-check      (run from inside the repo; ../a3-check = $ROOT/a3-check)"; (cd "$REPO" && git clone "$REPO" ../a3-check 2>&1); echo "[exit code $?]"; } > "$LOG/git_clone.log"
{ echo "\$ git -C ../a3-check checkout a3"; (cd "$REPO" && git -C ../a3-check checkout a3 2>&1); echo "[exit code $?]"; } > "$LOG/git_checkout_a3.log"
{ echo "\$ git -C ../a3-check log --oneline --decorate"; (cd "$REPO" && git -C ../a3-check log --oneline --decorate 2>&1); echo "[exit code $?]"; } > "$LOG/git_clone_log.log"
{ echo "\$ git -C ../a3-check ls-files | head -40  (the tag a3 checked out in the clone)"; (cd "$REPO" && git -C ../a3-check ls-files 2>&1); echo "[exit code $?]"; } > "$LOG/git_clone_ls_files.log"
echo "== git_clone"; cat "$LOG/git_clone.log"; echo "== git_checkout_a3"; cat "$LOG/git_checkout_a3.log"; echo "== git_clone_log"; cat "$LOG/git_clone_log.log"
echo "== remotes in the scratch repo:"; (cd "$REPO" && git remote -v | wc -l | tr -d ' '); echo "(0 = no remote)"
# --- B64: in the clone, import once and run the check (the clone has no .godot/ and no .blend1: both were ignored)
{ echo "\$ ls ../a3-check/art/3d ../a3-check/godot   (what the clone contains: no .blend1, no .godot)"; ls "$ROOT/a3-check/art/3d" "$ROOT/a3-check/godot"; echo "[exit code $?]"; } > "$LOG/clone_contents.log"
{ echo "\$ godot --headless --path godot --import   (inside ../a3-check)"; (cd "$ROOT/a3-check" && godot --headless --path godot --import 2>&1); echo "[exit code $?]"; } > "$LOG/clone_import.log"
{ echo "\$ timeout 120 godot --headless --path godot --script res://tests/check_assets.gd --fixed-fps 60   (inside ../a3-check)"; (cd "$ROOT/a3-check" && timeout 120 godot --headless --path godot --script res://tests/check_assets.gd --fixed-fps 60 2>&1); echo "[exit code $?]"; } > "$LOG/clone_check.log"
echo "== clone_contents"; cat "$LOG/clone_contents.log"; echo "== clone_check"; cat "$LOG/clone_check.log"
