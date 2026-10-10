#!/usr/bin/env python3
"""SCRIPT.md: the film's narration, beat by beat, with what is on screen (from beat_sheet.json)."""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
md = sheet["metadata"]
out = [f"# SCRIPT — {md['title']}", "",
       f"Narrator: {md['persona']}, Kokoro `{md['voice_kokoro']}`. Source revision shown: `{md['game']['source_revision'][:7]}`. "
       "Timings are the measured narration (or the clip itself for game-sound beats).", ""]
t = 0.0
for b in sheet["beats"]:
    d = float(b.get("render_duration_s") or b.get("actual_duration_s"))
    mm = f"{int(t // 60)}:{t % 60:04.1f}"
    shows = "; ".join(s["event"] for s in b["shot"].get("show", []))
    out.append(f"## {b['beat_id']} · {b['act']} · {mm} ({d:.1f} s)")
    out.append("")
    out.append(f"*On screen:* {shows}")
    out.append("")
    if b.get("kind") == "source_report":
        out.append("**[Game sound only — no narration.]** " + b["role_note"])
    elif b["beat_id"] == "B33":
        out.append("**[Outro card — stock jingle only, no narration.]**")
    else:
        out.append(b["narration_text"])
    out.append("")
    t += d
out.append(f"Total: {int(t // 60)} min {t % 60:.1f} s.")
(REEL / "SCRIPT.md").write_text("\n".join(out) + "\n")
print("SCRIPT.md", round(t, 1), "s")
