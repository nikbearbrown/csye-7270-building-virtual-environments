#!/usr/bin/env bash
# evidence/headless-probe/import_check.sh
#
# Does a fresh headless import of the game report a broken shader? It never
# touches game/. Run it from assignment-5/:
#   evidence/headless-probe/import_check.sh 2>&1 | tee logs/probe_import_check.log
#
# It exports the committed game/ twice into a temporary folder with git archive.
# In both copies it removes the semicolon at the end of line 39 of
# systems/art/outline.gdshader, the outline the main scene uses through
# systems/art/outline.tres. Copy 1 also gets unused_typo.gdshader: the outline
# with COLOR misspelt COLOUR on line 41, used by nothing. Copy 2 has no main
# scene. It imports each copy once, then compiles the unused shader with
# probe_shader.gd. The sed calls are macOS sed's.
set -o pipefail
cd "$(dirname "$0")/../.." || exit 2
tmp=$(mktemp -d) || exit 2
trap 'rm -rf "$tmp"' EXIT
echo "godot $(godot --version)"
for copy in 1 2; do
	mkdir "$tmp/$copy"
	git archive HEAD game | tar -x -C "$tmp/$copy" || exit 2
	sed -i '' '39s/;$//' "$tmp/$copy/game/systems/art/outline.gdshader"
done
sed '41s/COLOR = /COLOUR = /' game/systems/art/outline.gdshader > "$tmp/1/game/systems/art/unused_typo.gdshader"
sed -i '' '/^run\/main_scene=/d' "$tmp/2/game/project.godot"
labels=("" "the broken outline, used by the main scene, and unused_typo.gdshader" "the broken outline, and no main scene")
for copy in 1 2; do
	echo "=== copy $copy: ${labels[$copy]}"
	timeout 120 godot --headless --path "$tmp/$copy/game" --import > "$tmp/$copy.log" 2>&1
	echo "import exit $?; SHADER ERROR lines: $(grep -c 'SHADER ERROR' "$tmp/$copy.log")"
	grep -B6 -A1 'SHADER ERROR' "$tmp/$copy.log"
done
echo "=== copy 1's unused_typo.gdshader, compiled by probe_shader.gd"
timeout 120 godot --headless --path "$tmp/1/game" --script "$PWD/evidence/headless-probe/probe_shader.gd" -- res://systems/art/unused_typo.gdshader 2>&1 | grep -E 'SHADER ERROR|uniforms the engine reports'
