#!/bin/zsh
# e12_builtins.sh: compiles six one-line helper shaders on this Mac's Godot 4.7.2, one built-in each, and prints one line per compile.
# The six shaders are in evidence/planning-checks/check-shaders/e12-builtin-*.gdshader; the output is B45's terminal card, verbatim.
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot
S=$R/../_godot-shaders-series
echo '$ ./e12_builtins.sh'
for id in TIME TAU UV VERTEX SCREEN_UV INV_PROJECTION_MATRIX; do
  out=$($S/lab/check_shader.sh $R/evidence/planning-checks/check-shaders/e12-builtin-$id.gdshader --kind quad3d --size 160x90 2>&1)
  if echo "$out" | grep -q "Unknown identifier"; then res="Unknown identifier"; else res="compiles"; fi
  printf '%-22s %s\n' "$id" "$res"
done
