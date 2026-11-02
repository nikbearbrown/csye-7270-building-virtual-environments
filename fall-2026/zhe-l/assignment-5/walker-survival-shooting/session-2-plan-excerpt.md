# Session 2 excerpt — the `claude -p` run that planned the driver and test

**Labelled excerpt, not the full transcript.** I ran `prompt-2.txt` unchanged with `claude -p` in this folder. The raw stream-json transcript (`session-2-plan.jsonl`, about 225 KB) holds local absolute paths, which this repository must not contain, so it is kept locally and this excerpt is posted instead.

- Model: claude-opus-5-5
- Command: `claude -p "$(cat prompt-2.txt)" --model claude-opus-5-5 --permission-mode acceptEdits --allowedTools "Read,Glob,Grep,Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(ls:*)" --max-turns 40 --output-format stream-json --verbose > session-2-plan.jsonl` (tools scoped to reading; this round was for a plan only).
- Result: `success`, 13 turns, 121.7 s. It made 12 tool calls, all Read or Grep, and edited no file.
- What happened to this plan: the run finished on 2026-10-29 about five minutes before a second plan, `plan-2.md`, was written by Claude in my main working session. I had already chosen that route (option B) while this run was still going, so this plan was not read at the time. The driver I later wrote follows `plan-2.md`. Read afterwards, this plan proposes the same rule (dark when put away, lit on arrival at a hand slot, otherwise keep the previous value while moving), but puts the material handling in `humanoid.gd` instead of a `TabletDevice.set_screen_lit()` function.

## Tool calls

1. Read: `{"file_path": "godot/characters/human/humanoid/humanoid.gd"}`
2. Read: `{"file_path": "godot/shaders/pad_base_light.gdshader"}`
3. Read: `{"file_path": "godot/items/tablet/tablet_device.tscn"}`
4. Read: `{"file_path": "godot/items/tablet/tablet_device.gd"}`
5. Read: `{"file_path": "godot/characters/human/player/player_controller.gd"}`
6. Read: `{"file_path": "godot/tests/a3_asset_check.gd"}`
7. Read: `{"file_path": "godot/characters/human/humanoid/humanoid.tscn"}`
8. Read: `{"file_path": "godot/characters/human/player/player.tscn"}`
9. Read: `{"file_path": "scripts/run-test.sh"}`
10. Read: `{"file_path": "godot/characters/character_intent.gd"}`
11. Grep: `{"pattern": "tablet|Player|physics_ticks", "path": "godot/project.godot", "output_mode": "content", "-A": 5}`
12. Grep: `{"pattern": "node name=|instance=", "path": "godot/base.tscn", "output_mode": "content"}`

## The agent's final answer (unchanged)

I've read CLAUDE.md, the brief, the shader, the tablet and humanoid scenes and scripts, the player brain, the input map, the wrapper and the existing test. I haven't edited anything yet.

## Shader check

`godot/shaders/pad_base_light.gdshader` meets the spec as written: `spatial`, `unshaded`, `cold_white: source_color = vec4(0.902, 0.969, 0.969, 1.0)`, `pad_light_data: hint_range(0.0, 1.0) = 0.0`, and the exact `ALBEDO = mix(vec3(0.0), cold_white.rgb, pad_light_data);` line. I found nothing that blocks the plan, so I'm not stopping, and I won't touch any `.gdshader` file.

## Plan

### Step 0: give the screen a ShaderMaterial — no code needed
You already did this in the editor (`tablet_device.tscn` lines 10–15 and 31, with Local To Scene ticked). CLAUDE.md says an agent doesn't rework that, so I add nothing. The test checks it instead.

### Step 1: the driver (2 files, no change to the state machine)

**`godot/characters/human/humanoid/humanoid.gd`**: I add three members and one presentation function. It's called from `_update_visual()` right after `_update_tablet_visual(delta)`, so it runs on the same physics tick as the move progress it reads:

```gdscript
@export var light_strength_percentage: float = 0.39  # Screen-on strength written to pad_light_data once the tablet reaches a hand slot: 0 = dark, 1 = full cold white
var _screen_light := 0.0  # The value last written to this tablet's screen. Presentation, not game state (rule 5)
@onready var _screen_material: ShaderMaterial = _tablet.get_screen().get_surface_override_material(0) as ShaderMaterial  # This tablet's own screen material (Local To Scene)

## Sets this tablet's screen from the tablet state: dark on the hip, lit once the tablet has reached a hand slot.
## Reads _tablet_hold and the move progress only; never writes them (rule 5). Called by _update_visual() every physics frame.
func _update_screen_light() -> void:
	if _tablet_hold == TabletHold.NONE:
		_screen_light = 0.0  # Put away: switches off at once, without waiting for the hip
	elif _tablet_move_progress >= TABLET_MOVE_DONE:
		_screen_light = light_strength_percentage  # Arrived at a hand slot: on
	# Otherwise moving toward a hand slot: keep the value (lit stays lit between hands, dark stays dark until arrival)
	_screen_material.set_shader_parameter(&"pad_light_data", _screen_light)
```

How this one rule covers each spec case:
- **Dark until arrival:** taking the tablet out starts dark, and it lights on the arrival tick.
- **ONE ↔ TWO:** it keeps 0.39, so there's no frame at 0.
- **Taking it out again mid-way:** the move restarts, and it stays dark for the full 0.35 s.
- **Putting it away early:** it goes to 0 and never lights.
- **Pause:** physics doesn't tick, so the value holds.
- **`time_scale`:** inherited from the physics `delta`.

I put it on `Humanoid` because a separate node would have to read the private `_tablet_move_progress` and would run in `_process`, not on the tick where the progress changes.

**`godot/items/tablet/tablet_device.gd` lines 21–22**: I only rewrite the out-of-date comment to say Local To Scene gives each instance its own material.

### Step 2: new test `godot/tests/a5_screen_glow_check.gd`, then all runs

The test extends `SceneTree`, like the existing test.
- **Scene:** it instances `base.tscn`, which contains the real Player.
- **Second body:** it adds a second `humanoid.tscn` at another spot, driven by a stub brain in the test. The stub calls `apply_intent(CharacterIntent.new(), delta)` every physics frame, so that body's driver really runs but it never takes out its tablet.
- **Sampler:** a `Sampler` node with `process_priority = 1000` and `process_mode = ALWAYS`. Every frame, after all other `_process` calls, it adds up the game clock (`delta`) and the real clock (frames / fps). It reads `get_tablet_hold()` and `pad_light_data` on both screens, and it drives a timed script of real Tab key events (`Input.parse_input_event(InputEventKey)` with `physical_keycode = KEY_TAB`).
- **Timing:** "Change time" means the first sample where the hold changed, and "lit time" means the first sample where the value is 0.39. The tolerance is `1/fps`.

| # | Assertion | Spec rule |
|---|---|---|
| S1 | `get_shader_uniform_list()` holds exactly `cold_white` (TYPE_COLOR) and `pad_light_data` (TYPE_FLOAT, range hint `0.0,1.0`) | The shader parses; names and types are right |
| S2 | The shader source text has `shader_type spatial`, `render_mode unshaded`, `source_color` on `cold_white`, defaults `vec4(0.902, 0.969, 0.969, 1.0)` and `0.0`, and the exact ALBEDO line | Uniform defaults (not reported headless); failure case 2 |
| S3 | Each `Screen` override is a `ShaderMaterial` with `pad_base_light.gdshader` and `resource_local_to_scene == true`. The two bodies' materials are different objects. Exactly 2 materials in the tree use this shader (so the prop `tablet`, the tablet model and `UpMarker` don't) | Several instances; boundaries |
| S4 | `light_strength_percentage` defaults to 0.39 | Screen-on strength |
| D1 | Short press → ONE_HAND: the value is 0 on the change frame, and the lit time minus the change time is 0.35 ± 1/fps | Start value; 0.35 s at 30/60/144; failure case 5 |
| D2 | Long press ONE → TWO: every sample across the switch and the move is 0.39, never 0 | Retrigger ①; failure case 3 |
| D3 | Long press TWO → NONE: the value is 0 on the change frame | End value |
| D4 | While it's still moving back to the hip, a short press → ONE: dark until the full 0.35 ± 1/fps from this change | Retrigger ② (restart) |
| D5 | Lit → put away; take it out, then put it away 0.1 s later: 0.39 never appears for 0.6 s | Put away before arrival; failure case 6 |
| D6 | `Engine.time_scale = 0.5`, take it out: game time 0.35 ± 1/fps, real time 0.70 ± 1/fps (then restore 1.0) | `time_scale` |
| D7 | `paused = true` for 0.3 s while lit: the value doesn't change | Paused tree |
| D8 | On every sample, the second body's value is 0.0, and the value is only ever 0.0 or 0.39 | Independence; no stray values |

Runs, with real output and any `SHADER ERROR` lines shown:
```bash
./scripts/run-test.sh a3_asset_check.gd 60          # must stay 55 PASS
./scripts/run-test.sh a5_screen_glow_check.gd 30
./scripts/run-test.sh a5_screen_glow_check.gd 60
./scripts/run-test.sh a5_screen_glow_check.gd 144
```

## What the headless test can't prove

These need you to check by eye:
- **Pixel colour:** nothing renders headless. You need one capture each at `pad_light_data` = 0.0 / 0.39 / 1.0, comparing P1 and P2 with (0,0,0) / (151,162,162) / (230,247,247), with P1 and P2 equal and P3 unchanged. This also confirms `source_color` works end to end (failure case 2).
- **GPU compile:** headless only proves the shader parses. A GPU compile error would show in the editor or game output.
- **The screen quad:** that it's visible, not z-fighting with the model, and covers the model's screen. The 1 mm gap isn't checked.
- **`UpMarker`:** it must be hidden or deleted before the captures (failure case 7).
- **The `hint_range` clamp prediction:** setting 2.0 from code and seeing pure white is a capture check. Reading the value back from the material only proves storage.
- **Real keyboard and frame rate:** `parse_input_event` uses the engine's real input path but not the OS keyboard, and the frame rates are fixed. Normal play by hand (take it out, put it away, switch hands) covers this, plus judging whether 0.39 looks right.

Do you approve Step 1, the driver?
