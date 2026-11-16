#!/usr/bin/env python3
"""make_editor_clips.py: B43's clip from the four SCRIPT-RECORDED editor frames (editor-capture/png/1920x1080/renderer-path/), dissolved with ffmpeg at the
lane's fractions (0.19, 0.42, 0.56 of the beat). 'scripted editor session'. Output: TK/runtime/remotion/public/shaders-in-3d/editor-renderer.mp4"""
import json, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent
F = R.parent / "_godot-shaders-series/editor-capture/png/1920x1080/renderer-path"
OUT = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/shaders-in-3d")
d = float(next(b["actual_duration_s"] for b in json.loads((R / "beat_sheet.json").read_text())["beats"] if b["beat_id"] == "B43"))
frames = ["renderer-path_R1-A_Project-menu-open.png", "renderer-path_R1-C_Project-Settings_Rendering-Renderer_menu-closed.png",
          "renderer-path_R1-D_Project-Settings_Rendering-Method_menu-open.png", "renderer-path_R1-E_Project-Settings_restart-note.png"]
edges = [0.19 * d, 0.42 * d, 0.56 * d]; fade = 0.5
cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for f in frames: cmd += ["-loop", "1", "-t", f"{d + 1:.2f}", "-framerate", "30", "-i", str(F / f)]
parts, last = [], "[0:v]"
for i, e in enumerate(edges):
    parts.append(f"{last}[{i + 1}:v]xfade=transition=fade:duration={fade}:offset={e - fade / 2:.3f}[v{i}]"); last = f"[v{i}]"
cmd += ["-filter_complex", ";".join(parts) + f";{last}format=yuv420p[o]", "-map", "[o]", "-t", f"{d + 0.5:.2f}", "-c:v", "libx264", "-crf", "14", "-r", "30", str(OUT / "editor-renderer.mp4")]
subprocess.run(cmd, check=True); print("wrote", OUT / "editor-renderer.mp4")
