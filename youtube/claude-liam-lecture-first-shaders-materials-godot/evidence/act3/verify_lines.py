#!/usr/bin/env python3
"""verify_lines.py (Act III) — proves that the real code and log text drawn in scenes_act3.py is verbatim from its source.
  B19 A3_WRAP    : rows (soft-wrapped rows joined with single spaces) == the lines of evidence/runs/scripts/run-test.sh, in order; line numbers are real
  B23 A3_CLAUDEMD: each (line number, text) == that line of evidence/example/sources/CLAUDE.md; the file has 65 lines
  B24 A3_FLAG    : rows joined (no space: it is broken after a comma) == a substring of the assignment's claude -p line (assignment-05.md line 207); the allowed-tools list is its own
The Remotion terminal beats (B20-B22) are checked by build_lanes_act3.py. Run: python3 evidence/act3/verify_lines.py"""
import ast, sys
from pathlib import Path
R = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot")
src = ast.parse((R / "scenes_act3.py").read_text())
const = {}
for n in src.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("A3_WRAP", "A3_CLAUDEMD", "A3_FLAG"):
        const[n.targets[0].id] = ast.literal_eval(n.value)
bad = 0
# B19
real = (R / "evidence/runs/scripts/run-test.sh").read_text().splitlines()
logical, cur = [], None
for lab, text in const["A3_WRAP"]:
    if lab is not None:
        if cur is not None: logical.append(cur)
        cur = [lab, text]
    else:
        cur[1] += " " + text
logical.append(cur)
for lab, text in logical:
    ok = real[int(lab) - 1] == text
    bad += not ok
    print("B19 line", lab, "OK" if ok else f"MISMATCH {text!r} vs {real[int(lab)-1]!r}")
print("B19 lines in the file:", len(real), "| lines shown:", len(logical))
# B23
cm = (R / "evidence/example/sources/CLAUDE.md").read_text().splitlines()
for lab, text in const["A3_CLAUDEMD"]:
    if not lab:
        continue
    ok = cm[int(lab) - 1] == text if text.strip() else cm[int(lab) - 1].strip() == ""
    bad += not ok
    print("B23 line", lab, "OK" if ok else f"MISMATCH {text!r} vs {cm[int(lab)-1]!r}")
print("B23 CLAUDE.md length:", len(cm), "lines")
# B24
a = (R / "evidence/example/sources/assignment-05.md").read_text().splitlines()
claude_line = [l for l in a if l.startswith('claude -p "$(cat prompt-1.txt)"')][0]
flag = "".join(t for _, t in const["A3_FLAG"])      # the flag line is wrapped after a comma, so the rows join with no space
ok = flag in claude_line
bad += not ok
print("B24 flag rows joined are in the assignment's prompt-1 claude -p line:", ok, "| assignment line", a.index(claude_line) + 1, "| length", len(flag))
sys.exit(1 if bad else 0)
