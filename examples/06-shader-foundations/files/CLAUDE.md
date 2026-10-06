@AGENTS.md

## Project context

**Engine and renderer.** Feature tag 4.7 (`godot/project.godot` line 7);
tested with Godot 4.7.2 (`README.md`). GL Compatibility renderer
(`godot/project.godot` line 27, `renderer/rendering_method="gl_compatibility"`).

**Main scene.** `res://game/main.tscn`. Source: `godot/project.godot` line 6.

**How Clawd is drawn.** Pure GDScript vector drawing — no textures, no
existing shader. `player.gd:_draw()` (line 93) calls
`ClawdArt.paint(self, ...)`, which issues `canvas.draw_rect()` calls directly
on the `CharacterBody2D` CanvasItem. Body color is `Color("dd775b")`; eyes are
`Color.BLACK`; surroundings are transparent. Source: `godot/features/player/
clawd_art.gd` lines 7–8 and 84–98, `godot/features/player/player.gd` line 93.

**Session state machine.** Owned by `godot/game/session.gd`. The `State` enum
(line 13) has MENU, PLAYING, PAUSED, DYING, COMPLETE. State transitions happen
in `resolve_contacts()` (lines 131–144) and `_physics_process()` (lines
146–163). Presentation code may read `state`; it must never write it (comment,
session.gd line 3–8).

**Retry countdown.** `retry_remaining: float` in `session.gd` (line 23). Set
to `0.55` in `resolve_contacts()` (line 137) when a fatal contact occurs.
Decremented each physics frame in `_physics_process()` (line 149); hits zero
to trigger `restart_attempt()` (line 150). Pressing R calls `restart_attempt()`
directly, bypassing the timer (line 175).

**Clawd's collision shape.** `RectangleShape2D`, size `Vector2(18, 28)`,
offset `Vector2(0, -14)` — bottom edge at feet level (y=0), top edge at y=−28.
Source: `godot/features/player/player.gd` lines 26–31.

**Headless test commands** (from `README.md` lines 37–40):
```
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
godot --headless --path godot --script res://tests/test_clawd.gd --fixed-fps 60
```
(`node scripts/clawd-build.cjs` in the README writes a build manifest; it is not
a test, and `scripts/` is not in this copy.)

**Headless facts on this machine (checked 2026-09-27, Godot 4.7.2).**
- `--headless` uses a dummy renderer. It runs Godot's shader parser, so shader
  errors print as `SHADER ERROR`, but it draws nothing and cannot read pixels.
- A shader error does not change Godot's exit code. Any `SHADER ERROR` line in
  a log is a failure, whatever the exit code says.
- A `.gdshader` error appears when the shader is first used (assigned to a
  material), not when it is loaded.
- Always pass `--headless`. Never add `--rendering-driver` to a headless
  command: on macOS it silently falls back to a windowed display.

---

## Effect specification

Failure flash (Chapter 6)
Visible effect: when a run fails (spikes or a fall), Clawd is tinted toward a
flash color, then fades back to normal by the moment the retry happens.
1. One float uniform, flash_amount, 0.0 to 1.0, drives the effect. It is 1.0
   on the first frame of the failure and reaches 0.0 when the retry starts.
   The fade is linear in time and lasts the same wall-clock time at 30, 60
   and 144 frames per second.
2. Pressing R during the failure ends the flash at once. In every state
   except the failure, flash_amount is 0.0.
3. A second uniform, flash_color, is a color with default #25354a (the
   level's ink). Not white: the background is #f6f3ec, and white against it
   has a contrast ratio of about 1.1 to 1.
4. At flash_amount 0.0 Clawd looks exactly as before: same body color, same
   black eyes, same transparent surroundings. At 1.0 every visible pixel of
   Clawd is flash_color; transparent pixels stay transparent.
5. Only Clawd changes. The level, background, HUD and gallery do not.
6. No change to collision, movement, input, the session state machine, the
   0.55 s retry delay, or any existing test's expectations. Presentation
   code may read session state; it never writes it.
7. It must work in this project's renderer.
8. Evidence: a new headless test proves the shader is accepted by Godot's
   shader parser in a headless run, the two uniforms exist with the right
   types, and flash_amount obeys rules 1 and 2 at 30 and 144 fps. How it
   looks is a human check.

---

## Out of scope

This change must not touch:

- **Collision shape.** The 18×28 RectangleShape2D in `player.gd` is unchanged.
- **Physics and movement.** All tuning constants in `tuning.gd`, velocity math,
  `move_and_slide()`, gravity, jump, coyote/buffer windows — untouched.
- **Input bindings.** The action map set up in `session.gd:_setup_input()` is
  unchanged. R still calls `restart_attempt()` directly; the flash implementation
  reads that R was pressed, it does not intercept or re-bind the key.
- **Session state machine.** `session.gd` state transitions, `resolve_contacts()`,
  `restart_attempt()`, and `set_paused()` are read-only to presentation code.
- **Retry delay.** The `retry_remaining = 0.55` constant in `session.gd:137`
  is unchanged.
- **Existing tests.** All assertions in `test_game.gd`, `test_keyboard.gd`, and
  `test_clawd.gd` must still pass without modification.
- **Level, background, HUD, gallery.** The `_draw()` method in `session.gd`,
  `hud.gd`, and `clawd_gallery.tscn` are unchanged.
- **`clawd_art.gd` animation math.** The `sample()` and `paint()` functions and
  their outputs must remain byte-identical so existing fixture checks pass.

---

## Unconfirmed

- **Contents of `main.tscn`.** The file was not read. It is the instantiated
  root; how `session.gd` is attached as a script vs. a child node was not
  verified from these files.
- **CanvasItem material slot in GL Compatibility.** Whether a `ShaderMaterial`
  on the `CharacterBody2D` tints the `draw_rect()` output in the GL
  Compatibility renderer cannot be confirmed headless (dummy renderer). It is a
  human check in the editor or running game.
- **Gallery scene path.** `README.md` names `res://gallery/clawd_gallery.tscn`;
  the file was not read to confirm it is unaffected by a CanvasItem material
  placed on the player node only.
