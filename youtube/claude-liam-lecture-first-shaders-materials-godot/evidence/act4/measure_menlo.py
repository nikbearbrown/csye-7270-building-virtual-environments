#!/usr/bin/env python3
"""measure_menlo.py — measures Menlo's advance per character at the sizes Act IV uses (Manim 0.20.1, this Mac): 0.15 at size 20, 0.20 at 24, 0.25 at 28/32.
Also shows why a4_cell() places rows by character cell: Text.width is the INK width, so leading spaces never count (indentation would be lost)."""
from manim import *
for size in (20, 24, 28, 32):
    a = Text("0", font="Menlo", font_size=size).width
    b = Text("00", font="Menlo", font_size=size).width
    print(f"size {size}: advance {b - a:.4f}")
s = "    float stripe = step(0.5, fract(UV.x * stripe_count));"
print("57 characters, 4 leading spaces: Text.width", round(Text(s, font="Menlo", font_size=20).width, 3), "(57 cells would be", round(57 * 0.15, 3), ")")
