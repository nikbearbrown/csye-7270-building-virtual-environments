#!/bin/zsh
# with_lab_lock.sh <command...>
# Runs any command that starts a Godot editor, project manager or window while holding the shared Lab lock
# (/private/tmp/claude-501/shaderlab.lock: a DIRECTORY taken with mkdir, waits up to 30 minutes, a lock older than 3 minutes counts as stale,
# so a background loop touches it every 30 s while the command runs; released with rmdir in a trap).
set -u
LOCK=/private/tmp/claude-501/shaderlab.lock
mkdir -p /private/tmp/claude-501
GOT=0
for i in $(seq 1 3600); do
  if mkdir "$LOCK" 2>/dev/null; then GOT=1; break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
[ "$GOT" = 1 ] || { echo "could not get the Lab lock in 30 minutes"; exit 4; }
touch "$LOCK"
( while kill -0 $$ 2>/dev/null; do sleep 30; touch "$LOCK" 2>/dev/null; done ) &
REFRESH_PID=$!
trap 'kill $REFRESH_PID 2>/dev/null; rmdir "$LOCK" 2>/dev/null' EXIT INT TERM HUP
"$@"
