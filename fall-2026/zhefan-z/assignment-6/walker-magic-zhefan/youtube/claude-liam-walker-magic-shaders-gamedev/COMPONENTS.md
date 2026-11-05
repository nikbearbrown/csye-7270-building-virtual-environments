# COMPONENTS — walker-magic Assignment 5 gamedev film

Scope: what Assignment 5 added to `walker-magic-zhefan`, from the copied Assignment 3 project (`60fe5d7`) to the game source revision shown, `40c42f5`. Everything else in the project is unchanged and explained in the earlier films (`docs/a2/youtube/`, `docs/a3/youtube/`); those files are exclusions with that reason in `gamedev-evidence.json`.

| Component | Files | Beats | Code → result |
|---|---|---|---|
| **a5-hurt-tint** — canvas_item shader, presentation-only driver, the player's local-to-scene ShaderMaterial | `shaders/hurt_tint.gdshader`, `features/player/hurt_tint_driver.gd`, `features/player/player.tscn`, `tests/test_hurt_tint.gd` | B03–B08, B20–B21 | B04 (shader 1–7) → B05 (controlled captures); B06 (driver 6–15) → B07 (recorded test results); B20 (shader 1–4) → B21 (two pipelines) |
| **a5-frosted-rock** — spatial shader with three samplers, two materials, Rock 01 textures with explicit import settings, the compare scene | `shaders/rock_frost.gdshader`, `assets/materials/mat_rock_{dry,frosted}.tres`, `assets/textures/rock_01/*` (+ `.import`), `showcase3d/material_compare.tscn` | B09–B11, B14–B19 | B09 (frosted .tres 8–17) → B10; B14 (samplers 15–19) → B15 (recorded data checks); B16 (frost mask 30–35) → B17; B18 (interface 3–12) → B19 |
| **a5-hint-experiment** — one grey PNG, two samplers, two unshaded quads | `shaders/hint_experiment.gdshader`, `assets/materials/mat_hint_*.tres`, `assets/textures/hint/*`, `showcase3d/hint_experiment.tscn`, `tools/write_hint_png.gd` | B12–B13 | B12 (shader 1–14) → B13 (hint_quads.png) |
| **a5-generated-shader** — the editor's StandardMaterial3D conversion | `shaders/standard_generated.gdshader` | B22 | source view (lines 7, 19 beside rock_frost 16, 17), not a code beat |
| **a5-tests-and-captures** — material test and audit, curl check and calibration, inspection, F9–F12 capture scenes | `MATERIALS.md`, `tests/test_materials.gd`, `normal_map_check.gd`, `calibrate_normal_check.gd`, `inspect_rock_surfaces.gd`, `tests/capture/*` | B23–B24 | recorded results (TEST-REPORT.md) |

**Why it was built this way, and one trade-off each**
- *Hurt tint:* the driver only reads `Player` and writes one uniform, so game logic is untouched (CHANGE-BRIEF.md §2, Boundaries). Trade-off: a wolf contact during the window cannot restart the tint (R5, "Ignore"), because a restart would need a game-logic change.
- *Frosted rock:* the material lives in scene overrides, so `rock.glb.import` and the Assignment 3 test stay as they were (revision 2026-10-27). Trade-off: the frosted rock appears only in the 3D showcase, not in the 2D level (README.md).
- *Hint experiment:* one file, two samplers, unshaded under a Linear tonemap, so the hint is the only variable. Trade-off: it isolates the hint, not real lighting.
- *Tests:* headless checks pin names, values, hints, imports and the driver's numbers. Trade-off: the dummy renderer draws nothing, so the look needs the captures and the author's eyes.

**One complete input → state → output trace:** a wolf's lunge lands (input) → `Player.invulnerable` set to 1.0 (`player.gd:155`, state) → each frame the driver writes `invulnerable / INVULNERABLE_TIME` into the material (`hurt_tint_driver.gd:14–15`) → line 7 of the shader mixes the sprite toward red by that value (output; first sampled value 0.9833, TEST-REPORT.md R1; the pixel arithmetic shown with controlled values in B05).

**Tests:** given their own beats (B07, B15, B23, B24), including the three mutations and what no headless run can show.
