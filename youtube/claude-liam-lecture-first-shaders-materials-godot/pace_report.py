#!/usr/bin/env python3
"""pace_report.py — after the audio exists: render EVERY Manim beat class at low quality (full clip, `manim -ql`), read its `[pace]` line and write _qc/pace.md.
A class whose content time is within 0.1 s of its audio target (OVER) would be centre-cut by the compiler: shorten its final waits or its fixed sequences, never the narration.
Usage: python3 pace_report.py [--scenes scenes.py] [BEAT_ID ...]      (run assemble_scenes.py first; one class at a time; scratch media is deleted per class)"""
import json, re, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
args = sys.argv[1:]
scenes = "scenes.py"
if "--scenes" in args:
    i = args.index("--scenes"); scenes = args[i + 1]; del args[i:i + 2]
sheet = json.loads((HERE / "beat_sheet.json").read_text())
SCR = Path("/private/tmp/claude-501/lecture-a5shaders-pace")
rows = []
for b in sheet["beats"]:
    cls = (b.get("shot", {}).get("manim") or {}).get("class")
    if not cls or (args and b["beat_id"] not in args):
        continue
    shutil.rmtree(SCR, ignore_errors=True)
    r = subprocess.run(["manim", "-ql", "--media_dir", str(SCR), str(HERE / scenes), cls], cwd=HERE, capture_output=True, text=True)
    line = next((l for l in (r.stdout + r.stderr).splitlines() if "[pace]" in l), "")
    m = re.search(r"content=([\d.]+)s target=([\d.]+)s(\s+OVER)?", line)
    if m:
        rows.append((b["beat_id"], cls, float(m.group(1)), float(m.group(2)), bool(m.group(3))))
        print(b["beat_id"], cls, m.group(1), m.group(2), "OVER" if m.group(3) else "ok", flush=True)
    else:
        rows.append((b["beat_id"], cls, None, None, True))
        print(b["beat_id"], cls, "NO PACE LINE (render failed?)", (r.stdout + r.stderr)[-400:], flush=True)
shutil.rmtree(SCR, ignore_errors=True)
(HERE / "_qc").mkdir(exist_ok=True)
out = ["# pace report (manim -ql, full clips; content must be <= target - 0.1 s)", "", "| beat | class | content s | target s | verdict |", "|---|---|---|---|---|"]
for bid, cls, c, t, over in rows:
    out.append(f"| {bid} | {cls} | {c if c is not None else '—'} | {t if t is not None else '—'} | {'OVER' if over else 'ok'} |")
(HERE / "_qc/pace.md").write_text("\n".join(out) + "\n")
print("OVER:", [r[0] for r in rows if r[4]] or "none")
