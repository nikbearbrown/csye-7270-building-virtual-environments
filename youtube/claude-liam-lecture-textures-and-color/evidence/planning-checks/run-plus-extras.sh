#!/bin/zsh
# run-plus-extras.sh: follow-up probes for the film's captures (runner_plus.gd through plus.sh). Output: run-12-plus-extras.log (label, then the RESULT line)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
SH="$FILM/lab-shaders"; SC="$HERE/scratch-shaders"; PLUS="$HERE/plus.sh"
OUT="$HERE/run-12-plus-extras.log"; : > "$OUT"
r() { echo "## $1" >> "$OUT"; shift; "$PLUS" "$@" >> "$OUT" 2>&1; }
SQ=(--size 360x360)
# (a) repeat on the 6 x 6 F table, probes placed inside texels: (0.625, 0.2083) and (0.125, 0.625) -> repeat on: cream, cream; repeat off: teal, teal
for s in 04-repeat-off 05-repeat-on; do r "repeat $s" $SH/$s.gdshader --kind rect "${SQ[@]}" --tex tex=tiny_f --probe 0.625,0.2083 --probe 0.125,0.625 --probe 0.0833,0.0833; done
# (b) the noise as a plain grey number at the three points the film reads out
r "noise values (grey view)" $SC/t-noise-view.gdshader --kind rect "${SQ[@]}" --tex noise_tex=noise2d --probe 0.363,0.454 --probe 0.181,0.606 --probe 0.637,0.698
r "noise mask (teal ColorRect, alpha = noise) at the same points" $SH/15-noise-mask.gdshader --kind rect "${SQ[@]}" --rect-color "#5FA391" --tex noise_tex=noise2d --probe 0.363,0.454 --probe 0.181,0.606 --probe 0.637,0.698
# (d) where the 0.5 threshold cuts a grey ramp: probes every 0.01 around the two cut positions, Forward+ 3D, hinted and plain
P50=(); for x in 0.48 0.49 0.50 0.51 0.52 0.53; do P50+=(--probe $x,0.5); done
P74=(); for x in 0.72 0.73 0.74 0.75 0.76 0.77; do P74+=(--probe $x,0.5); done
r "mask plain, forward_plus, near 0.50"  $SH/27-mask-plain.gdshader  --kind quad3d --renderer forward_plus --tex mask=ramp_grey "${P50[@]}"
r "mask hinted, forward_plus, near 0.74" $SH/28-mask-hinted.gdshader --kind quad3d --renderer forward_plus --tex mask=ramp_grey "${P74[@]}"
# (f) setting a hinted uniform from code: the colour as picked, and srgb_to_linear() of it (converted twice), HDR 2D Forward+ and 3D Forward+
r "hdr2d forward_plus: as picked"        $SH/23-patch-hinted.gdshader --kind rect --renderer forward_plus --hdr2d --set tint=0.2,0.4,0.6,1 --probe 0.5,0.5
r "hdr2d forward_plus: converted first"  $SH/23-patch-hinted.gdshader --kind rect --renderer forward_plus --hdr2d --set tint=0.0331,0.1328,0.3184,1 --probe 0.5,0.5
# (g) the same two cases on an unshaded 3D quad, Forward+ (hinted vec4 uniform "a"; added so the 3D claim has a log of its own)
r "3d forward_plus: as picked"           $SC/cs2-flat-3d-hinted.gdshader --kind quad3d --renderer forward_plus --set a=0.2,0.4,0.6,1 --probe 0.5,0.5
r "3d forward_plus: converted first"     $SC/cs2-flat-3d-hinted.gdshader --kind quad3d --renderer forward_plus --set a=0.0331,0.1328,0.3184,1 --probe 0.5,0.5
echo "wrote $OUT"
