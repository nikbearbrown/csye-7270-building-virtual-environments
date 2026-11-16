#!/bin/zsh
# check_all.sh: compile check of every shaders/*.gdshader through the series Lab's check_shader.sh, in both renderers, plus the Lab's own
# deliberately broken shader as a negative control (it must FAIL). Output: evidence/compile/check_shader-<renderer>.txt, negative-control.txt
# A passing file prints "RESULT {...ok:true...}" and exits 0; a shader error prints SHADER ERROR and exits 1.
set -u
PROJ="$(cd "$(dirname "$0")/.." && pwd)"
LAB="$PROJ/../youtube/_godot-shaders-series/lab"
OUT="$PROJ/evidence/compile"
mkdir -p "$OUT"
for R in forward_plus gl_compatibility; do
  : > "$OUT/check_shader-$R.txt"
  for f in "$PROJ"/shaders/*.gdshader; do
    echo "### $R  $(basename "$f")" >> "$OUT/check_shader-$R.txt"
    timeout 90 "$LAB/check_shader.sh" "$f" --kind quad3d --renderer $R >> "$OUT/check_shader-$R.txt" 2>&1
    echo "exit $?" >> "$OUT/check_shader-$R.txt"
  done
done
{ echo "### negative control: the Lab's own broken.gdshader must FAIL"; timeout 60 "$LAB/check_shader.sh" "$LAB/shaders/broken.gdshader" --kind quad3d; echo "exit $?"; } > "$OUT/negative-control.txt" 2>&1
python3 - "$OUT" <<'PY'
import re, json, sys
out = sys.argv[1]
for r in ("forward_plus", "gl_compatibility"):
    txt = open(f"{out}/check_shader-{r}.txt").read()
    ok = 0
    for blk in txt.split("### ")[1:]:
        name = blk.split("\n")[0].split()[1]
        m = re.search(r"RESULT (\{.*\})", blk)
        e = re.search(r"exit (\d+)", blk).group(1)
        j = json.loads(m.group(1)) if m else {}
        good = e == "0" and j.get("ok") and "SHADER ERROR" not in blk
        ok += 1 if good else 0
        print(f"{r:16s} {name:30s} exit {e} ok={j.get('ok')} uniforms={len(j.get('uniforms', []))} renderer={j.get('renderer')}")
    print(f"{r}: {ok} shaders compile")
PY
