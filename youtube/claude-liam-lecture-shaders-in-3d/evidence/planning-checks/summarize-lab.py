#!/usr/bin/env python3
"""summarize-lab.py: turns lab-results.jsonl into lab-summary.txt (one line per check: label | renderer that ran | exit | probes or the error text)."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
lines = []
for raw in (here / "lab-results.jsonl").read_text().splitlines():
    rec = json.loads(raw)
    out = rec["output"]
    result = None
    errs = []
    for line in out.splitlines():
        if line.startswith("RESULT "):
            result = json.loads(line[7:])
        elif line.startswith("SHADER ERROR") or line.startswith("ERROR"):
            errs.append(line.strip())
    if rec["exit"] != 0:
        status = f"exit {rec['exit']} (EXPECTED FAILURE: the compiler's own message follows)" if "broken" in rec["check"] else f"exit {rec['exit']} (UNEXPECTED)"
        lines.append(f"{rec['check']} | {rec['renderer_requested']} | {status} | " + " / ".join(errs))
        continue
    probes = [(p["at"], p["rgba"][:3]) for p in result["probes"]] if result else []
    lines.append(f"{rec['check']} | {result['renderer'] if result else '?'} | exit 0 | " + "; ".join(f"{a} -> {c}" for a, c in probes))
(here / "lab-summary.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
