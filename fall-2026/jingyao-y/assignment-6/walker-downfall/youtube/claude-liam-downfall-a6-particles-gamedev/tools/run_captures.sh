#!/usr/bin/env bash
# New Movie Maker captures for the A6 film (fixtures; windowed; 30 fps).
# Writes into the film folder's capture/ (gitignored). Usage: run_captures.sh NAME...
set -u
GODOT="/d/CSYE 7370/Godot_v4.7.2-stable_win64_console.exe"
GAME="/d/CSYE 7370/csye-7270-course/fall-2026/jingyao-y/assignment-6/walker-downfall"
REEL="$GAME/youtube/claude-liam-downfall-a6-particles-gamedev"
OUTW="D:/CSYE 7370/csye-7270-course/fall-2026/jingyao-y/assignment-6/walker-downfall/youtube/claude-liam-downfall-a6-particles-gamedev/capture"
cap() { # name frames scene-or-script user-args...
  local name=$1 frames=$2 target=$3; shift 3
  mkdir -p "$REEL/capture/$name"
  local cmd=("$GODOT" --path "$GAME")
  if [[ $target == *.gd ]]; then cmd+=(--script "$target"); else cmd+=("$target"); fi
  cmd+=(--write-movie "$OUTW/$name/frame.png" --fixed-fps 30 --quit-after "$frames")
  if [ $# -gt 0 ]; then cmd+=(-- "$@"); fi
  printf '%q ' "${cmd[@]}" > "$REEL/capture/$name/command.txt"
  sha256sum "$GAME/effects/hit_spark.tscn" "$GAME/effects/fire_pit_flames.tscn" > "$REEL/capture/$name/effect-hashes.txt"
  "${cmd[@]}" > "$REEL/capture/$name/capture.log" 2>&1
  echo "exit=$?" >> "$REEL/capture/$name/capture.log"
  echo "done $name"
}
for n in "$@"; do
  case $n in
    a_loop_city) cap a_loop_city 660 res://previews/hit_spark_preview.tscn --loop ;;
    a_loop_snow) cap a_loop_snow 660 res://previews/hit_spark_preview.tscn --loop --snow ;;
    b_loop) cap b_loop 540 res://previews/fire_pit_flames_preview.tscn --loop ;;
    a_play) cap a_play 260 res://youtube/claude-liam-downfall-a6-particles-gamedev/tools/capture_play.gd ;;
    b_states) cap b_states 330 res://youtube/claude-liam-downfall-a6-particles-gamedev/tools/capture_fire_states.gd ;;
  esac
done
