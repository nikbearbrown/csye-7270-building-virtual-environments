# COMPONENTS — Sparks and Dust for Walker Rudy.

One Godot project, `game/`, one ledger: `checks/game/gamedev-evidence.json` (see `tools/make_evidence.py`). `.uid` identifiers and `.godot/` are left out by the contract.

## `game/` at `d0ed415` — 19 files in components, 117 excluded

| Component | Files | Beats | What it does |
| --- | ---: | --- | --- |
| `slash-sparks` | 3 | B02, B03, B04, B05, B06, B07, B08, B09, B10, B11 | Effect A, SlashSparks: effects/slash_sparks.tscn, a Node2D root with two GPUParticles2D emitters, Flash (1 particle, 0.12 s) and Sparks (28 streaks, 0.45 s, one shot, explosiveness 1.0), each with a ParticleProcessMaterial and a GradientTexture2D with a dark rim; local_coords off. previews/slash_sparks_preview.gd/.tscn is the fixture the strips were captured from: Level 1 frozen, a still Rudy, seeded bursts on frames 10 and 20. |
| `run-dust` | 3 | B02, B12, B13, B14, B15, B16, B17, B18, B19, B20, B21, B22 | Effect B, RunDust: effects/run_dust.tscn, one GPUParticles2D (40 puffs, 0.5 s, a steady stream) with a box emission shape, velocity 80–160 px/s up, and damping 120–180 px/s², the feature Effect A does not use; local_coords off makes the trail, trail_enabled stays false because the Compatibility renderer does not draw it. previews/run_dust_preview.gd/.tscn is the strip fixture: the emitter and Rudy's sprite move at 560 px/s from frame 10 and stop at frame 40. |
| `effects-driver` | 4 | B02, B09, B10, B11, B18, B20, B21, B22 | effects/effects_driver.gd, after Rudy in app/main.tscn: each physics tick it starts a new SlashSparks burst on the true → false edge of Rudy's SwordHitbox/Shape.disabled, placed on the hitbox and mirrored with facing, and switches RunDust's emitting with the run condition (mode PLAY, on the floor, |velocity.x| > 1, visible in the tree), keeping it at his soles. content/rudy/rudy.gd owns the event and the condition and is unchanged; project.godot names GL Compatibility. |
| `process-shader` | 1 | B03, B23 | shaders/particles_generated.gdshader: the particles shader Godot 4.7.2's editor generated from a copy of Sparks' ParticleProcessMaterial, saved by shuai-z; nothing uses it. Line 139 picks each speed between the velocity uniforms, line 311 starts the force from gravity. |
| `effects-tests` | 7 | B24, B25, B26, B27, B28, BVD1 | The new headless tests: tests/test_slash_sparks_config.gd (108 checks) and tests/test_run_dust_config.gd (61) compare every setting with the brief and scan for Godot 3 names; tests/test_slash_sparks_state.gd/.tscn and tests/test_run_dust_state.gd/.tscn (14 each) run the real Main through input actions; tests/cost_effects.gd measures the headless CPU price against an empty-scene control. |
| `vsync-debug` | 1 | B27 | app/vsync_debug.gd, the VsyncDebug node last in Main: F9 turns vsync off and on again, for the FPS fallback when the Visual Profiler reports no GPU time. |

| Code beat | Source | Result beat | Observed |
| --- | --- | --- | --- |
| B05 | `effects/slash_sparks.tscn:73–82` | B06 | Fixture captures (the preview, r0, 14 sparks, the same process settings): frames 10, 12, 15, 20, 30 and 50 against the brief's predictions, with Claude's reading and shuai-z's first verdict. |
| B07 | `effects/slash_sparks.tscn:107–115` | B08 | Fixture captures r0 and r1 at frames 12, 15 and 20: Claude predicted 16–20 streaks, 18–22 with halved gaps, and 3–5 specks of the first burst; r1 shows about 14–18, about 20, and about 8, higher. shuai-z kept it. |
| B09 | `effects/effects_driver.gd:35–46` | B10 | The real Main in Godot 4.7.2 Compatibility, Movie Maker at 3840×2160 and 30 fps, scripted input: one cut (burst at frame 214); five cuts as fast as the game allows, two bursts alive at once on frames 250–253, 260–263, 270–273 and 280–283; two cuts facing left, spraying left. Then labelled one-third-speed replays, enlarged 2× around Rudy, of the single cut, the five cuts and the two left cuts. |
| B17 | `effects/run_dust.tscn:31–41` | B18 | The real Main, Movie Maker at 3840×2160 and 30 fps, scripted input: Enter on the title, the run to the right from frame 61 with RunDust emitting, the jump over the first spikes and over the first goblin, the sword and the stop at frame 190; then labelled half-speed replays, enlarged 1.5×, of frames 60–99 (the trail building) and 182–205 (the stop, the trail emptying). |
| B19 | `effects/run_dust.tscn:52–63` | B20 | One-third-speed replays of the same capture: the jump over the first spikes (RunDust off from frame 97 while airborne, on again at the landing on frame 118), the trail already laid staying in world space as the camera follows; the same over the first goblin (off at 136, on at 157). Frames 85–164 first at 1.0×, then the two replays, enlarged 1.5×. |
| B21 | `effects/effects_driver.gd:52–59` | B22 | The real Main, scripted input, with two labelled half-speed replays enlarged 1.5× (the start at frame 356, the stop at 422): running left from frame 356 with RunDust emitting; Esc at frame 376, paused frames 376–411 with the puffs frozen and still drawn; the resume, the run carrying on, the stop at 422 and the trail emptying; a turn, a run and a jump with a cut at the top (no puffs in the air), and the landing. |
| B24 | `tests/test_slash_sparks_state.gd:181–190` | B25 | Recorded headless output through scripts/run-test.sh at pinned frame rates: configuration tests 108 and 61 PASS, state tests 14 and 14, the existing 141 and 15; S7, S8 and D11 lines shown. |

**Excluded, with the reason recorded in the ledger:**

- 117 file(s): `app/main.gd`, `app/system_keys.gd`, `content/goblin/frames/ENEMY-GOBLIN-SQUASH.png`, `content/goblin/frames/ENEMY-GOBLIN-SQUASH.png.import`, `content/goblin/frames/ENEMY-GOBLIN-WALK-A.png`, `content/goblin/frames/ENEMY-GOBLIN-WALK-A.png.import` and 111 more. The 2D game as Assignment 5 left it (tag a5, 9bd96c5a), copied unchanged into assignment-6/game; Assignment 6 changed none of it, and this film covers the layer Assignment 6 added. The existing 141 checks in tests/checks.gd and the 15 in tests/invulnerable_tint_checks guard it, and pass.

## Shown on still cards and figures rather than as Workbench excerpts

- `game/shaders/particles_generated.gdshader` lines 10–11, 43, 139 and 311 beside the brief's velocity and gravity rows (B23), and `slash_sparks.tscn` lines 108, 79, 109 with the shader's line 311 (B03): `tools/make_stills.py` reads the lines from the files.
- `CHANGE-BRIEF.md` sections 2 and 3, The intent (B04, B12): the timing-phase bullets are read from the file; the other rows are labelled as a summary.
- Every number the strip cards quote from `TUNING.md` (B06, B08, B13–B16) is asserted to be in it by `tools/make_stills.py`.

