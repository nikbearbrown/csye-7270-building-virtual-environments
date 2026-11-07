# PROMPTS — walker-magic gamedev film

## Prompts shown on screen

| Beat | Prompt | Status on screen |
|---|---|---|
| B01 | "Please use Walker to convert my game design document about a young fire mage carrying the only warm light through a dark cave into a small Godot asset slice." | **Reconstructed prompt**, not a saved chat (the skill's Walker opening). |
| B06 | CHAR-REF v1, the setup message, CHAR-IDLE v1 — full text | **Verbatim** from `SOURCES.md` → Image prompts; drafted by Claude, sent by the author in the Gemini app (model shown in the app: Gemini 3.8 Flash); the author confirmed all were sent unchanged. |
| B25 | "Please use Walker to shorten the wolf's growl from 0.5 s to a third of a second. Predict the hurt count in the real-lunge test, then run it." | **Suggested prompt**, not a saved chat. |

## Prompts that made the film

- **Script and beat sheet:** drafted by Claude Code (Claude Opus 5.5) from the author's film brief and approved by the author on 2026-10-07 (`SCRIPT.md`, title supplied by the author).
- **Narration:** Kokoro-82M (`am_onyx`), run locally from `beat_sheet.json`; no prompt beyond the approved narration text.
- **Visuals:** no generative image or video model was used for the film. Cards are drawn by `scripts/cards.py`; Remotion compositions come from the Brutalist library; gameplay is the game itself, captured by `capture_driver.gd`.
- **The game's own assets** (images, effects, music) and every prompt behind them are in the game's `SOURCES.md`.
