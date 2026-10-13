#!/bin/zsh
# SubViewports film: the checks that need ANOTHER Godot window on top of the checking window (what happens all day on Bear's Mac when several Godot runs are open).
#   run-10d  draws counted while covered           (regular frames almost stop; force_draw still draws)
#   run-11b  Update Mode Once while covered         (O1 with a forced draw per frame still freezes at the right moment; O2 waiting for regular frames does not)
#   run-7d   capture scene c21 while covered         (the capture rehearsal is the same with the window covered)
# The cover window (hold_window.gd) is stopped by its PID. Nothing here removes files or kills by name.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
W="${SV_SCRATCH:-/private/tmp/claude-501/godot-shaders-subviewports/proj-final}"
LOGS="$HERE/logs"; mkdir -p "$LOGS" "$W"
PIDF="/private/tmp/claude-501/godot-shaders-subviewports/hold.pid"
cp "$HERE/scratch-project.godot" "$W/project.godot"
cp "$HERE"/*.gd "$W/"
godot --headless --path "$W" --import >/dev/null 2>&1
run() {   # logname script [-- args]
  local name="$1"; local script="$2"; shift 2
  echo "== $name"
  ( cd "$W" && timeout 590 godot --path . --fixed-fps 30 --script "res://$script" "$@" 2>&1 ) | grep -v "^Godot Engine\|^Metal\|^OpenGL\|^$" > "$LOGS/$name.log"
  grep -c RESULT "$LOGS/$name.log"
}
cover() {   # start the cover window and wait until it is up; the PID of the Godot process itself goes to $PIDF
  cd "$W" || return
  nohup godot --path . --always-on-top --position 0,0 --resolution 1700x1000 --script res://hold_window.gd >/dev/null 2>&1 &
  echo $! > "$PIDF"
  cd "$HERE" || return
  sleep 8
  echo "   cover window running: $(ps -p "$(cat "$PIDF")" -o pid= 2>/dev/null | wc -l | tr -d ' ') (1 = yes)"
}
uncover() { kill "$(cat "$PIDF")" 2>/dev/null; sleep 2; }
cover
run run-10d-verify10-draws-covered-by-another-window verify10_draw_skipping.gd
uncover
cover
run run-11b-verify11-once-covered-forward_plus verify11_once_needs_a_draw.gd
uncover
cover
run run-7d-verify7-c21-covered-forward_plus verify7_capture_rehearsal.gd -- c21
uncover
echo "done: covered runs in $LOGS"
