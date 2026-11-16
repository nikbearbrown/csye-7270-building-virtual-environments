#!/usr/bin/env python3
"""gates_static.py — the render-free gates run.sh runs before any render, over EVERY Manim class of the assembled scenes.py:
GATE A (static_scene_check.py, from an isolated folder holding only scenes.py, as run.sh does) and GATE W (wcag_margin_check.py), plus GATE L (beat_lint.py) and build_safety.
Usage (from anywhere): python3 evidence/gates_static.py   -> evidence/GATES-STATIC.md. Run assemble_scenes.py first."""
import json, re, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
QC = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc")
SC = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
SCR = Path("/private/tmp/claude-501/a5-gates-static")
shutil.rmtree(SCR, ignore_errors=True); (SCR / "gateA").mkdir(parents=True)
shutil.copy(HERE / "scenes.py", SCR / "gateA" / "scenes.py")
shutil.copy(HERE / "beat_sheet.json", SCR / "gateA" / "beat_sheet.json")
classes = re.findall(r"^class (B[A-Z0-9]+_\w+)\(Scene\):", (HERE / "scenes.py").read_text(), re.M)
rows, bad = [], 0
for c in classes:
    ra = subprocess.run([sys.executable, str(QC / "static_scene_check.py"), "scenes.py", "--class", c, "--quiet"], cwd=SCR / "gateA", capture_output=True, text=True)
    rw = subprocess.run([sys.executable, str(QC / "wcag_margin_check.py"), "scenes.py", "--class", c, "--quiet"], cwd=SCR / "gateA", capture_output=True, text=True)
    a = "PASS" if ra.returncode == 0 else "FAIL"; w = "PASS" if rw.returncode == 0 else "FAIL"
    if a == "FAIL" or w == "FAIL":
        bad += 1
        print(c, "A", a, "W", w, (ra.stdout + ra.stderr + rw.stdout + rw.stderr)[-400:].replace("\n", " | "))
    rows.append((c, a, w))
rl = subprocess.run([sys.executable, str(QC / "beat_lint.py"), str(HERE / "beat_sheet.json")], capture_output=True, text=True)
rb = subprocess.run([sys.executable, str(SC / "build_safety.py"), str(HERE)], capture_output=True, text=True)
out = ["# GATES-STATIC.md — render-free gates over the assembled scenes.py", "",
       f"{len(classes)} Manim classes: GATE A (static) and GATE W (contrast/margins/overlap). GATE L (beat_lint): exit {rl.returncode}. build_safety: exit {rb.returncode}.", "",
       "```", (rl.stdout + rl.stderr).strip()[-600:], (rb.stdout + rb.stderr).strip()[-600:], "```", "", "| class | GATE A | GATE W |", "|---|---|---|"]
out += [f"| {c} | {a} | {w} |" for c, a, w in rows]
(HERE / "evidence/GATES-STATIC.md").write_text("\n".join(out) + "\n")
print(f"{len(classes)} classes; failures: {bad}; GATE L exit {rl.returncode}; build_safety exit {rb.returncode}")
sys.exit(1 if bad or rl.returncode or rb.returncode else 0)
