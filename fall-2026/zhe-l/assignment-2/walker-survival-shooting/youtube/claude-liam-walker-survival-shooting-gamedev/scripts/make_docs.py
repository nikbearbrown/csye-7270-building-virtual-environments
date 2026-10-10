"""Write SHOTLIST.md and PROMPTS.md from beat_sheet.json (so they cannot drift)."""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
md = sheet["metadata"]

shot = ["# Shot list — " + md["title"], "",
        "One row per beat, in order. Durations are measured narration (or the measured sound file for B09).",
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
        ev = f"`{p.get('path')}`" + (f" ({p.get('mode')} mode)")
        lab = "Godot editor reconstruction · source-backed teaching view"
    elif pat in ("GodotDesignFigure",):
        ev = f"`{p.get('imageLabel')}`"
        lab = p.get("status", "")
    elif pat == "GodotDesignBoard":
        ev = p.get("image") and f"`{p.get('visualLabel')}`" or "document excerpt + cards"
        lab = p.get("status", "")
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
      "```text", sheet["beats"][0]["shot"]["remotion"]["props"]["command"], "```", "",
      "## Your Turn prompt (B19)", "", "```text",
      next(b for b in sheet["beats"] if b["beat_id"] == "B19")["shot"]["remotion"]["props"]["command"], "```", "",
      "## Generation prompts shown in the film",
      "Prompt A1 (rejected V01) and A4 (accepted V03) are quoted from the game's SOURCES.md appendix; the full",
      "texts and every seed are there. The film adds no new generation; no model was run for the film except",
      "Kokoro for narration.", "",
      "## Narration script (Kokoro am_onyx, exact text sent to TTS)", ""]
for b in sheet["beats"]:
    t = b.get("narration_text") or "(no narration — listening segment: generated sound files, not in-engine)"
    pr += [f"**{b['beat_id']} · {b.get('act','')}**", "", t, ""]
(REEL / "PROMPTS.md").write_text("\n".join(pr), encoding="utf-8")
print("wrote SHOTLIST.md, PROMPTS.md")
