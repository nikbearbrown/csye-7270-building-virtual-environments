# Prompts — walker-survival-shooting pitch

## What the author asked for (2026-11-25 to 11-26, translated from Chinese)
- The final-project pitch film, built around the tablet system; target role technical game designer; comparable games Metal Gear Solid V: The Phantom Pain, Subnautica, Abiotic Factor and Escape from Tarkov, with the author's own observations.
- The 19 beats were reviewed one by one; the narration was compressed under 4 minutes, translated, and the trial voice approved.
- "You capture it": Claude recorded all footage with scripted input. "Narration only says landing dust": the light dust is not mentioned, because it barely shows from the player camera.
- Drawings in the show-tell isometric style (chosen over the godot-gamedev figure layout).

## Narration
The English narration is `narration_text` in `beat_sheet.json`, translated by Claude from the author's approved Chinese draft (working copy, not uploaded) and approved by the author after listening. Voice: local Kokoro `am_onyx`, speed 1.0, via `runtime/scripts/generate_audio_kokoro.py`. It speaks as the author; no instructor persona.

## Tools and models
- Claude Code (Claude Opus 5.5): beat sheet, narration translation, capture scripts, scenes, media preparation, paperwork.
- Kokoro (local, free): narration audio.
- Godot 4.7.2 Movie Maker: game footage (scripted input, see CAPTURE.md).
- Manim 0.18.1 and Remotion (from the Brutalist toolkit, local checkout 22264a3): drawings and the name card.
- Microsoft Edge (headless): screenshots of the README and test-log pages.
No paid generation, no API keys.
