# COMPONENTS — what the film explains, and where

Scope: what Assignment 6 added to `walker-magic-zhefan` (files changed between `41504c6`, the copy of the Assignment 5 project, and `3c37fe0`). The machine-readable version, with every file's hash and every exclusion, is `gamedev-evidence.json`.

| Component | Files | Beats | Code → result |
|---|---|---|---|
| **Wiring** | `features/fireball/fireball.gd` (explode, `_release_trail`, the timeout), `features/fireball/fireball.tscn` (the trail child) | B02, B03, B04 | B03 `fireball.gd` 43–49 → B04 gameplay, scripted input |
| **Effect A, the impact** | `effects/fireball_impact.tscn`, `effects/fireball_impact.gd`, `assets/textures/fx/` (spark, smoke, imports, ATTRIBUTION), `tools/write_fx_textures.gd` | B05, B07, B08, B09, B11, B12, B13 | B08 `fireball_impact.tscn` 25–36 → B09 strip r0; B11 44–46 → B12 r0 against r1 |
| **Effect B, the trail** | `effects/fireball_trail.tscn` | B14–B19 | B15 `fireball_trail.tscn` 25–38 → B16 strip r0; B17 15–18 → B18 r0 against r1 |
| **Previews (fixtures)** | `previews/fireball_impact_preview.*`, `previews/fireball_trail_preview.*` | B09, B10, B16 | — (they made the strips) |
| **Generated process shader** | `shaders/particles_generated.gdshader` | B05, B20 | — (source view, lines 139, 311, 324 beside the brief's settings) |
| **Tests and price** | `tests/test_fireball_{impact,trail}{,_config}.gd`, `tests/probe_trail_direction.gd`, `tests/cost_effects.gd`, `previews/effect_load.gd`, `previews/gpu_price.*` | B06, B21, B22, B23, B24 | — (recorded results, labelled "not a render") |

Input → state → output, traced once end to end: B03 → B04. A left click (input) makes `Player.cast()` spawn a fireball whose child trail emits (state: the fireball exists); on `body_entered`, `explode()` instances the impact into `Main` and releases the trail (state change); on screen the burst appears where the fireball was and the trail fades in place (output).

Not explained here (excluded, unchanged in Assignment 6): the 2D game, wolf, level, audio, HUD, the A3 prop room, the A5 shaders and materials, and the earlier films' records — see the earlier films in `docs/a2`, `docs/a3` and `docs/a5`.
