# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it loads base.tscn itself
## A7 behaviour pins: what the game does with the tablet today, written before the animation change (CHANGE-BRIEF, "The evidence split").
## Every pin passes before the change and must still pass after it, because the brief keeps these behaviours unchanged.
## Timings the brief changes (the 0.35 s slide, when the screen lights) are NOT pinned here; they belong to the edge tests.
## Run: ./scripts/run-test.sh test_tablet_pins.gd 60
## What it can prove: driven by real key events at a fixed frame rate, the hold-state table, the movement rules per hold, the screen and demo-tablet states
## once the tablet has settled, the tablet OS canvas switching, the tablet's scale, and the F key only working with the tablet put away.
## What it cannot prove: how anything looks (headless mode draws nothing).

# ============================================================
# Constants: the numbers the pins compare against
# ============================================================
const BASE_SCENE := "res://base.tscn"  # The main game scene: the player, the light switch and the ceiling lights are in it
const PLAYER_PATH := "Player"  # Path of the player body under the base scene's root
const LIGHTS_PATH := "CeilingLights"  # Path of the ceiling-lights state node
const SCREEN_TABLET_PATH := "PlayerController/ScreenTabletLayer/SubViewportContainer/SubViewport/ScreenTablet"  # The demo tablet, under the player
const TABLET_OS_VIEWPORT_PATH := "PlayerController/TabletOSViewport"  # The tablet OS canvas, under the player
const FPS := 60  # The wrapper pins --fixed-fps 60, so one physics frame is 1/60 s
const TAP_FRAMES := 6  # A short press: hold 0.1 s, then release (a long press needs 0.4 s)
const HOLD_FRAMES := 30  # A long press: hold 0.5 s (past the 0.4 s threshold)
const SETTLE_FRAMES := 90  # Wait 1.5 s after each change: longer than any raise or slide, so the tablet has settled whatever the timing
const WALK_FRAMES := 30  # How long we hold a movement key before reading the speed
const WALK_SPEED := 3.5  # Humanoid.walk_speed (humanoid.gd); sprint is 6.0
const SPEED_EPS := 0.05  # Tolerance on speeds
const SCALE_EPS := 0.001  # Tolerance on the tablet's scale
const SPAWN_SPOT := Vector3(2.0, 0.25, 1.5)  # The player's spawn point in base.tscn; we put the player back here before every speed measurement so it never walks into a wall
const JUMP_WATCH_FRAMES := 10  # How many frames after a jump press we watch for the upward speed
const SWITCH_SPOT := Vector3(2.0, 0.25, 4.0)  # A floor spot inside the light switch's interact area (switch at (2, 1.55, 4.49) in base.tscn)
const NONE := 0  # Humanoid.TabletHold.NONE
const ONE_HAND := 1  # Humanoid.TabletHold.ONE_HAND
const TWO_HAND := 2  # Humanoid.TabletHold.TWO_HAND

# ============================================================
# Member variables: what the pins record while they run
# ============================================================
var failures := 0  # How many checks failed
var root_scene: Node  # The loaded base scene
var player: Humanoid  # The player body (driven through its real brain by key events)
var changes: Array = []  # Every tablet_hold_changed signal we heard, as [old, new]

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (these act as the entry points)
# ============================================================
## Called by Godot once when the script starts as the SceneTree. Starts the whole run.
func _initialize() -> void:
	_run()


# ============================================================
# Functions: the parts of the run
# ============================================================
## The whole run: load the scene, then go through the pins in order, print the result and quit with 1 if anything failed.
func _run() -> void:
	await _build_scene()
	await _pin_hold_table()
	await _pin_movement_rules()
	await _pin_screen_and_canvas()
	await _pin_tablet_scale()
	await _pin_interact_only_when_put_away()
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)


## Sends one action press or release through Input.parse_input_event, the way a real key reaches the game (CHANGE-BRIEF / A7 rule: never Input.action_press).
## The brain reads the action state on its next physics frame, exactly as for a real key.
func _act(action: StringName, pressed: bool) -> void:
	var event := InputEventAction.new()
	event.action = action
	event.pressed = pressed
	Input.parse_input_event(event)
	Input.flush_buffered_events()  # We let Godot handle the queued event now, so the brain sees it on this physics frame and not one frame later


## Records one check: prints PASS if it passed, otherwise prints FAIL and counts it.
func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


## Loads base.tscn as the current scene, finds the player, starts listening to its hold changes, and lets it land on the floor.
func _build_scene() -> void:
	root_scene = load(BASE_SCENE).instantiate()  # First we build the real game scene
	root.add_child(root_scene)  # then put it in the tree, so every _ready() and _physics_process() runs as in the game
	current_scene = root_scene
	player = root_scene.get_node(PLAYER_PATH) as Humanoid  # The player body; its brain (PlayerController) reads our key events
	player.tablet_hold_changed.connect(func(old_hold, new_hold): changes.append([old_hold, new_hold]))  # We write down every hold change the body announces
	await _wait(SETTLE_FRAMES)  # The player spawns 0.25 m up; we wait until it has landed and everything has started


## Waits the given number of physics frames.
func _wait(frames: int) -> void:
	for i in frames:
		await physics_frame


## Presses an action like a real key (through Input.parse_input_event): down for the given frames, then up, then one more frame so the brain sees the release.
func _press(action: StringName, frames: int) -> void:
	_act(action, true)  # The key goes down; the brain reads it on its next physics frame
	await _wait(frames)
	_act(action, false)  # The key comes up; for the tablet key, a release before 0.4 s is what makes a short press
	await _wait(1)


## A short Tab press, then a wait until the tablet has settled.
func _tap_tablet() -> void:
	await _press(&"tablet", TAP_FRAMES)
	await _wait(SETTLE_FRAMES)


## A long Tab press, then a wait until the tablet has settled.
func _hold_tablet() -> void:
	await _press(&"tablet", HOLD_FRAMES)
	await _wait(SETTLE_FRAMES)


## Pin 1: the hold-state table (humanoid.gd _next_tablet_hold()), driven by real key presses, and one signal per change with the right old and new state.
func _pin_hold_table() -> void:
	_check(player.get_tablet_hold() == NONE, "1.0 the tablet starts put away")
	var steps := [  # Each step: which press, the hold we expect after it
		["tap", ONE_HAND], ["tap", NONE], ["hold", TWO_HAND], ["tap", ONE_HAND], ["hold", TWO_HAND], ["hold", NONE],
	]
	var before := NONE  # The hold before each step, for checking the signal's "old" value
	for i in steps.size():
		changes.clear()  # We only look at the signals this step produced
		if steps[i][0] == "tap":
			await _tap_tablet()
		else:
			await _hold_tablet()
		var expected: int = steps[i][1]
		_check(player.get_tablet_hold() == expected, "1.%d %s press: %d -> %d" % [i + 1, steps[i][0], before, expected])
		_check(changes.size() == 1 and changes[0][0] == before and changes[0][1] == expected,
			"1.%d exactly one tablet_hold_changed(%d, %d)" % [i + 1, before, expected])
		before = expected


## Puts the player back on its spawn point, standing still, and waits until it has settled on the floor.
func _reset_position() -> void:
	player.global_position = SPAWN_SPOT
	player.velocity = Vector3.ZERO
	await _wait(SETTLE_FRAMES)


## Measures the player's horizontal speed after holding one movement key (forward) for a while.
func _walk_speed() -> float:
	await _reset_position()  # First we go back to the spawn point, so earlier walks never leave us against a wall
	_act(&"move_forward", true)
	await _wait(WALK_FRAMES)
	var speed := Vector2(player.velocity.x, player.velocity.z).length()  # We read the speed while the key is still down
	_act(&"move_forward", false)
	await _wait(WALK_FRAMES)  # and let the player stop again before the next measurement
	return speed


## Measures how fast the player goes up right after a jump press (0 if the jump was ignored).
func _jump_rise() -> float:
	await _reset_position()  # First we stand still on the floor at the spawn point
	_act(&"jump", true)
	var rise := 0.0
	for i in JUMP_WATCH_FRAMES:  # Then for a few frames we keep the highest upward speed we see; a jump shows as one
		await physics_frame
		rise = maxf(rise, player.velocity.y)
	_act(&"jump", false)
	await _wait(SETTLE_FRAMES)  # We wait until the player is back on the floor
	return rise


## Measures the speed while holding sprint and forward together.
func _sprint_speed() -> float:
	await _reset_position()
	_act(&"sprint", true)
	var speed := await _walk_speed()
	_act(&"sprint", false)
	return speed


## Pin 2: what each hold allows (player_controller.gd _read_intent()): put away = walk, sprint, jump; one-handed (settled) = walk only; two-handed = no movement.
func _pin_movement_rules() -> void:
	# Put away
	_check(absf(await _walk_speed() - WALK_SPEED) < SPEED_EPS, "2.1 put away: walking reaches walk_speed")
	_check(await _sprint_speed() > WALK_SPEED + 1.0, "2.2 put away: sprint is faster than walking")
	_check(await _jump_rise() > 1.0, "2.3 put away: jump lifts the player")
	# One-handed, after the tablet has settled
	await _tap_tablet()
	_check(player.get_tablet_hold() == ONE_HAND, "2.4 now holding one-handed")
	_check(absf(await _walk_speed() - WALK_SPEED) < SPEED_EPS, "2.5 one-handed (settled): walking still reaches walk_speed")
	_check(absf(await _sprint_speed() - WALK_SPEED) < SPEED_EPS, "2.6 one-handed: sprint is ignored (walk speed)")
	_check(absf(await _jump_rise()) < 0.01, "2.7 one-handed: jump is ignored")
	# Two-handed
	await _hold_tablet()
	_check(player.get_tablet_hold() == TWO_HAND, "2.8 now holding two-handed")
	_check(await _walk_speed() < SPEED_EPS, "2.9 two-handed: no movement")
	await _hold_tablet()  # A long press from two hands puts it away again
	_check(player.get_tablet_hold() == NONE, "2.10 put away again")


## Pin 3: once settled, the screen is dark when put away and lit while held; the demo tablet is out only one-handed; the tablet OS canvas draws only while held.
func _pin_screen_and_canvas() -> void:
	var tablet := player.get_tablet()
	var screen_mat := tablet.get_screen().get_surface_override_material(0) as ShaderMaterial  # The material the screen glow is written to
	var demo := player.get_node(SCREEN_TABLET_PATH)  # The demo tablet (bottom right)
	var canvas := player.get_node(TABLET_OS_VIEWPORT_PATH) as SubViewport  # The tablet OS canvas
	_check(float(screen_mat.get_shader_parameter(&"pad_light_data")) == 0.0, "3.1 put away: screen dark")
	_check(demo.get("_screen_want_show") == false, "3.2 put away: demo tablet not out")
	_check(canvas.render_target_update_mode == SubViewport.UPDATE_DISABLED, "3.3 put away: tablet OS canvas not drawing")
	await _tap_tablet()
	_check(float(screen_mat.get_shader_parameter(&"pad_light_data")) > 0.0, "3.4 one-handed (settled): screen lit")
	_check(demo.get("_screen_want_show") == true, "3.5 one-handed: demo tablet out")
	_check(canvas.render_target_update_mode == SubViewport.UPDATE_ALWAYS, "3.6 one-handed: tablet OS canvas drawing")
	await _hold_tablet()
	_check(float(screen_mat.get_shader_parameter(&"pad_light_data")) > 0.0, "3.7 two-handed (settled): screen lit")
	_check(demo.get("_screen_want_show") == false, "3.8 two-handed: demo tablet not out")
	_check(canvas.render_target_update_mode == SubViewport.UPDATE_ALWAYS, "3.9 two-handed: tablet OS canvas drawing")
	await _hold_tablet()
	_check(float(screen_mat.get_shader_parameter(&"pad_light_data")) == 0.0, "3.10 put away again: screen dark")


## Pin 4: the tablet keeps its real size whatever holds it (CHANGE-BRIEF prediction 3: hanging it on a bone must not scale it).
func _pin_tablet_scale() -> void:
	var tablet := player.get_tablet()
	for step in ["put away", "one-handed", "two-handed"]:
		var s := tablet.global_transform.basis.get_scale()  # The scale the tablet really has in the world
		_check(absf(s.x - 1.0) < SCALE_EPS and absf(s.y - 1.0) < SCALE_EPS and absf(s.z - 1.0) < SCALE_EPS,
			"4 %s: TabletDevice global scale is 1 (got %s)" % [step, s])
		if step == "put away":
			await _tap_tablet()
		elif step == "one-handed":
			await _hold_tablet()
	await _hold_tablet()  # Back to put away for the next pin


## Pin 5: F works on the light switch only with the tablet put away (player_controller.gd reads interact only when the hold is NONE).
func _pin_interact_only_when_put_away() -> void:
	var lights := root_scene.get_node(LIGHTS_PATH) as CeilingLights
	player.global_position = SWITCH_SPOT  # First we stand the player inside the switch's interact area
	player.velocity = Vector3.ZERO
	await _wait(SETTLE_FRAMES)
	var before := lights.is_lights_on()
	await _press(&"interact", 2)
	_check(lights.is_lights_on() != before, "5.1 put away: F toggles the lights")
	await _tap_tablet()
	var during := lights.is_lights_on()
	await _press(&"interact", 2)
	_check(lights.is_lights_on() == during, "5.2 one-handed: F does nothing")
	await _tap_tablet()
