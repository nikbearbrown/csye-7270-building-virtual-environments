# Plan for prompt-2 — the screen-glow driver and its test

**How this plan was made:** `claude -p` could not log in on this machine, so, as the assignment allows ("run it interactively in claude"), my main interactive Claude Code session (Claude Opus 5.5) took `prompt-2.txt` unchanged as its instruction, read CLAUDE.md, CHANGE-BRIEF.md and the files below, and wrote this plan without editing anything. That session already knew the project from earlier work, so this run does not test whether CLAUDE.md alone is enough. I approve or change each step before it is implemented.

Read: `CLAUDE.md`, `CHANGE-BRIEF.md`, `godot/shaders/pad_base_light.gdshader`, `godot/items/tablet/tablet_device.tscn` and `.gd`, `godot/characters/human/humanoid/humanoid.gd` and `.tscn`, `godot/characters/human/player/player_controller.gd` and `player.tscn`, `godot/characters/character_intent.gd`, `godot/base.tscn`, `godot/project.godot`, `godot/tests/a3_asset_check.gd`, `scripts/run-test.sh`.

The shader is not touched. If it could not meet the spec I would stop and say so; it can.

## Step 0 — the material (already done, nothing to write)

The `Screen` node already has a `ShaderMaterial` using `res://shaders/pad_base_light.gdshader` with `resource_local_to_scene = true` (`godot/items/tablet/tablet_device.tscn` lines 10–15 and 31), set up by the human in the editor. CLAUDE.md says an agent does not rework it. The test (Step 3) only asserts it.

## Step 1 — the screen side: `godot/items/tablet/tablet_device.gd`

- `@export_range(0.0, 1.0) var light_strength_percentage: float = 0.39` — the screen-on strength (spec: "Screen-on strength").
- `const SCREEN_LIGHT_PARAM := &"pad_light_data"` — the uniform name, written once.
- `func set_screen_lit(lit: bool) -> void` — sets `pad_light_data` on **this tablet's own** screen material to `light_strength_percentage` when lit, `0.0` when not. Presentation only; it decides nothing.
- Update the stale doc comment on lines 21–22 (it still says every tablet shares one material).

## Step 2 — the decision: `godot/characters/human/humanoid/humanoid.gd`

- One presentation member `var _tablet_screen_lit := false` (it is "what the screen shows", not game state).
- One function `_update_tablet_screen()`, called at the end of `_update_tablet_visual()` every physics frame:
  - `_tablet_hold == NONE` → not lit (at once, the same frame the state changes);
  - else, the tablet has arrived (`_tablet_move_progress == TABLET_MOVE_DONE`) → lit;
  - else (still moving) → keep the previous value.
  Keeping the previous value is what makes ONE_HAND ↔ TWO_HAND stay lit while the tablet moves between the two hand slots, and keeps it dark while it comes off the hip.
- It reads `_tablet_hold` and the move progress and writes neither (code rule 5); the state machine and its timings are unchanged.
- It calls `_tablet.set_screen_lit(_tablet_screen_lit)`; `_tablet` is this body's own tablet, so another character's screen is never touched.

## Step 3 — the test: `godot/tests/screen_glow_check.gd` (new, `extends SceneTree`)

It loads `godot/base.tscn` (the real player) and instances a second `humanoid.tscn` that is never given input. A sampler node with `process_priority = 1000` reads `pad_light_data` of both screens in `_process()` every frame and records it with the frame's game time. Tab is pressed and released with `Input.parse_input_event()` (real input through `PlayerController`), never by calling `_update_tablet_screen()` directly.

| # | Assertion | Spec rule it covers |
|---|---|---|
| 1 | `get_shader_uniform_list()` has `cold_white` (Color) and `pad_light_data` (float, range hint `0.0,1.0`) | Shader parses; uniform names and types (both mutations) |
| 2 | From the shader **source text**: `cold_white` has `source_color` and default `vec4(0.902, 0.969, 0.969, 1.0)`; `pad_light_data` default `0.0` | Uniform table; failure case 2 |
| 3 | The `Screen` material is a `ShaderMaterial` with that shader path and `resource_local_to_scene` true; the two bodies' materials are different objects | Several instances; failure case 1 |
| 4 | Before any input, both screens read 0.0 | Default / NONE is dark |
| 5 | Short press (NONE → ONE_HAND): 0.0 on the state-change frame and until arrival; first 0.39 at 0.35 s ± one frame period after the state change | Value when the state begins; how long; failure case 5 |
| 6 | Long press (ONE_HAND → TWO_HAND), then short press (TWO_HAND → ONE_HAND): never 0 on any frame across both switches | Retrigger ① (ignore); failure case 3 |
| 7 | Long press (ONE_HAND → NONE): 0.0 on the same frame the state changes | Value when the state ends |
| 8 | Short press out, short press back after 0.1 s: 0.39 never appears | Ends before reaching the hand; failure case 6 |
| 9 | Take out, put away, take out again mid-way: lit again 0.35 s ± one frame after the last take-out | Retrigger ② (restart) |
| 10 | The second body's screen reads 0.0 on every frame of the whole run | Several instances; failure case 1 |
| 11 | With `Engine.time_scale = 0.5`: the delay is 0.35 s of scaled game time (0.7 s of frames) | `Engine.time_scale` rule |
| 12 | The lit value equals `light_strength_percentage` (0.39) | Screen-on strength |

Runs: `./scripts/run-test.sh screen_glow_check.gd 30`, `60`, `144`, and `./scripts/run-test.sh a3_asset_check.gd 60` (must stay 55 PASS).

**What the test proves:** the uniforms exist with the right names, types and hints; the driver sets the right value on the right frame through real input at three frame rates; each tablet's value is independent.

**What it cannot prove headless:** anything on screen (nothing is rendered). Human checks: captures at `pad_light_data` = 0.0 / 0.39 / 1.0 with pixels P1–P3 against the predicted table; a capture with 2.0 set from code for the `hint_range` question; normal play (take out, put away, switch hands) several times; `UpMarker` hidden before captures.

## Step 4 — mutations (after the test passes)

Delete one semicolon in the shader, then rename `pad_light_data` in the shader only; each time the test must exit 1; then restore the file byte for byte. These edits are made by the human, not the agent.

Nothing is committed by the agent.
