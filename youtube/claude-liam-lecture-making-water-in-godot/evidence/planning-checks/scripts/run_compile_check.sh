#!/bin/zsh
# run_compile_check.sh: lab/check_shader.sh --kind quad3d on every shader of the film in both renderers. Writes ../logs/compile-check.txt
# 06c-builtin-in-helper-error is a deliberate error (a built-in used inside a helper function): it must print SHADER ERROR.
G=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot
S=$G/../_godot-shaders-series
out=$G/evidence/planning-checks/logs/compile-check.txt
echo "# compile check: lab/check_shader.sh --kind quad3d, every film shader in both renderers ($(date +%F), Godot 4.7.2, Apple M4 Pro)" > $out
for f in $G/lab-shaders/*.gdshader; do for rend in forward_plus gl_compatibility; do
  r=$($S/lab/check_shader.sh $f --kind quad3d --size 320x180 --renderer $rend 2>&1 | tr '\n' ' ')
  rr=$(echo "$r" | grep -o '"renderer":"[a-z_]*"' | head -1)
  err=$(echo "$r" | grep -o "SHADER ERROR[^.]*\." | head -1)
  echo "$(basename $f) $rend ${rr:-no-result} ${err:-compiles}" >> $out
done; done
echo done >> $out
