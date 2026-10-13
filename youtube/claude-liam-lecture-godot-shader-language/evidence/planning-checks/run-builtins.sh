#!/bin/zsh
# Which built-ins can a function you write see? Eleven tiny shaders, each using one built-in INSIDE a user function called from fragment().
# Also boundary cases the film does NOT claim: built-in function calls and vector constructors accept an int where a float is expected;
# a shader with no shader_type (or with render_mode first) prints NO error when assigned at run time through the Lab and simply is not applied
# (the probe reads the unshaded default), so the Lab cannot show the missing-shader_type error: the film leans on the documentation for 'first line'.
# Output: builtins-results.txt (shader, exit code, the engine's first error or the probe). Godot 4.7.2, Forward+, Apple M4 Pro.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
OUT="$HERE/builtins-results.txt"; : > "$OUT"
for f in "$HERE"/builtins/*.gdshader; do
  b="$(basename "$f" .gdshader)"
  res=$("$LAB/check_shader.sh" "$f" --kind rect --probe 0.5,0.5 2>&1); code=$?
  err=$(echo "$res" | grep -m1 'SHADER ERROR')
  probe=$(echo "$res" | grep -o '"rgba":\[[^]]*\]' | head -1)
  echo "$b | exit $code | ${err:-compiled} | $probe" | tee -a "$OUT"
done
