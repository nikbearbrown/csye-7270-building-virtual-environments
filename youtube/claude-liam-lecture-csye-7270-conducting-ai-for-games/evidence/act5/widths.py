#!/usr/bin/env python3
"""widths.py — measures the real Manim width of every left-aligned label in scenes_act5.py (Gate A's stub cannot measure text).
  python3 evidence/act5/widths.py"""
from manim import *
def T(s, size, bold=False): return Text(s, font="EB Garamond", font_size=size, weight="BOLD" if bold else "NORMAL")
def M(s, size): return Text(s, font="Menlo", font_size=size)
for s, sz, b in [("Claude Code", 38, 0), ("Codex", 38, 0), ("scripted input, recorded 2026-10-09", 32, 0), ("Frictional — an honest effort log", 38, 1),
                 ("did", 34, 0), ("decided", 34, 0), ("doubted", 34, 0), ("the engine", 36, 0), ("the rules", 36, 0),
                 ("Professor Bear", 34, 0), ("conducting", 44, 0), ("How the Course Works", 40, 0)]:
    print(f"{s!r:50} {sz} {T(s, sz, b).width:.3f}")
print("Menlo 32 per char:", round(M("M" * 40, 32).width / 40, 4))
