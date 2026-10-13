#!/bin/zsh
# run-glow-checks.sh: the glow experiment matrix. Each run is a fresh Godot 4.7.2 process in a scratch project (glow_check.gd copied in).
# Output: glow-results.jsonl (label, renderer, full argument list, exit code, RESULT line) and png/glow-<label>.png (what the screen shows).
# Holds the shared Shader Lab lock while it runs, so no other Godot window overlaps. Safe to re-run.
# Stage colour #5F7A96 (a mid-dark slate blue): glow adds light, and a light stage leaves almost no headroom for a halo.
# It is 79 RGB away from the type gate's MUTE grey (#5D584F) and 131 from ink, so GATE T will not read the stage as text (the earlier #57625E was 19 away).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
SCRATCH=/private/tmp/claude-501/godot-shaders-soft-edges-glow-and-noise/scratch-glow
SCRATCH_PROJ=/private/tmp/claude-501/godot-shaders-soft-edges-glow-and-noise/scratch-glow-projhdr   # same project but with the HDR 2D PROJECT SETTING on
SHADER="$FILM/lab-shaders/14-glow-bubble.gdshader"
EVS="$HERE/shaders"
OUT="$HERE/png"; mkdir -p "$OUT" "$SCRATCH" "$SCRATCH_PROJ"
cp "$HERE/glow_check.gd" "$SCRATCH/glow_check.gd"; cp "$HERE/glow_check.gd" "$SCRATCH_PROJ/glow_check.gd"
printf 'config_version=5\n\n[application]\n\nconfig/name="glow-scratch"\nconfig/features=PackedStringArray("4.7")\n\n[display]\n\nwindow/size/viewport_width=640\nwindow/size/viewport_height=360\n' > "$SCRATCH/project.godot"
printf 'config_version=5\n\n[application]\n\nconfig/name="glow-scratch-projhdr"\nconfig/features=PackedStringArray("4.7")\n\n[display]\n\nwindow/size/viewport_width=640\nwindow/size/viewport_height=360\n\n[rendering]\n\nviewport/hdr_2d=true\n' > "$SCRATCH_PROJ/project.godot"
RES="$HERE/glow-results.jsonl"; : > "$RES"
LOCK=/private/tmp/claude-501/shaderlab.lock
for i in $(seq 1 480); do
  if mkdir "$LOCK" 2>/dev/null; then break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
STAGE="#5F7A96"
runp() {  # label project-dir renderer shader args...
  local label="$1"; local proj="$2"; local rend="$3"; local shader="$4"; shift 4
  local rm=(); [ "$rend" != "forward_plus" ] && rm=(--rendering-method "$rend")
  local log; log=$(mktemp -t glowcheck.XXXXXX)
  timeout 60 godot --path "$proj" "${rm[@]}" --script res://glow_check.gd -- --shader "$shader" --label "$label" --clear "$STAGE" --png "$OUT/glow-$label${rend/forward_plus/}.png" "$@" > "$log" 2>&1
  local code=$?
  python3 - "$label" "$rend" "$code" "$*" "$(grep -E '^RESULT ' "$log" | head -1)" "$(grep -E 'ERROR|SCRIPT' "$log" | head -3)" >> "$RES" <<'PY'
import json, sys
label, rend, code, args, res, err = sys.argv[1:7]
print(json.dumps({"label": label, "renderer_flag": rend, "args": args, "exit": int(code), "result": res, "errors": err}))
PY
  echo "[$code] $label ($rend)"
  rm -f "$log"
}
run() { local label="$1"; local rend="$2"; shift 2; runp "$label" "$SCRATCH" "$rend" "$SHADER" "$@"; }
# --- Forward+ (Metal on this Mac) ---
run G0-sdr-glow0            forward_plus --glow 0.0 --sub
run G1-sdr-glow1            forward_plus --glow 1.0 --sub
run G2-hdr-glow0            forward_plus --glow 0.0 --hdr2d --sub
run G3-hdr-glow1            forward_plus --glow 1.0 --hdr2d --sub
run G4-hdr-glow1-env-nocanvas forward_plus --glow 1.0 --hdr2d --env --intensity 2.0 --sub
run G5-hdr-glow1-env-canvas-default forward_plus --glow 1.0 --hdr2d --env --bgcanvas --sub
run G6-hdr-glow1-env-canvas-int2 forward_plus --glow 1.0 --hdr2d --env --bgcanvas --intensity 2.0 --sub
run G7-hdr-glow0-env-canvas-int2 forward_plus --glow 0.0 --hdr2d --env --bgcanvas --intensity 2.0 --sub
run G8-sdr-glow1-env-canvas-thr0.5-int2 forward_plus --glow 1.0 --env --bgcanvas --threshold 0.5 --intensity 2.0 --sub
run G9-sdr-glow1-env-canvas-thr1.0-int2 forward_plus --glow 1.0 --env --bgcanvas --intensity 2.0 --sub
runp G10-projsetting-hdr-glow1-env-canvas-int2 "$SCRATCH_PROJ" forward_plus "$SHADER" --glow 1.0 --env --bgcanvas --intensity 2.0 --sub
# --- the glow dial: where does the halo start? (HDR 2D + environment + canvas background, intensity 2)
run G11-dial-0.1 forward_plus --glow 0.1 --hdr2d --env --bgcanvas --intensity 2.0 --sub
run G12-dial-0.2 forward_plus --glow 0.2 --hdr2d --env --bgcanvas --intensity 2.0 --sub
run G13-dial-0.3 forward_plus --glow 0.3 --hdr2d --env --bgcanvas --intensity 2.0 --sub
run G14-dial-0.5 forward_plus --glow 0.5 --hdr2d --env --bgcanvas --intensity 2.0 --sub
# --- the same settings as G6 on the Lab's LIGHT stage (#D9D5CA): how much room does a halo have?
run G15-lightstage-hdr-glow1-env-canvas-int2 forward_plus --glow 1.0 --hdr2d --env --bgcanvas --intensity 2.0 --clear "#D9D5CA" --sub
# --- the source_color hint with and without HDR 2D (flat colour, display values) ---
runp H0-hint-sdr          "$SCRATCH" forward_plus "$EVS/ev-flat-hint.gdshader"
runp H1-hint-hdr          "$SCRATCH" forward_plus "$EVS/ev-flat-hint.gdshader" --hdr2d
runp H2-nohint-sdr        "$SCRATCH" forward_plus "$EVS/ev-flat-nohint.gdshader"
runp H3-nohint-hdr        "$SCRATCH" forward_plus "$EVS/ev-flat-nohint.gdshader" --hdr2d
# --- Compatibility (OpenGL on this Mac): the same shader, three of the runs ---
run G1-sdr-glow1            gl_compatibility --glow 1.0 --sub
run G3-hdr-glow1            gl_compatibility --glow 1.0 --hdr2d --sub
run G6-hdr-glow1-env-canvas-int2 gl_compatibility --glow 1.0 --hdr2d --env --bgcanvas --intensity 2.0 --sub
runp H1-hint-hdr          "$SCRATCH" gl_compatibility "$EVS/ev-flat-hint.gdshader" --hdr2d
runp H3-nohint-hdr        "$SCRATCH" gl_compatibility "$EVS/ev-flat-nohint.gdshader" --hdr2d
echo "wrote $RES"
