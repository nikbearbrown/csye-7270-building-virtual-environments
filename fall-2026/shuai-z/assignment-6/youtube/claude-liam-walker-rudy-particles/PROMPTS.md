# PROMPTS — Sparks and Dust for Walker Rudy.

Every prompt shown or read in the film.

## B00 — Jambo, Liam

**Status:** reconstructed prompt — illustrative, not a transcript

```text
Please use Walker to convert my game design document about Walker Rudy — a chibi boy who crosses the Harvest Fields with a sword — into two particle effects: sparks that mark where and when his cut can land, and a dust trail while he runs, each specified before it is built, tuned by eye against frame strips, tested headless, and priced against a budget.
```

On-screen result lines (each checked in FACTCHECK.md):

- Repo walker-rudy · assignment-6/game at d0ed415 · Godot 4.7.2 · GL Compatibility · one 2D game.
- Built: SlashSparks (a burst per live cut) and RunDust (a world-space trail), their previews, tests and driver.
- Effects and tests: scoped claude -p sessions · every verdict and approval: shuai-z · Use It records: Codex.

## BHTF — Your turn.

**Status:** suggested prompt for the viewer

```text
Read my CHANGE-BRIEF.md and game/effects/run_dust.tscn. Before you change anything, let me predict by hand how high the dust band's top rises above the walk line at strip frame 25 if damping_min / _max go from 120 / 180 to 60 / 90, using TUNING.md's r3 model. Then, on a copy of game/, change only those two lines, capture run_dust_preview.tscn with Movie Maker, measure the top against a no-dust render, and show me your number beside my prediction.
```

## The prompts behind the work shown

The film quotes no prompt from the build sessions. The scoped `claude -p` prompts it refers to are in the assignment folder's `sessions/`: `prompt-1.txt` (CLAUDE.md), `prompt-2.txt` (Effect A, its configuration test and preview), `prompt-3.txt` and `prompt-3b.txt` (the plan and the wiring of Effect A, with its state test), `prompt-4.txt` (Effect B), `prompt-5.txt` and `prompt-5b.txt` (the plan and the wiring of Effect B), `prompt-6.txt` (the cost script), each beside its transcript `session-*.jsonl`.
