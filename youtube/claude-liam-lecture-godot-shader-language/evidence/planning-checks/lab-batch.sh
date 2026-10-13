#!/bin/zsh
# (This script was called run-lab-checks.sh until another session's `pkill -f run-lab-checks.sh` killed a batch of that name; it is now
# lab-batch.sh and resumable: RESUME=1 ./lab-batch.sh skips every label already recorded in lab-results.jsonl.)
# Re-runs every shader this film shows through the Shader Lab (real Godot 4.7.2 window) and records, for each run:
# the exact command, the exit code, the Lab's output, and the date. Output: lab-results.jsonl and png/*.png.
# Expected-to-fail shaders (names containing "-err-") must exit 1 with the engine's message; everything else must exit 0.
# Safe to re-run; it overwrites its own outputs. Machine: Apple M4 Pro, Godot 4.7.2, Forward+ (the Lab default).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results.jsonl"
if [ "${RESUME:-0}" != "1" ]; then : > "$RES"; fi; touch "$RES"
run() {  # label shader args...
  local label="$1"; local shader="$2"; shift 2
  local out code stamp
  if [ "${RESUME:-0}" = "1" ] && grep -q "\"check\": \"$label\"" "$RES"; then echo "[skip] $label"; return; fi
  stamp="$(date '+%Y-%m-%d %H:%M:%S')"
  out=$("$LAB/check_shader.sh" "$SH/$shader" "$@" --png "$OUT/$label.png" 2>&1); code=$?
  python3 - "$label" "$shader" "$code" "$stamp" "$*" "$out" >> "$RES" <<'PY'
import json, sys
label, shader, code, stamp, args, out = sys.argv[1:7]
print(json.dumps({"check": label, "shader": shader, "command": f"lab/check_shader.sh lab-shaders/{shader} {args} --png png/{label}.png",
                  "exit": int(code), "date": stamp, "output": out.strip()}))
PY
  echo "[$code] $label"
}
CORNERS=(--probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98 --probe 0.98,0.98 --probe 0.5,0.5)

run 01-breathe-tint-teal   01-breathe.gdshader          --kind rect --set tint=#5FA391 --wait 0.0 --probe 0.5,0.5
run 01-breathe-tint-unset  01-breathe.gdshader          --kind rect --wait 0.0 --probe 0.5,0.5
run 02-spacing-neat        02-spacing-neat.gdshader     --kind rect $CORNERS
run 02-spacing-squeezed    02-spacing-squeezed.gdshader --kind rect $CORNERS
run 02-spacing-spread      02-spacing-spread.gdshader   --kind rect $CORNERS
run 02-spacing-oneline     02-spacing-oneline.gdshader  --kind rect $CORNERS
run 03-comment-on          03-comment-on.gdshader       --kind rect $CORNERS
run 03-comment-off         03-comment-off.gdshader      --kind rect $CORNERS
run 04-globals             04-globals.gdshader          --kind rect --probe 0.1,0.5 --probe 0.9,0.5
run 05-pastel              05-pastel.gdshader           --kind rect $CORNERS
run 06-pastel-bgr          06-pastel-bgr.gdshader       --kind rect $CORNERS
run 07-vec-times-vec       07-vec-times-vec.gdshader    --kind rect --probe 0.5,0.5
run 07b-vec-times-float    07b-vec-times-float.gdshader --kind rect --probe 0.5,0.5
run 08-texture-vec4        08-texture-vec4.gdshader     --kind sprite --probe 0.5,0.5 --probe 0.02,0.02
run 09-soften-function     09-soften-function.gdshader  --kind rect $CORNERS
run 10-pass-uv-in          10-pass-uv-in.gdshader       --kind rect $CORNERS
run 11-global-time         11-global-time.gdshader      --kind rect --wait 0.0 --probe 0.5,0.5
run 12-in-copy             12-in-copy.gdshader          --kind rect --probe 0.5,0.5
run 13-inout               13-inout.gdshader            --kind rect --probe 0.5,0.5
run 14-out                 14-out.gdshader              --kind rect --probe 0.5,0.5
run 15-overload            15-overload.gdshader         --kind rect --probe 0.25,0.5 --probe 0.75,0.5
run 16-split-if            16-split-if.gdshader         --kind rect --probe 0.25,0.5 --probe 0.75,0.5
run 17-split-ternary       17-split-ternary.gdshader    --kind rect --probe 0.25,0.5 --probe 0.75,0.5
run 18-stripes             18-stripes.gdshader          --kind rect --probe 0.5,0.1 --probe 0.5,0.2 --probe 0.5,0.3 --probe 0.5,0.4 --probe 0.5,0.5 --probe 0.5,0.7 --probe 0.5,0.9
run 19-float-equals-640     19-float-equals.gdshader    --kind rect --size 640x360 --probe 0.5,0.5
run 19-float-equals-1280    19-float-equals.gdshader    --kind rect --size 1280x720 --probe 0.5,0.5
run 19-float-equals-1920    19-float-equals.gdshader    --kind rect --size 1920x1080 --probe 0.5,0.5
run 19-float-equals-641     19-float-equals.gdshader    --kind rect --size 641x360 --probe 0.5,0.5
run 19-float-equals-1001    19-float-equals.gdshader    --kind rect --size 1001x500 --probe 0.5,0.5
run 19-float-equals-321     19-float-equals.gdshader    --kind rect --size 321x180 --probe 0.5,0.5
run 20-float-range-640      20-float-range.gdshader     --kind rect --size 640x360 --probe 0.5,0.5 --probe 0.25,0.5
run 20-float-range-1280     20-float-range.gdshader     --kind rect --size 1280x720 --probe 0.5,0.5
run 20-float-range-1920     20-float-range.gdshader     --kind rect --size 1920x1080 --probe 0.5,0.5
run 21-blend-add           21-blend-add.gdshader        --kind rect --probe 0.5,0.5
run 22-blend-mix           22-blend-mix.gdshader        --kind rect --probe 0.5,0.5
run 24-fill-vec3           24-fill-vec3.gdshader        --kind rect --probe 0.5,0.5
run 25-constructor-ints    25-constructor-ints.gdshader --kind rect --probe 0.5,0.5

run 29-float-sum-equals    29-float-sum-equals.gdshader --kind rect --probe 0.5,0.5
run 30-float-dot-shorthand 30-float-dot-shorthand.gdshader --kind rect --probe 0.5,0.5
run 32-declaration         32-declaration.gdshader      --kind rect --probe 0.5,0.5
run 33-swizzle-pick        33-swizzle-pick.gdshader     --kind rect --probe 0.5,0.5
run 27-unset-tint          27-unset-tint.gdshader       --kind rect --probe 0.5,0.5
run 28-ctor-vec2-vec2      28-ctor-vec2-vec2.gdshader   --kind rect --probe 0.5,0.5

for f in "$SH"/*-err-*.gdshader; do
  b="$(basename "$f" .gdshader)"
  run "$b" "$(basename "$f")" --kind rect --probe 0.5,0.5
done
echo "wrote $RES"
