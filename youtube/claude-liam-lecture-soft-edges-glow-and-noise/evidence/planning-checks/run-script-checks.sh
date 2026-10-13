#!/bin/zsh
# run-script-checks.sh: runs the GDScript checks that the Lab cannot do (noise_check.gd, extra_checks.gd, and toggle_check.gd, the run-time switches)
# in scratch projects and keeps their raw RESULT lines: run-noise.log, run-extra.log, run-toggle.log, run-finale.log. Holds the shared Shader Lab lock. Safe to re-run (about 25 s).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
ROOT=/private/tmp/claude-501/godot-shaders-soft-edges-glow-and-noise
mkdir -p "$ROOT/scratch-noise" "$ROOT/scratch-extra" "$HERE/png/noise"
for d in scratch-noise scratch-extra; do
  [ -f "$ROOT/$d/project.godot" ] || printf 'config_version=5\n\n[application]\n\nconfig/name="%s"\nconfig/features=PackedStringArray("4.7")\n\n[display]\n\nwindow/size/viewport_width=640\nwindow/size/viewport_height=360\n' "$d" > "$ROOT/$d/project.godot"
done
cp "$HERE/noise_check.gd" "$ROOT/scratch-noise/noise_check.gd"; cp "$HERE/extra_checks.gd" "$ROOT/scratch-extra/extra_checks.gd"
LOCK=/private/tmp/claude-501/shaderlab.lock
for i in $(seq 1 480); do
  if mkdir "$LOCK" 2>/dev/null; then break; fi
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; fi
  sleep 0.5
done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
{ echo "# noise_check.gd, $(date '+%Y-%m-%d %H:%M'), Godot $(godot --version)"; echo "# command: godot --path <scratch> --script res://noise_check.gd -- --film <film folder> --png-dir <film>/evidence/planning-checks/png/noise"; } > "$HERE/run-noise.log"
godot --path "$ROOT/scratch-noise" --script res://noise_check.gd -- --film "$FILM" --png-dir "$HERE/png/noise" 2>&1 | grep -E "^RESULT |ERROR|SCRIPT" >> "$HERE/run-noise.log"
{ echo "# extra_checks.gd, $(date '+%Y-%m-%d %H:%M'), Godot $(godot --version)"; echo "# command: godot --path <scratch> --script res://extra_checks.gd -- --film <film folder>"; } > "$HERE/run-extra.log"
godot --path "$ROOT/scratch-extra" --script res://extra_checks.gd -- --film "$FILM" 2>&1 | grep -E "^RESULT |ERROR|SCRIPT" >> "$HERE/run-extra.log"
mkdir -p "$ROOT/scratch-glow"
[ -f "$ROOT/scratch-glow/project.godot" ] || printf 'config_version=5\n\n[application]\n\nconfig/name="glow-scratch"\nconfig/features=PackedStringArray("4.7")\n\n[display]\n\nwindow/size/viewport_width=640\nwindow/size/viewport_height=360\n' > "$ROOT/scratch-glow/project.godot"
cp "$HERE/toggle_check.gd" "$ROOT/scratch-glow/toggle_check.gd"; cp "$HERE/finale_check.gd" "$ROOT/scratch-glow/finale_check.gd"
{ echo "# toggle_check.gd, $(date '+%Y-%m-%d %H:%M'), Godot $(godot --version)"; echo "# command: godot --path <scratch> --script res://toggle_check.gd -- --shader <film>/lab-shaders/14-glow-bubble.gdshader"; } > "$HERE/run-toggle.log"
godot --path "$ROOT/scratch-glow" --script res://toggle_check.gd -- --shader "$FILM/lab-shaders/14-glow-bubble.gdshader" 2>&1 | grep -E "^RESULT |ERROR|SCRIPT" >> "$HERE/run-toggle.log"
{ echo "# finale_check.gd, $(date '+%Y-%m-%d %H:%M'), Godot $(godot --version)"; echo "# command: godot --path <scratch> --script res://finale_check.gd -- --film <film folder> --png-dir <film>/evidence/planning-checks/png"; } > "$HERE/run-finale.log"
godot --path "$ROOT/scratch-glow" --script res://finale_check.gd -- --film "$FILM" --png-dir "$HERE/png" 2>&1 | grep -E "^RESULT |ERROR|SCRIPT" >> "$HERE/run-finale.log"
echo "wrote run-noise.log run-extra.log run-toggle.log run-finale.log"
