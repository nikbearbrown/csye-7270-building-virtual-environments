#!/bin/zsh
# Batch 1 of planning renders for "Making Water in Godot" (2026-10-16). Run from anywhere. Output PNGs: evidence/planning-checks/png/, logs: evidence/planning-checks/logs/.
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot
S=$R/../_godot-shaders-series
OUT=$R/evidence/planning-checks/png; LOG=$R/evidence/planning-checks/logs
mkdir -p $OUT $LOG
cap() { # name shader size extra-harness-args...   (environment W_* is set by the caller)
  local name=$1 shader=$2 size=$3; shift 3
  W_ID=$name W_SHADER=$shader CLIP_L=1 $S/lab/capture_shader.sh --scene $R/capture-scenes/water_scene.gd --length 0.5 --size $size --warmup 60 --name $name --dest $OUT --png 1 "$@" > $LOG/$name.log 2>&1
  grep -E "SHADER|SCRIPT ERROR|NO RESULT|Parse" $LOG/$name.log | head -3
  echo "$name done"
}
# A. pow of a negative base: the power-curve foam without and with the clamp (top view, plane fills the frame)
W_BARE=1 W_VIEW=top W_TOPSIZE=8 W_SET="clamped=0" cap pow-broken 03b-power-curve.gdshader 1080x1080
W_BARE=1 W_VIEW=top W_TOPSIZE=8 W_SET="clamped=1" cap pow-clamped 03b-power-curve.gdshader 1080x1080
# B. repeat_disable vs repeat_enable (cove view)
cap repeat-disable ../evidence/planning-checks/check-shaders/e11-no-repeat.gdshader 1280x720
cap repeat-enable 04b-scrolling-normals.gdshader 1280x720
# C. NORMAL not updated vs updated (cove, vertex stage, script clock 1.0)
W_CUTS=127 W_FOLLOW=1 W_CLOCK0=1.0 cap normal-missing ../evidence/planning-checks/check-shaders/e13-no-normal.gdshader 1280x720
W_CUTS=127 W_FOLLOW=1 W_CLOCK0=1.0 cap normal-updated 05b-synced-clock.gdshader 1280x720
# D. silhouettes from a low camera: normal-map-only water (04d) vs real waves (05b)
W_BARE=1 W_VIEW=low cap low-flat 04d-warped-foam.gdshader 1280x720
W_BARE=1 W_VIEW=low W_CUTS=127 W_FOLLOW=1 W_CLOCK0=1.0 cap low-waves 05b-synced-clock.gdshader 1280x720
# F. function foam vs baked texture foam (top view)
W_BARE=1 W_VIEW=top W_TOPSIZE=8 cap foam-function 03-noise-foam.gdshader 1080x1080
W_BARE=1 W_VIEW=top W_TOPSIZE=8 cap foam-texture 03d-foam-from-texture.gdshader 1080x1080
