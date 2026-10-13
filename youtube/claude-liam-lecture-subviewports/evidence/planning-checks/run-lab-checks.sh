#!/bin/zsh
# Re-runs every shader this film shows through the Shader Lab (real Godot 4.7.2 window) and records the result lines.
# Output: lab-results.jsonl (one record per run), png/*.png, lab-summary.txt. Safe to re-run; it overwrites its own outputs.
# What it proves: every file in lab-shaders/ COMPILES (exit 0), the hue function gives the six pure colours, and the stripe shader draws on-fractions equal to its width.
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
  line=$("$LAB/check_shader.sh" "$SH/$shader" "$@" 2>&1)
  local code=$?
  echo "{\"check\":\"$label\",\"shader\":\"$shader\",\"exit\":$code,\"output\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' <<<"$line")}" >> "$RES"
  echo "[$code] $label"
}
# every shader compiles (sprite kind), Forward+ and Compatibility
for f in "$SH"/*.gdshader; do
  b=$(basename "$f")
  run "compile $b (forward_plus)" "$b" --kind sprite
  run "compile $b (gl_compatibility)" "$b" --kind sprite --renderer gl_compatibility
done
# the hue function: six exact hues (saturation 1, value 1), plus an orange, a grey, a half-saturated and a half-bright colour
for h in 0.0 0.1666667 0.3333333 0.5 0.6666667 0.8333333 1.0 0.0833333; do
  run "hue $h (forward_plus)" 06b-hsv-probe.gdshader --kind rect --set hue=$h --probe 0.5,0.5
  run "hue $h (gl_compatibility)" 06b-hsv-probe.gdshader --kind rect --set hue=$h --probe 0.5,0.5 --renderer gl_compatibility
done
run "hue 0 saturation 0 value 0.5" 06b-hsv-probe.gdshader --kind rect --set hue=0.0 --set saturation=0.0 --set value=0.5 --probe 0.5,0.5
run "hue 0 saturation 0.5 value 1" 06b-hsv-probe.gdshader --kind rect --set hue=0.0 --set saturation=0.5 --set value=1.0 --probe 0.5,0.5
run "hue 0 saturation 1 value 0.5" 06b-hsv-probe.gdshader --kind rect --set hue=0.0 --set saturation=1.0 --set value=0.5 --probe 0.5,0.5
# the hue strip as a full 640 x 360 image, for the independent Python comparison (analyze-hue.py)
"$LAB/check_shader.sh" "$SH/06-hsv-strip.gdshader" --kind rect --png "$OUT/06-hsv-strip-rect.png" >/dev/null 2>&1
# stripes on a plain rectangle: on-fraction = width, `count` saws across the top edge (analyze-stripes.py)
for cfg in "6.0 0.5" "10.0 0.25" "3.0 0.8"; do
  c=${cfg% *}; w=${cfg#* }
  "$LAB/check_shader.sh" "$SH/04-stripes.gdshader" --kind rect --set count=$c --set width=$w --png "$OUT/stripes-$c-$w.png" >/dev/null 2>&1
done
python3 "$HERE/analyze-hue.py" | tee "$HERE/lab-hue-analysis.txt"
python3 "$HERE/analyze-stripes.py" | tee "$HERE/lab-stripes-analysis.txt"
python3 - "$RES" > "$HERE/lab-summary.txt" <<'PY'
import json, sys
for line in open(sys.argv[1]):
    r = json.loads(line)
    out = r["output"]
    probes = ""
    if out.startswith("RESULT "):
        d = json.loads(out[7:])
        probes = f'{d["renderer"]} ' + str([p["rgba"][:3] for p in d["probes"]])
    else:
        probes = out[:120]
    print(f'{r["check"]:60} exit {r["exit"]} {probes}')
PY
echo "wrote $RES and lab-summary.txt"
