#!/bin/zsh
# Runs every shader this film shows through the Shader Lab (real Godot 4.7.2 window) and records the pixels.
# The Lab's "screen" is empty: a flat warm grey (stage colour 0.851, 0.8353, 0.7922). A screen-reading shader therefore reads that colour,
# which makes the arithmetic checkable: window = stage colour, invert = 1 - stage, gray = luma of the stage, water = half stage + half water colour.
# Output: lab-results.jsonl (one RESULT per check, with the exit code) and png/*.png. Safe to re-run; it overwrites its own outputs.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results.jsonl"; : > "$RES"
run() {  # label shader args...
  local label="$1"; local shader="$2"; shift 2
  local line code
  line=$("$LAB/check_shader.sh" "$SH/$shader" "$@" --png "$OUT/$label.png" 2>&1)
  code=$?
  printf '%s\n' "$(python3 -c 'import json,sys; print(json.dumps({"check": sys.argv[1], "shader": sys.argv[2], "exit": int(sys.argv[3]), "output": sys.stdin.read().strip()}))' "$label" "$shader" "$code" <<<"$line")" >> "$RES"
  echo "[$code] $label"
}
C=(--probe 0.5,0.5)
run 01-window            01-window.gdshader              --kind rect $C
run 02-miniature         02-miniature.gdshader           --kind rect $C
run 03-invert            03-invert.gdshader              --kind rect $C
run 04-godot3-expected-to-FAIL 04-godot3-screen-texture.gdshader --kind rect $C
run 05-gray-1            05-gray.gdshader                --kind rect --set amount=1.0 $C
run 05-gray-0.5          05-gray.gdshader                --kind rect --set amount=0.5 $C
run 06-oval-inside       06-spotlight-oval.gdshader      --kind rect --set player=0.5,0.5 --set radius=0.25 $C
run 06-oval-outside      06-spotlight-oval.gdshader      --kind rect --set player=0.5,0.5 --set radius=0.25 --probe 0.95,0.5
run 07-spot-inside       07-spotlight.gdshader           --kind rect --set player=0.5,0.5 --set radius=0.25 $C
run 07-spot-outside      07-spotlight.gdshader           --kind rect --set player=0.5,0.5 --set radius=0.25 --probe 0.95,0.5
run 08-shift             08-shift.gdshader               --kind rect --set shift=0.1 $C
run 09-ripple-still      09-ripple-still.gdshader        --kind rect --set amount=0.01 $C
run 10-ripple            10-ripple.gdshader              --kind rect --set amount=0.01 --wait 0.5 $C
run 11-water             11-water.gdshader               --kind rect $C
run 12-pool-above-edge   12-pool.gdshader                --kind rect --probe 0.5,0.02
run 12-pool-below-edge   12-pool.gdshader                --kind rect --probe 0.5,0.5
run 13-ripple-ride       13-ripple-ride.gdshader         --kind rect $C
run 14-blur-0            14-blur.gdshader                --kind rect --set blur=0.0 $C
run 14-blur-4            14-blur.gdshader                --kind rect --set blur=4.0 $C
run 15-edge-clamp        15-edge-clamp.gdshader          --kind rect --set shift=0.3 $C
echo "wrote $RES"
