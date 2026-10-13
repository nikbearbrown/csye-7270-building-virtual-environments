"""summarize_glow.py: prints a readable table from glow-results.jsonl (display-referred values: what the screen shows)."""
import json
from pathlib import Path
here = Path(__file__).resolve().parent
rows = [json.loads(l) for l in open(here / "glow-results.jsonl")]
f = lambda c: "(" + ", ".join(f"{x:.3f}" for x in c[:3]) + ")"
for r in rows:
    res = r["result"]
    if not res.startswith("RESULT "):
        print(r["label"], r["renderer_flag"], "NO RESULT", r["errors"][:160]); continue
    j = json.loads(res[7:]); p = j["probes"]; d = j["display"]
    sub = j.get("sub_probes")
    line = (f"{r['label']:44} {j['renderer'][:7]:7} root_hdr={str(j['root_use_hdr_2d'])[0]} fmt={j['window_image_format']:>2} "
            f"| shows: body {f(d['body_far_from_spot'])} band {f(d['edge_band_mid'])} halo108 {f(d['halo_r108'])} halo118 {f(d['halo_r118'])} halo130 {f(d['halo_r130'])} stage {f(d['far_corner'])}")
    if sub:
        line += f" | frame holds body {f(sub['body_far_from_spot'])} (sub fmt {j['sub_format']})"
    print(line)
