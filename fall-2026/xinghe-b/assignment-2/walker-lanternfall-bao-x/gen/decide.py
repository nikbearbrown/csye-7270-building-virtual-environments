#!/usr/bin/env python3
"""Record Bao's decision on one generation run.

    python gen/decide.py ART-PC-01 <run_id> accept "reason" --edits "..." --final godot/assets/art/pc_sheet.png
"""
import argparse, json, shutil
from pathlib import Path
from common import ROOT, utc_now

ap = argparse.ArgumentParser()
ap.add_argument("asset_id")
ap.add_argument("run_id")
ap.add_argument("verdict", choices=["accept", "modify", "reject"])
ap.add_argument("reason")
ap.add_argument("--edits", default="")
ap.add_argument("--final", nargs="*", default=[])
ap.add_argument("--by", default="Bao Xing")
a = ap.parse_args()

side = ROOT / "gen" / "log" / a.asset_id / f"{a.run_id}.json"
meta = json.loads(side.read_text())
meta["decision"] = {"verdict": a.verdict, "reason": a.reason, "edits": a.edits, "final_paths": a.final,
                    "decided_by": a.by, "decided_utc": utc_now()}
if a.verdict in ("accept", "modify"):
    for raw in meta.get("raw_outputs", []):
        src = ROOT / raw
        if src.exists():
            dst = ROOT / "gen" / "accepted" / a.asset_id / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            meta.setdefault("accepted_copies", []).append(str(dst.relative_to(ROOT)))
side.write_text(json.dumps(meta, indent=2) + "\n")
print(f"{a.asset_id} {a.run_id}: {a.verdict}")
