#!/bin/zsh
# Re-creates pantry/a1_editor.png: a REAL Godot 4.7.2 editor window (Movie Maker records the root window), 2026-10-09, Mac with M4 Pro.
# Everything happens in a scratch COPY of the Claude Walker project (the original is untouched); the only edit is the copy's window
# size override (1280x720 -> 1920x1080) so Movie Maker records 1920x1080. Frame 230 of 241 (7.7 s in) is the one used.
set -e
W=/private/tmp/claude-501/godot-editor-shot; rm -rf $W; mkdir -p $W/frames
rsync -a --exclude .godot --exclude evidence --exclude youtube /Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot/ $W/proj/
sed -i '' 's/window_width_override=1280/window_width_override=1920/; s/window_height_override=720/window_height_override=1080/' $W/proj/project.godot
godot --editor --path $W/proj res://gallery/clawd_gallery.tscn --write-movie $W/frames/f.png --fixed-fps 30 --quit-after 240
cp $W/frames/f00000230.png "$(dirname "$0")/../../pantry/a1_editor.png"
