"""Turns lab-results.jsonl into lab-summary.txt: one line per run, with the renderer, every probe, and the engine's first error line."""
import json, re
from pathlib import Path
here = Path(__file__).resolve().parent
lines = []
for raw in (here / "lab-results.jsonl").read_text().splitlines():
    r = json.loads(raw)
    out = r["output"]
    m = re.search(r"^RESULT (\{.*\})$", out, re.M)
    probes, renderer, size = [], "?", "?"
    if m:
        j = json.loads(m.group(1))
        renderer = j.get("renderer"); size = "x".join(map(str, j.get("size", [])))
        probes = [(p["at"], p["rgba"][:3]) for p in j.get("probes", [])]
    err = re.findall(r"^SHADER ERROR: (.*)$", out, re.M)
    lines.append(f'{r["check"]} | exit {r["exit"]} | {renderer} | {size} | ' + (f'SHADER ERROR: {err[0]}' if err else str(probes)))
(here / "lab-summary.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
