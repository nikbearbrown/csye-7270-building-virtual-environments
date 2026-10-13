#!/bin/zsh
# Re-runs every shader this film shows through the Shader Lab (real Godot 4.7.2 window) and records the pixels.
# Output: lab-results.jsonl (one line per check) and png/*.png. Safe to re-run; it overwrites its own outputs.
# Probe positions are given as pixels (px,py) in a W x H window and converted to the Lab's normalized form (pixel + 0.25 so the
# truncation lands on the intended pixel). Expected values are in FACTCHECK.md and CAPTURE-PLAN.md.
# zsh note: arguments are kept in arrays ((--size ...) and "${S[@]}"): an unquoted $S is NOT split by zsh, and the first run of this
# script (not kept) silently dropped --size and --kind for that reason.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
# RENDERER=gl_compatibility ./run-lab-checks.sh  re-runs everything on the Compatibility renderer (outputs get a suffix); default is Forward+.
SUFFIX=""; RFLAG=()
if [ -n "${RENDERER:-}" ]; then SUFFIX="-$RENDERER"; RFLAG=(--renderer "$RENDERER"); fi
OUT="$HERE/png$SUFFIX"; mkdir -p "$OUT"
RES="$HERE/lab-results$SUFFIX.jsonl"; : > "$RES"

P() {  # P W H px py -> "x,y" normalized for the Lab's --probe
  python3 -c "import sys; W,H,px,py=map(float,sys.argv[1:5]); print('%.7f,%.7f' % ((px+0.25)/(W-1), (py+0.25)/(H-1)))" "$@"
}
run() {  # label shader args...
  local label="$1"; local shader="$2"; shift 2
  local line
  line=$("$LAB/check_shader.sh" "$SH/$shader" "${RFLAG[@]}" "$@" --png "$OUT/$label.png" 2>&1)
  local code=$?
  print -r -- "{\"check\":\"$label\",\"shader\":\"$shader\",\"exit\":$code,\"output\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' <<<"$line")}" >> "$RES"
  echo "[$code] $label"
}
W=1280; H=720
S=(--size ${W}x${H} --kind sprite --sprite-scale 1.0)      # a 128 px sprite, 1:1, centred at (640,360)
R=(--size ${W}x${H} --kind rect)                           # a ColorRect over the whole 1280 x 720 view

# B01 hook: the same sky read from local and from world position (gradient stands in for the sky texture in the Lab)
run 01-sky-local-p32   01-sky-local.gdshader  "${S[@]}" --sprite-tex white --tex sky=gradient --probe "$(P $W $H 672 392)" --probe "$(P $W $H 608 328)"
run 02-sky-world-p32   02-sky-world.gdshader  "${S[@]}" --sprite-tex white --tex sky=gradient --probe "$(P $W $H 672 392)" --probe "$(P $W $H 608 328)"
# B13 direction, not place
run 03-direction       03-direction-not-place.gdshader "${S[@]}" --sprite-tex white --probe "$(P $W $H 672 392)" --probe "$(P $W $H 608 328)"
# B14 the compiler's message (expected: exit 1, "Unknown identifier in expression: 'MODEL_MATRIX'")
run 04-broken          04-broken-matrix-in-fragment.gdshader "${S[@]}" --sprite-tex white
# B16 world position as colour
run 05-world-field     05-world-field.gdshader "${S[@]}" --sprite-tex white --probe "$(P $W $H 672 392)" --probe "$(P $W $H 608 328)" --probe "$(P $W $H 576 296)"
# B20 repeat on / off over the whole view (rect, so world position = pixel position)
run 02-sky-world-rect  02-sky-world.gdshader  "${R[@]}" --tex sky=gradient --probe "$(P $W $H 300 100)" --probe "$(P $W $H 800 100)"
run 06-sky-no-repeat   06-sky-no-repeat.gdshader "${R[@]}" --tex sky=gradient --probe "$(P $W $H 300 100)" --probe "$(P $W $H 800 100)"
# B23 TEXTURE_PIXEL_SIZE: scale follows the art (128 px art here)
run 07-pattern-texel-size 07-pattern-texel-size.gdshader "${S[@]}" --sprite-tex white --tex pattern=gradient --probe "$(P $W $H 672 392)"
# B24 the hole: inside / just inside / just outside the radius, on a full-view rect
run 08-world-hole      08-world-hole.gdshader "${R[@]}" --probe "$(P $W $H 640 360)" --probe "$(P $W $H 699 360)" --probe "$(P $W $H 700 360)" --probe "$(P $W $H 1000 360)"
# B25 spacing out: amount 0, 0.5, 1 on the test sprite
run 09-spacing-out-0   09-spacing-out.gdshader "${S[@]}" --sprite-tex sprite --tex sky=gradient --set amount=0.0 --probe "$(P $W $H 640 360)"
run 09-spacing-out-0.5 09-spacing-out.gdshader "${S[@]}" --sprite-tex sprite --tex sky=gradient --set amount=0.5 --probe "$(P $W $H 640 360)"
run 09-spacing-out-1   09-spacing-out.gdshader "${S[@]}" --sprite-tex sprite --tex sky=gradient --set amount=1.0 --probe "$(P $W $H 640 360)"
# B26-B33: the four ways to read the screen address (no camera in the Lab, so the order and the camera cases are in the scratch scripts)
run 10-screen-matrices 10-screen-via-matrices.gdshader "${R[@]}" --probe "$(P $W $H 286 236)" --probe "$(P $W $H 0 0)" --probe "$(P $W $H 1279 719)"
run 11-wrong-order     11-wrong-order.gdshader "${R[@]}" --probe "$(P $W $H 286 236)" --probe "$(P $W $H 0 0)" --probe "$(P $W $H 1279 719)"
run 12-screen-vertex   12-screen-vertex-in-fragment.gdshader "${R[@]}" --probe "$(P $W $H 286 236)" --probe "$(P $W $H 0 0)" --probe "$(P $W $H 1279 719)"
run 13-screen-fragcoord 13-screen-fragcoord.gdshader "${R[@]}" --probe "$(P $W $H 286 236)" --probe "$(P $W $H 0 0)" --probe "$(P $W $H 1279 719)"
run 14-screen-uv       14-screen-uv.gdshader "${R[@]}" --probe "$(P $W $H 286 236)" --probe "$(P $W $H 0 0)" --probe "$(P $W $H 1279 719)"
# B35-B38: stripes. Test sprite (teal blob), local x = +10 (no stripe) and +34 (stripe) on the horizontal midline
run 15-anchor-local    15-anchor-local.gdshader "${S[@]}" --sprite-tex sprite --probe "$(P $W $H 650 360)" --probe "$(P $W $H 674 360)"
run 16-anchor-world    16-anchor-world.gdshader "${S[@]}" --sprite-tex sprite --probe "$(P $W $H 650 360)" --probe "$(P $W $H 674 360)"
run 17-anchor-screen   17-anchor-screen.gdshader "${S[@]}" --sprite-tex sprite --probe "$(P $W $H 650 360)" --probe "$(P $W $H 674 360)"
echo "wrote $RES"
