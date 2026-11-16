#!/usr/bin/env python3
"""verify_lines.py (Act X) — proves that the real shader lines drawn in scenes_act10.py (B73) are verbatim, with their real line numbers, from the frozen
sources evidence/example/sources/signal.gdshader and surface.gdshader (a tab is drawn as four spaces, as the kit does), and that the B72 numbers in the scene
equal the assignment's rubric. B71's terminal lines and the lane's other numbers are checked by build_lanes_act10.py.  Run: python3 evidence/act10/verify_lines.py"""
import ast, re, sys
from pathlib import Path
R = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot")
tree = ast.parse((R / "scenes_act10.py").read_text())
bad = 0
files = {"signal": (R / "evidence/example/sources/signal.gdshader").read_text().split("\n"), "surface": (R / "evidence/example/sources/surface.gdshader").read_text().split("\n")}
shown = []
for n in ast.walk(tree):
    if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "a10_code" and isinstance(n.args[0], ast.List):
        for el in n.args[0].elts:
            shown.append(ast.literal_eval(el))
for lab, text in shown:
    hits = [(f, int(lab)) for f, ls in files.items() if int(lab) <= len(ls) and ls[int(lab) - 1].replace("\t", "    ") == text.replace("\t", "    ")]
    ok = bool(hits)
    bad += not ok
    print("B73 line", lab, text.strip()[:60], "->", hits if ok else "MISMATCH")
# B72: the scene's segments equal the rubric
src = (R / "scenes_act10.py").read_text()
segs = [int(x) for x in re.findall(r'\(-?[\d.]+, -?[\d.]+, \w+, (?:None|\w+), "(\d+)", "', src)]
split = [int(x) for x in re.findall(r'\("(\d+)", "(?:specification|shader from code|textures, materials|the language|verification|the film)"\)', src)]
print("B72 segments", segs, "sum", sum(segs), "| split", split, "sum", sum(split))
bad += (sum(segs) != 100 or sum(split) != 60 or segs != [60, 10, 10, 20] or split != [8, 12, 14, 10, 8, 8])
sys.exit(1 if bad else 0)
