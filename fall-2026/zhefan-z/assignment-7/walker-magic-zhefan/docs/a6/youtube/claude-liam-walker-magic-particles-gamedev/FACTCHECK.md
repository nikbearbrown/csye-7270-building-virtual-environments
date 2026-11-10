# FACTCHECK — every spoken claim and its source

Documents at 3c37fe0. "Capture" = `capture/run-01-inputs.jsonl` (CAPTURE.md). Line numbers are of the files at 3c37fe0.

| Beat | Claim (spoken) | Source |
|---|---|---|
| B00 | two effects: a burst of sparks and smoke where it lands; a trail while it flies | CHANGE-BRIEF.md "Effect A — The job", "Effect B — The job", Layers (line 34) |
| B00 | specified first, tested headlessly, tuned from strips, priced on the GPU | CHANGE-BRIEF.md (original 2026-11-05, before any build); TEST-REPORT.md; TUNING.md; TEST-REPORT.md "Price" |
| B00 output | 14 / 0 and 20 / 0 at 30, 60, 144 fps | TEST-REPORT.md lines 20–21 |
| B01 | three steps: born, moved, drawn | CHANGE-BRIEF.md short answer 6 (emission, process, draw) |
| B02 | walker magic: a pixel-art mage crosses a cave, casts fireballs at a wolf | README.md (Assignment 6) line 3 |
| B02 | A's job: where and when a shot landed, on the wolf, a wall or the ground; event Fireball.explode() | CHANGE-BRIEF.md lines 23–25 |
| B02 | B's job: where a shot is heading; condition: fireball exists and hasn't exploded | CHANGE-BRIEF.md lines 78–80 |
| B03 | explode keeps the old flash, instances the impact into the parent (Main) | `fireball.gd` 43–48; CHANGE-BRIEF.md revision 2026-11-05 (flash outside); A5 rule (Main) line 73 |
| B03 | reparent to Main keeping its place, emitting off, freed one lifetime later; timeout calls the same release | `fireball.gd` 28, 49, 57–63 |
| B04 | one click into the ground; the trail fades where it was | capture frames 16–70 (CAPTURE.md); RIFF.md |
| B05 | 24 sparks, all at once, once | `fireball_impact.tscn` 80, 83, 85 |
| B05 | process moves each particle every frame, in a shader on the GPU | `particles_generated.gdshader` `process()` 277–379, line 324 |
| B05 | draw: a 4×4 texture added onto the cave | `fireball_impact.tscn` 8 (`blend_mode = 1`, Add), 81; ATTRIBUTION.md (4×4) |
| B05 | the colour ramp belongs to process; the author's first answer got it wrong | CHANGE-BRIEF.md short answer 6, "(Corrected: I had put the colour ramp under draw.)" |
| B06 | dummy renderer: 0 draw calls, empty capture rect, no process shader runs | CLAUDE.md "Headless facts" (A6); TEST-REPORT.md line 8 |
| B06 | node state observable; emitting turns false when all are emitted, not when they die; aliveness by instance | CLAUDE.md "Headless facts" (A6); CHANGE-BRIEF.md revision 2026-11-05 |
| B07 | flash at frame 0; sparks 0–0.15 s fast, then slow, red, vanish by 0.45; puff to 0.8; gone by 0.9 | CHANGE-BRIEF.md line 29 |
| B07 | six rules | CHANGE-BRIEF.md lines 69–74 (A1–A6) |
| B08 | spread 180, flat because disable z is on; velocity 90–160; gravity 300 down; damping 40–60; scale curve 1 → 0 | `fireball_impact.tscn` 25, 28–33, 36, 17–19; CHANGE-BRIEF.md revision 2026-11-05 |
| B08 | every value lives in the scene file | CLAUDE.md "Ownership"; `fireball.gd` sets no particle value |
| B09 | fixture capture, 30 fps, not gameplay; readings per frame | TUNING.md line 3; CHANGE-BRIEF.md line 141; captures/fireball_impact/r0/ |
| B09 | frame n ≈ (n − 9)/30 s | CHANGE-BRIEF.md revision "Effect A r1 kept" |
| B10 | stamped; 0.83 scale, 1.6 px vs 4.1 px rotated control; seed + 1; seeds spaced by 1000; prediction from frame 20; verdict different, kept | TUNING.md lines 13–21; commit 0069149 |
| B11 | wanted brighter; frame 10 centre a grey disc; smoke over the sparks at full opacity from age 0; ramp fades in over 0.1 s | TUNING.md lines 29–33; `fireball_impact.tscn` 44–46; commit 35a1f70 |
| B12 | 86 → 175, 144 → 230; frame 12 −5 % vs −33 %; one step older; brighter, kept | TUNING.md lines 35–39 |
| B13 | wall shot bursts at the screen edge; walks, jumps, two hits on the wolf; clicks about every 0.37 s, overlapping instances | capture (frames 86–92, 120–281, 311, 333, 384–496); CHANGE-BRIEF.md A4 |
| B13 | how it reads in play judged by the author | TEST-REPORT.md "Human checks" |
| B14 | trail job; first frame, 60–80 px at 260 px/s, fade within 0.3 s; turbulence and sphere emission | CHANGE-BRIEF.md lines 80–82, 86–88 |
| B15 | shape 1 = sphere, radius 3; direction (−1, 0); turbulence strength 1, scale 2, influence 0.1–0.2 | `fireball_trail.tscn` 25–27, 36–40 |
| B15 | brief called it world space; probe: follows rotation; gravity world space | CHANGE-BRIEF.md revision 2026-11-06 (7957614); TEST-REPORT.md "Trail direction" (e174c96) |
| B16 | carrier 260 px/s from frame 10, stops at 40; ~71 px at frame 30; 4–6 px tall, a third of the intent; dots every 8.7 px with gaps | `previews/fireball_trail_preview.gd`; TUNING.md Effect B r1 entry (Claude's reading of r0) |
| B17 | wanted thicker or brighter; ramp must match Sparks; curve 1→0 to 2→0, max value 2, curves clamp to 1 | TUNING.md (in-game check, r1); CHANGE-BRIEF.md (Effect B ramp "same as Sparks"; revision "Effect B r1 kept"); `fireball_trail.tscn` 16–17; commit cc1f2f2 |
| B18 | prediction 8–12 px continuous; every r0 pixel still lit; head 11–13 px; frame 40 tripled; gaps 1–3 px behind; thicker and brighter, kept | TUNING.md Effect B r1 entry |
| B19 | right shot times out after 2 s and fades in place; left shot trails to the right; Esc freezes, second Esc resumes | capture (frames 623–683, 706–740, 765–873); `fireball.gd` 7, 27–29 |
| B19 | in the state test, a pause after an impact held the fading trail; freed 0.3 s of game time later | TEST-REPORT.md line 21 (B2 + B3); `logs/test_fireball_trail_*fps.log` |
| B20 | the author converted a scratch process material; line 139 picks the speed between min and max (90, 160); 311 and 324 start the force from gravity and add it times delta (300) | TEST-REPORT.md "The process shader"; `particles_generated.gdshader` 139, 311, 324; `fireball_impact.tscn` 29–31 |
| B21 | 54 and 32 configuration checks; state tests with real input at 30/60/144: 14 and 20, zero failures; nine earlier suites kept their counts | TEST-REPORT.md lines 14–21 |
| B22 | a1: Godot 3 name, a Vector2 pair in 4.7, dropped silently, still fires at 0–160, exit 1 with two failures; a2: lifetime 0.6, exit 1 | TEST-REPORT.md lines 18–19; commit ab0784c |
| B23 | control < 4 µs; off ~240; A +8.2 own; B +25.1 own; within spread; dry run | TEST-REPORT.md lines 51–60 |
| B24 | Update GPUParticles absent / 0.01 / 0.09 ms; budgets 0.5 and 0.3 ms, ~4 % and ~33 %; vsync off ~1000 FPS, under 1 % apart | TEST-REPORT.md lines 62–73 |
| B25 | what no headless run shows; pit, ground cap, walls | TEST-REPORT.md lines 34–42, 94–96 |
| B26 | three agent mistakes: frame timing (frame 12), head size for the whole trail, cost script timing itself (+41 / +81 µs) | FRICTIONAL.md entries 10, 13, 14 |
| B27 | frame 20 overruled; open: beads at 8.7 px, vsync-off ~1000, hidden emitter, _spent guard; next step proposed by the film | TUNING.md line 23; FRICTIONAL.md entry 9 and "Still open"; README.md "Known limitations" |
| B28 | contributions; textures written by code; revision 3c37fe0 | FRICTIONAL.md "Human and AI contributions"; SOURCES.md; ATTRIBUTION.md; `git log` |
| B29 | built / measured / judged / unknown | the beats above (each line restates sourced claims) |
| B30 | the suggested prompt | PROMPTS.md (proposed by this film; targets README.md's untested `_spent` guard) |
