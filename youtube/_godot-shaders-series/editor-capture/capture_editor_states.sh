#!/bin/zsh
# capture_editor_states.sh <scratch-project> <scene|-> <state_script.json> <out_dir> [options]
#
# Runs the REAL Godot editor (godot --editor) on a SCRATCH project with the driver plugin enabled, while Movie Maker records the editor
# window as PNG frames, then prints where the frames and the driver log (states.json) are. Never run on a project Bear works in.
#
#   <scratch-project>  folder with project.godot, addons/driver/ (plugin.gd, plugin.cfg) and the scenes
#   <scene>            res:// path opened on the command line (e.g. res://scenes/e1_sprite.tscn), or - for none (the script can open_scene)
#   <state_script.json> the steps the driver executes (see addons/driver/plugin.gd); copied to <project>/state_script.json
#   <out_dir>          OUTSIDE the project (frames inside res:// are imported as assets and slow the editor to ~13 % of real time)
#                      gets frames/f00000000.png ..., states.json (the driver log), run.log, run-info.txt
# Options:
#   --size WxH         window override written into the scratch project.godot before the run (default: leave as is; the pilot uses 1920x1080)
#   --renderer R       forward_plus | mobile | gl_compatibility  (default: Godot's default, forward_plus)
#   --cap N            --quit-after N safety cap in frames (default: estimated from the script; the driver quits itself when done)
#   --home DIR         HOME for the editor process (default: $GODOT_CAPTURE_HOME or /private/tmp/claude-501/godot-shaders-editor-capture/home). An isolated HOME keeps the editor's settings and cache
#                      away from the real ~/Library/Application Support/Godot and gives the factory-default editor look.
#   --no-import        skip the headless import pass (it runs when <project>/.godot is missing)
#   --reimport         force the headless import pass
#   --keep-frames      do not delete an existing <out_dir>/frames first
#   --settings FILE    copy FILE to <home>/Library/Application Support/Godot/editor_settings-4.7.tres before the run (default: delete it, so the
#                      editor starts from its factory settings every time; the project's .godot/editor layout/fold state is also reset every run)
#   --keep-state       do not reset <project>/.godot/editor (layout, fold state, open shader files) or the editor settings
#
# THE LAB LOCK (shared with 16 other agents): /private/tmp/claude-501/shaderlab.lock is a DIRECTORY taken with mkdir. A lock older than
# 3 minutes is treated as stale by everybody. An editor run takes longer than that, so while this script holds the lock a background
# loop touches it every 30 s. The loop dies with this script; the lock is released with rmdir in a trap. The editor never runs without it.
set -u
if [ $# -lt 4 ]; then sed -n '2,28p' "$0"; exit 2; fi
PROJ="$(cd "$1" && pwd)" || exit 2; SCENE="$2"; STATES="$(cd "$(dirname "$3")" && pwd)/$(basename "$3")"; OUT_ARG="$4"; shift 4
mkdir -p "$OUT_ARG" || exit 2
OUT="$(cd "$OUT_ARG" && pwd)"
SIZE=""; RENDERER=""; CAP=""; HOME_DIR="${GODOT_CAPTURE_HOME:-/private/tmp/claude-501/godot-shaders-editor-capture/home}"; DO_IMPORT=auto; KEEP=0; SETTINGS=""; KEEP_STATE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --size) SIZE="$2"; shift 2;;
    --renderer) RENDERER="$2"; shift 2;;
    --cap) CAP="$2"; shift 2;;
    --home) HOME_DIR="$2"; shift 2;;
    --no-import) DO_IMPORT=no; shift;;
    --reimport) DO_IMPORT=yes; shift;;
    --keep-frames) KEEP=1; shift;;
    --settings) SETTINGS="$2"; shift 2;;
    --keep-state) KEEP_STATE=1; shift;;
    *) echo "unknown option $1"; exit 2;;
  esac
done
[ -f "$PROJ/project.godot" ] || { echo "no project.godot in $PROJ"; exit 2; }
[ -f "$STATES" ] || { echo "no state script $STATES"; exit 2; }
case "$OUT/" in "$PROJ"/*) echo "REFUSING: out_dir $OUT is inside the project; frames there get imported as assets and the editor crawls"; exit 2;; esac
mkdir -p "$HOME_DIR"

# ---- take the lab lock (never run an editor/window without it) -----------------------------------------------------------------
LOCK=/private/tmp/claude-501/shaderlab.lock
mkdir -p /private/tmp/claude-501
GOT=0; WAIT_START=$(date +%s)
for i in $(seq 1 3600); do
  if mkdir "$LOCK" 2>/dev/null; then GOT=1; break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
[ "$GOT" = 1 ] || { echo "could not get the Lab lock in 30 minutes"; exit 4; }
LOCK_WAIT=$(( $(date +%s) - WAIT_START ))
touch "$LOCK"
( while kill -0 $$ 2>/dev/null; do sleep 30; touch "$LOCK" 2>/dev/null; done ) &
REFRESH_PID=$!
trap 'kill $REFRESH_PID 2>/dev/null; rmdir "$LOCK" 2>/dev/null' EXIT INT TERM HUP
LOCK_T0=$(date +%s)
echo "lock taken (waited ${LOCK_WAIT}s); refreshing every 30 s; released on exit"

# ---- prepare (inside the lock; all of it is inside the scratch project or out_dir) ----------------------------------------------
[ "$KEEP" = 1 ] || rm -rf "$OUT/frames"
mkdir -p "$OUT/frames"
rm -f "$OUT/states.json" "$OUT/run.log" "$OUT/run-info.txt"
if [ -n "$SIZE" ]; then
  W="${SIZE%x*}"; H="${SIZE#*x}"
  sed -i '' -E "s/^window\/size\/window_width_override=.*/window\/size\/window_width_override=$W/; s/^window\/size\/window_height_override=.*/window\/size\/window_height_override=$H/" "$PROJ/project.godot"
fi
if [ "$DO_IMPORT" = yes ] || { [ "$DO_IMPORT" = auto ] && [ ! -d "$PROJ/.godot" ]; }; then
  echo "headless import pass..."
  HOME="$HOME_DIR" timeout 120 godot --headless --path "$PROJ" --import > "$OUT/import.log" 2>&1
fi
GODOT_SETTINGS_DIR="$HOME_DIR/Library/Application Support/Godot"
if [ "$KEEP_STATE" = 0 ]; then
  rm -rf "$PROJ/.godot/editor" "$PROJ/created"; mkdir -p "$PROJ/created"   # created/ holds shaders the driver makes through the real New Shader dialog
  rm -f "$GODOT_SETTINGS_DIR"/editor_settings-4*.tres
fi
if [ -n "$SETTINGS" ]; then mkdir -p "$GODOT_SETTINGS_DIR"; cp "$SETTINGS" "$GODOT_SETTINGS_DIR/editor_settings-4.7.tres"; fi
cp "$STATES" "$PROJ/state_script.json"
if [ -z "$CAP" ]; then
  CAP=$(python3 - "$STATES" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
steps = d["steps"] if isinstance(d, dict) else d
boot = d.get("boot_frames", 25) if isinstance(d, dict) else 25
n = boot + 40
for s in steps:
    n += 2 + int(s.get("settle", 0))
    if s.get("op") == "wait_frames": n += int(s.get("n", 1)) + 1
    if s.get("op") == "open_scene": n += 150
print(int(n * 1.5) + 200)
PY
)
fi
SCENE_ARG=(); [ "$SCENE" != "-" ] && SCENE_ARG=("$SCENE")
RM=(); [ -n "$RENDERER" ] && RM=(--rendering-method "$RENDERER")
{
  echo "date: $(date)"; echo "godot: $(godot --version)"; echo "project: $PROJ"; echo "scene: $SCENE"; echo "state script: $STATES"
  echo "home: $HOME_DIR"; echo "settings: ${SETTINGS:-factory (reset each run)}"; echo "renderer arg: ${RENDERER:-default}"; echo "size arg: ${SIZE:-as in project.godot}"; echo "cap: $CAP"
  grep -E "^window/size/window_(width|height)_override" "$PROJ/project.godot"
} > "$OUT/run-info.txt"

# ---- the run ------------------------------------------------------------------------------------------------------------------
T0=$(date +%s)
HOME="$HOME_DIR" DRIVER_LOG="$OUT/states.json" timeout 900 godot --editor --path "$PROJ" "${SCENE_ARG[@]}" "${RM[@]}" \
  --write-movie "$OUT/frames/f.png" --fixed-fps 30 --quit-after "$CAP" > "$OUT/run.log" 2>&1
CODE=$?
T1=$(date +%s)
echo "godot exit $CODE; wall $((T1 - T0))s; lock held $((T1 - LOCK_T0))s so far" | tee -a "$OUT/run-info.txt"

# ---- report -------------------------------------------------------------------------------------------------------------------
NF=$(ls "$OUT/frames"/f*.png 2>/dev/null | wc -l | tr -d ' ')
echo "frames: $NF in $OUT/frames  (first: $(ls "$OUT/frames"/f*.png 2>/dev/null | head -1 | xargs -n1 basename 2>/dev/null), last: $(ls "$OUT/frames"/f*.png 2>/dev/null | tail -1 | xargs -n1 basename 2>/dev/null))"
grep -E "Movie Maker|Done recording|frames at|recorded in|Encoding time" "$OUT/run.log" | sed 's/^/  /'
if [ -f "$OUT/states.json" ]; then
  python3 - "$OUT/states.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("driver log: %s  finished_frame=%s  marks=%d  errors=%d" % (sys.argv[1], d.get("finished_frame"), len(d["marks"]), len(d["errors"])))
for k, v in d["marks"].items():
    print("  mark %-44s frame %s" % (k, v["frame"]))
for e in d["errors"]:
    print("  ERROR frame %s: %s" % (e["frame"], e["text"]))
PY
else
  echo "NO states.json (the driver did not finish or never started). Last log lines:"; tail -15 "$OUT/run.log"
fi
grep -E "SCRIPT ERROR|ERROR:|Parse Error|DRIVER ERROR" "$OUT/run.log" | head -12 | sed 's/^/  log: /'
echo "next: python3 $(dirname "$0")/extract_marks.py $OUT/states.json $OUT/frames <named_png_dir>"
exit $CODE
