# TEST-REPORT — walker-magic

> Draft — filled in step by step while the slice is built; completed at S8. Engine: Godot 4.7.2-stable (win64).

## Playtest notes (human)

### Playtest 1 — 2026-10-06, after S2 (source revision `2667fc9`)
- **Who / how:** the author, playing with the keyboard in the 1280x720 window (640x360 viewport, 2x).
- **Covered:** running and turning, full and short jumps, clearing the pit at a run, walking into the pit, the 1.2 s reload, camera follow, readability against the cave.
- **Result:** movement, jump height, the pit and the 1.2 s reload all feel fine; the camera follows smoothly; the mage stays readable against the cave. No changes needed.
- **Not covered yet:** cast, wolf, exit, HUD and fail text, pause, mute, sound (later steps).

## Automated checks

| Check | Command (from the project folder) | Result | Revision |
|---|---|---|---|
| Player states, facing, jump, pit, collision vs sheet | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_player.gd` | `WALKER TESTS: 11 checks / 0 failures` | `2667fc9` |
| Cast: spawn at the crystal, aim, facing, walls, held and rapid input (real `Input`) | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_cast.gd` | `WALKER TESTS: 11 checks / 0 failures` (held 2 s: 1 cast; tapping 2 s: 6 casts, cooldown 0.35 s) | S3 commit |
