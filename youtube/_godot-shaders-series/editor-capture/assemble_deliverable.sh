#!/bin/zsh
# Copies everything reusable from the scratch folder into the series' editor-capture folder (the README is written by hand).
set -eu
setopt null_glob
S=/private/tmp/claude-501/godot-shaders-editor-capture
D=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture
mkdir -p "$D"
# tools
for f in capture_editor_states.sh extract_marks.py compare_frames.py make_state_scripts.py run_all.sh run_compare.sh assemble_deliverable.sh; do cp "$S/$f" "$D/$f"; done
cp "$S/api/introspect.gd" "$D/introspect.gd"
# the scratch project (no import cache, no files the driver creates at run time)
mkdir -p "$D/proj"
rsync -a --delete --exclude .godot --exclude created --exclude state_script.json --exclude .DS_Store "$S/proj/" "$D/proj/"
mkdir -p "$D/proj/created" ; : > "$D/proj/created/.gitkeep"
# settings + state scripts
mkdir -p "$D/settings" "$D/state-scripts/final" "$D/state-scripts/probes"
cp "$S"/settings/*.tres "$D/settings/"
cp "$S"/state-scripts/final/*.json "$D/state-scripts/final/"
cp "$S"/state-scripts/probe*.json "$D/state-scripts/probes/"
# PNGs by size and film
film_of() { case "$1" in godot-shaders_*) echo godot-shaders;; drawing-shapes_*) echo drawing-shapes-with-math;; local-world_*) echo local-world-and-screen-space;; textures-and-color_*) echo textures-and-color;; *) echo other;; esac }
for pair in "final-1080:1920x1080" "final-3456:3456x1944"; do
  src="${pair%%:*}"; size="${pair##*:}"
  for run in "$S/runs/$src"/*/; do
    for f in "$run"named/*.png; do
      b="$(basename "$f")"; film="$(film_of "$b")"
      mkdir -p "$D/png/$size/$film"; cp "$f" "$D/png/$size/$film/$b"
    done
  done
done
mkdir -p "$D/png/true-1080p-at-100pct-scale"
for run in "$S"/runs/compare/true-1080p-100pct/*/; do cp "$run"named/*.png "$D/png/true-1080p-at-100pct-scale/" 2>/dev/null || true; done
rm -f "$D"/png/true-1080p-at-100pct-scale/*.dock.png
# logs
copy_logs() { # src_dir dest_dir [with_png]
  mkdir -p "$2"; for f in states.json run.log run-info.txt import.log; do [ -f "$1/$f" ] && cp "$1/$f" "$2/$f" || true; done
  [ -f "$1/named/marks.json" ] && cp "$1/named/marks.json" "$2/marks.json" || true
  if [ "${3:-}" = "with_png" ] && [ -d "$1/named" ]; then mkdir -p "$2/named"; cp "$1"/named/*.png "$2/named/" 2>/dev/null || true; fi
}
for pair in "final-1080:final-1080" "final-3456:final-3456"; do
  src="${pair%%:*}"; dst="${pair##*:}"
  for run in "$S/runs/$src"/*/; do copy_logs "${run%/}" "$D/logs/$dst/$(basename "$run")"; done
done
for kind in factory compat true-1080p-100pct; do
  for run in "$S/runs/compare/$kind"/*/; do copy_logs "${run%/}" "$D/logs/compare/$kind/$(basename "$run")" with_png; done
done
for p in probe1 probe2 probe3 probe4 probe5 probe6 probe6b probe7 probe8a probe8b probe8c probe8d; do copy_logs "$S/runs/$p" "$D/logs/probes/$p" with_png; done
copy_logs "$S/runs/final-1080-attempt1-frames_drawn-indexing-WRONG" "$D/logs/failed-attempts/attempt1-frames_drawn-indexing-WRONG-batch" ""
for run in "$S/runs/final-1080-attempt1-frames_drawn-indexing-WRONG"/*/; do copy_logs "${run%/}" "$D/logs/failed-attempts/attempt1-frames_drawn-indexing-WRONG/$(basename "$run")" with_png; done
rm -rf "$D/logs/failed-attempts/attempt1-frames_drawn-indexing-WRONG-batch"
for run in "$S/runs/final-1080-attempt2-open_picker_menu-flaky-E1-failed"/*/; do copy_logs "${run%/}" "$D/logs/failed-attempts/attempt2-open_picker_menu-flaky-E1-failed/$(basename "$run")" with_png; done
copy_logs "$S/runs/final-1080-attempt3-local-world-clean-root-3D-menu-failed" "$D/logs/failed-attempts/attempt3-local-world-clean-root-3D-View-menu-failed" with_png
copy_logs "$S/runs/final-1080-attempt3-local-world-plan-exact-3D-menu-failed" "$D/logs/failed-attempts/attempt3-local-world-plan-exact-3D-View-menu-failed" with_png
for run in "$S"/runs/superseded/*/; do copy_logs "${run%/}" "$D/logs/superseded-runs-with-an-older-shader-copy/$(basename "$run")" ""; done
mkdir -p "$D/logs/launcher"; cp "$S"/logs/*.log "$S"/logs/api-introspect-1.txt "$D/logs/launcher/" 2>/dev/null || true
( cd "$D/proj/shaders" && shasum -a 256 *.gdshader > "$D/SHADERS.sha256" )
echo assembled; du -sh "$D"
