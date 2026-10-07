# TEST-REPORT — walker-magic

> Draft — filled in step by step while the slice is built; completed at S8. Engine: Godot 4.7.2-stable (win64).

## Playtest notes (human)

### Playtest 1 — 2026-10-06, after S2 (source revision `2667fc9`)
- **Who / how:** the author, playing with the keyboard in the 1280x720 window (640x360 viewport, 2x).
- **Covered:** running and turning, full and short jumps, clearing the pit at a run, walking into the pit, the 1.2 s reload, camera follow, readability against the cave.
- **Result:** movement, jump height, the pit and the 1.2 s reload all feel fine; the camera follows smoothly; the mage stays readable against the cave. No changes needed.
- **Not covered yet:** cast, wolf, exit, HUD and fail text, pause, mute, sound (later steps).

### Playtest 2 — 2026-10-06, after S3 (source revision `5156280`)
- **Who / how:** the author, keyboard and mouse in the 1280x720 window.
- **Covered:** casting in every direction (up, behind her, down into the ground), turning to cast behind her while running, rapid clicking, casting mid-jump, finding the crosshair.
- **Result:** fireballs go where the crosshair is in all directions; turning to cast behind her feels natural; the 0.35 s cooldown and the 260 px/s fireball speed feel right; the crosshair is easy to see; the cast pose looks fine mid-jump. No changes needed.
- **Not covered yet:** wolf, exit, HUD and fail text, pause, mute, sound.

### Playtest 3 — 2026-10-07, after S4 (source revision `40595ce`)
- **Who / how:** the author, keyboard and mouse in the 1280x720 window.
- **Covered:** approaching the wolf, reacting to the growl, taking lunge hits, knockback, defeating it with two fireballs, losing all 5 HP.
- **Result:** the 0.5 s growl gives enough time to react; the lunge feels fair and only hits on visible contact; the knockback reads clearly; the white flash and the down image read as defeated; the 36 px wolf reads as a threat next to the 64 px mage.
- **Issue observed:** HP 0 feels abrupt, because there is no HP display yet. Addressed in S5 (HUD hearts and the "Out of HP" text).
- **Not covered yet:** exit, HUD and fail text, pause, mute, sound.

## Automated checks

| Check | Command (from the project folder) | Result | Revision |
|---|---|---|---|
| Player states, facing, jump, pit, collision vs sheet | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_player.gd` | `WALKER TESTS: 11 checks / 0 failures` | `2667fc9` |
| Cast: spawn at the crystal, aim, facing, walls, held and rapid input (real `Input`) | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_cast.gd` | `WALKER TESTS: 11 checks / 0 failures` (held 2 s: 1 cast; tapping 2 s: 6 casts, cooldown 0.35 s) | `5156280` |
| Wolf: patrol, 0.5 s growl telegraph, lunge, hurt + knockback + blink, HP 0, flash, down image, removal, one defeat for two same-frame fireballs | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_wolf.gd` | `WALKER TESTS: 13 checks / 0 failures` | `40595ce` |
| Flow: HUD hearts, fail texts, exit and Cleared once, input stops after clear, R restart only after clear, Esc pause/resume, no pause after fail or clear | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_flow.gd` | `WALKER TESTS: 14 checks / 0 failures` | S5 commit |

Measured during S5: the code-drawn exit's brightest pixel is L* 89.0, below the hair base (L* 91.7) and highlight (L* 97.3), so the hair stays the brightest shape on screen (pillar 3, CHANGE-BRIEF failure case 3); the margin is small and is a human check in playtest 4.
