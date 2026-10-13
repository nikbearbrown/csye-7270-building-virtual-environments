#!/bin/zsh
# run-lab-checks.sh: every shader this film shows goes through the Shader Lab (lab/check_shader.sh: a real Godot 4.7.2 window) with the Lab's own
# stand-in textures (checker, gradient, noise: the Lab cannot make this film's tiny F, swatches, burn ramp or a teal ColorRect; run-plus-checks.sh does those).
# Output: lab-results.jsonl (one line per run: label, shader, exit code, the RESULT line) and png/lab-*.png. Safe to re-run.
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
  line=$("$LAB/check_shader.sh" "$SH/$shader" "$@" --png "$OUT/lab-$label.png" 2>&1)
  local code=$?
  echo "{\"check\":\"$label\",\"shader\":\"$shader\",\"exit\":$code,\"output\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' <<<"$line")}" >> "$RES"
  echo "[$code] $label"
}
run 01-lookup          01-lookup.gdshader          --kind rect --tex tex=checker --probe 0.06,0.1 --probe 0.19,0.1
run 02-nearest         02-nearest.gdshader         --kind rect --tex tex=checker --probe 0.06,0.1
run 03-flip            03-flip.gdshader            --kind rect --tex tex=gradient --probe 0.1,0.5 --probe 0.9,0.5
run 04-repeat-off      04-repeat-off.gdshader      --kind rect --tex tex=gradient --probe 0.25,0.5 --probe 0.75,0.5
run 05-repeat-on       05-repeat-on.gdshader       --kind rect --tex tex=gradient --probe 0.25,0.5 --probe 0.75,0.5
run 06-empty           06-empty.gdshader           --kind sprite --sprite-tex checker --sprite-scale 1.0 --probe 0.45,0.45
run 07-own-texture     07-own-texture.gdshader     --kind sprite --sprite-tex checker --sprite-scale 1.0 --probe 0.45,0.45
run 08-tint            08-tint.gdshader            --kind sprite --sprite-tex checker --sprite-scale 1.0 --probe 0.45,0.45 --probe 0.5,0.5
run 09-invert          09-invert.gdshader          --kind sprite --sprite-tex checker --sprite-scale 1.0 --probe 0.45,0.45
run 10-invert-all      10-invert-all.gdshader      --kind sprite --sprite-tex sprite --probe 0.5,0.5 --probe 0.3,0.2
run 11-brighten        11-brighten.gdshader        --kind sprite --sprite-tex checker --sprite-scale 1.0 --probe 0.45,0.45 --probe 0.55,0.45
run 12-gray-red        12-gray-red.gdshader        --kind sprite --sprite-tex checker --sprite-scale 1.0 --probe 0.45,0.45 --probe 0.5,0.5
run 13-gray-weighted   13-gray-weighted.gdshader   --kind sprite --sprite-tex checker --sprite-scale 1.0 --probe 0.45,0.45 --probe 0.5,0.5
run 14-mix-0.0         14-mix.gdshader             --kind sprite --sprite-tex checker --sprite-scale 1.0 --set amount=0.0 --probe 0.45,0.45
run 14-mix-0.5         14-mix.gdshader             --kind sprite --sprite-tex checker --sprite-scale 1.0 --set amount=0.5 --probe 0.45,0.45
run 14-mix-1.0         14-mix.gdshader             --kind sprite --sprite-tex checker --sprite-scale 1.0 --set amount=1.0 --probe 0.45,0.45
run 15-noise-mask      15-noise-mask.gdshader      --kind rect --tex noise_tex=noise --probe 0.5,0.5
run 16-step-cut-0.25   16-step-cut.gdshader        --kind rect --tex noise_tex=noise --set threshold=0.25 --probe 0.5,0.5
run 16-step-cut-0.5    16-step-cut.gdshader        --kind rect --tex noise_tex=noise --set threshold=0.5 --probe 0.5,0.5
run 16-step-cut-0.75   16-step-cut.gdshader        --kind rect --tex noise_tex=noise --set threshold=0.75 --probe 0.5,0.5
run 17-dissolve-cut    17-dissolve-cut.gdshader    --kind sprite --tex noise_tex=noise --set progress=0.5 --probe 0.5,0.5
run 18-dissolve-0.0    18-dissolve.gdshader        --kind sprite --tex noise_tex=noise --tex ramp_tex=gradient --set progress=0.0 --probe 0.5,0.5
run 18-dissolve-0.5    18-dissolve.gdshader        --kind sprite --tex noise_tex=noise --tex ramp_tex=gradient --set progress=0.5 --probe 0.5,0.5
run 18-dissolve-1.0    18-dissolve.gdshader        --kind sprite --tex noise_tex=noise --tex ramp_tex=gradient --set progress=1.0 --probe 0.5,0.5
run 19-first-try-0.0   19-dissolve-first-try.gdshader --kind sprite --tex noise_tex=noise --tex ramp_tex=gradient --set progress=0.0 --probe 0.5,0.5
run 20-blend-3d        20-blend-3d.gdshader        --kind quad3d --probe 0.1,0.5 --probe 0.5,0.5 --probe 0.9,0.5
run 21-blend-2d        21-blend-2d.gdshader        --kind rect --probe 0.1,0.5 --probe 0.5,0.5 --probe 0.9,0.5
run 22-picker          22-picker.gdshader          --kind rect --probe 0.5,0.5
run 23-patch-hinted    23-patch-hinted.gdshader    --kind rect --probe 0.5,0.5
run 24-patch-plain     24-patch-plain.gdshader     --kind rect --probe 0.5,0.5
run 25-swatch-hinted   25-swatch-hinted.gdshader   --kind quad3d --tex picture=checker --probe 0.06,0.1 --probe 0.19,0.1
run 26-swatch-plain    26-swatch-plain.gdshader    --kind quad3d --tex picture=checker --probe 0.06,0.1 --probe 0.19,0.1
run 27-mask-plain      27-mask-plain.gdshader      --kind quad3d --tex mask=gradient --probe 0.55,0.5 --probe 0.7,0.5 --probe 0.8,0.5
run 28-mask-hinted     28-mask-hinted.gdshader     --kind quad3d --tex mask=gradient --probe 0.55,0.5 --probe 0.7,0.5 --probe 0.8,0.5
echo "wrote $RES"
