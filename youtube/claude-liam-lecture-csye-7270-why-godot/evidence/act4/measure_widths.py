#!/usr/bin/env python3
"""measure_widths.py — measures the real rendered width of every EB Garamond string Act IV positions (a4_tl / a4_w), and writes them into
scenes_act4.py's A4_W table (between the markers).  Why: left-aligned labels must not rely on a per-character estimate.
  1. REEL/preflight.sh with A4_REC=<file> records every (string, size, bold) a4_w() is asked for;  2. this script measures them with real Manim.
  A4_REC=/private/tmp/claude-501/lecture-csye-godot-act4/widths.jsonl ./preflight.sh 4 B19_... ;  python3 evidence/act4/measure_widths.py
"""
import json, re, sys
from pathlib import Path
from manim import Text
REEL = Path(__file__).resolve().parents[2]
rec = Path("/private/tmp/claude-501/lecture-csye-godot-act4/widths.jsonl")
keys = sorted({tuple(json.loads(l)) for l in rec.read_text().splitlines() if l.strip()})
tab = {}
for s, size, bold in keys:
    t = Text(s, font="EB Garamond", font_size=size, weight="BOLD" if bold else "NORMAL")
    tab[(s, size, bold)] = round(float(t.width), 3)
body = "A4_W = {\n" + "".join(f"    ({k[0]!r}, {k[1]}, {k[2]}): {v},\n" for k, v in tab.items()) + "}"
p = REEL / "scenes_act4.py"
src = p.read_text()
src2 = re.sub(r"A4_W = \{.*?\n\}\n|A4_W = \{\}[^\n]*\n", body + "  # measured\n", src, count=1, flags=re.S)
p.write_text(src2)
print(len(tab), "widths written")
