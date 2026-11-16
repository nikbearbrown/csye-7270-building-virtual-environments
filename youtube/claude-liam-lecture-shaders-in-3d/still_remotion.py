#!/usr/bin/env python3
"""still_remotion.py <BEAT_ID> [...] [--pcts 25 50 95] [--scale 1]: 25/50/95% stills of Remotion beats from beat_sheet.json props
into /private/tmp/claude-501/<slug>-stills/<BID>_<pct>.png (LOOK at them before any render)."""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
RM = "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion"
OUT = Path(f"/private/tmp/claude-501/{HERE.name}-stills"); OUT.mkdir(parents=True, exist_ok=True)
args = sys.argv[1:]; pcts = [25, 50, 95]; scale = "1"
if "--pcts" in args:
    i = args.index("--pcts"); pcts = [int(x) for x in args[i + 1:] if x.isdigit()]; args = args[:i]
if "--scale" in args:
    i = args.index("--scale"); scale = args[i + 1]; del args[i:i + 2]
sheet = json.loads((HERE / "beat_sheet.json").read_text())
chrome = "/Users/bear/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell"
for bid in args:
    b = next(x for x in sheet["beats"] if x["beat_id"] == bid)
    r = b["shot"]["remotion"]; dur = float(b.get("actual_duration_s") or b["estimated_duration_s"])
    props = dict(r["props"])
    if props.get("durationSeconds") == "__AUDIO__": props["durationSeconds"] = dur
    pf = OUT / f"{bid}_props.json"; pf.write_text(json.dumps(props))
    for pct in pcts:
        frame = max(0, min(int(dur * 24) - 1, int(dur * 24 * pct / 100)))
        png = OUT / f"{bid}_{pct}.png"
        p = subprocess.run(["npx", "remotion", "still", "src/index.ts", r["pattern"], str(png), f"--frame={frame}", f"--props={pf}", f"--scale={scale}", f"--browser-executable={chrome}"],
                           cwd=RM, capture_output=True, text=True, timeout=600)
        print(bid, pct, "ok" if png.exists() else "FAILED\n" + p.stderr[-600:], flush=True)
