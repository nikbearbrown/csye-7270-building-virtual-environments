#!/bin/zsh
# Runs the four scratch GDScript checks (things the Shader Lab cannot do) in a scratch Godot project and saves the logs next to this file.
#   verify-aspect.gd   which source of "aspect" is right for which node (ColorRect, Sprite2D, TextureRect), and the uniform following a resize
#   verify-repeat.gd   texture_repeat (node) and repeat_enable (sampler): clamp, repeat, mirror, defaults
#   verify-scroll.gd   UV.x += TIME * 0.1: speed and direction in ONE process
#   verify-identity.gd the lookup shader (and the unbent template) against no material at all: pixel for pixel
# Run: ./run-scratch-checks.sh      (needs godot on PATH; uses a scratch copy in /private/tmp, never a project of Bear's)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ=/private/tmp/claude-501/godot-shaders-uv-space/proj
mkdir -p "$PROJ"
cp "$HERE/project.godot" "$HERE"/verify-*.gd "$PROJ/"
n=1
for t in aspect repeat scroll identity; do
  LOG="$HERE/run-$n-$t.log"
  {
    echo "# $(date '+%Y-%m-%d %H:%M:%S %Z')  host: $(uname -srm)  command: godot --path $PROJ --script res://verify-$t.gd"
    godot --path "$PROJ" --script "res://verify-$t.gd" 2>&1
  } > "$LOG"
  echo "wrote $LOG"
  n=$((n+1))
done
