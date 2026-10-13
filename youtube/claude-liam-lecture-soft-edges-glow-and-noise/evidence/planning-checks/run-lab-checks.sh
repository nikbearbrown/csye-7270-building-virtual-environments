#!/bin/zsh
# Re-runs every shader this film shows (and the evidence-only edge cases) through the Shader Lab (real Godot 4.7.2 window)
# and records the pixels. Output: lab-results.jsonl (one line per run: label, the arguments, exit code, the RESULT line) and png/*.png.
# Then run analyze_lab.py for the expected-against-measured tables (lab-analysis.txt).
# Safe to re-run; it overwrites its own outputs. Apple M4 Pro, macOS; Forward+ unless a run says --renderer.
#
# Square runs use --kind rect --size 256x256 so UV is a square (a circle stays a circle): the pixel (px, py) has UV ((px + 0.5) / 256, (py + 0.5) / 256).
# The Lab reads the probe pixel int(fx * 255): P px py prints the fraction that lands exactly on that pixel.
# NOTE for zsh: an unquoted string variable is NOT split into words; the option lists below are ARRAYS.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
EV="$HERE/shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results.jsonl"; : > "$RES"
run() {  # label shader-path args...
  local label="$1"; local shader="$2"; shift 2
  local line
  line=$("$LAB/check_shader.sh" "$shader" "$@" --png "$OUT/$label.png" 2>&1)
  local code=$?
  python3 - "$label" "$shader" "$code" "$*" "$line" >> "$RES" <<'PY'
import json, sys
label, shader, code, args, out = sys.argv[1:6]
print(json.dumps({"check": label, "shader": shader.split("/")[-1], "args": args, "exit": int(code), "output": out.strip()}))
PY
  echo "[$code] $label"
}
P() { printf -- "--probe %.5f,%.5f" $(( ($1 + 0.25) / 255.0 )) $(( ($2 + 0.25) / 255.0 )); }
SQ=(--kind rect --size 256x256)
# probe sets are built as arrays so every word reaches the runner
ROW_DISC=($(P 128 127) $(P 229 127) $(P 231 127) $(P 196 127) $(P 211 127) $(P 227 127) $(P 100 127))   # centre, just inside 0.4, just outside, d = 0.2656 / 0.3242 / 0.3867 (px 196, 211, 227), a point inside
ROW_SPOT=($(P 89 89) $(P 115 89) $(P 140 89) $(P 166 89) $(P 255 89) $(P 255 255) $(P 230 89))          # the spot centre, 0.10 / 0.20 / 0.30 away, the picture's right edge, its far corner, a point outside the disc

# ---- Act I: from a cut to a ramp
run 01-hard-disc          "$SH/01-hard-disc.gdshader"      "${SQ[@]}" "${ROW_DISC[@]}"
run 02-soft-disc          "$SH/02-soft-disc.gdshader"      "${SQ[@]}" "${ROW_DISC[@]}"
# the five pixels whose t (how far along the band) is 0.100, 0.250, 0.500, 0.750, 0.900 to within 0.001 (found by searching all pixels)
run 02-soft-disc-t        "$SH/02-soft-disc.gdshader"      "${SQ[@]}" $(P 141 61) $(P 145 56) $(P 152 48) $(P 135 35) $(P 131 29)
run 03-soft-width-0.15    "$SH/03-soft-width.gdshader"     "${SQ[@]}" --set softness=0.15 "${ROW_DISC[@]}"
run 03-soft-width-0.05    "$SH/03-soft-width.gdshader"     "${SQ[@]}" --set softness=0.05 "${ROW_DISC[@]}"
run 03-soft-width-0.4     "$SH/03-soft-width.gdshader"     "${SQ[@]}" --set softness=0.4 "${ROW_DISC[@]}"
run 03-soft-width-0.0     "$SH/03-soft-width.gdshader"     "${SQ[@]}" --set softness=0.0 "${ROW_DISC[@]}"
run ev-equal-edges-fplus  "$EV/ev-equal-edges.gdshader"    "${SQ[@]}" "${ROW_DISC[@]}"
run ev-equal-edges-compat "$EV/ev-equal-edges.gdshader"    "${SQ[@]}" "${ROW_DISC[@]}" --renderer gl_compatibility
run ev-reversed-fplus     "$EV/ev-reversed-edges.gdshader" "${SQ[@]}" "${ROW_DISC[@]}"
run ev-reversed-compat    "$EV/ev-reversed-edges.gdshader" "${SQ[@]}" "${ROW_DISC[@]}" --renderer gl_compatibility

# ---- Act II: falloff and highlight
run 04-spot               "$SH/04-spot.gdshader"           "${SQ[@]}" "${ROW_SPOT[@]}"
run 05-spot-power-1       "$SH/05-spot-power.gdshader"     "${SQ[@]}" --set power=1 "${ROW_SPOT[@]}"
run 05-spot-power-3       "$SH/05-spot-power.gdshader"     "${SQ[@]}" --set power=3 "${ROW_SPOT[@]}"
run 05-spot-power-8       "$SH/05-spot-power.gdshader"     "${SQ[@]}" --set power=8 "${ROW_SPOT[@]}"
run 06-spot-in-disc       "$SH/06-spot-in-disc.gdshader"   "${SQ[@]}" "${ROW_SPOT[@]}"
run 07-spot-moves-a       "$SH/07-spot-moves.gdshader"     "${SQ[@]}" --set spot_center=0.35,0.35 "${ROW_SPOT[@]}"
run 07-spot-moves-b       "$SH/07-spot-moves.gdshader"     "${SQ[@]}" --set spot_center=0.65,0.4 "${ROW_SPOT[@]}"
run ev-pow-negative-fplus "$EV/ev-pow-negative.gdshader"   --kind rect --size 256x256 --probe 0.1,0.5 --probe 0.5,0.5 --probe 0.9,0.5
run ev-pow-negative-compat "$EV/ev-pow-negative.gdshader"  --kind rect --size 256x256 --probe 0.1,0.5 --probe 0.5,0.5 --probe 0.9,0.5 --renderer gl_compatibility
run ev-pow-fraction-fplus  "$EV/ev-pow-negative-fraction.gdshader" --kind rect --size 256x256 --probe 0.1,0.5 --probe 0.9,0.5
run ev-pow-fraction-compat "$EV/ev-pow-negative-fraction.gdshader" --kind rect --size 256x256 --probe 0.1,0.5 --probe 0.9,0.5 --renderer gl_compatibility
run ev-pow-unclamped      "$EV/ev-pow-unclamped.gdshader"  "${SQ[@]}" $(P 242 242) $(P 229 229) $(P 25 25)
run ev-pow-clamped        "$EV/ev-pow-clamped.gdshader"    "${SQ[@]}" $(P 242 242) $(P 229 229) $(P 25 25)

# ---- Act III: layering. Probes: the spot centre, a body point away from it (px 154, 154), the middle of the soft band, a point outside the disc
BUB=($(P 89 89) $(P 154 154) $(P 211 127) $(P 128 128) $(P 245 245))
run 08-bubble-1.0         "$SH/08-bubble.gdshader"         "${SQ[@]}" --set brightness=1.0 "${BUB[@]}"
run 08-bubble-0.6         "$SH/08-bubble.gdshader"         "${SQ[@]}" --set brightness=0.6 "${BUB[@]}"
run 09-bubble-bug-1.0     "$SH/09-bubble-bug.gdshader"     "${SQ[@]}" --set brightness=1.0 "${BUB[@]}"
run 09-bubble-bug-0.6     "$SH/09-bubble-bug.gdshader"     "${SQ[@]}" --set brightness=0.6 "${BUB[@]}"

# ---- Act IV: noise. The Lab can only bind a plain, non-seamless image (--tex noise=noise); the real NoiseTexture2D checks are in noise_check.gd.
run 10-noise-cloud        "$SH/10-noise-cloud.gdshader"    "${SQ[@]}" --tex noise=noise
# Compile checks for the two TIME shaders at the default wait (TIME about 0.3: a plain cloud). The pictures at stepped times are noise_check.gd's F renders:
# a Lab window that is covered by another window is not drawn and TIME stands still, so a --wait picture could silently show the wrong time (a 4 s run did).
run 11-noise-scroll-compile    "$SH/11-noise-scroll.gdshader"    "${SQ[@]}" --tex noise=noise
run 12-noise-no-repeat-compile "$SH/12-noise-no-repeat.gdshader" "${SQ[@]}" --tex noise=noise
run 13-noise-reveal-0.3   "$SH/13-noise-reveal.gdshader"   "${SQ[@]}" --tex noise=noise --set progress=0.3
run 13-noise-reveal-0.6   "$SH/13-noise-reveal.gdshader"   "${SQ[@]}" --tex noise=noise --set progress=0.6

# ---- Act V: the glow bubble in the Lab (default 2D rendering, no environment): the shader compiles, glow 0 and glow 1
run 14-glow-bubble-0      "$SH/14-glow-bubble.gdshader"    "${SQ[@]}" --set glow=0.0 "${BUB[@]}"
run 14-glow-bubble-1      "$SH/14-glow-bubble.gdshader"    "${SQ[@]}" --set glow=1.0 "${BUB[@]}"
run 14-glow-bubble-0.1    "$SH/14-glow-bubble.gdshader"    "${SQ[@]}" --set glow=0.1 "${BUB[@]}"

# ---- the finale: all layers in one shader (the Lab binds a plain noise image; the real NoiseTexture2D run is finale_check.gd)
run 15-bubble-complete    "$SH/15-bubble-complete.gdshader" "${SQ[@]}" --tex noise=noise --set glow=0.0 --wait 1.0

# ---- left out of the film, kept as a note for a vertex-stage film: VERTEX += normalize(VERTEX) * 30.0
run ev-vertex-pulse-sprite "$EV/ev-vertex-pulse.gdshader" --kind sprite --sprite-tex white --sprite-scale 1.0 --size 256x256 --probe 0.5,0.5
run ev-vertex-pulse-rect   "$EV/ev-vertex-pulse.gdshader" --kind rect --size 256x256 --probe 0.5,0.5
echo "wrote $RES"
