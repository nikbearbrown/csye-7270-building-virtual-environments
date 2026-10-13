#!/bin/zsh
# run-all.sh: re-runs every planning check of the Reflections film and rewrites the logs next to this script.
# Needs `godot` (4.7.2) on PATH. Scripts are copied into a SCRATCH Godot project (default /private/tmp/claude-501/godot-shaders-reflections/proj)
# and run there; nothing outside this folder and that scratch folder is written. Every log starts with the command, the date and the machine.
# Each capture and each rect-mode case runs in its OWN Godot process (rect mode depends on history).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="${PROJ:-/private/tmp/claude-501/godot-shaders-reflections/proj}"
mkdir -p "$PROJ"
[ -f "$PROJ/project.godot" ] || cp "$HERE/project.godot" "$PROJ/project.godot"
cp "$HERE"/*.gd "$PROJ/"
MACHINE="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo unknown) · $(godot --version)"

hdr() { echo "# command: $1"; echo "# date: $(date '+%F %T') · machine: $MACHINE"; }
filt() { grep -v "^WARNING\|^   at\|RID alloc\|resources still in use\|ObjectDB instance\|^$\|^Godot Engine\|^Metal\|^OpenGL"; }

# runlog <logfile> <renderer or -> <script.gd> [user args...]
runlog() {
  local lf="$1" rend="$2" script="$3"; shift 3
  local rm=(); [ "$rend" != "-" ] && rm=(--rendering-method "$rend")
  local ua=(); [ $# -gt 0 ] && ua=(-- "$@")
  { hdr "godot --path <scratch project> ${rm[*]:-} --script res://$script ${ua[*]:-}"
    timeout 300 godot --path "$PROJ" "${rm[@]}" --script "res://$script" "${ua[@]}" 2>&1 | filt
  } > "$HERE/$lf"
  echo "wrote $lf"
}
# append another run to an existing log
runlog_append() {
  local lf="$1" rend="$2" script="$3"; shift 3
  local rm=(); [ "$rend" != "-" ] && rm=(--rendering-method "$rend")
  local ua=(); [ $# -gt 0 ] && ua=(-- "$@")
  { echo "# ---"; hdr "godot --path <scratch project> ${rm[*]:-} --script res://$script ${ua[*]:-}"
    timeout 300 godot --path "$PROJ" "${rm[@]}" --script "res://$script" "${ua[@]}" 2>&1 | filt
  } >> "$HERE/$lf"
}

WHAT="${1:-all}"      # all | experiments | scenes | route | editor | retime | gatet   (record is NOT part of all: 13 minutes on a busy machine)
if [ "$WHAT" = "all" ] || [ "$WHAT" = "experiments" ]; then
for R in forward_plus gl_compatibility; do
  S=""; [ "$R" = "gl_compatibility" ] && S="-compat"
  runlog "run-01-expA-copy-order$S.log"                       "$R" exp_a_copy_order.gd
  runlog "run-02-expB-modes-and-readers-INCONCLUSIVE-rect$S.log" "$R" exp_b_modes_and_second_reader.gd
  runlog "run-03-expB2-rect-outside-fresh-process$S.log"      "$R" exp_b2_rect_outside.gd
  runlog "run-04-expC-pond$S.log"                             "$R" exp_c_pond.gd
  runlog "run-05-expC4-rect-fresh$S.log"                      "$R" exp_c4_rect_fresh.gd
  runlog_append "run-05-expC4-rect-fresh$S.log"               "$R" exp_c4_rect_fresh.gd --cover
  runlog "run-06-expD-polish$S.log"                           "$R" exp_d_polish.gd
  runlog "run-07-expE-extras$S.log"                           "$R" exp_e_extras.gd
  runlog "run-08-expF-z-index-and-layers$S.log"               "$R" exp_f_z_index_and_layers.gd
  runlog "run-09-expG-mirror-the-screen$S.log"                "$R" exp_g_mirror_the_screen.gd
  : > "$HERE/run-10-expH-rect-region$S.log"
  { hdr "each case in its own process: exp_h_rect_region.gd -- --case H1 ... H8"; } > "$HERE/run-10-expH-rect-region$S.log"
  for C in H1 H2 H3 H4 H5 H6 H7 H8; do
    runlog_append "run-10-expH-rect-region$S.log" "$R" exp_h_rect_region.gd --case "$C"
  done
done

fi
if [ "$WHAT" = "all" ] || [ "$WHAT" = "experiments" ] || [ "$WHAT" = "route" ]; then
# the same question as run-10 on the 4K capture route (SubViewport 3840 x 2160 over the 1280 x 720 canvas): how big is the default Rect box there?
for R in forward_plus gl_compatibility; do
  S=""; [ "$R" = "gl_compatibility" ] && S="-compat"
  { hdr "each case in its own process: exp_i_rect_region_4k.gd -- --case I1 I3 I4 I7 (the 4K SubViewport route)"; } > "$HERE/run-13-expI-rect-region-4k-route$S.log"
  for C in I1 I3 I4 I7; do
    runlog_append "run-13-expI-rect-region-4k-route$S.log" "$R" exp_i_rect_region_4k.gd --case "$C"
  done
done
fi
if [ "$WHAT" = "all" ] || [ "$WHAT" = "scenes" ]; then
# the capture scenes at 1280 x 720 (direct route), each in its own process; times chosen to land inside every state
typeset -A TIMES
TIMES=( C01 "0.5,3,50%,9.5,85%" C02 "0.5,2.8,50%,85%" C03 "2,50%,85%" C04 "1,5,50%,85%" C05 "1.5,4,50%,85%" C06 "0.5,3,50%,85%" C07 "4,50%,85%"
        C08 "3,50%,85%" C09 "1,50%,85%" C10 "2,50%,85%" C11 "2,50%,85%" C12 "2,50%,85%" C13 "2,50%,85%" C14 "2,50%,85%" C15 "3,50%,85%" C16 "3,50%,85%"
        C17 "3,50%,85%" C18 "1,2.5,50%,85%" C19 "1,3.5,50%,85%" )
{ hdr "godot --path <scratch project> --script res://scene_runner.gd -- --capture <id> --route direct --scale 1 --times <t,...> (one process per capture)"; } > "$HERE/run-11-scene-checks.log"
for C in C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19; do
  runlog_append "run-11-scene-checks.log" - scene_runner.gd --capture "$C" --route direct --scale 1 --times "${TIMES[$C]}" --out "$PROJ/../frames-scenes"
done
python3 "$HERE/contact_sheet.py" "$PROJ/../frames-scenes" "$HERE/png/contact-sheet-captures.png" || true
fi
if [ "$WHAT" = "all" ] || [ "$WHAT" = "scenes" ] || [ "$WHAT" = "route" ]; then
# the 4K route (SubViewport 3840 x 2160 over the 1280 x 720 canvas) for ALL nineteen captures (the route the film is recorded on), then
# the comparison with the direct route: no probe may move (the shaders read SCREEN_UV, never a pixel count)
typeset -A TIMES
TIMES=( C01 "0.5,3,50%,9.5,85%" C02 "0.5,2.8,50%,85%" C03 "2,50%,85%" C04 "1,5,50%,85%" C05 "1.5,4,50%,85%" C06 "0.5,3,50%,85%" C07 "4,50%,85%"
        C08 "3,50%,85%" C09 "1,50%,85%" C10 "2,50%,85%" C11 "2,50%,85%" C12 "2,50%,85%" C13 "2,50%,85%" C14 "2,50%,85%" C15 "3,50%,85%" C16 "3,50%,85%"
        C17 "3,50%,85%" C18 "1,2.5,50%,85%" C19 "1,3.5,50%,85%" )
{ hdr "godot --path <scratch project> --script res://scene_runner.gd -- --capture <id> --route sv --scale 3 --times <t,...> (all nineteen, one process each)"; } > "$HERE/run-11b-scene-checks-4k-route.log"
for C in C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19; do
  runlog_append "run-11b-scene-checks-4k-route.log" - scene_runner.gd --capture "$C" --route sv --scale 3 --times "${TIMES[$C]}"
done
{ hdr "python3 compare_routes.py run-11-scene-checks.log run-11b-scene-checks-4k-route.log"
  python3 "$HERE/compare_routes.py" "$HERE/run-11-scene-checks.log" "$HERE/run-11b-scene-checks-4k-route.log"
} > "$HERE/run-14-route-comparison.log" || true
fi
if [ "$WHAT" = "all" ] || [ "$WHAT" = "editor" ]; then
# the editor project (pond.tscn) that the editor frames E1 and E2 are recorded from, and a check that it behaves like the scripted scene
EDIT="$PROJ/../editor-run12-$(date +%H%M%S)/pond"
{ hdr "make-editor-project.sh <scratch dir> (builds pond.tscn and its images), then verify_scene_file.gd in that project"
  "$HERE/make-editor-project.sh" "$EDIT" 2>&1 | filt
} > "$HERE/run-12-editor-project-verify.log"
cp "$HERE/verify_scene_file.gd" "$EDIT/"
for R in forward_plus gl_compatibility; do
  if [ "$R" = "forward_plus" ]; then LF="$HERE/run-12-editor-project-verify.log"; else LF="$HERE/run-12-editor-project-verify-compat.log"; : > "$LF"; fi
  { echo "# ---"; hdr "godot --path <editor project> --rendering-method $R --script res://verify_scene_file.gd"
    timeout 300 godot --path "$EDIT" --rendering-method "$R" --script res://verify_scene_file.gd 2>&1 | filt
  } >> "$LF"
done
fi
if [ "$WHAT" = "all" ] || [ "$WHAT" = "retime" ]; then
# --length: a capture recorded at the length of its beat. Events keep their place as a fraction of the clip, so the probes at 50 % and 85 %
# of the CLIP must be the same at every length; frames_written must be length x 30.
{ hdr "scene_runner.gd --length: C07 and C11 at their planned length and at two other lengths; probes at 50 % and 85 % of the clip"; } > "$HERE/run-15-retime-length.log"
for L in "" 12 19; do
  if [ -n "$L" ]; then LA=(--length "$L"); else LA=(); fi
  runlog_append "run-15-retime-length.log" - scene_runner.gd --capture C07 --route direct --scale 1 --times "50%,85%" "${LA[@]}"
done
for L in "" 9 14; do
  if [ -n "$L" ]; then LA=(--length "$L"); else LA=(); fi
  runlog_append "run-15-retime-length.log" - scene_runner.gd --capture C11 --route direct --scale 1 --times "50%,85%" "${LA[@]}"
done
runlog_append "run-15-retime-length.log" - scene_runner.gd --capture C07 --route direct --scale 1 --length 12 --all-frames "$PROJ/../frames-retime-12s"
fi
if [ "$WHAT" = "all" ] || [ "$WHAT" = "gatet" ]; then
# could anything in a capture be read as text by GATE T? (the toolkit's own ink mask and blob functions, imported read-only; 50 % and 85 % frames)
{ hdr "python3 gate_t_ink_precheck.py <scratch project> <frames dir> (renders the 50 % and 85 % frames of all 19 captures at 3840 x 2160)"
  python3 "$HERE/gate_t_ink_precheck.py" "$PROJ/../proj-gatet" "$PROJ/../frames-gatet"
} > "$HERE/run-16-gate-t-ink-precheck.log"
fi
if [ "$WHAT" = "record" ]; then
# the whole capture pipeline end to end (the nineteen clips at their beats' estimated lengths, one fresh Godot process each), checked and sheeted
OUTC="$PROJ/../out-recorded"
{ echo "# command: FRAMES_DIR=<scratch frames dir> capture_all.sh <scratch out dir> <scratch project>, then verify_recorded_clips.py <scratch out dir>"
  echo "# date: $(date '+%F %T') · machine: $MACHINE"
  echo "# ---"
  FRAMES_DIR="$PROJ/../frames-recorded" "$HERE/capture_all.sh" "$OUTC" "$PROJ/../proj-capture" 2>&1 | grep -v '^$'
  echo "# ---"; echo "# command: python3 verify_recorded_clips.py <scratch out dir>"
  python3 "$HERE/verify_recorded_clips.py" "$OUTC"
} > "$HERE/run-17-capture-all-end-to-end.log"
python3 "$HERE/capture_contact_sheet.py" "$OUTC" "$HERE/png/contact-sheet-recorded-clips.png"
fi
echo "done. Editor project: ./make-editor-project.sh <dir>; Lab: ./run-lab-checks.sh"
