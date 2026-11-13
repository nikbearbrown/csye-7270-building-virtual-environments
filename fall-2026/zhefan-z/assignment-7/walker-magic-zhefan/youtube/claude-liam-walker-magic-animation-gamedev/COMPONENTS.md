# COMPONENTS — what the film explains, and where

Scope: what Assignment 7 added to `walker-magic-zhefan` (files changed between `027a0ab`, the copy of the Assignment 6 project, and `f860fed`). The machine-readable version, with every file's hash and every exclusion, is `gamedev-evidence.json`.

| Component | Files | Beats | Code → result |
|---|---|---|---|
| **Clip 1, the run** | `features/player/player.gd` (`_set_state()`, `_play()`), `features/player/player.tscn` (nine state clips; `run`), `assets/sprites/mage/mage_run_cycle_sheet.png` (r2) and `mage_run_sheet.png` (r0) with their imports, `tools/clean_run_cycle.py`, `tools/pack_run_sheet.gd`, `tools/make_contact_far_legs.gd` (a rejected attempt), `design/a7/` Gemini inputs and outputs, `design/IMAGE-PROMPTS-from-chat.md`, `previews/run_preview.*` | B03, B09–B13, B21, B22 | B10 `player.tscn` 93–101 → B11 the run cell by cell (scripted input); B12 `player.gd` 143–154 → B13 land, run, cell 0 (scripted input) |
| **Clip 2, the lunge rig** | `features/wolf/wolf.gd` (`_play()`, `take_damage()` growl cancel), `features/wolf/wolf.tscn` (rig under Facing; `patrol`, `lunge`, `dead`), `features/wolf/lunge_afterimage.gd`, `previews/lunge_preview.*` | B04–B08, B15, B25 | B07 `wolf.tscn` 99–110 → B08 read-back + logged poses (fixture); B15 `wolf.gd` 152–163 → B16 the pin timeline |
| **Motion reference** | `design/a7/reference/` (Muybridge plates 707 and 60, SOURCES.md) | B06, B09 | — (reference images beside the clips) |
| **Torches and embers** | `effects/cave_lights.tscn` (flicker clip), `effects/embers.tscn`, `game/main.tscn` | B23–B25 | B23 `cave_lights.tscn` 19–30 → B24 the flicker measured in the capture |
| **Pin and tests** | `tests/test_pin_behaviour.gd`, `test_anim_edges.gd`, `test_clip_run.gd`, `test_clip_lunge.gd`, `test_clip_flicker.gd`, `test_anim_structure.gd`, `test_afterimage.gd`, `anim_checks.gd`, `probe_growl_cancel.gd`, the capture harnesses `capture_look.gd`, `capture_lunge.gd`, `capture_run_game.gd`, `tools/make_figures.py` | B08, B11, B13, B14, B16–B20 | — (recorded results and figures, labelled) |

Input → state → output, traced once end to end: B05 (in play) and B15 → B16 (code and pin). A left click (input) makes `Player.cast()` spawn a fireball; when it reaches the wolf during GROWL, `take_damage()` lowers HP, enters RECOVER and seeks the `lunge` clip to frame 52 (state); on screen the wolf never lunges, its hitbox never arms, and the hit tick shows clip frame 53 (output: capture frame 1549; the pin's `hit_growl` from tick 24).

Two clocks, shown: both AnimationPlayers on the physics callback (`callback_mode_process = 0`, `process_physics_priority = -1`), the same tick the state machines read (B12 notes, B18); the frame-clock removal timer after death (B20).

Not explained here (excluded, unchanged in Assignment 7): the 2D game's movement, the fireball and both A6 effects, the hurt tint, the level, audio, HUD, the A3 prop room, the A5 shaders and materials, earlier tests, and the earlier films' records — see the earlier films in `docs/a2`, `docs/a3`, `docs/a5` and `docs/a6`.
