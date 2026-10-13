#!/usr/bin/env python3
"""summarize-lab.py: print lab-results.jsonl as a compact table (label, exit, renderer, probes) and write lab-summary.txt.
Probe values are 0..1 floats exactly as the Lab read them from the rendered frame."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
lines = []
for raw in (HERE / "lab-results.jsonl").read_text().splitlines():
    r = json.loads(raw)
    out = r["output"]
    head = f"[{r['exit']}] {r['check']:42}"
    res = None
    for ln in out.splitlines():
        if ln.startswith("RESULT "):
            res = json.loads(ln[7:])
    if res is None:
        lines.append(head + " " + out.replace("\n", " | ")[:200])
        continue
    probes = " ".join(f"({p['at'][0]:g},{p['at'][1]:g})=" + ",".join(f"{v:.3f}" for v in p['rgba'][:3]) for p in res.get("probes", []))
    extra = "" if r["exit"] == 0 else " | " + " | ".join(l for l in out.splitlines() if not l.startswith("RESULT "))[:160]
    lines.append(head + f" {res['renderer']:16} {res['size'][0]}x{res['size'][1]}  {probes}{extra}")
text = "\n".join(lines)
(HERE / "lab-summary.txt").write_text(text + "\n")
print(text)
