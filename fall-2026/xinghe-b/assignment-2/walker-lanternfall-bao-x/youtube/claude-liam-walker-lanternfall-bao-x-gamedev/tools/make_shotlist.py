#!/usr/bin/env python3
"""SHOTLIST.md from beat_sheet.json and the composition specs in media/_work (what each beat actually shows)."""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
rows, total = [], 0.0
for b in sheet["beats"]:
    bid = b["beat_id"]
    rem = b["shot"].get("remotion")
    spec_p = REEL / "media" / "_work" / f"{bid}.json"
    if rem:
        src = f"Remotion `{rem['pattern']}`"
        if rem["pattern"].startswith("GodotDevWorkbench"):
            p = rem["props"]
            n = len(p["code"].split("\n"))
            src += f" · `{p['path'].replace('res://', 'godot/')}` lines {p['startLine']}–{p['startLine'] + n - 1}"
        dur = float(b.get("actual_duration_s") or 0)
    elif spec_p.exists():
        spec = json.loads(spec_p.read_text())
        vids = []
        for L in spec["layers"]:
            if L["kind"] == "video" and L["src"].startswith("capture/"):
                f0 = round(L["ss"] * 30)
                span = (L["t"][1] if L["t"][1] < 9000 else spec["duration"]) - L["t"][0]
                vids.append(f"`{Path(L['src']).name}` frames {f0}–{f0 + round(span * 30) - 1}")
        imgs = sorted({Path(L["src"]).name for L in spec["layers"] if L["kind"] == "image" and not L["src"].startswith("media/_work")})
        src = "composed (tools/compose.py)" + (": " + "; ".join(dict.fromkeys(vids)) if vids else "") + \
              (" · files: " + ", ".join(imgs) if imgs else "")
        dur = spec["duration"]
    else:
        src, dur = "MISSING", 0.0
    total += dur
    kind = "game sound only" if b.get("kind") == "source_report" else ("code" if b.get("kind") == "code" else b.get("act", "").lower())
    rows.append(f"| {bid} | {b['act']} | {kind} | {dur:.2f} | {src} |")
out = ["# SHOTLIST", "",
       f"`{sheet['metadata']['slug']}` · {len(rows)} beats · {total:.1f} s ({total / 60:.1f} min) · source revision "
       f"{sheet['metadata']['game']['source_revision'][:7]}", "",
       "Durations are measured narration (Kokoro am_onyx) or, for game-sound-only beats, the source clip itself. "
       "Frame numbers are 30 fps frames of the takes in `capture/` (see CAPTURE.md).", "",
       "| Beat | Act | Kind | Seconds | What is on screen |", "|---|---|---|---|---|"] + rows
(REEL / "SHOTLIST.md").write_text("\n".join(out) + "\n")
print(f"SHOTLIST.md: {len(rows)} beats, {total:.1f} s")
