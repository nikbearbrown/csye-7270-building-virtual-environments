#!/usr/bin/env python3
"""Act IV Remotion test stills: 25 / 50 / 95 % of each beat from evidence/act4/remotion/<BID>_props.json (same props as lanes/act4.json).
python3 evidence/act4/remotion/stills.py [B31 B32 B33]  ->  /private/tmp/claude-501/a4scratch/<BID>_<pct>.png  (one still at a time)"""
import json, subprocess, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
RM = "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion"
OUT = pathlib.Path("/private/tmp/claude-501/a4scratch"); OUT.mkdir(parents=True, exist_ok=True)
for bid in (sys.argv[1:] or ["B31", "B32", "B33"]):
    d = json.loads((HERE / f"{bid}_props.json").read_text())
    pf = OUT / f"{bid}_p.json"; pf.write_text(json.dumps(d["props"]))
    for pct in (25, 50, 95):
        fr = max(1, int(d["props"]["durationSeconds"] * 30 * pct / 100))
        png = OUT / f"{bid}_{pct}.png"
        r = subprocess.run(["npx", "remotion", "still", "src/index.ts", d["pattern"], str(png), f"--frame={fr}", f"--props={pf}"],
                           cwd=RM, capture_output=True, text=True)
        print(bid, pct, fr, "ok" if r.returncode == 0 else "FAIL " + r.stderr[-400:])
