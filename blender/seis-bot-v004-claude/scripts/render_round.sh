#!/bin/bash
# render_round.sh <assembled.blend> <outdir> <prefix> [samples]
# Renders 4 cove views (front three_q left back) in ONE process and 2 workshop views in a second process, from a private
# copy of the .blend.  Keep it to two processes: each Blender holds ~7 GB for the full figure and six at once drove this Mac
# into swap (renders stalled for 20+ minutes).
set -e
W=/PATH/TO/seis-bot-v004-detailed
SRC="$1"; OUT="$2"; PFX="$3"; SMP="${4:-48}"
TMP=$(mktemp -d /tmp/seis-render.XXXXXX)
cp "$SRC" "$TMP/copy.blend"
B=/Applications/Blender.app/Contents/MacOS/Blender
mkdir -p "$OUT"
( $B -b --factory-startup "$TMP/copy.blend" --python $W/src/render_gallery.py -- --out "$OUT" --set full --only front,three_q,left,back --w 900 --h 1200 --samples $SMP --prefix ${PFX}_ > $W/logs/${PFX}_cove.log 2>&1 ) &
( $B -b --factory-startup "$TMP/copy.blend" --python $W/src/render_gallery.py -- --out "$OUT" --set full --only front,three_q --w 900 --h 1200 --samples $SMP --prefix w${PFX#r}_ --stage workshop --fstop 4 > $W/logs/w${PFX#r}_workshop.log 2>&1 ) &
wait
rm -rf "$TMP"
