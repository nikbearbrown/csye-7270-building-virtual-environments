#!/bin/zsh
# Run 16 (2026-10-13): defaults of a sampler2D uniform on a canvas item (default project settings): filter and repeat; and that a square texture stretches
# across a 16:9 shape. tiny4b = a 4 x 4 gray ramp (texel centres 0.125, 0.375, 0.625, 0.875 hold 0, 1/3, 2/3, 1).
#   filter: probe x = 0.30 -> nearest 0.3333, linear 0.2314 (blend of the two nearest texel centres); the default must match one of them
#   repeat: gradient texture, UV * 2, probe x = 0.75 asks for 1.5 -> repeat on 0.498 (wraps to 0.5), off 1.0 (edge stretched)
#   stretch: the 8 x 8 checker on a 640 x 360 ColorRect: first cell is 80 x 45 pixels
# Output: run-16-filter-repeat-defaults.log (+ png/scratch-stretch-checker.png)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PLUS="$HERE/plus.sh"; SH="$HERE/scratch-shaders"
OUT="$HERE/run-16-filter-repeat-defaults.log"; : > "$OUT"
run() { echo "## $*" >> "$OUT"; "$PLUS" "$@" >> "$OUT" 2>&1; }
for m in nearest linear default; do run $SH/t-filter-$m.gdshader --kind rect --tex tex=tiny4b --probe 0.30,0.5 --probe 0.45,0.5 --probe 0.55,0.5; done
for m in enable disable default; do run $SH/t-repeat-$m.gdshader --kind rect --tex tex=gradient --probe 0.25,0.5 --probe 0.75,0.5 --probe 0.9,0.5; done
run $SH/t-lookup.gdshader --kind rect --tex tex=checker --png "$HERE/png/scratch-stretch-checker.png"
python3 -I - "$HERE/png/scratch-stretch-checker.png" >> "$OUT" <<'PY'
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB"); W, H = im.size
first = im.getpixel((2, 2))
w = next(x for x in range(W) if im.getpixel((x, 2)) != first)
h = next(y for y in range(H) if im.getpixel((2, y)) != first)
print(f"STRETCH first checker cell on the {W} x {H} rect: {w} x {h} pixels (the table is square, the shape is not)")
PY
echo "wrote $OUT"
