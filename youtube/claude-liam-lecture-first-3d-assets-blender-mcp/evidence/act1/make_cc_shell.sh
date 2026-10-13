#!/usr/bin/env bash
# make_cc_shell.sh — pantry/a1_cc_shell.png: the library's Claude Code skin (CC kit, CCSession) with NOTHING typed
# (an empty prompt bar), rendered as one 2x still and cropped to its window. Used in B02 and B11 as Claude Code's own surface
# (SHOW-THE-THING rung 2). No session ran; nothing is shown as typed or returned. (The corner mascot is off: Clawd's
# terracotta body reads as accent-coloured text under GATE T.)
set -euo pipefail
REEL="$(cd "$(dirname "$0")/../.." && pwd)"
RM=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion
TMP=/private/tmp/claude-501/a1scratch/rm; mkdir -p "$TMP"
(cd "$RM" && npx remotion still src/index.ts CCSession "$TMP/ccsession_nomascot.png" --frame=40 --scale=2 \
   --props='{"title":"claude","mode":"default","blocks":[{"type":"prompt","text":"","cue":0,"typeDuration":1}],"mascot":"off"}')
python3 -c "from PIL import Image; Image.open('$TMP/ccsession_nomascot.png').crop((276,136,3564,2024)).save('$REEL/pantry/a1_cc_shell.png')"
echo "wrote $REEL/pantry/a1_cc_shell.png"
