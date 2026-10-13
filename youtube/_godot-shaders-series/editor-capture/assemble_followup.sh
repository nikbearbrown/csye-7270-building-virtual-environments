#!/bin/zsh
# assemble_followup.sh: copies the renderer-path follow-up (README section 11) from the scratch folder into the series' editor-capture folder.
# Idempotent. Touches the phase-1 pieces only where the follow-up superseded them with a superset: proj/addons/driver/plugin.gd (the old one is kept in
# tools-history/) and settings/ (new files added). README.md is written by hand and is never overwritten here.
set -eu
setopt null_glob
S=/private/tmp/claude-501/godot-shaders-editor-capture
D=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture
mkdir -p "$D/tools-history"
[ -f "$D/tools-history/plugin-v1-for-readme-sections-1-to-10.gd" ] || cp "$D/proj/addons/driver/plugin.gd" "$D/tools-history/plugin-v1-for-readme-sections-1-to-10.gd"
# tools
for f in pm_driver.gd run_pm.sh with_lab_lock.sh probe.sh run_followup.sh make_followup_scripts.py make_followup_stills.py assemble_followup.sh capture_editor_states.sh extract_marks.py; do cp "$S/$f" "$D/$f"; done
mkdir -p "$D/pmproj"; cp "$S/pmproj/project.godot" "$S/pmproj/pm_driver.gd" "$D/pmproj/"
# the scratch project with the extended driver (a superset: all phase-1 ops unchanged, see README 11.8)
rsync -a --delete --exclude .godot --exclude created --exclude state_script.json --exclude .DS_Store "$S/proj/" "$D/proj/"
mkdir -p "$D/proj/created"; : > "$D/proj/created/.gitkeep"
# settings
cp "$S"/settings/*.tres "$D/settings/"
cp "$S/runs/followup/final-1080/fresh/editor_settings-4.7.written-by-the-editor-on-first-run.tres" "$D/settings/editor_settings-fresh-home-written-by-the-editor-4.7.2.tres"
# state scripts
mkdir -p "$D/state-scripts/followup" "$D/state-scripts/probes/followup"
cp "$S"/state-scripts/followup/*.json "$D/state-scripts/followup/"
cp "$S"/state-scripts/fu-probe-*.json "$S"/state-scripts/pm-probe*.json "$D/state-scripts/probes/followup/"
# PNGs (full frames, dialog crops, title strips, renderer blocks, composites, stills.json)
for pair in "final-1080:1920x1080" "final-3456:3456x1944"; do
  src="${pair%%:*}"; size="${pair##*:}"
  mkdir -p "$D/png/$size/renderer-path"
  cp "$S/runs/followup/$src/png/"* "$D/png/$size/renderer-path/"
done
# logs
copy_logs() { # src_dir dest_dir [with_png]
  mkdir -p "$2"; for f in states.json run.log run-info.txt import.log; do [ -f "$1/$f" ] && cp "$1/$f" "$2/$f" || true; done
  [ -f "$1/named/marks.json" ] && cp "$1/named/marks.json" "$2/marks.json" || true
  if [ "${3:-}" = "with_png" ] && [ -d "$1/named" ]; then mkdir -p "$2/named"; cp "$1"/named/*.png "$2/named/" 2>/dev/null || true; fi
}
for src in final-1080 final-3456; do
  for part in editor pm fresh; do copy_logs "$S/runs/followup/$src/$part" "$D/logs/followup/$src/$part" ""; done
done
for run in "$S"/runs/followup/regression-1080/*/; do copy_logs "${run%/}" "$D/logs/followup/regression-1080/$(basename "$run")" ""; done
cp "$S/runs/followup/regression-1080/regression-compare.txt" "$D/logs/followup/regression-1080/regression-compare.txt"
for p in fu-probe-A fu-probe-B fu-probe-C fu-probe-D fu-probe-E fu-probe-E2 fu-probe-F pm-probe1 pm-probe2 pm-probe3 pm-probe4; do copy_logs "$S/runs/followup/$p" "$D/logs/followup/probes/$p" with_png; done
echo assembled; du -sh "$D"
