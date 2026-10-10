# COMPONENTS — walker-magic at 74c0443

> The film's component map. File-level coverage (153 files, 7 exclusions with reasons) is in `gamedev-evidence.json`, checked by `./art godot-gamedev --check` against a `git archive` of `74c0443`.

| Component | What it is | Data in → what changes → what the player sees | Beats | Trade-off |
|---|---|---|---|---|
| Design documents | CONCEPT, CHARACTER-SHEET, STORYBOARD, CHANGE-BRIEF | Pillars, 64 px size, palette, 14×44 collision, predicted failures → the targets every asset is checked against | B04, B05, B12 | Written before generation, so some numbers were revised (append-only revisions) |
| Character art pipeline | Gemini outputs, `tools/clean_sprites.py` + `sprites.json`, cleaned sprites, EDIT-LOG | 1920 px green-screen JPG → key, palette map in CIELAB, block-majority downscale, outline → 62×69 PNG on the sheet's palette | B06–B09, B12, B13 | A script makes every edit repeatable and logged, but scale is inferred from face width, a proxy |
| Player | `features/player/` | Input actions + `get_global_mouse_position()` → state machine, `TEXTURES[state]`, cast → one image per state on screen | B10, B11, B14 | No animation frames: readable at 64 px, but motion is coarse |
| Fireball | `features/fireball/` | `cast()` sets origin and direction → projectile, burst on hit | B14, B15 | — |
| Wolf | `features/wolf/` | Sees the player within 120×40 px → GROWL 0.5 s → LUNGE → flash, down image, removal | B15 | The telegraph is fair but brief; no growl sound in the slice |
| Level and environment | `features/level/`, `features/exit/`, cave art | Ground, pit kill zone, code-drawn exit → fail and clear events | B11, B13 | Exit drawn in code so it stays the second-brightest shape |
| Audio | `audio/audio_director.gd`, buses, five SFX, MUS-LOOP | Game signals → `_play(id)`; fail/clear stop the music; M/N mute buses | B16–B18, B20 | The director never decides game state, so muting cannot change play; tests prove triggers, not audibility |
| Game flow and UI | `game/`, `ui/`, `project.godot` | Keys → SessionInput (Esc, M, N) → pause, mutes; HUD hearts, labels, crosshair | B19, B20 | Bus mutes are global, so they persist across a restart |
| Tests | `tests/` | Headless suites with real `Input` events; `test_sound_triggers.gd` counts sound requests per event | B21, B22 | Dummy audio driver: no proof of what is heard |
| Project records | SOURCES, TEST-REPORT | Models, licenses, prompts, playtests | B23, B24 | — |

**Input → state → output trace (B10 → B11, B14 → B15):** a left click (`InputEventMouseButton`) → `_read_cast_pressed()` (`is_action_just_pressed`) → `cast(aim)` → `cast_fired` → fireball on screen and, through the AudioDirector, SFX-CAST.
