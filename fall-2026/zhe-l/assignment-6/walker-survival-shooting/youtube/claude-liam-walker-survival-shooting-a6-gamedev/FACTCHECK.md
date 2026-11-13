# Fact check — claude-liam-walker-survival-shooting-a6-gamedev

Every narrated claim, with the file it comes from. Paths are relative to `assignment-6/walker-survival-shooting/` in the course repository at `1828bb6b` unless marked. Checked by Claude Code (Opus 5.5) while building the film; the user watches the film before anything is committed.

| Beat | Claim | Source |
|---|---|---|
| B00 | Two effects, four tests, a cost script, eighteen fixture strips | `godot/effects/`; `godot/tests/test_{landing,light}_dust_{config,events,state}.gd` (4), `cost_effects.gd`; `captures/` holds 8 Effect A sets (r0, r1 × 4) and 10 Effect B sets (r0, r0-wired, r1, redesign, redesign-2 × 2) |
| B00 | Answer lines: 157 / 27 / 110 / 41 PASS; GPU +0.001 / +0.017 ms | `logs/test_*_60fps.log`; `logs/gpu_price.log` |
| B01 | Claude built from my brief; I judged every strip and change | FRICTIONAL Steps 2–5 "What I did" / "contributed"; TUNING verdicts |
| B02 | Effect A event = `landed` on the body; Effect B condition = ceiling lights | CHANGE-BRIEF "The job" (both effects); `humanoid.gd` line 29; `light_dust_listener.gd` |
| B03 | Peak 0.15 s, gone 1.6 s; ~1.5 capsules wide; two layers; restart, peak 25 | CHANGE-BRIEF Effect A Intent, Observable rules |
| B04 | Line 117 amount 24, 119 one_shot, 121 explosiveness 1, 124 process_material, 125 draw_pass_1 | `godot/effects/landing_dust.tscn` lines 113–125 (excerpt read from the file) |
| B05 | Triggered frame 10, first change frame 11; ring clear; dust warm dots, gone by 30; my verdict "grey cloud-like puffs, not dots" | TUNING r0 (my first verdict; Claude's reading) |
| B06 | Ankle rule broke → intent revised first; r1 quad 0.08 → 0.32; agent edited before approval (07:56:36 vs 07:57:19 UTC); approved after the fact, kept; prediction held at most frames incl. 30, missed at 50; tuning stopped at r1 on my in-game judgement | CHANGE-BRIEF revisions 2026-11-11 / 2026-11-12; TUNING r1 |
| B07 | Lines 112–113 landing test and emit; line 115 fix; Jolt left the player 2.7 mm in the floor on frame 1 and pushed it out on frame 2 → counted as landing; test caught it | `humanoid.gd` 109–115; TEST-REPORT Step 3 "First run" |
| B08 | Two single jumps, four rapid jumps (inside the 1.6 s lifetime), no pile-up | `capture/landing-run-02.log` (landings at ticks 118, 268, 398, 458, 518, 578; 60 ticks = 1.0 s apart); clip `media/B08.mp4` |
| B09 | restart() on both emitters; `emitting = true` would not restart a live one-shot burst | `landing_dust_trigger.gd` 38–41 and its doc comment; TEST-REPORT Step 3 mutation |
| B10 | Second landing frame 25, 0.5 m away; old gone at 25; new ring at 27; never returns; `emitting = true` → 22 PASS, 5 FAIL | TUNING r0 reading (retrigger); TEST-REPORT Step 3 mutation |
| B11 | First intent: under one light; settled on first frame, frozen paused, gone hidden/off; revised to whole room, lit | CHANGE-BRIEF Effect B; revision 2026-11-12 |
| B12 | Box emission (line 12), offset (13), turbulence (25; settings to 29), ramp (24; gradient lines 4–5), ADD + per-pixel (45–46), preprocess 6 (62) | `godot/effects/light_dust.tscn` |
| B13 | r0 150 specks ≈ 115 px; my words (size should vary; too dense); r1 150 → 90, agent proposed first; predicted ~70 (55–85), measured 74; kept | TUNING Effect B r0, r1 |
| B14 | Had to walk up to a light; asked for all at once; redesign, not tuning; 3000 too dense and bright; 900 half brightness; then 1300 | TUNING redesign; CHANGE-BRIEF redesign revisions |
| B15 | Lights on: show and exactly one restart; off: hidden, emitting false; listener only reads the lights | `light_dust_listener.gd` 43–51 and header |
| B16 | Off → gone that frame; on → spread at once; paused frozen; hidden gone; shown full at once | `capture/lights-film-01.log`; pixel checks in CAPTURE.md §2; clip `media/B16.mp4` |
| B17 | I converted Effect B's material in the editor; line 261 × emission_box_extents (7, 1.3, 4.5); line 263 + offset (0, 0.15, 3.2); 14 × 9 m centred on the room | TEST-REPORT "The process shader"; `godot/shaders/particles_generated.gdshader` 257–264; CHANGE-BRIEF redesign |
| B19 | Line 253 colour × ramp at age, every frame; ramp stops 0, 0.6, 0.15, 0.9…; gravity lines 397 / 410; gravity zero in both | shader 251–255, 397, 410; `light_dust.tscn` line 5; both scenes `gravity = Vector3(0, 0, 0)` |
| B20 | f11 / f40 same density, specks differ; f46 = f54; f61 none; f66 full; f71 none | TUNING redesign-2 reading; `fig_b_timeline.png` |
| B21 | ClassDB name check first; values compared with the brief; 44 names | `test_landing_dust_config.gd` 100–106; TEST-REPORT ("44 property names") |
| B22 | 157 / 27 / 110 / 41 at 60 fps headless; real keys Space and D, S and F | logs; TEST-REPORT |
| B23 | Mutation 1: no engine error; Vector2 editor-only property (type 5, usage 12); min 0.6 → 0.0; mutation 2 amount 30; both 156 / 1, exit 1 | TEST-REPORT mutations; `logs/mutation_*.log` |
| B24 | Frame = gap between two process frames; 300 frames, 3 repeats, round-robin; empty and 10,000-CPU controls | `cost_effects.gd` 102–111; TEST-REPORT Step 7 |
| B25 | 0.0041 / 1.8764 ms; A +0.0057, B +0.0246 within noise; dummy renderer | `logs/cost_effects_60fps.log` |
| B26 | RTX 5070 Ti Laptop GPU, windowed, vsync off, lights on; B +0.017 ≤ 0.3; A ≈ +0.001 ≤ 0.2; 144 → about 1350 FPS with V | `logs/gpu_price.log`; TEST-REPORT GPU price and FPS; CHANGE-BRIEF budgets |
| B27 | Headless shows no pixels; A puffs reach ~0.23 m up, ~0.68 m out vs 0.2 / 0.6 box; next step enlarge | TEST-REPORT Use It item 3; README Known limitations |
| B28 | Caught: fixed seed missing (Step 2), dust on scene load (Step 3), edit before approval (Step 4); overruled: warm, flat bottoms, capsule hiding, 6–8 puffs not separate; "a human, not a mech" | FRICTIONAL Steps 2–4; TUNING r1 verdict |
| B29 | Human / AI split; textures none from outside (GradientTexture2D in the scenes); narration local Kokoro; revision 1828bb6b | README "What this assignment added"; SOURCES; FRICTIONAL contributions |

## Choices reused from Assignment 5 (not re-asked)
Greeting "Hola", the narrator line "Liam, narrating for Jonathan", the title = the slug, voice `am_onyx`.

## Known wording limits
- B02/B08 "the event is a new signal" — `landed` was added in Step 3 by the agent with my approval (CHANGE-BRIEF Boundaries).
- B16's F presses are scripted key events through the InputMap (said in the narration and labelled on screen).
- `capture/play_capture.gd` is the final version of the capture script; `landing-run-02` was taken with an earlier revision that differed only in the lights-shot code (the film camera and the fixed 1 s walk were added afterwards).
- `light_dust_listener.gd`'s header and `test_light_dust_state.gd` still say "under ceiling light 1"; after the redesign the node stays there and the box is moved by `emission_shape_offset`. The film does not quote those comments.
