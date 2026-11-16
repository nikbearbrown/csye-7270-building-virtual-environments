#!/usr/bin/env python3
"""verify_lines.py — diffs every verbatim literal Act IV shows (A4_SRC_* in scenes_act4.py) against the frozen source or the log it came from, and checks
that every until(self, "phrase") cue of scenes_act4.py is a phrase of that beat's narration (a cue whose phrase is missing silently does nothing).
Run from anywhere:  python3 evidence/act4/verify_lines.py        (exit 0 = every literal is verbatim, every cue exists)"""
import ast, json, re, sys
from pathlib import Path
REEL = Path(__file__).resolve().parent.parent.parent
SRC = REEL / "evidence" / "example" / "sources"
RUNS = REEL / "evidence" / "runs"
tree = ast.parse((REEL / "scenes_act4.py").read_text())
lit = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id.startswith("A4_SRC_"):
        lit[node.targets[0].id] = eval(compile(ast.Expression(node.value), 'scenes_act4.py', 'eval'), {})   # the file's own literals / comprehensions
bad = 0


def check(name, ok, detail=""):
    global bad
    print(("OK   " if ok else "FAIL ") + name + (" " + detail if detail and not ok else ""))
    bad += 0 if ok else 1


def lines_of(path):
    return path.read_text().split("\n")


# consecutive lines of a source file
for name, (f, first) in {"A4_SRC_SIGNAL": ("signal.gdshader", 1), "A4_SRC_GARDEN_4": ("garden.gd", 4), "A4_SRC_GARDEN_227": ("garden.gd", 227),
                         "A4_SRC_GARDEN_253": ("garden.gd", 253)}.items():
    L = lines_of(SRC / f)
    got = lit[name]
    want = L[first - 1:first - 1 + len(got)]
    check(f"{name} == {f} lines {first}-{first + len(got) - 1}", got == want, f"\n  got  {got}\n  want {want}")
# the specification's colour line: CHANGE-BRIEF-a5.md line 5 contains it
check("A4_SRC_BRIEF_COLOUR in CHANGE-BRIEF-a5.md line 5", lit["A4_SRC_BRIEF_COLOUR"] in lines_of(SRC / "CHANGE-BRIEF-a5.md")[4])
# the prompt fragments are consecutive words of the assignment's driver prompt
t = (SRC / "assignment-05.md").read_text()
i = t.index("Read CLAUDE.md first. The specification in CHANGE-BRIEF.md")
flat = " ".join(t[i:t.index("```", i)].split())
for fr in lit["A4_SRC_PROMPT"]:
    check(f"prompt fragment {fr!r}", fr in flat)
# real log lines: (file, line number, text)
for name in ("A4_SRC_LOG_B31", "A4_SRC_LOG_B33", "A4_SRC_LOG_B34"):
    for f, n, txt in lit[name]:
        got = lines_of(RUNS / f)[n - 1].rstrip()
        check(f"{name} {f}:{n}", got == txt, f"got {got!r}")
# the command of B33 is the journal's M1-parse row
j = (RUNS / "journal-commands-exit-codes-elapsed.tsv").read_text()
row = [l for l in j.splitlines() if "\tM1-parse\t" in l][0]
check("B33 command + exit=1 in the run journal", lit["A4_SRC_CMD_B33"] in row and "exit=1" in row, row)
# sample counts and exit codes quoted in the factcheck
for fps, n in ((30, 294), (60, 409), (144, 726)):
    check(f"R2-driver-{fps}fps.log sample count {n}", f"sample count {n}" in (RUNS / f"R2-driver-{fps}fps.log").read_text())
# DURATION render_samples drawn as ticks in B32
for fps, n in ((30, 16), (60, 34), (144, 83)):
    d = [l for l in (RUNS / f"R2-driver-{fps}fps.log").read_text().splitlines() if l.startswith("DURATION") and '"scale":1.0' in l][0]
    check(f"R2-driver-{fps}fps.log DURATION render_samples {n}", json.loads(d.split(" ", 1)[1])["render_samples"] == n)
# cues exist in the narration
sheet = json.loads((REEL / "beat_sheet.json").read_text())
narr = {b["beat_id"]: b["narration_text"] for b in sheet["beats"]}
src = (REEL / "scenes_act4.py").read_text()
for m in re.finditer(r"class (B\d+[A-Z]?)_\w+\(Scene\):(.*?)(?=\nclass |\Z)", src, re.S):
    bid, body = m.group(1), m.group(2)
    for c in re.finditer(r'until\(self, "([^"]+)"', body):
        check(f"{bid} cue {c.group(1)!r}", c.group(1) in narr[bid])
print("\nALL VERBATIM" if not bad else f"\n{bad} PROBLEM(S)")
sys.exit(1 if bad else 0)
