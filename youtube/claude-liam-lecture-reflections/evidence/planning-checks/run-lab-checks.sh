#!/bin/zsh
# Compiles every shader this film shows through the Shader Lab (real Godot 4.7.2 window) and records one probe each.
# The Lab draws the shader on an otherwise empty stage, so a screen-reading shader sees the stage colour (0.851, 0.8353, 0.7922) and the
# reflection shaders hide themselves (no red anywhere): that is the expected result here. The real behaviour is checked by exp_*.gd
# (the Lab cannot add a second node or a BackBufferCopy). Output: lab-results.jsonl, png/.
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
  echo "{\"check\":\"$label\",\"shader\":\"$shader\",\"exit\":$code,\"date\":\"$(date +%F\ %T)\",\"output\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' <<<"$line")}" >> "$RES"
  echo "[$code] $label"
}
run 01-screen-preview     01-screen-preview.gdshader      --kind rect   --probe 0.5,0.5
run 02-reflection         02-reflection.gdshader          --kind sprite --sprite-tex sprite --probe 0.5,0.5
run 03-reflection-final   03-reflection-final.gdshader    --kind sprite --sprite-tex sprite --probe 0.5,0.5
run 03-final-tint-teal    03-reflection-final.gdshader    --kind sprite --sprite-tex sprite --set tint=#5FA391 --probe 0.5,0.5
run 04-compare-equal      04-compare-equal.gdshader       --kind sprite --sprite-tex sprite --probe 0.5,0.5
run 05-compare-distance   05-compare-distance.gdshader    --kind sprite --sprite-tex sprite --probe 0.5,0.5
run 01-compat             01-screen-preview.gdshader      --kind rect   --probe 0.5,0.5 --renderer gl_compatibility
run 03-compat             03-reflection-final.gdshader    --kind sprite --sprite-tex sprite --probe 0.5,0.5 --renderer gl_compatibility
echo "wrote $RES"
