"""Write SHOTLIST.md and PROMPTS.md from beat_sheet.json (so they cannot drift)."""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
md = sheet["metadata"]
beats = {b["beat_id"]: b for b in sheet["beats"]}

shot = ["# Shot list — " + md["title"], "",
        "One row per beat, in order. Durations are measured Kokoro narration (B01 includes 0.8 s lead silence, "
        "B23 a 1.0 s tail hold).",
        "\"Reconstruction\" = Godot editor reconstruction (source-backed teaching view, not a recording).", "",
        "| Beat | Act | Dur (s) | Visual | Evidence shown | Label on screen |", "|---|---|---|---|---|---|"]
total = 0.0
for b in sheet["beats"]:
    d = b.get("actual_duration_s") or 0
    total += d
    s = b.get("shot", {})
    rem = s.get("remotion") or {}
    pat = rem.get("pattern", "real footage")
    p = rem.get("props", {})
    if pat == "GodotDevWorkbench":
        ev = f"`{p.get('path')}` (code mode)"
        lab = "Godot editor reconstruction · source-backed teaching view"
    elif pat == "GodotDesignFigure":
        ev = f"`{p.get('imageLabel')}`"
        lab = p.get("status", "")
    elif pat == "GodotDesignBoard":
        ev = "document excerpt + cards"
        lab = p.get("excerptLabel", "") + " · " + p.get("status", "")
    elif pat == "ClaudeComposerAsk":
        ev, lab = "composer prompt", p.get("segment", "")
    elif pat == "real footage":
        ev, lab = f"`{s.get('evidence_media')}` (native 4K Godot render)", "burned-in disclosure label"
    else:
        ev, lab = "—", ""
    shot.append(f"| {b['beat_id']} | {b.get('act','')} | {d:.2f} | {pat} | {ev} | {lab} |")
shot += ["", f"Total ≈ {total:.1f} s ({total/60:.1f} min) before frame alignment.", ""]
(REEL / "SHOTLIST.md").write_text("\n".join(shot), encoding="utf-8")

pr = ["# Prompts and script — " + md["title"], "",
      "## Reconstructed opening prompt (B00)",
      "Illustrative reconstruction written for this film. It is **not** a saved session or a historical transcript.", "",
      "```text", beats["B00"]["shot"]["remotion"]["props"]["command"], "```", "",
      "## Your Turn prompt (B22)", "", "```text", beats["B22"]["shot"]["remotion"]["props"]["command"], "```", "",
      "## The designer's prompts shown in the film",
      "Shown in B04, B05 and B07, in English translation, exactly as the game's SOURCES.md asset log gives them",
      "(rows PROP-TABLET-01 and CRATE-LONG-02; the B07 quote is shortened with an ellipsis). The originals were",
      "typed in Chinese. No model was run for the film except Kokoro for the narration.", "",
      "## Narration script (Kokoro am_onyx, exact text sent to TTS)", ""]
for b in sheet["beats"]:
    pr += [f"**{b['beat_id']} · {b.get('act','')}**", "", b.get("narration_text", ""), ""]
(REEL / "PROMPTS.md").write_text("\n".join(pr), encoding="utf-8")
print("wrote SHOTLIST.md, PROMPTS.md")
