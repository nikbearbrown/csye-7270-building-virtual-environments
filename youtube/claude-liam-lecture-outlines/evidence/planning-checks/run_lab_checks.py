#!/usr/bin/env python3
"""run_lab_checks.py: re-runs every Lab render this film's numbers come from (real Godot 4.7.2 window via the series Shader Lab).
Writes lab-results.jsonl (one line per run: command, exit code, RESULT line) and png/<label>.png. Safe to re-run.
Usage: python3 run_lab_checks.py [label-prefix ...]   (no argument: every check)
Then:  python3 analyze_lab.py   (measures the PNGs and writes lab-summary.txt)
"""
import json, subprocess, sys, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab" / "check_shader.sh"
SH = FILM / "lab-shaders"
PNG = HERE / "png"; PNG.mkdir(exist_ok=True)
OUT = HERE / "lab-results.jsonl"

S1 = ["--kind", "sprite", "--sprite-scale", "1.0"]            # one image pixel = one screen pixel: distances are literal
P = "--probe"
CHECKS = []
def add(label, shader, *args, size=None):
    a = list(args)
    if size: a += ["--size", size]
    CHECKS.append((label, shader, a))

# Act 1 ------------------------------------------------------------------------------------------------
add("01-look-0.000", "01-look-right.gdshader", *S1, "--set", "look=0.0")
add("01-look-0.125", "01-look-right.gdshader", *S1, "--set", "look=0.125")
add("01-look-0.250", "01-look-right.gdshader", *S1, "--set", "look=0.25")
add("02-paints-the-sprite", "02-paints-the-sprite.gdshader", *S1)
add("03-one-question", "03-one-question.gdshader", *S1)
add("04-lighter-diagonals", "04-lighter-diagonals.gdshader", *S1)
add("05-four-questions", "05-four-questions.gdshader", *S1)
# fit-to-view versions (what the film shows: the sprite large, 1280x720 logical canvas is the capture's, here 640x360)
add("05-four-questions-fit", "05-four-questions.gdshader", "--kind", "sprite")
add("04-lighter-diagonals-fit", "04-lighter-diagonals.gdshader", "--kind", "sprite")
# Act 2 ------------------------------------------------------------------------------------------------
for t in (1, 2, 3, 4, 8):
    add(f"06-pixel-steps-t{t}", "06-pixel-steps.gdshader", *S1, "--set", f"thickness={t}")
    add(f"07-eight-reads-t{t}", "07-eight-reads.gdshader", *S1, "--set", f"thickness={t}")
    add(f"08-loop-t{t}", "08-loop.gdshader", *S1, "--set", f"thickness={t}")
    add(f"10-ring-t{t}", "10-ring.gdshader", *S1, "--set", f"thickness={t}")
    add(f"09-guard-t{t}", "09-guard.gdshader", *S1, "--set", f"thickness={t}")
    add(f"11-soft-edges-t{t}", "11-soft-edges.gdshader", *S1, "--set", f"thickness={t}")
add("06-pixel-steps-t0", "06-pixel-steps.gdshader", *S1, "--set", "thickness=0.0")
add("09-guard-t0", "09-guard.gdshader", *S1, "--set", "thickness=0.0")
for sc in ("2.0", "3.0"):
    add(f"06-pixel-steps-t2-scale{sc}", "06-pixel-steps.gdshader", "--kind", "sprite", "--sprite-scale", sc, "--set", "thickness=2", size="960x540")
add("06-pixel-steps-t1-fit", "06-pixel-steps.gdshader", "--kind", "sprite", "--set", "thickness=1")
add("06-pixel-steps-t3-fit", "06-pixel-steps.gdshader", "--kind", "sprite", "--set", "thickness=3")
# renderer comparison for one line-colour pixel (Forward+ default above; Compatibility here)
add("06-pixel-steps-t2-compat", "06-pixel-steps.gdshader", *S1, "--set", "thickness=2", "--renderer", "gl_compatibility")
add("05-four-questions-compat", "05-four-questions.gdshader", *S1, "--renderer", "gl_compatibility")

def main(argv):
    sel = [c for c in CHECKS if not argv or any(c[0].startswith(p) for p in argv)]
    existing = {}
    if OUT.exists() and argv:
        for line in OUT.read_text().splitlines():
            r = json.loads(line); existing[r["check"]] = r
    for label, shader, args in sel:
        cmd = [str(LAB), str(SH / shader), *args, "--png", str(PNG / f"{label}.png")]
        p = subprocess.run(cmd, capture_output=True, text=True)
        out = (p.stdout + p.stderr).strip()
        res = next((l for l in out.splitlines() if l.startswith("RESULT ")), "")
        existing[label] = {"check": label, "shader": shader, "args": args, "exit": p.returncode,
                           "date": datetime.date.today().isoformat(), "result": json.loads(res[7:]) if res else None,
                           "raw": None if res and p.returncode == 0 else out[:1500]}
        print(f"[{p.returncode}] {label}")
    OUT.write_text("\n".join(json.dumps(r) for r in sorted(existing.values(), key=lambda r: r["check"])) + "\n")

if __name__ == "__main__":
    main(sys.argv[1:])
