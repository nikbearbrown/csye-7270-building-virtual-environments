#!/usr/bin/env zsh
# check_midpoints.sh — GATE T + Gate V on the MIDPOINT frame of each Act II beat (the frame GATE T samples), emulated at 4K:
# the capture is sampled exactly as Manim 0.20 does (PIL transform, bicubic), masked to the viewer frame, labels/ring/spark
# drawn in PIL, then round-tripped through h264 yuv420 at crf 18 / 23 (Manim's) / 28, each with sub-pixel jitter.
# Why: a Blender capture is full of small dark UI shapes; GATE T §8.3b reads some (a glyph counter, a padlock, the navigation
# gizmo's camera icon, a piece of viewport grid cut off by a ring) as low-contrast "text". The cameras in scenes_act2.py were
# chosen so every midpoint passes under every variant. No Manim render, no 4K video. Run from the reel folder.
cd "${0:A:h}"; P=../../../pantry; OUT=${TMPDIR:-/tmp}/a2_mid; mkdir -p $OUT
L=(--lab label@-6.2,-2.3,40 --lab word@-4.5,1.6,36)
cfg=( "B15 B16|$P/a2_bl_sidebar_closed.png|999|956|1.25|"
      "B17|$P/a2_bl_sidebar_closed.png|999|956|1.25|--ring 22,236,250,1568"
      "B18|$P/ev_bl_object_mode.png|2026.5|760|1.6|--ring 1316,240,2440,1100"
      "B19|$P/a2_bl_sidebar_closed.png|960|797|1.3|--dot 1095,985"
      "B20|$P/a2_bl_sidebar_closed.png|999|956|1.25|--dot 1095,985" )
for c in $cfg; do
  IFS='|' read nm img cx cy sc extra <<< "$c"; r=""
  for crf in 18 23 28; do sed "s/\"-crf\", \"23\"/\"-crf\", \"$crf\"/" emulate4k.py > $OUT/e.py
    for j in -1.5 0 1.5; do
      python3 $OUT/e.py $OUT/f.png --img $img --cam $(python3 -c "print($cx+$j)"),$(python3 -c "print($cy+$j)"),$sc ${=extra} $L
      r="$r $(python3 gates.py $OUT/f.png | head -1 | cut -c1-4)"; done; done
  echo "$nm midpoint (crf 18/23/28 x jitter):$r"
done
