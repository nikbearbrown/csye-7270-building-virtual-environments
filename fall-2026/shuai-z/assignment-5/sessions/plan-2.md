# Plan: the hearts' safe tint (`game/` only)

I read `CLAUDE.md`, the brief, your shader, `hud.tscn`, `hearts.gd`, `hud.gd`, `main.tscn`, `main.gd`, `rudy.gd`, `spikes.gd`, `system_keys.gd`, `run-test.sh` and the parts of `checks.gd` that matter here. I created and edited no files and did not run Godot.

**The shader can meet the spec, so I'm not stopping.** `game/shaders/invulnerable_tint.gdshader` matches section 2 exactly: `canvas_item`, no `render_mode`, three uniforms with the spec's types, hints and defaults, and the colour line word for word. `logs/probe_invulnerable_tint.log` shows the engine reports `tint_amount: float`, `tint_color: Color` and `tint_strength: float`. The test expects those types. Note that `vec4 : source_color` comes back as `TYPE_COLOR`, not `TYPE_VECTOR4`.

## Steps

**1. Create the material: `game/ui/hearts_tint.tres`** (new file)
- It is a `ShaderMaterial` whose `shader` is your shader, referenced by its uid `uid://ck6nqhwys3e5v` and its path.
- It sets `resource_local_to_scene = true`. Every instance of `hud.tscn` (every load or reload of `main.tscn`) then gets its own copy, which starts at the shader's default of 0.0 (rules 10–11). Without this flag, the cached resource would keep the last `tint_amount` the driver set. This is one line, and you can turn it down.
- It stores no `tint_color` or `tint_strength`, so the defaults in your shader apply and there's only one place they're set. If you'd rather the `.tres` hold them explicitly, say so.

**2. Attach it: `game/ui/hud.tscn`** (changed)
- Add one `ext_resource` for `hearts_tint.tres` and one line on the `Hearts` node: `material = ExtResource(...)`.
- Nothing else in the scene changes.

**3. Drive `tint_amount`: `game/ui/hud.gd`** (changed, about 8 lines)
- `_process()` currently returns early when the debug line is hidden. The tint goes before that return:
  ```gdscript
  func _process(_delta: float) -> void:
  	if _rudy == null:
  		return
  	_tint_hearts()
  	if not _debug.visible:
  		return
  	... (unchanged)

  ## The hearts take on the lit waystone's glow while Rudy is invulnerable,
  ## fading with the time left (CHANGE-BRIEF.md). Reads his state, never sets it.
  func _tint_hearts() -> void:
  	(_hearts.material as ShaderMaterial).set_shader_parameter(&"tint_amount", _rudy._invulnerable_left / _rudy.invulnerable_time)
  ```
- It sets only `tint_amount`. `tint_color` and `tint_strength` stay with the material.
- It has no clock and counts no frames, so frame rate (prediction 2) and `Engine.time_scale` can't change the duration.
- It keeps Hud's default process mode, so it stops while paused (prediction 4).
- Rudy's window controls the tint, not the hit (prediction 3).
- `rudy.gd`, `main.gd` and `hearts.gd` are untouched. The hud.gd doc comment gets one added phrase.
- In the implementing session I'll check the log for a GDScript warning about reading `_invulnerable_left`. A warning wouldn't fail the wrapper, but I'll point it out if one appears.

**4. New headless test: `game/tests/invulnerable_tint_checks.gd` and `invulnerable_tint_checks.tscn`** (new)
- Same pattern as `checks.tscn`: the script extends `Node` and the `.tscn` runs it. It prints one `PASS`/`FAIL` line per check and exits 1 if any check fails.
- It uses its own copies of `checks.gd`'s small helpers (`_frames`, `_tap`, `_wait_until`); `checks.gd` itself isn't touched.
- `checks.gd`'s step 5 scans every `res://` path named anywhere in `res://`, tests included. So the new test names only paths that exist.
- **Sampler:** an inner `Node` with `process_priority = 1000` and `PROCESS_MODE_ALWAYS`. In each `_process` it records:
  - the material's `tint_amount`;
  - `rudy.is_invulnerable()` and `_invulnerable_left`;
  - whether the tree is paused;
  - the unscaled delta;
  - how many physics ticks passed since the last frame (its `_physics_process` counts them).

  With `--fixed-fps`, the delta is 1/fps, so the test gets fps from it instead of hard-coding it.
- **Real play.** It starts on the title. A `restart` tap starts play. Holding `move_right` walks Rudy from x 300 to `SpikesA` at x 1065, all on Segment1 with no gap; GoblinA patrols from x 1500 to the right, so it never reaches him. The script drives the run this way:
  - **Hit 1** at time scale 1: the test checks the start value, the fade and the duration. Once Rudy has control back, it holds `move_right` until he overlaps the spikes while still invulnerable, then holds `move_left` to step off before the window ends. Stepping off avoids prediction 6, where the window ending while he stands on the spikes causes a fresh hit.
  - **Hit 2** with `Engine.time_scale = 0.5`: the time-scale duration. The test sets the scale back to 1.0 afterwards.
  - **Hit 3** takes the last heart. Rudy is defeated and respawns about 1.15 s later, which tests the restart.
  - **Hit 4**, after the respawn window has run out: `pause` is tapped in mid-window, 30 frames are held, then `pause` is tapped again.

  If a setup step misses (for example, he doesn't reach the spikes in time), it prints its own `FAIL` naming the step, so it isn't confused with a broken rule.

### Assertions and the rule each covers

| # | Assertion | Rule |
|---|---|---|
| A1 | `get_shader_uniform_list()` holds exactly `tint_amount` FLOAT, `tint_color` COLOR and `tint_strength` FLOAT; both floats have `PROPERTY_HINT_RANGE` with `0.0,1.0` | Parse; names and types |
| A2 | Read by RegEx from the shader's source: defaults `0.0`, `vec4(0.6, 0.88, 1.0, 1.0)` and `0.4`; `shader_type canvas_item`; no `render_mode` | Defaults; §2 |
| A3 | In the running `Main`, the only node whose material uses this shader is `Hud/Hearts`; among the `.tscn` and `.tres` files under `res://`, only `hud.tscn` names `hearts_tint.tres`; the material is `resource_local_to_scene` | 11; prediction 1 |
| A4 | Under `res://app`, `content`, `ui` and `systems`, no script names `tint_color` or `tint_strength`, and only `hud.gd` names `tint_amount`. After play, the material's `tint_color` and `tint_strength` are still unset or equal to the defaults | "Set by the material only" |
| A5 | `tint_amount` is 0.0 on the title and in play before any hit | 3, 7 (value only) |
| A6 | First frame of hits 1 and 4: ≥ 70/72; at 60 and 144 fps, 71/72 ± 1e-6 | 1 |
| A7 | Every frame of a window: `tint_amount` == `_invulnerable_left / invulnerable_time`, and also == (first value) − (physics ticks since that frame × physics delta × time scale) / 1.2, within 1e-6. The second check is independent of Rudy's own arithmetic | 2 |
| A8 | Every sampled frame of the whole run: `tint_amount > 0` exactly when `is_invulnerable()`. The first frame after each window is exactly 0.0 | 3; 10 (cannot outlast the window) |
| A9 | Span from the first frame above zero to the first frame at zero: 71/60 = 1.183 s ± 1/fps for hit 1; 144/60 = 2.4 s of real time ± 1/fps for hit 2 at time scale 0.5 | 4, 6; prediction 2 |
| A10 | Walking back into the spikes during hit 1: Rudy overlaps them on at least one invulnerable frame, hearts don't change, and `tint_amount` never rises from one frame to the next | 5 (hit ignored); prediction 3 |
| A11 | After the defeat: the first frame after `respawn_at()` has a value ≥ 70/72 and ≤ 1.0, above the previous frame's. The value before the jump is logged | 5 (respawn restarts) |
| A12 | Paused: `tint_amount` is identical across the 30 paused frames and "Paused" is showing. On resume, the first frame's value is ≤ the held value and ≥ the held value minus one frame's worth of ticks. Across the pause, A9's duration counts unpaused game time only | 6 (pause); prediction 4 |
| A13 | While hit 4's window is open, the test instantiates a fresh `main.tscn`, which is what a reload does. The new `Hearts` material is a different object, and its `tint_amount` is 0.0 before its first frame and on that frame | 10 |
| A14 | `rendering/renderer/rendering_method` is `gl_compatibility`. This is only a settings read | 12 (setting only) |

**5. Run and report** (no commits)
- `scripts/run-test.sh game invulnerable_tint_checks.tscn 30`, then `60`, then `144`.
- `scripts/run-test.sh game checks.tscn 60`: 141 `PASS` lines and `all checks passed`.
- `scripts/run-test.sh godot check_props.gd 60`: 44 `ok` lines and `PASS: 0 failed check(s)`.
- `grep -c` the `PASS`/`FAIL`/`SHADER ERROR`/`SCRIPT ERROR` lines in each log, and show the real output and exit status.
- `git diff --stat` on `game/content/rudy/rudy.gd`, `game/app/main.gd`, `game/tests/checks.gd`, `game/shaders/` and `godot/`, all of which should be empty.
- Optional, for you to approve separately: two temporary mutations of `hud.gd` only, reverted afterwards, to show the test can fail.
  - The driver counts frames instead of reading Rudy's state: A9 should fail at 30 and 144 fps.
  - The driver uses `PROCESS_MODE_ALWAYS` with its own real-time clock: A12 should fail.

## What the headless test proves, and what it cannot

**It proves:**
- The shader parses (no `SHADER ERROR` in the log) and has exactly three uniforms with these names and types.
- Its source declares the spec's defaults.
- The material is on `Hud/Hearts` only, and no code sets `tint_color` or `tint_strength`.
- The value of `tint_amount` the material holds on every frame, through real input and the real game loop, at 30, 60 and 144 fps. That covers rules 1–6, 10 and 11.

**It cannot prove anything about pixels:**
- `--headless` uses the dummy renderer, which draws nothing and can't be read back.
- `get_shader_parameter()` returns the value stored in the material, not what a GPU used.
- So rules 7–9, alpha, sRGB handling, contrast, whether `hint_range` clamps, and whether Compatibility actually renders it are all outside a headless run.
- A14 reads a setting; it doesn't observe a renderer.
- A13 re-instantiates `main.tscn` and does not press Enter on the end card. Reaching the end card would take the whole route, and by then the 2 s celebration has already closed any window.

## Checks only you can make

1. Captures at `tint_amount` 0.0, 0.5 and 1.0, with the driver stopped and after one hit at the first spikes, so the hearts are two full and one empty. Compare P1, P2, P3 and B with the table in section 3. More than one step per channel off the prediction is a finding (the Compatibility sRGB claim).
2. P3 (inside the empty heart) and the gaps between hearts at 0.5 and 1.0 still show the sky unchanged (rule 8, prediction 5).
3. At 1.0, the outline against the sky measures ≥ 3:1, about 3.5:1 predicted (rule 9, prediction 11).
4. The 0.0 capture matches a capture taken with no material at all (rule 7).
5. A capture with `tint_amount` set to 2.0 from code: `#A2C0D7` means `hint_range` doesn't clamp; `#B58086` means it does (short answer 7).
6. A windowed run at 60 fps in Compatibility (rule 12):
   - the hearts fade in from the title and tint after a hit;
   - Rudy, the goblins, the spikes, the outline, the title, the debug line, the fade, the end card and "Paused" look as before.

None of the existing capture tools set `tint_amount` and stop the driver, so these captures need one. I've left it out of the plan; if you want it, I'd write it as a separate step: `game/tests/capture_tint.gd` and `.tscn`, a windowed scene like `capture.tscn`.

**Files touched:** `game/ui/hearts_tint.tres` (new), `game/ui/hud.tscn`, `game/ui/hud.gd`, `game/tests/invulnerable_tint_checks.gd` and `.tscn` (new), and the new `logs/game_invulnerable_tint_checks_{30,60,144}fps.log`. Nothing in `godot/`, `game/shaders/` or the existing tests changes.