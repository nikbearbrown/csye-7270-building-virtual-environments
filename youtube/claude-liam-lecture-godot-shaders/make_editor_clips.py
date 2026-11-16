#!/usr/bin/env python3
"""make_editor_clips.py: cuts the two editor clips of this film from the SCRIPT-RECORDED editor frames (editor-capture/png/1920x1080/godot-shaders/),
cross-dissolved with ffmpeg at the beats' measured durations. The frames are real Godot 4.7.2 editor states recorded by the editor driver
('scripted editor session'); the dissolves are the only thing added. Output: TK/runtime/remotion/public/godot-shaders/editor-attach.mp4, editor-slider.mp4"""
import json, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent
F = R.parent / "_godot-shaders-series/editor-capture/png/1920x1080/godot-shaders"
OUT = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/godot-shaders")
sheet = json.loads((R / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"] if b.get("actual_duration_s")}
def clip(name, frames, edges, total, fade=0.5):
    """frames: list of png names; edges: seconds at which the dissolve to the next frame is CENTRED."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in frames:
        cmd += ["-loop", "1", "-t", f"{total + 1:.2f}", "-framerate", "30", "-i", str(F / f)]
    parts, last = [], "[0:v]"
    for i, e in enumerate(edges):
        out = f"[v{i}]"
        parts.append(f"{last}[{i + 1}:v]xfade=transition=fade:duration={fade}:offset={e - fade / 2:.3f}{out}")
        last = out
    fc = ";".join(parts) + f";{last}format=yuv420p[o]"
    cmd += ["-filter_complex", fc, "-map", "[o]", "-t", f"{total + 0.5:.2f}", "-c:v", "libx264", "-crf", "14", "-r", "30", "-movflags", "+faststart", str(OUT / name)]
    subprocess.run(cmd, check=True)
    print("wrote", OUT / name)
OUT.mkdir(parents=True, exist_ok=True)
d = DUR["B10"]
clip("editor-attach.mp4", ["godot-shaders_E1-1_material-empty.png", "godot-shaders_E1-2b_shadermaterial-in-slot.png",
     "godot-shaders_E1-3e_shader-in-slot-editor-closed.png", "godot-shaders_E1-4_shader-editor-open-after-Create.png"],
     [0.30 * d, 0.57 * d, 0.79 * d], d)
d = DUR["B27"]
clip("editor-slider.mp4", ["godot-shaders_E2-2_red-0.2.png", "godot-shaders_E2-3_red-0.5-after-0.2.png", "godot-shaders_E2-4_red-0.9.png"],
     [0.58 * d, 0.80 * d], d, fade=0.4)
