#!/usr/bin/env bash
# gate4k.sh <Class> [<Class> ...] — What Is Walker, Act III: render each class at REAL 4K (3840x2160, 24 fps, caching off) into a private scratch
# folder, one at a time under the shared 4K lock, then run the toolkit's own GATE T functions (type_check.py) on the 50% frame and
# Gate V (final_frame_check.analyze_frame) on the 50% and 85% frames, and compare the clip length with the beat's audio.
# Read-only on the reel: never touches its scenes.py, manim/, media/ or beat_sheet.json.
set -u
REEL="$(cd "$(dirname "$0")/../.." && pwd)"
SCR=/private/tmp/claude-501/lecture-walker-act3-4k
LOCK=/private/tmp/claude-501/lecture-csye-4k.lock
mkdir -p "$SCR"
python3 "$REEL/assemble_scenes.py" --out "$SCR" --acts 3 >/dev/null || exit 1
cp "$REEL/beat_sheet.json" "$SCR/"; ln -sfn "$REEL/pantry" "$SCR/pantry"
for C in "$@"; do
  until mkdir "$LOCK" 2>/dev/null; do sleep 20; done
  rm -rf "$SCR/media/videos/scenes/2160p24/partial_movie_files/$C"
  (cd "$SCR" && manim -r 3840,2160 --fps 24 --disable_caching --media_dir "$SCR/media" scenes.py "$C" 2>&1 | grep -E "\[pace\]|Traceback|Error" | sed 's/.*\[pace\]/[pace]/')
  rmdir "$LOCK"
  MP4="$SCR/media/videos/scenes/2160p24/$C.mp4"
  [ -f "$MP4" ] || { echo "  no 4K clip for $C"; continue; }
  cp "$MP4" "$SCR/$C.mp4"
  python3 "$REEL/evidence/act3/gate_frames.py" "$SCR/$C.mp4" "$C"
done
