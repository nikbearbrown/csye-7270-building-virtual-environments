#!/bin/zsh
# Compiles every shader this film shows through the Shader Lab (real Godot 4.7.2 window), on Forward+ and on Compatibility, and records the RESULT lines.
# A light() function only runs where a light reaches it, and the Lab has no lights, so the Lab proves "compiles, uniforms as declared" only;
# what light() does is measured by the scene scripts (verify*.gd). Output: lab-results.jsonl. Safe to re-run; it overwrites its own output.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
RES="$HERE/lab-results.jsonl"; : > "$RES"
for f in "$SH"/*.gdshader; do
  for r in forward_plus gl_compatibility; do
    line=$("$LAB/check_shader.sh" "$f" --kind rect --probe 0.5,0.5 --renderer $r 2>&1)
    code=$?
    echo "{\"shader\":\"$(basename $f)\",\"renderer\":\"$r\",\"exit\":$code,\"output\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' <<<"$line")}" >> "$RES"
    echo "[$code] $(basename $f) $r"
  done
done
echo "wrote $RES"
