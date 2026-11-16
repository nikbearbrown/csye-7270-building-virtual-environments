#!/usr/bin/env python3
"""gate_b_all.py — GATE B (manim_layout_audit.py --curve-strict: text/frame/overlap audit) over every Manim class of the assembled scenes.py, one class at a time
in a private scratch (pantry/captures/evidence symlinked). Writes evidence/GATE-B.md. Run assemble_scenes.py first."""
import re, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
QC = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc")
SCR = Path("/private/tmp/claude-501/a5-gate-b")
shutil.rmtree(SCR, ignore_errors=True); SCR.mkdir(parents=True)
shutil.copy(HERE / "scenes.py", SCR / "scenes.py"); shutil.copy(HERE / "beat_sheet.json", SCR / "beat_sheet.json")
for d in ("pantry", "captures", "evidence"):
    (SCR / d).symlink_to(HERE / d)
classes = re.findall(r"^class (B[A-Z0-9]+_\w+)\(Scene\):", (HERE / "scenes.py").read_text(), re.M)
rows, bad = [], 0
for c in classes:
    r = subprocess.run([sys.executable, str(QC / "manim_layout_audit.py"), "scenes.py", "--class", c, "--curve-strict"], cwd=SCR, capture_output=True, text=True, timeout=900)
    md = (SCR / "layout_audit.md").read_text() if (SCR / "layout_audit.md").exists() else ""
    errs = len(re.findall(r"\*\*ERROR\*\*", md)); warns = len(re.findall(r"\*\*WARN\*\*", md))
    ok = r.returncode == 0 and errs == 0 and warns == 0
    bad += 0 if ok else 1
    rows.append((c, r.returncode, errs, warns))
    print(c, "ok" if ok else f"rc={r.returncode} errors={errs} warns={warns}", flush=True)
    shutil.rmtree(SCR / "media", ignore_errors=True)
out = ["# GATE-B.md — layout audit (--curve-strict) over every Manim class", "", f"{len(classes)} classes; {bad} with a non-zero exit, ERROR or WARN.", "", "| class | exit | errors | warnings |", "|---|---|---|---|"]
out += [f"| {c} | {rc} | {e} | {w} |" for c, rc, e, w in rows]
(HERE / "evidence/GATE-B.md").write_text("\n".join(out) + "\n")
print(f"{len(classes)} classes; not clean: {bad}")
