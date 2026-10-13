#!/bin/zsh
# Capture real renders of walker-claude (Jumpman + Clawd gallery) from a SCRATCH COPY.
# Source project is never touched: copy = rsync of walker-claude/godot minus .godot/evidence/youtube,
# plus res://capture/capture_driver.gd registered as an autoload in the copy's project.godot.
set -eu
WORK=/private/tmp/claude-501/capture-work/walker-claude
COPY=$WORK/godot
OUT="/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude"
GODOT=/opt/homebrew/bin/godot
mkdir -p "$OUT" "$WORK/frames-game" "$WORK/frames-gallery"
rm -rf "$WORK/frames-game" "$WORK/frames-gallery"; mkdir -p "$WORK/frames-game" "$WORK/frames-gallery"

# 1) Jumpman: title screen -> Enter -> run right + jumps -> level complete (Movie Maker, fixed 30 fps, windowed)
$GODOT --path "$COPY" --write-movie "$WORK/frames-game/f.png" --fixed-fps 30 --resolution 1920x1080 --always-on-top \
  res://game/main.tscn -- --mode=game --out="$OUT" 2>&1 | tee "$OUT/raw-log-game.txt"

# 2) Clawd 18-animation gallery, pages 1..3 via Right arrow
$GODOT --path "$COPY" --write-movie "$WORK/frames-gallery/f.png" --fixed-fps 30 --resolution 1920x1080 --always-on-top \
  res://gallery/clawd_gallery.tscn -- --mode=gallery --out="$OUT" 2>&1 | tee "$OUT/raw-log-gallery.txt"

# 3) Encode H.264 MP4s, 30 fps, 1920x1080. Game clip = 8 s from frame 30 (title -> Enter -> run/jump).
ffmpeg -y -loglevel error -framerate 30 -start_number 30 -i "$WORK/frames-game/f%08d.png" -frames:v 240 \
  -c:v libx264 -pix_fmt yuv420p -crf 16 -preset slow -r 30 "$OUT/walker-claude-jumpman-gameplay.mp4"
# Gallery clip = 8 s from frame 90 (page 1 animating -> Right arrow -> page 2)
ffmpeg -y -loglevel error -framerate 30 -start_number 90 -i "$WORK/frames-gallery/f%08d.png" -frames:v 240 \
  -c:v libx264 -pix_fmt yuv420p -crf 16 -preset slow -r 30 "$OUT/walker-claude-clawd-gallery.mp4"
pkill -x Godot 2>/dev/null || true; pkill -f /opt/homebrew/bin/godot 2>/dev/null || true
# Sanity: count distinct movie frames (Godot skips drawing when its window is occluded; --always-on-top fixed that here)
echo "DISTINCT game frames: $(md5 -q "$WORK"/frames-game/*.png | sort -u | wc -l) of $(ls "$WORK"/frames-game/*.png | wc -l)" | tee -a "$OUT/raw-log-game.txt"
echo "DISTINCT gallery frames: $(md5 -q "$WORK"/frames-gallery/*.png | sort -u | wc -l) of $(ls "$WORK"/frames-gallery/*.png | wc -l)" | tee -a "$OUT/raw-log-gallery.txt"
