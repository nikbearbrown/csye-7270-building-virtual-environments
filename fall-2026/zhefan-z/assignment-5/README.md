# walker-magic — Assignment 5: shaders, materials and the Godot shading language

Zhefan Zhang (zhefan-z), CSYE 7270 Fall 2026. Game: *walker-magic*, a 2D side-scroller in which a mage crosses a cave and casts fireballs at a wolf, plus the 3D prop room from Assignment 3. Starting point: my Assignment 3 project, unchanged (see `SOURCES.md`).

**Engine:** Godot 4.7.2-stable, renderer Forward+ (the engine default; `project.godot` sets none). Windows, Git Bash.

## Run it

- Open `walker-magic-zhefan/project.godot` in Godot 4.7.2 and press F5 for the game.
- Tests, from this folder in Git Bash, after `godot --headless --path walker-magic-zhefan --import` once:
  - `./scripts/run-test.sh test_hurt_tint.gd 30` (also 60 and 144)
  - `./scripts/run-test.sh test_materials.gd 60`
  - the seven earlier suites at 60: `test_player`, `test_cast`, `test_wolf`, `test_flow`, `test_audio`, `test_sound_triggers`, `test_a3_assets`
- Captures (real window): open `tests/capture/capture_hurt_tint.tscn`, `capture_hint.tscn` or `capture_rock_sweep.tscn`, press F6, then F9 (rock: also F10 to F12).
- 3D scenes: `showcase3d/material_compare.tscn` (dry and frosted rock), `showcase3d/hint_experiment.tscn`.

**Controls:** A/D or arrows to walk, Space/W/Up to jump, left mouse to cast a fireball toward the cursor, Esc to pause, R to restart, M and N to mute music and sound effects.

## What this assignment added

- **Hurt tint** (`shaders/hurt_tint.gdshader`, canvas_item, written by me): while the mage is invulnerable after a hit, her sprite is mixed toward red, fading from 1 to 0 over the 1.0 s window, on top of the existing blink. A presentation-only driver (`features/player/hurt_tint_driver.gd`) sets `intensity` from `Player.invulnerable`, and forces 0 on fail or clear.
- **Frosted rock** (`shaders/rock_frost.gdshader`, spatial, written by me): albedo sampled as colour, normal and roughness maps as data; the roughness map also decides where frost settles. Two materials, dry and frosted, from one shader, side by side in `material_compare.tscn`.
- **Hint experiment:** one 3×1 grey PNG sampled with and without `source_color` on two unshaded quads.
- **Language notes:** `LANGUAGE-NOTES.md`, with the shader Godot generates for a StandardMaterial3D annotated.
- Specification `CHANGE-BRIEF.md`, context `CLAUDE.md`, audit `walker-magic-zhefan/MATERIALS.md`, evidence `TEST-REPORT.md`, log `FRICTIONAL.md`.

## Known limitations

- The textured shader appears only in the 3D showcase scenes; the 2D level has no rock. The Assignment 3 prop room is unchanged, because putting the material behind Use External would have broken an earlier test (CHANGE-BRIEF revision 2026-10-27).
- `ice_roughness` (0.15) is a constant, not a uniform; `roughness_scale` does not move where frost settles.
- The imported roughness map is DXT1 (error up to 13 of 255); no blocking was visible in my captures.
- Two explanations are untested: why the GPU wrote the two x.5 channels one step lower, and why a pause shifts summed frame time by more than one physics step.

## Film

*A Red Flash, a Frosted Rock: Two Shaders for a Cave Mage*, 8:37.6, 3840×2160, 30 fps, narrated by Liam (AI).

- Link: https://drive.google.com/file/d/1kcRLbb-tBHbCoba332OigrF90URMO3-A/view?usp=sharing
- File: `claude-liam-walker-magic-shaders-gamedev.mp4`
- SHA-256: `412bff788d24c1513bcac7bc8a6797dab11f50b53302883e1e94275b76f1d69a`
- Game source shown: `40c42f5`. Film records (script, fact check, sources, checks, QC): `walker-magic-zhefan/youtube/claude-liam-walker-magic-shaders-gamedev/`. The MP4 is not in git.
