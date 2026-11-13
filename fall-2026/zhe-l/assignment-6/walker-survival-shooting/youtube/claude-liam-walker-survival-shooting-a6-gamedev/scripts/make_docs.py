"""Write SHOTLIST.md, PROMPTS.md and COMPONENTS.md from beat_sheet.json and gamedev-evidence.json (no drift)."""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
ev = json.loads((REEL / "gamedev-evidence.json").read_text(encoding="utf-8"))
md = sheet["metadata"]
beats = {b["beat_id"]: b for b in sheet["beats"]}

shot = ["# Shot list — " + md["title"], "",
        "One row per beat, in order. Durations are measured Kokoro narration (B01 includes 0.8 s lead silence, "
        "B31 a 1.0 s tail hold; B08 and B16 run their full captures).",
        "\"Reconstruction\" = Godot editor reconstruction (source-backed teaching view, not a recording).", "",
        "| Beat | Act | Dur (s) | Visual | Evidence shown | Label on screen |", "|---|---|---|---|---|---|"]
total = 0.0
for b in sheet["beats"]:
    d = b.get("render_duration_s") or b.get("actual_duration_s") or 0
    total += d
    s = b.get("shot", {})
    rem = s.get("remotion") or {}
    pat = rem.get("pattern", "real footage")
    p = rem.get("props", {})
    if pat == "GodotDevWorkbench":
        ev_s, lab = f"`{p.get('path')}` (code mode)", "Godot editor reconstruction · source-backed teaching view"
    elif pat == "GodotDesignFigure":
        ev_s, lab = f"`{p.get('imageLabel')}`", p.get("status", "")
    elif pat == "ClaudeComposerAsk":
        ev_s, lab = "composer prompt", p.get("segment", "")
    elif pat == "real footage":
        ev_s, lab = f"`{s.get('evidence_media')}` (native 4K Godot render)", "burned-in labels: scripted input, camera, code-set states"
    else:
        ev_s, lab = "—", ""
    shot.append(f"| {b['beat_id']} | {b.get('act', '')} | {d:.2f} | {pat} | {ev_s} | {lab} |")
shot += ["", f"Total ≈ {total:.1f} s ({total / 60:.1f} min) before frame alignment.", ""]
(REEL / "SHOTLIST.md").write_text("\n".join(shot), encoding="utf-8")

pr = ["# Prompts and script — " + md["title"], "",
      "## Reconstructed opening prompt (B00)",
      "Illustrative reconstruction written for this film. It is **not** a saved session or a historical transcript.",
      "", "```text", beats["B00"]["shot"]["remotion"]["props"]["command"], "```", "",
      "## Your Turn prompt (B30)", "", "```text", beats["B30"]["shot"]["remotion"]["props"]["command"], "```", "",
      "No model was run for the film except Kokoro (am_onyx) for the narration.", "",
      "## Narration script (Kokoro am_onyx, exact text sent to TTS)", ""]
for b in sheet["beats"]:
    pr += [f"**{b['beat_id']} · {b.get('act', '')}**", "", b.get("narration_text", ""), ""]
(REEL / "PROMPTS.md").write_text("\n".join(pr), encoding="utf-8")

co = ["# Components — " + md["title"], "",
      f"Game files: `godot/` of the course repository at {md["game"]["source_revision"]}.",
      f"{len(ev['files'])} files inventoried, {len(ev['exclusions'])} excluded with reasons, "
      f"{len(ev['excerpts'])} verbatim excerpts, {len(ev['code_result_pairs'])} code → result pairs "
      "(`gamedev-evidence.json`).", ""]
for c in ev["components"]:
    co += [f"## {c['id']}", "", c["explanation"], "", "Beats: " + ", ".join(c["beat_ids"]), "",
           "Files: " + ", ".join(f"`{f}`" for f in c["files"]), ""]
co += ["## Excluded files", ""] + [f"- `{x['path']}`: {x['reason']}" for x in ev["exclusions"]] + [""]
(REEL / "COMPONENTS.md").write_text("\n".join(co), encoding="utf-8")
print("wrote SHOTLIST.md, PROMPTS.md, COMPONENTS.md")
