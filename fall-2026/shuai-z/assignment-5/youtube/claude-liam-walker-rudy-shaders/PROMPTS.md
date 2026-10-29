# PROMPTS — Two Shaders for Walker Rudy.

Every prompt shown or read in the film.

## B00 — Jambo, Liam

**Status:** reconstructed prompt — illustrative, not a transcript

```text
Please use Walker to convert my game design document about Walker Rudy — a chibi boy who crosses the Harvest Fields, safe for a moment after each hit — into two shaders: hearts that tint while he is invulnerable, driven from game state, and a textured stone shader with two materials for the waystone and the teleport circle, each claim checked headless or by eye.
```

On-screen result lines (each checked in FACTCHECK.md):

- Repo walker-rudy · assignment-5/ at a2a3a77 · Godot 4.7.2 · game/ GL Compatibility · godot/ Forward+.
- Built: invulnerable_tint.gdshader on the hearts; weathered_stone.gdshader with two materials; the hint experiment.
- Every shader line: shuai-z, by hand · brief, driver, tests and captures: Claude Code, reviewed by shuai-z.

## BHTF — Your turn.

**Status:** suggested prompt for the viewer

```text
Read my CHANGE-BRIEF.md and game/shaders/invulnerable_tint.gdshader. Before you change anything, let me predict by hand P1's colour at tint_amount 1.0 if tint_strength were 0.6, and the heart outline's contrast against the sky (rule 9 asks for 3:1). Then, on a copy of game/, set tint_strength to 0.6 in ui/hearts_tint.tres, not in the shader, run tests/capture_tint.tscn in a window, and show me the measured pixels beside my prediction.
```

## The prompts behind the work shown

The film quotes no prompt from the build sessions. The scoped `claude -p` prompts it refers to are in the assignment folder: `sessions/prompt-1.txt` (CLAUDE.md), `prompt-2.txt` and `prompt-2b.txt` (the driver and its test), `prompt-3.txt` (the materials audit), with their transcripts described in `sessions/README.md`.
