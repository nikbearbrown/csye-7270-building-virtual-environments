# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it loads base.tscn itself
## A5 headless test for the screen glow: checks the parameters of pad_base_light.gdshader, and whether the driver (humanoid.gd + tablet_device.gd)
## sets pad_light_data by the rules in CHANGE-BRIEF.
## Run: ./scripts/run-test.sh screen_glow_check.gd 30 (and 60, 144)
## What it can prove: the parameter names, types, hints and defaults are right; driven by real Tab key events at a fixed frame rate, pad_light_data follows the rules on every frame;
##           every tablet's value is independent.
## What it cannot prove: what colour the screen looks (headless mode renders nothing). Colour needs captures and a human eye.

# ============================================================
# Constants: the numbers the test compares against, all from CHANGE-BRIEF and the shader
# ============================================================
const SHADER_PATH := "res://shaders/pad_base_light.gdshader"  # Path of the screen shader
const BASE_SCENE := "res://base.tscn"  # The main game scene: the player is in it
const HUMANOID_SCENE := "res://characters/human/humanoid/humanoid.tscn"  # Humanoid body: used for the second character (no brain)
const SCREEN_PATH := "Visual/TabletDevice/Screen"  # Path from a humanoid body to its screen node
const PARAM := &"pad_light_data"  # Name of the driven shader parameter
const LIT := 0.39  # Lit strength (CHANGE-BRIEF: light_strength_percentage = 0.39)
const OFF := 0.0  # Screen off
const MOVE_SECONDS := 0.35  # Tablet move time = from the state change to the screen lighting (CHANGE-BRIEF: 0.35 s ± one frame period)
const SLOW_TIME_SCALE := 0.5  # Slow speed used for the Engine.time_scale rule
const TAP_SECONDS := 0.1  # Short press: hold for 0.1 s, then release (a long press needs 0.4 s)
const HOLD_SECONDS := 0.5  # Long press: hold for 0.5 s (more than 0.4 s)
const SETTLE_SECONDS := 0.6  # Wait after each action: longer than the move, so the tablet has arrived
const QUICK_BACK_SECONDS := 0.1  # The wait in "take it out and put it away after 0.1 s"
const EPS := 0.0001  # Tolerance when comparing decimals

# ============================================================
# Member variables: what the test records while it runs
# ============================================================
var failures := 0  # How many checks failed
var player: Humanoid  # The player body in base.tscn (driven by real key events)
var other: Humanoid  # A second humanoid body: gets an empty intent every frame, never takes the tablet out
var player_mat: ShaderMaterial  # The material of the player's tablet screen
var other_mat: ShaderMaterial  # The material of the second body's tablet screen
var sampler: Sampler  # The node that samples every frame
var change_physics_frame := -1  # Which physics frame the latest tablet state change happened in
var change_hold := -1  # The new state after the latest change

# ============================================================
# Inner classes: two small nodes the test uses
# ============================================================
## Sampler node: its process_priority is high, so every frame it runs after all other _process() calls and reads that frame's final values.
## Records per frame: game time, physics frame number, the player's tablet state, and pad_light_data on both screens.
class Sampler extends Node:
	var player: Humanoid
	var player_mat: ShaderMaterial
	var other_mat: ShaderMaterial
	var game_time := 0.0  # Accumulated game time (delta is added every frame; delta already includes Engine.time_scale)
	var frame_delta := 0.0  # The latest frame's delta
	var samples: Array[Dictionary] = []  # One record per frame

	## Called by Godot once per rendered frame. Records this frame's values.
	func _process(delta: float) -> void:
		game_time += delta
		frame_delta = delta
		samples.append({
			"t": game_time,
			"pf": Engine.get_physics_frames(),
			"hold": player.get_tablet_hold(),
			"pad": float(player_mat.get_shader_parameter(&"pad_light_data")),
			"other": float(other_mat.get_shader_parameter(&"pad_light_data")),
		})


## A "fake brain" for the second body: gives it an empty intent (do nothing) every physics frame, so its own screen driver runs every frame.
## If the two tablets shared one material, it would set the screen off every frame and darken the player's screen too, and the test would catch it.
class IdleBrain extends Node:
	var body: Humanoid

	## Called by Godot once every physics frame.
	func _physics_process(delta: float) -> void:
		body.apply_intent(CharacterIntent.new(), delta)


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (these act as the entry points)
# ============================================================
## Called by Godot once when the script starts as the SceneTree. Starts the whole test.
func _initialize() -> void:
	_run()


# ============================================================
# Feature functions: the parts of the test
# ============================================================
## The whole test: check the shader and materials first, then build the scene and simulate key presses, then check the records, print the result and quit.
func _run() -> void:
	_check_shader()
	await _build_scene()
	_check_materials()
	await _scenario()
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)


## Records one check: prints PASS if it passed, otherwise prints FAIL and counts it.
func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


## Checks 1 and 2: the shader parses and the parameter names, types and hints are right (uniform list); the defaults are right (read from the shader source).
## When the shader fails to parse the uniform list is empty, so both mutations ("delete a semicolon" and "rename the parameter") fail here.
func _check_shader() -> void:
	var shader: Shader = load(SHADER_PATH)
	var uniforms := {}
	for u in shader.get_shader_uniform_list():
		uniforms[u["name"]] = u
	_check(uniforms.has("cold_white") and uniforms["cold_white"]["type"] == TYPE_COLOR,
		"uniform cold_white exists and is a colour (source_color)")
	_check(uniforms.has("pad_light_data") and uniforms["pad_light_data"]["type"] == TYPE_FLOAT,
		"uniform pad_light_data exists and is a float")
	_check(uniforms.has("pad_light_data") and uniforms["pad_light_data"]["hint"] == PROPERTY_HINT_RANGE
		and String(uniforms["pad_light_data"]["hint_string"]).begins_with("0.0,1.0"),
		"pad_light_data has hint_range(0.0, 1.0)")
	# Headless mode cannot read the defaults (CLAUDE.md, Headless facts), so look for them in the source text
	var source := FileAccess.get_file_as_string(SHADER_PATH)
	var re_color := RegEx.create_from_string(
		"uniform\\s+vec4\\s+cold_white\\s*:\\s*source_color\\s*=\\s*vec4\\(\\s*0\\.902\\s*,\\s*0\\.969\\s*,\\s*0\\.969\\s*,\\s*1\\.0\\s*\\)")
	var re_float := RegEx.create_from_string(
		"uniform\\s+float\\s+pad_light_data\\s*:\\s*hint_range\\(\\s*0\\.0\\s*,\\s*1\\.0\\s*\\)\\s*=\\s*0\\.0\\s*;")
	_check(re_color.search(source) != null, "source: cold_white has source_color and default vec4(0.902, 0.969, 0.969, 1.0)")
	_check(re_float.search(source) != null, "source: pad_light_data default is 0.0")


## Builds the test scene: loads base.tscn (the real player), adds a humanoid body with no brain, and attaches the fake brain and the sampler.
func _build_scene() -> void:
	var base: Node = load(BASE_SCENE).instantiate()
	root.add_child(base)
	player = base.get_node("Player")
	other = load(HUMANOID_SCENE).instantiate()
	other.position = Vector3(-3.0, 0.25, 1.5)  # On open floor beside the player, not overlapping it
	base.add_child(other)
	var brain := IdleBrain.new()
	brain.body = other
	other.add_child(brain)
	player_mat = player.get_node(SCREEN_PATH).get_surface_override_material(0)
	other_mat = other.get_node(SCREEN_PATH).get_surface_override_material(0)
	player.tablet_hold_changed.connect(_on_hold_changed)
	sampler = Sampler.new()
	sampler.process_priority = 1000  # Higher numbers run later: it reads the values after all of this frame's code has run
	sampler.player = player
	sampler.player_mat = player_mat
	sampler.other_mat = other_mat
	root.add_child(sampler)
	await process_frame


## Check 3: the screen has a ShaderMaterial using this shader, with Local To Scene ticked, and the two tablets' materials are different objects.
func _check_materials() -> void:
	_check(player_mat != null and player_mat.shader != null and player_mat.shader.resource_path == SHADER_PATH,
		"player Screen uses a ShaderMaterial with pad_base_light.gdshader")
	_check(player_mat != null and player_mat.resource_local_to_scene, "Screen material has Local To Scene")
	_check(player_mat != other_mat, "the two bodies' screen materials are different objects")


## Called whenever the tablet state changes (the player body's tablet_hold_changed signal). Records which physics frame it happened in and the new state.
func _on_hold_changed(_old_hold: Humanoid.TabletHold, new_hold: Humanoid.TabletHold) -> void:
	change_physics_frame = Engine.get_physics_frames()
	change_hold = new_hold


## Simulates the real Tab key: press or release. It goes through Input, so the player brain PlayerController reads it as usual.
func _tab(pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = KEY_TAB
	event.pressed = pressed
	Input.parse_input_event(event)


## Waits for an amount of game time (counted with the sampler's accumulated time, so it is the same length at any frame rate).
func _wait(seconds: float) -> void:
	var end := sampler.game_time + seconds
	while sampler.game_time < end - EPS:
		await process_frame


## Holds Tab for hold_seconds, then releases it (a short or long press).
## After release, a short press is read by the brain only on the next physics frame (at 144 fps there is a physics frame only about every 2.4 rendered frames),
## so first wait until the physics frame number changes, then one more rendered frame, so the sampler also records "the frame the state changed".
func _press(hold_seconds: float) -> void:
	_tab(true)
	await _wait(hold_seconds)
	var physics_before := Engine.get_physics_frames()
	_tab(false)
	while Engine.get_physics_frames() <= physics_before:
		await process_frame
	await process_frame


## From record from_index on, finds the first record where pad_light_data equals LIT; returns -1 if there is none.
func _first_lit(from_index: int) -> int:
	for i in range(from_index, sampler.samples.size()):
		if absf(sampler.samples[i]["pad"] - LIT) < EPS:
			return i
	return -1


## From record from_index on, whether any frame has pad_light_data equal to value.
func _any_pad(from_index: int, value: float) -> bool:
	for i in range(from_index, sampler.samples.size()):
		if absf(sampler.samples[i]["pad"] - value) < EPS:
			return true
	return false


## How many seconds of game time passed from the state change to the screen lighting.
## The tablet starts moving in the physics frame in which the state changes, so that frame is counted too: (lit physics frame − change physics frame + 1) × time per physics frame.
## Game time per physics frame = 1 / physics frames per second × Engine.time_scale.
func _lit_delay(lit_index: int) -> float:
	var ticks: int = sampler.samples[lit_index]["pf"] - change_physics_frame + 1
	return ticks * Engine.time_scale / float(Engine.physics_ticks_per_second)


## Checks 4–12: simulates the player's actions in order; each part checks one rule from CHANGE-BRIEF.
func _scenario() -> void:
	await _wait(0.2)  # Run a few frames first: the first frame's delta is 0, the real frame period is only readable after a few frames
	var fps := 1.0 / sampler.frame_delta
	var tolerance := sampler.frame_delta + EPS  # Tolerance: one frame period
	print("  (fps %.0f, frame period %.4f s, physics %d ticks/s)" % [fps, sampler.frame_delta, Engine.physics_ticks_per_second])
	_check(not _any_pad(0, LIT) and absf(sampler.samples[-1]["pad"] - OFF) < EPS, "4  NONE at start: screen 0.0")

	# 5: short press to take it out (NONE → ONE_HAND): 0 until it reaches the hand, 0.39 on the frame it arrives
	var start := sampler.samples.size()
	await _press(TAP_SECONDS)
	var changed_at := sampler.samples.size() - 1
	await _wait(SETTLE_SECONDS)
	var lit := _first_lit(start)
	_check(change_hold == Humanoid.TabletHold.ONE_HAND, "5  short press: NONE -> ONE_HAND")
	_check(lit > changed_at, "5  screen still 0.0 on the frame the state changed")
	if lit >= 0:
		var delay := _lit_delay(lit)
		print("     lit %.4f s after the state change (frame-based: %.4f s)" % [delay, sampler.samples[lit]["t"] - sampler.samples[changed_at]["t"]])
		_check(absf(delay - MOVE_SECONDS) <= tolerance, "5  lit %.2f s +- one frame after the state change" % MOVE_SECONDS)
	_check(lit >= 0 and absf(sampler.samples[lit]["pad"] - player.get_node("Visual/TabletDevice").light_strength_percentage) < EPS,
		"12 lit value equals light_strength_percentage (0.39)")

	# 6: long press (ONE_HAND → TWO_HAND), then short press (TWO_HAND → ONE_HAND): no frame is 0
	start = sampler.samples.size()
	await _press(HOLD_SECONDS)
	_check(change_hold == Humanoid.TabletHold.TWO_HAND, "6  long press: ONE_HAND -> TWO_HAND")
	await _wait(SETTLE_SECONDS)
	await _press(TAP_SECONDS)
	_check(change_hold == Humanoid.TabletHold.ONE_HAND, "6  short press: TWO_HAND -> ONE_HAND")
	await _wait(SETTLE_SECONDS)
	_check(not _any_pad(start, OFF), "6  never 0.0 on any frame across ONE_HAND <-> TWO_HAND")

	# 7: short press to put it away (ONE_HAND → NONE; in the switch table a short press while one-handed = put away): 0 on the frame the state becomes NONE
	start = sampler.samples.size()
	await _press(TAP_SECONDS)
	_check(change_hold == Humanoid.TabletHold.NONE, "7  short press: ONE_HAND -> NONE")
	var first_none := -1
	for i in range(start, sampler.samples.size()):
		if sampler.samples[i]["hold"] == Humanoid.TabletHold.NONE:
			first_none = i
			break
	_check(first_none >= 0 and absf(sampler.samples[first_none]["pad"] - OFF) < EPS, "7  0.0 on the same frame the state becomes NONE")
	await _wait(SETTLE_SECONDS)

	# 8: take it out and put it away after 0.1 s: never lit
	start = sampler.samples.size()
	await _press(TAP_SECONDS)
	await _wait(QUICK_BACK_SECONDS)
	await _press(TAP_SECONDS)
	_check(change_hold == Humanoid.TabletHold.NONE, "8  out and back: ends in NONE")
	await _wait(SETTLE_SECONDS)
	_check(not _any_pad(start, LIT), "8  put away before reaching the hand: never lit")

	# 9: taken out again while being put away: counting from the last take-out, it lights only after another 0.35 s
	await _press(TAP_SECONDS)
	await _wait(SETTLE_SECONDS)
	await _press(TAP_SECONDS)  # Put away: the screen goes off at once and the tablet starts toward the hip
	await _wait(QUICK_BACK_SECONDS)
	start = sampler.samples.size()
	await _press(TAP_SECONDS)  # Taken out again half-way
	_check(change_hold == Humanoid.TabletHold.ONE_HAND, "9  taken out again mid-way")
	await _wait(SETTLE_SECONDS)
	lit = _first_lit(start)
	if lit >= 0:
		print("     lit %.4f s after the second take-out" % _lit_delay(lit))
	_check(lit >= 0 and absf(_lit_delay(lit) - MOVE_SECONDS) <= tolerance, "9  restart: lit %.2f s +- one frame after the last take-out" % MOVE_SECONDS)
	await _press(TAP_SECONDS)  # Put away, ready for the next part
	await _wait(SETTLE_SECONDS)

	# 11: Engine.time_scale = 0.5: still 0.35 s of "scaled game time", i.e. 0.7 s of real time
	Engine.time_scale = SLOW_TIME_SCALE
	start = sampler.samples.size()
	await _press(TAP_SECONDS)
	await _wait(SETTLE_SECONDS)
	lit = _first_lit(start)
	if lit >= 0:
		var scaled := _lit_delay(lit)
		print("     time_scale %.1f: lit %.4f s scaled game time = %.4f s real time" % [SLOW_TIME_SCALE, scaled, scaled / SLOW_TIME_SCALE])
		_check(absf(scaled - MOVE_SECONDS) <= tolerance, "11 time_scale %.1f: %.2f s of scaled game time" % [SLOW_TIME_SCALE, MOVE_SECONDS])
	else:
		_check(false, "11 time_scale %.1f: screen never lit" % SLOW_TIME_SCALE)
	Engine.time_scale = 1.0
	await _press(TAP_SECONDS)
	await _wait(SETTLE_SECONDS)

	# 10: the second body is 0 on every frame of the whole test
	var other_lit := false
	for s in sampler.samples:
		if absf(s["other"] - OFF) > EPS:
			other_lit = true
	_check(not other_lit, "10 the second body's screen stayed 0.0 on every frame (%d frames)" % sampler.samples.size())
