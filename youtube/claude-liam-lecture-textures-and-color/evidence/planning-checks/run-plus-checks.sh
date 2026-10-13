#!/bin/zsh
# run-plus-checks.sh: the same shaders as run-lab-checks.sh, but with the film's REAL textures (tiny F, swatches, burn ramp, NoiseTexture2D, grey ramp) and,
# where a film beat needs it, a second renderer or HDR 2D, through runner_plus.gd (the Lab's runner plus those extras; see plus.sh).
# Output: plus-results.jsonl (label, shader, exit code, RESULT line) and png/plus-*.png. Safe to re-run.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/plus-results.jsonl"; : > "$RES"
PLUS="$HERE/plus.sh"
run() {  # label shader args...
  local label="$1"; local shader="$2"; shift 2
  local line
  line=$("$PLUS" "$SH/$shader" "$@" --png "$OUT/plus-$label.png" 2>&1)
  local code=$?
  echo "{\"check\":\"$label\",\"shader\":\"$shader\",\"exit\":$code,\"output\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' <<<"$line")}" >> "$RES"
  echo "[$code] $label"
}
SQ=(--size 360x360)
# the 6 x 6 F table: texel centres are at (i + 0.5) / 6; probes: cream texel (1,1), teal margin (0,0), teal inside the F (2,2), between margin and cream (0.15, 0.25), stem at row 2, mirrored stem
F4=(--probe 0.25,0.25 --probe 0.0833,0.0833 --probe 0.4167,0.4167 --probe 0.15,0.25 --probe 0.25,0.4167 --probe 0.75,0.4167)
# ---- Act I
run a1-01-lookup-f-linear   01-lookup.gdshader   --kind rect "${SQ[@]}" --tex tex=tiny_f "${F4[@]}"
run a1-01-lookup-checker    01-lookup.gdshader   --kind rect "${SQ[@]}" --tex tex=checker --probe 0.06,0.06 --probe 0.19,0.06
run a1-01-lookup-gradient   01-lookup.gdshader   --kind rect "${SQ[@]}" --tex tex=gradient --probe 0.02,0.02 --probe 0.98,0.02 --probe 0.02,0.98
run a1-01-lookup-noise      01-lookup.gdshader   --kind rect "${SQ[@]}" --tex tex=noise
run a1-02-nearest-f         02-nearest.gdshader  --kind rect "${SQ[@]}" --tex tex=tiny_f "${F4[@]}"
run a1-03-flip-f            03-flip.gdshader     --kind rect "${SQ[@]}" --tex tex=tiny_f "${F4[@]}"
run a1-04-repeat-off-f      04-repeat-off.gdshader --kind rect "${SQ[@]}" --tex tex=tiny_f --probe 0.625,0.2083 --probe 0.125,0.625 --probe 0.0833,0.0833
run a1-05-repeat-on-f       05-repeat-on.gdshader  --kind rect "${SQ[@]}" --tex tex=tiny_f --probe 0.625,0.2083 --probe 0.125,0.625 --probe 0.0833,0.0833
# ---- Act II: the swatch picture on the test sprite at fit scale (patch centres)
SW=(--probe 0.388,0.301 --probe 0.613,0.301 --probe 0.388,0.702 --probe 0.613,0.702)
run a2-00-swatches-untouched 06-empty.gdshader   --kind sprite --sprite-tex swatches "${SW[@]}"
run a2-06-empty-modulated    06-empty.gdshader   --kind sprite --sprite-tex swatches --modulate "#808080" "${SW[@]}"
run a2-07-own-texture-modulated 07-own-texture.gdshader --kind sprite --sprite-tex swatches --modulate "#808080" "${SW[@]}"
run a2-08-tint              08-tint.gdshader     --kind sprite --sprite-tex swatches "${SW[@]}"
run a2-09-invert            09-invert.gdshader   --kind sprite --sprite-tex swatches "${SW[@]}"
run a2-10-invert-all-sprite 10-invert-all.gdshader --kind sprite --sprite-tex sprite --probe 0.5,0.5 --probe 0.3,0.2 --probe 0.5,0.1
run a2-11-brighten          11-brighten.gdshader --kind sprite --sprite-tex swatches "${SW[@]}"
run a2-12-gray-red          12-gray-red.gdshader --kind sprite --sprite-tex swatches "${SW[@]}"
run a2-13-gray-weighted     13-gray-weighted.gdshader --kind sprite --sprite-tex swatches "${SW[@]}"
run a2-14-mix-0.0           14-mix.gdshader      --kind sprite --sprite-tex swatches --set amount=0.0 "${SW[@]}"
run a2-14-mix-0.5           14-mix.gdshader      --kind sprite --sprite-tex swatches --set amount=0.5 "${SW[@]}"
run a2-14-mix-1.0           14-mix.gdshader      --kind sprite --sprite-tex swatches --set amount=1.0 "${SW[@]}"
# ---- Act III
run a3-15-noise-mask        15-noise-mask.gdshader --kind rect "${SQ[@]}" --rect-color "#5FA391" --tex noise_tex=noise2d --probe 0.363,0.454 --probe 0.181,0.606 --probe 0.637,0.698
for t in 0.25 0.5 0.75; do run a3-16-step-$t 16-step-cut.gdshader --kind rect "${SQ[@]}" --rect-color "#5FA391" --tex noise_tex=noise2d --set threshold=$t; done
for p in 0.0 0.25 0.5 0.75 1.0; do
  run a3-17-cut-$p      17-dissolve-cut.gdshader --kind sprite --tex noise_tex=noise2d --set progress=$p
  run a3-18-dissolve-$p 18-dissolve.gdshader     --kind sprite --tex noise_tex=noise2d --tex ramp_tex=burn_ramp_tex --set progress=$p
done
run a3-19-first-try-0.0     19-dissolve-first-try.gdshader --kind sprite --tex noise_tex=noise2d --tex ramp_tex=burn_ramp_tex --set progress=0.0
for p in 0.35 0.5 0.65; do run a3-18-wipe-$p 18-dissolve.gdshader --kind sprite --tex noise_tex=gradient --tex ramp_tex=burn_ramp_tex --set progress=$p; done
# ---- Act IV: one blend, every renderer; 2D with HDR 2D on
B=(--probe 0.1,0.5 --probe 0.5,0.5 --probe 0.9,0.5)
for r in forward_plus mobile gl_compatibility; do
  run a4-20-blend-3d-$r  20-blend-3d.gdshader --kind quad3d --renderer $r "${B[@]}"
  run a4-21-blend-2d-$r  21-blend-2d.gdshader --kind rect   --renderer $r "${B[@]}"
done
for r in forward_plus mobile; do run a4-21-blend-2d-$r-hdr2d 21-blend-2d.gdshader --kind rect --renderer $r --hdr2d "${B[@]}"; done
# ---- Act V
for r in forward_plus mobile gl_compatibility; do
  run a5-25-swatch-hinted-$r  25-swatch-hinted.gdshader --kind quad3d --renderer $r --tex picture=swatches "${SW[@]}"
  run a5-26-swatch-plain-$r   26-swatch-plain.gdshader  --kind quad3d --renderer $r --tex picture=swatches "${SW[@]}"
  run a5-27-mask-plain-$r     27-mask-plain.gdshader    --kind quad3d --renderer $r --tex mask=ramp_grey --probe 0.45,0.5 --probe 0.55,0.5 --probe 0.70,0.5 --probe 0.73,0.5 --probe 0.75,0.5 --probe 0.80,0.5
  run a5-28-mask-hinted-$r    28-mask-hinted.gdshader   --kind quad3d --renderer $r --tex mask=ramp_grey --probe 0.45,0.5 --probe 0.55,0.5 --probe 0.70,0.5 --probe 0.73,0.5 --probe 0.75,0.5 --probe 0.80,0.5
done
for r in forward_plus mobile; do
  run a5-23-patch-hinted-$r-hdr2d 23-patch-hinted.gdshader --kind rect --renderer $r --hdr2d --probe 0.5,0.5
  run a5-24-patch-plain-$r-hdr2d  24-patch-plain.gdshader  --kind rect --renderer $r --hdr2d --probe 0.5,0.5
done
run a5-23-patch-hinted-forward_plus 23-patch-hinted.gdshader --kind rect --renderer forward_plus --probe 0.5,0.5
run a5-24-patch-plain-forward_plus  24-patch-plain.gdshader  --kind rect --renderer forward_plus --probe 0.5,0.5
echo "wrote $RES"
