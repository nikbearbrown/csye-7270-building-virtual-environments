#!/bin/zsh
# Act VI's own Godot run, in a FRESH scratch project that holds only the three good assets, launched from the folder ABOVE the
# project so the commands read exactly as the assignment writes them (`--path godot`). Real stdout kept, one log per command,
# with its exit code. Scratch: /private/tmp/claude-501/a6_godot (rebuilt each run; nothing in the repo is touched).
HERE="${0:A:h}"
SRC="$HERE/../godot/project_src"
ASSETS="$HERE/../assets"
WORK=/private/tmp/claude-501/a6_godot
rm -rf "$WORK"; mkdir -p "$WORK/godot/assets" "$WORK/godot/tests"
cp "$SRC/project.godot" "$SRC/showcase.tscn" "$WORK/godot/"
cp "$SRC/tests/check_assets.gd" "$WORK/godot/tests/"
cp "$ASSETS/crate.glb" "$ASSETS/lantern.glb" "$ASSETS/coin.glb" "$WORK/godot/assets/"
cd "$WORK" || exit 1
run() {   # logname  command...
  local log="$HERE/$1.log"; shift
  { echo "\$ $*"; "$@" 2>&1; echo "[exit code $?]"; } > "$log"
  echo "$(basename $log): $(tail -1 $log)"
}
run a6_ls_assets  ls godot/assets
run a6_import     godot --headless --path godot --import
run a6_check      timeout 120 godot --headless --path godot --script res://tests/check_assets.gd --fixed-fps 60
