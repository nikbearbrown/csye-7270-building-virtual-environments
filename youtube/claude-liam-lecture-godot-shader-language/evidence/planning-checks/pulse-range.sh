#!/bin/zsh
# Samples 01-breathe.gdshader (the film's hook shader, tint set to teal #5FA391 as the Inspector would) at many moments to show what the pulse really does.
# `--wait S` runs S seconds of process time before the frame is read, so TIME is roughly S plus the engine's start-up time.
# Output: pulse-range.txt (one line per sample: wait, red, green, blue) and a min/max summary. Forward+, Apple M4 Pro, Godot 4.7.2.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
OUT="$HERE/pulse-range.txt"; : > "$OUT"
for w in 0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4 2.6 2.8 3.0 3.2 3.4; do
  line=$("$LAB/check_shader.sh" "$FILM/lab-shaders/01-breathe.gdshader" --kind rect --set tint=#5FA391 --wait $w --probe 0.5,0.5 2>&1 | grep '^RESULT')
  python3 - "$w" "$line" >> "$OUT" <<'PY'
import json, sys
w, line = sys.argv[1], sys.argv[2]
j = json.loads(line[len("RESULT "):])
print(w, *j["probes"][0]["rgba"][:3], j["renderer"])
PY
done
python3 - "$OUT" >> "$OUT" <<'PY'
import sys
rows = [l.split() for l in open(sys.argv[1]) if l[0].isdigit()]
for i, name in ((1, "red"), (2, "green"), (3, "blue")):
    v = [float(r[i]) for r in rows]
    print(f"# {name}: min {min(v):.4f}, max {max(v):.4f}")
PY
cat "$OUT"
