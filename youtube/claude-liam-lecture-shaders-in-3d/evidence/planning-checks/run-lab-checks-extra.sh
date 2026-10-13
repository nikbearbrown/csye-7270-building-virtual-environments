#!/bin/zsh
# Extra Lab checks added after the first batch (run-lab-checks.sh), kept in their own script and results file so each file's rows match its run lines.
# Why: the pad's stripes are hard to see at activation 0.5 (stripe-contrast.txt), so the held stills for the line-by-line reading and the box-versus-square
# picture are held at activation 0.3 instead; this records the pad's two stripe colors there in all three renderers.
# Output: lab-results-extra.jsonl (one record per check: label, shader, renderer, exit code, the Lab's own output) and png/*.png.
#   Machine: Apple M4 Pro, Godot 4.7.2 stable (official). Probe positions are normalized 0..1 (x right, y down).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="$HERE/lab-results-extra.jsonl"; : > "$RES"

run() {  # label shader renderer kind [lab args...]
  local label="$1" shader="$2" renderer="$3" kind="$4"; shift 4
  local line code
  line=$("$LAB/check_shader.sh" "$SH/$shader" --kind "$kind" --renderer "$renderer" "$@" --png "$OUT/$label.png" 2>&1)
  code=$?
  python3 -I -c '
import json, sys
label, shader, renderer, code, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.stdin.read().strip()
print(json.dumps({"check": label, "shader": shader, "renderer_requested": renderer, "exit": code, "output": out}))
' "$label" "$shader" "$renderer" "$code" <<<"$line" >> "$RES"
  echo "[$code] $label"
}

for r in forward_plus gl_compatibility mobile; do
  run 12-signal-pad-$r-0.3  12-signal-pad.gdshader  $r quad3d --set activation=0.3 --probe 0.03125,0.5 --probe 0.09375,0.5
done
echo "wrote $RES"
