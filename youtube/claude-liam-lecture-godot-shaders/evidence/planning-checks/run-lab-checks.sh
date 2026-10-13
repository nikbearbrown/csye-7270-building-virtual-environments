#!/bin/zsh
# Re-runs every shader this film shows through the Shader Lab (real Godot 4.7.2 window) and records the pixels.
# Output: lab-results.jsonl (one RESULT per check) and png/*.png. Safe to re-run; it overwrites its own outputs.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results.jsonl"; : > "$RES"
run() {  # label shader args...
  local label="$1"; local shader="$2"; shift 2
  local line
  line=$("$LAB/check_shader.sh" "$SH/$shader" "$@" --png "$OUT/$label.png" 2>&1)
  local code=$?
  echo "{\"check\":\"$label\",\"shader\":\"$shader\",\"exit\":$code,\"output\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' <<<"$line")}" >> "$RES"
  echo "[$code] $label"
}
run 01-gradient       01-gradient.gdshader      --kind rect --probe 0.02,0.5 --probe 0.5,0.5 --probe 0.98,0.5
run 02-hook-wobble    02-hook-wobble.gdshader   --kind sprite --sprite-tex checker --wait 0.6
run 03-red            03-red.gdshader           --kind rect --probe 0.5,0.5
run 04-lean-white     04-lean.gdshader          --kind sprite --sprite-tex white --sprite-scale 1.0
run 04-lean-checker   04-lean.gdshader          --kind sprite --sprite-tex checker --sprite-scale 1.0
run 05-discard-half   05-discard-half.gdshader  --kind rect --probe 0.25,0.5 --probe 0.75,0.5 --probe 0.9,0.9
run 06-dial-default   06-dial.gdshader          --kind rect --probe 0.5,0.5
run 06-dial-0.9       06-dial.gdshader          --kind rect --set red=0.9 --probe 0.5,0.5
run 07-mixer          07-mixer.gdshader         --kind rect --set red=1.0 --set green=0.5 --set blue=0.0 --probe 0.5,0.5
run 08-uv-colors      08-uv-colors.gdshader     --kind rect --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98
run 09-uv-fade        09-uv-fade.gdshader       --kind sprite --sprite-tex white --probe 0.05,0.5 --probe 0.30,0.5 --probe 0.70,0.5
run 10-pulse-a        10-pulse.gdshader         --kind rect --wait 0.0 --probe 0.5,0.5
run 10-pulse-b        10-pulse.gdshader         --kind rect --wait 0.5 --probe 0.5,0.5
run 11-time-bar       11-time-bar.gdshader      --kind rect --wait 1.2 --probe 0.5,0.97 --probe 0.5,0.78 --probe 0.5,0.59 --probe 0.5,0.40 --probe 0.5,0.22 --probe 0.5,0.03
run 12-iris-0.3       12-iris.gdshader          --kind sprite --sprite-tex checker --set radius=0.3 --probe 0.5,0.5 --probe 0.32,0.18
run 12-iris-0.0       12-iris.gdshader          --kind sprite --sprite-tex checker --set radius=0.0 --probe 0.5,0.5
run 12-iris-0.8       12-iris.gdshader          --kind sprite --sprite-tex checker --set radius=0.8 --probe 0.5,0.5 --probe 0.32,0.18

run 13-light-count      13-light-count.gdshader   --kind rect
echo "wrote $RES"
