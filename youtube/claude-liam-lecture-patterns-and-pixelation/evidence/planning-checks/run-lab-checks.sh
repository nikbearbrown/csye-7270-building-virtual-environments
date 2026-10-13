#!/bin/zsh
# Re-runs every shader this film shows (and the evidence-only reference shaders) through the series Shader Lab: a real Godot 4.7.2
# window. Writes lab-results.jsonl (one line per run: date, label, command, shader, options, exit code, the Lab's RESULT line or error) and png/*.png.
# Safe to re-run; it overwrites its own outputs. Then run: python3 verify-patterns.py   (compares renders with the formulas)
# Machine: Apple M4 Pro, macOS, Godot 4.7.2 stable (official). Renderer: Forward+ unless the label says "compat".
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
REF="$HERE/reference-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results.jsonl"
# Optional: ONLY="12-dots 14-halftone" ./run-lab-checks.sh re-runs only the labels that start with those prefixes and replaces their lines
# in lab-results.jsonl (used after a shader file was edited). Without ONLY the whole batch runs and the file is rewritten.
if [ -z "${ONLY:-}" ]; then : > "$RES"; fi
run() {  # label shaderfile (in lab-shaders/, or ref:name in reference-shaders/) args...
  local label="$1"; local shader="$2"; shift 2
  if [ -n "${ONLY:-}" ]; then local hit=0; for pre in ${=ONLY}; do case "$label" in ${pre}*) hit=1;; esac; done; [ $hit -eq 1 ] || return 0; fi
  local spath="$SH/$shader"
  case "$shader" in ref:*) spath="$REF/${shader#ref:}";; esac
  local line
  line=$("$LAB/check_shader.sh" "$spath" "$@" --png "$OUT/$label.png" 2>&1)
  local code=$?
  python3 -c 'import json,sys,datetime; sh=sys.argv[2]; pa=("evidence/planning-checks/reference-shaders/"+sh[4:]) if sh.startswith("ref:") else "lab-shaders/"+sh; print(json.dumps({"date": datetime.date.today().isoformat(), "check": sys.argv[1], "command": "lab/check_shader.sh "+pa+" "+sys.argv[3]+" --png png/"+sys.argv[1]+".png", "shader": sh, "options": sys.argv[3], "exit": int(sys.argv[4]), "output": sys.stdin.read().strip()}))' \
    "$label" "$shader" "$*" "$code" <<<"$line" >> "$RES"
  echo "[$code] $label"
}
SQ=(--kind rect --size 360x360)            # a square rect: normalized probe positions are UV
SP=(--kind sprite --sprite-tex sprite)     # the test sprite at the Lab's fit scale (a 288 px square on the stage)
SP1=(--kind sprite --sprite-tex sprite --sprite-scale 1.0)   # picture pixels = screen pixels (measurements)
GR1=(--kind sprite --sprite-tex gradient --sprite-scale 1.0)

# ── Hook: the four patterns in one shader (phase swept 0 to 1 by the capture harness) ──
for ph in 0.0 0.25 0.5 0.75 1.0; do run "01-showcase-p$ph" 01-showcase.gdshader "${SP[@]}" --set phase=$ph; done

# ── Act I: cells ──
run 02-cells-floor-sq     02-cells-floor.gdshader "${SQ[@]}" --probe 0.125,0.125 --probe 0.875,0.125 --probe 0.125,0.875 --probe 0.875,0.875 --probe 0.625,0.375
run 02-cells-floor-sprite 02-cells-floor.gdshader --kind sprite --sprite-tex white
run 03-cells-fract-sq     03-cells-fract.gdshader "${SQ[@]}" --probe 0.025,0.025 --probe 0.525,0.525 --probe 0.225,0.225 --probe 0.725,0.725 --probe 0.125,0.125
run 03-cells-fract-sprite 03-cells-fract.gdshader --kind sprite --sprite-tex white
run 04-tile-sprite        04-tile.gdshader "${SP[@]}"

# ── Act II: pixelate (sprite = blob with eyes; gradient = a picture that varies everywhere) ──
run ref-sprite-1x         ref:ref-passthrough.gdshader "${SP1[@]}"
run ref-gradient-1x       ref:ref-passthrough.gdshader "${GR1[@]}"
for n in 8 16 32; do
  run 05-corner-n$n-sprite-1x  05-pixelate-corner.gdshader "${SP1[@]}" --set blocks=$n
  run 06-center-n$n-sprite-1x  06-pixelate-center.gdshader "${SP1[@]}" --set blocks=$n
  run 07-round-n$n-sprite-1x   07-pixelate-round.gdshader  "${SP1[@]}" --set blocks=$n
done
run 05-corner-n16-gradient-1x 05-pixelate-corner.gdshader "${GR1[@]}" --set blocks=16
run 06-center-n16-gradient-1x 06-pixelate-center.gdshader "${GR1[@]}" --set blocks=16
run 07-round-n16-gradient-1x  07-pixelate-round.gdshader  "${GR1[@]}" --set blocks=16
run 05-corner-n16-sprite-fit  05-pixelate-corner.gdshader "${SP[@]}" --set blocks=16
run 06-center-n16-sprite-fit  06-pixelate-center.gdshader "${SP[@]}" --set blocks=16
run 07-round-n16-sprite-fit   07-pixelate-round.gdshader  "${SP[@]}" --set blocks=16
for n in 128 64 32 16 8; do run 06-center-n$n-sprite-fit 06-pixelate-center.gdshader "${SP[@]}" --set blocks=$n; done

# same three variants in the Compatibility renderer (pixel values must agree)
for v in 05-pixelate-corner 06-pixelate-center 07-pixelate-round; do
  run "$v-n16-sprite-1x-compat"   $v.gdshader "${SP1[@]}" --set blocks=16 --renderer gl_compatibility
  run "$v-n16-gradient-1x-compat" $v.gdshader "${GR1[@]}" --set blocks=16 --renderer gl_compatibility
done

# ── Act III: block size in picture pixels ──
run 08-block1-sprite-1x   08-pixelate-block.gdshader "${SP1[@]}" --set block=1
run 08-block8-sprite-1x   08-pixelate-block.gdshader "${SP1[@]}" --set block=8
run 08-block8-gradient-1x 08-pixelate-block.gdshader "${GR1[@]}" --set block=8
run 08-block6-gradient-1x 08-pixelate-block.gdshader "${GR1[@]}" --set block=6
for b in 1 2 4 8 16 32; do run 08-block$b-sprite-fit 08-pixelate-block.gdshader "${SP[@]}" --set block=$b; done
run 08-block8-sprite-fit-compat 08-pixelate-block.gdshader "${SP[@]}" --set block=8 --renderer gl_compatibility

# ── Act IV: checkerboard and stripes ──
run 09-checker-sq         09-checker.gdshader "${SQ[@]}" --probe 0.0625,0.0625 --probe 0.1875,0.0625 --probe 0.0625,0.1875 --probe 0.1875,0.1875 --probe 0.9375,0.9375 --probe 0.9375,0.8125
run 09-checker-sprite     09-checker.gdshader --kind sprite --sprite-tex white
run 09-checker-sq-compat  09-checker.gdshader "${SQ[@]}" --probe 0.0625,0.0625 --probe 0.1875,0.0625 --renderer gl_compatibility
run 10-stripes-sq         10-stripes.gdshader "${SQ[@]}" --probe 0.02,0.02 --probe 0.15,0.02 --probe 0.30,0.02 --probe 0.40,0.02
run 10-stripes-sprite     10-stripes.gdshader --kind sprite --sprite-tex white
run 10-stripes-w25-sq     10-stripes.gdshader "${SQ[@]}" --set width=0.25
run 10-stripes-w75-sq     10-stripes.gdshader "${SQ[@]}" --set width=0.75
run 10-stripes-c8-sq      10-stripes.gdshader "${SQ[@]}" --set count=8
run 11-stripes-moving-t1  11-stripes-moving.gdshader "${SQ[@]}" --wait 0.3
run 11-stripes-moving-t2  11-stripes-moving.gdshader "${SQ[@]}" --wait 1.3
run 11-stripes-moving-t3  11-stripes-moving.gdshader "${SQ[@]}" --wait 0.6
run 11-stripes-moving-t0  11-stripes-moving.gdshader "${SQ[@]}" --wait 0.0
run 11-stripes-moving-sprite 11-stripes-moving.gdshader --kind sprite --sprite-tex white --wait 0.3

# ── Act V: dots ──
for r in 0.2 0.35 0.5 0.6 0.7 0.72; do run 12-dots-r$r-sq 12-dots.gdshader "${SQ[@]}" --set radius=$r; done
run 12-dots-sprite        12-dots.gdshader --kind sprite --sprite-tex white
run 12-dots-wide          12-dots.gdshader --kind rect --size 640x360
run 13-dots-square-wide   13-dots-square.gdshader --kind rect --size 640x360
run 12-dots-wide-compat   12-dots.gdshader --kind rect --size 640x360 --renderer gl_compatibility
run 14-halftone-sprite-fit 14-halftone.gdshader "${SP[@]}"
run 14-halftone-sprite-1x  14-halftone.gdshader "${SP1[@]}" --set cells=16
run 14-halftone-gradient-1x 14-halftone.gdshader "${GR1[@]}" --set cells=16
for c in 8 16 24 48; do run 14-halftone-c$c-sprite-fit 14-halftone.gdshader "${SP[@]}" --set cells=$c; done
# the rounded variant against the floored one on a picture that reaches the edges (the checker texture): 8 cells, at the fit scale and at scale 1.0
run 14-halftone-checker-c8-fit            14-halftone.gdshader         --kind sprite --sprite-tex checker --set cells=8
run 15-halftone-rounded-checker-c8-fit    15-halftone-rounded.gdshader --kind sprite --sprite-tex checker --set cells=8
run 14-halftone-checker-c8-1x             14-halftone.gdshader         --kind sprite --sprite-tex checker --sprite-scale 1.0 --set cells=8
run 15-halftone-rounded-checker-c8-1x     15-halftone-rounded.gdshader --kind sprite --sprite-tex checker --sprite-scale 1.0 --set cells=8
run 15-halftone-rounded-sprite-fit        15-halftone-rounded.gdshader "${SP[@]}"

# ── Evidence-only reference shaders (numbers spoken in the film, language facts) ──
run chk-negative-fract-mod   ref:chk-negative-fract-mod.gdshader --kind rect --probe 0.5,0.5
run chk-floor-fract-values   ref:chk-floor-fract-values.gdshader --kind rect --probe 0.5,0.5
run chk-mod-values           ref:chk-mod-values.gdshader --kind rect --probe 0.5,0.5
run chk-worked-example       ref:chk-worked-example.gdshader --kind rect --probe 0.5,0.5
run chk-percent-on-floats-EXPECTED-ERROR ref:chk-percent-on-floats.gdshader --kind rect --probe 0.5,0.5
run chk-percent-on-ints      ref:chk-percent-on-ints.gdshader --kind rect --probe 0.5,0.5
run chk-tps-sprite           ref:chk-texture-pixel-size-quarter.gdshader --kind sprite --sprite-tex sprite --probe 0.5,0.5
run chk-tps-rect             ref:chk-texture-pixel-size-quarter.gdshader --kind rect --probe 0.5,0.5
run chk-filter-linear        ref:chk-filter-center-lookup.gdshader --kind rect --size 256x256 --tex picture=sprite --probe 0.5,0.5
run chk-filter-nearest       ref:chk-filter-center-lookup-nearest.gdshader --kind rect --size 256x256 --tex picture=sprite --probe 0.5,0.5
if [ -n "${ONLY:-}" ]; then   # keep the newest line for each label, in order of first appearance
  python3 - "$RES" <<'PY'
import json, sys
rows, order = {}, []
for line in open(sys.argv[1]):
    d = json.loads(line)
    if d["check"] not in rows:
        order.append(d["check"])
    rows[d["check"]] = line
open(sys.argv[1], "w").write("".join(rows[k] for k in order))
PY
fi
echo "wrote $RES"
