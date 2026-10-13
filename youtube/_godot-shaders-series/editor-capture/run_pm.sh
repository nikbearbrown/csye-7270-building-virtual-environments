#!/bin/zsh
# run_pm.sh <size WxH> <out_dir> <pm_state_script.json> [--settings FILE] [--cap N] [--home DIR]
# Records the REAL Project Manager (godot --project-manager --script pm_driver.gd) with Movie Maker, under the shared Lab lock (taken with
# mkdir, refreshed every 30 s by a background loop, released with rmdir in a trap). The Project Manager runs with an isolated HOME, so its
# project list is empty and no real project list is touched; nothing is created (the driver only opens, reads and cancels dialogs).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SIZE="$1"; OUT_ARG="$2"; STATES="$(cd "$(dirname "$3")" && pwd)/$(basename "$3")"; shift 3
mkdir -p "$OUT_ARG"; OUT="$(cd "$OUT_ARG" && pwd)"
SETTINGS=""; CAP=900; HOME_DIR="${GODOT_CAPTURE_HOME:-/private/tmp/claude-501/godot-shaders-editor-capture/home-pm}"
while [ $# -gt 0 ]; do
  case "$1" in
    --settings) SETTINGS="$2"; shift 2;;
    --cap) CAP="$2"; shift 2;;
    --home) HOME_DIR="$2"; shift 2;;
    *) echo "unknown option $1"; exit 2;;
  esac
done
PROJ="$HERE/pmproj"
LOCK=/private/tmp/claude-501/shaderlab.lock
mkdir -p /private/tmp/claude-501
GOT=0; WAIT_START=$(date +%s)
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
echo "lock taken (waited $(( $(date +%s) - WAIT_START ))s)"
rm -rf "$OUT/frames"; mkdir -p "$OUT/frames"; rm -f "$OUT/states.json" "$OUT/run.log"
W="${SIZE%x*}"; H="${SIZE#*x}"
sed -i '' -E "s/^window\/size\/window_width_override=.*/window\/size\/window_width_override=$W/; s/^window\/size\/window_height_override=.*/window\/size\/window_height_override=$H/" "$PROJ/project.godot"
cp "$HERE/pm_driver.gd" "$PROJ/pm_driver.gd"
SDIR="$HOME_DIR/Library/Application Support/Godot"
rm -f "$SDIR"/editor_settings-4*.tres "$SDIR"/projects.cfg
mkdir -p "$SDIR"
[ -n "$SETTINGS" ] && cp "$SETTINGS" "$SDIR/editor_settings-4.7.tres"
{ echo "date: $(date)"; echo "godot: $(godot --version)"; echo "state script: $STATES"; echo "home: $HOME_DIR"; echo "settings: ${SETTINGS:-factory (fresh)}"; echo "size: $SIZE"; } > "$OUT/run-info.txt"
T0=$(date +%s)
HOME="$HOME_DIR" DRIVER_STATE_SCRIPT="$STATES" DRIVER_LOG="$OUT/states.json" timeout 300 godot --path "$PROJ" --project-manager --script res://pm_driver.gd \
  --write-movie "$OUT/frames/f.png" --fixed-fps 30 --quit-after "$CAP" > "$OUT/run.log" 2>&1
CODE=$?
echo "godot exit $CODE; wall $(( $(date +%s) - T0 ))s" | tee -a "$OUT/run-info.txt"
echo "frames: $(ls "$OUT/frames"/f*.png 2>/dev/null | wc -l | tr -d ' ') in $OUT/frames"
grep -E "Movie Maker|Done recording|frames at|recorded in" "$OUT/run.log" | sed 's/^/  /'
grep -E "PM_DRIVER|SCRIPT ERROR|ERROR:" "$OUT/run.log" | head -30 | sed 's/^/  log: /'
exit $CODE
