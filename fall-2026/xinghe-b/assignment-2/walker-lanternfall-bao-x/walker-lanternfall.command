#!/bin/bash
# Double-click to play. A fresh clone or ZIP has no Godot import cache (godot/.godot is not committed),
# so import the assets once first; without this the game would run with placeholder art and no sound.
cd "$(dirname "$0")"
G=/Applications/Godot.app/Contents/MacOS/Godot
[ -d godot/.godot/imported ] || "$G" --headless --path godot --import --quit
exec "$G" --path godot
