# PROMPTS

## B00 — the ask (reconstructed, shown in the Claude composer)

> Please use Walker to convert my game design document about a lamp-headed courier who must survive three minutes in a fog-bound night market into a playable Godot asset slice. Generate every sprite, sound effect and music loop with local open models, log every candidate, and make sure sound never decides the game.

This is a **reconstruction** written from Bao's design documents (CONCEPT.md, STORYBOARD.md, CHARACTER-SHEET.md, CHANGE-BRIEF.md), as the walker modifier asks. It is not a recording of a session. The actual work happened over several sessions in Bao's own words (Chinese), recorded in FRICTIONAL.md; the CONCEPT says the Walker `/gdd` skill was not used.

## B32 — Your Turn (on screen, read aloud)

> Please use Walker to read godot/audio/audio_bus.gd in my Lanternfall project. Change only the kill sound's cooldown_ms from 60 to 0. Before running anything, predict how many kill sounds play when twenty moths die in the same tick, and which checks in tests/test_audio.gd will fail. Then run the audio suite and compare.

One bounded change, a prediction written first, and a test that answers it. The answer was checked on an isolated copy (FACTCHECK.md, "Your Turn — answer key").

## The request that produced this film

Bao, 2026-10-01: "不用，直接开始做视频" (no — go straight to making the video), after the assignment brief named the film tool: "godot-gamedev skill + walker modifier", a 4K landscape film with Walker bookends and Verdict → Your Turn → regular outro, covering ten items (concept and pillars; one asset traced from design to prompt to raw output to edits to Godot; two or more character states; four SFX on real events; a game-sound-only segment; a source change and what the player sees or hears; tests, uncertainties and next steps; who did what; which model made each asset; the source revision shown).

## Prompts inside the film's evidence

The ART-PC-01 prompts shown in B05 are quoted verbatim from `gen/log/ART-PC-01/*.json`; they were written for FLUX.1-schnell during the asset work, not for the film.
