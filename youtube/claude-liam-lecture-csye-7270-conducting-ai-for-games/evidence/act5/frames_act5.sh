#!/usr/bin/env bash
# frames_act5.sh — regenerates the pantry stills Act V uses from the REAL captures (read-only on _conducting-series-evidence/)
REEL="$(cd "$(dirname "$0")/../.." && pwd)"; EV="$REEL/../_conducting-series-evidence"
mkdir -p "$REEL/pantry/a5_game_frames"
ffmpeg -v error -y -ss 1.3 -t 4.2 -i "$EV/godot-captures/walker-claude/walker-claude-jumpman-gameplay.mp4" -vf "fps=12,scale=960:540:flags=lanczos" "$REEL/pantry/a5_game_frames/f%03d.png"
python3 - "$EV" "$REEL" <<'PY'
import sys
from PIL import Image
EV, REEL = sys.argv[1], sys.argv[2]
g = Image.open(EV + '/web-captures/godot-home.png').convert('RGB')
c = g.crop((192, 0, 2304, 806)); c = c.resize((1800, int(806 * 1800 / 2112)), Image.LANCZOS); c.save(REEL + '/pantry/a5_godot_home_top.png')
im = Image.open('/Users/bear/Documents/CoWork/bear-textbooks/books/walker/games/walker-jumpman/evidence/screens/03-jump.png').convert('RGB')
im.crop((380, 410, 780, 635)).save(REEL + '/pantry/a5_starter_jump_crop.png')
PY
