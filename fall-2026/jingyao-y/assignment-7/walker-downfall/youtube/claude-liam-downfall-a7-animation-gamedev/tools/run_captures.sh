#!/usr/bin/env bash
# New Movie Maker captures for the A7 film (fixtures; windowed; 30 fps).
# Writes into the film folder's capture/. Usage: run_captures.sh NAME...
set -u
GODOT="/d/CSYE 7370/Godot_v4.7.2-stable_win64_console.exe"
GAME="/d/CSYE 7370/csye-7270-course/fall-2026/jingyao-y/assignment-7/walker-downfall"
REEL="$GAME/youtube/claude-liam-downfall-a7-animation-gamedev"
OUTW="D:/CSYE 7370/csye-7270-course/fall-2026/jingyao-y/assignment-7/walker-downfall/youtube/claude-liam-downfall-a7-animation-gamedev/capture"
cap() { # name frames scene
  local name=$1 frames=$2 target=$3
  mkdir -p "$REEL/capture/$name"
  local cmd=("$GODOT" --path "$GAME" "$target" --write-movie "$OUTW/$name/frame.png" --fixed-fps 30 --quit-after "$frames")
  printf '%q ' "${cmd[@]}" > "$REEL/capture/$name/command.txt"
  sha256sum "$GAME/animations/npc_idle.tscn" "$GAME/animations/lappland_wave_rig.tscn" "$GAME/entities/player.gd" > "$REEL/capture/$name/source-hashes.txt"
  "${cmd[@]}" > "$REEL/capture/$name/capture.log" 2>&1
  echo "exit=$?" >> "$REEL/capture/$name/capture.log"
  echo "done $name"
}
for n in "$@"; do
  case $n in
    wave_dodges) cap wave_dodges 620 res://previews/film_wave_dodges.tscn ;;
    npc_in_game) cap npc_in_game 760 res://previews/npc_idle_in_game.tscn ;;
    rig_turntable) cap rig_turntable 45 res://previews/wave_rig_turntable.tscn ;;
  esac
done
