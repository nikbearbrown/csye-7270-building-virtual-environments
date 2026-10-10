#!/usr/bin/env python3
"""Render ASSET-LOG.md from gen/log/**.json. The sidecars are the source of truth; never hand-edit ASSET-LOG.md."""
import json
from collections import defaultdict
from common import ROOT

FENCE = "`" * 3
runs = defaultdict(list)
for p in sorted((ROOT / "gen" / "log").glob("*/*.json")):
    m = json.loads(p.read_text())
    runs[m["asset_id"]].append(m)

out = ["# ASSET-LOG", "",
       "Rendered by `gen/render_log.py` from the JSON sidecars in `gen/log/`. Every run is listed, including rejects.",
       "Tag `design-v1` precedes every timestamp below (checked by `scripts/audit_repo.py --stage final`).", ""]
for asset in sorted(runs):
    out += [f"## {asset}", ""]
    contact = ROOT / "gen" / "rejected" / f"{asset}-contact.png"
    if contact.exists():
        out += [f"![{asset} contact sheet](gen/rejected/{asset}-contact.png)", ""]
    for m in sorted(runs[asset], key=lambda r: r["created_utc"]):
        d = m.get("decision") or {}
        out += [f"### {m['run_id']}", "",
                "| Field | Value |", "|---|---|",
                f"| Created (UTC) | {m['created_utc']} |",
                f"| Model / version | {m['model']} / {m['model_version']} |",
                f"| Runtime | {m['runtime']} |",
                f"| Licence / terms | {m['license']} |",
                f"| Settings | `{json.dumps(m['settings'])}` |",
                f"| Storyboard panels | {', '.join(m.get('storyboard_panels', []))} |",
                f"| Decision | **{d.get('verdict', 'PENDING')}** by {d.get('decided_by', '—')} at {d.get('decided_utc', '—')} |",
                f"| Reason | {d.get('reason', '—')} |",
                f"| Manual edits | {d.get('edits') or '—'} |",
                f"| Project files | {', '.join(d.get('final_paths', [])) or '—'} |",
                f"| Thumbnail | ![]({m['thumbnail']}) |", ""]
        if m.get("processing"):
            out += ["**Processing (every edit, in order)**", ""]
            out += [f"{i}. `{json.dumps(step, ensure_ascii=False)}`" for i, step in enumerate(m["processing"], start=1)]
            out += [""]
        out += [
                "**Prompt**", "", FENCE, m["prompt"], FENCE, "",
                "**Negative prompt**", "", FENCE, m.get("negative_prompt") or "(none)", FENCE, ""]
(ROOT / "ASSET-LOG.md").write_text("\n".join(out) + "\n")
print(f"ASSET-LOG.md: {sum(len(v) for v in runs.values())} runs across {len(runs)} assets")
