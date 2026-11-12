# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it loads base.tscn itself
## A6 headless state test for Effect B (dust under the ceiling light): loads the real base.tscn (real player, real PlayerController,
## the real LightSwitch and CeilingLights, the LightDust instance with its listener script), walks the player to the switch with the real S key,
## presses the real F key, and records what the dust does. It never calls set_lights_on(), toggle() or any listener function itself.
## The seven assertions follow CHANGE-BRIEF "Effect B: Observable rules":
##   1 lights on at scene load, so the dust is shown and emitting from the start, after one restart() (the start-up query);
##   2 F turns the lights off: on that same frame the dust is invisible and not emitting;
##   3 while the lights stay off, nothing comes back by itself;
##   4 F turns the lights on again: on that frame the dust is shown and emitting, after exactly one restart() (not two, although
##     showing also fires visibility_changed), and one lights_changed per press;
##   5 paused tree: the dust stops processing; visible, emitting and restart count do not change; unpaused, it processes again;
##   6 hidden node: emitting stops on that frame; shown again with the lights on, it restarts exactly once;
##   7 not a feedback loop: amount never changes during the test and amount_ratio stays 1.0.
## Run: ./scripts/run-test.sh test_light_dust_state.gd 60
## The pause and the hide are set by this test directly: the game has no pause feature and nothing hides the node yet (the brief allows this for pause).
## What it can prove: the input -> brain -> body -> switch -> CeilingLights -> lights_changed -> listener chain, on which frame the dust shows,
##           hides, starts and stops, how many restart() calls each start makes, and what the node does while paused and hidden.
## What it cannot prove: what the GPU draws (headless draws no particles): that preprocess really fills the box on the first visible frame,
##           that the specks freeze on screen while paused, that no glowing specks are left after the light goes off, and the look.

# ============================================================
# Constants: the scene, the timings, and the key presses
# ============================================================
const BASE_SCENE := "res://base.tscn"  # The real main scene, the same one the game runs
const DUST_POSITION := Vector3(0.0, 1.45, -3.20)  # CHANGE-BRIEF: the emission box is centred here, under ceiling light 1
const POSITION_EPS := 0.001  # How close two positions must be to count as the same point, metres
const IDLE_FRAMES := 30  # Frames we wait after scene load before touching any key
const WALK_TIMEOUT_FRAMES := 300  # If the player is not at the switch within 5 s, the walk is broken and we stop
const SETTLE_FRAMES := 20  # Frames we wait after releasing S, so the player has stopped inside the switch's area
const KEY_HOLD_FRAMES := 3  # Frames we hold F; the brain only interacts on the frame it was just pressed
const SIGNAL_TIMEOUT_FRAMES := 30  # If a press of F brings no lights_changed within 0.5 s, the chain is broken
const OFF_WAIT_FRAMES := 60  # Frames we wait with the lights off (1 s), to see that nothing comes back
const PAUSE_FRAMES := 20  # Frames the tree stays paused
const HIDE_FRAMES := 30  # Frames the node stays hidden

var _failures := 0  # How many checks have failed; turned into the exit code at the end
var _passes := 0  # How many checks have passed; printed in the summary
var _player: Humanoid  # The real player body from base.tscn
var _switch: Node3D  # The real wall switch
var _ceiling_lights: CeilingLights  # The real keeper of the light state; we only read it
var _light_1: Light3D  # ceiling_light_1, to see the lights really go off and on
var _dust: GPUParticles3D  # The LightDust instance with its listener script
var _sampler: Sampler  # Records one line per frame, after every other script has run
var _changes: Array[Dictionary] = []  # One entry per lights_changed: frame, state, and the dust as the listener left it


# ============================================================
# Inner classes: the small node the test uses
# ============================================================
## Sampler node: its process_priority is high and its process_mode is ALWAYS, so every frame (paused or not) it runs after the brain and the listener
## and writes down that frame's final values.
class Sampler extends Node:
	var dust: GPUParticles3D
	var samples: Array[Dictionary] = []  # One record per rendered frame

	## Called by Godot once per rendered frame. We write down the dust's amount and amount_ratio, the two values a feedback loop would touch.
	func _process(_delta: float) -> void:
		samples.append({"amount": dust.amount, "amount_ratio": dust.amount_ratio})


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points)
# ============================================================
## Called by Godot once when the script starts as the SceneTree. Starts the whole test.
func _initialize() -> void:
	_run()


# ============================================================
# Feature functions: the parts of the test
# ============================================================
## The whole test: build the scene, walk to the switch, press F twice, pause, hide, check the records, print the summary and quit.
func _run() -> void:
	if not await _build_scene():  # If the scene is not wired as expected, there is nothing to drive
		_finish()
		return
	await _wait_frames(IDLE_FRAMES)  # First we stand still after load, touching nothing
	var amount_at_load := _dust.amount  # The amount the scene loaded with; the configuration test checks it against the brief, here it only must not change
	_check_scene_load()  # Assertion 1
	if not await _walk_to_switch():  # Then we walk to the switch with the real S key; if we never get there, F cannot work
		_finish()
		return
	var restarts := _restart_count()  # Restarts so far (1 from scene load)
	if not await _press_f_and_wait(1):  # We press F: the lights should go off
		_finish()
		return
	_check_lights_off(_changes[0], restarts)  # Assertion 2
	await _wait_frames(OFF_WAIT_FRAMES)  # We wait 1 s with the lights off
	_check_stays_off(restarts)  # Assertion 3
	if not await _press_f_and_wait(2):  # We press F again: the lights should come on
		_finish()
		return
	await _wait_frames(KEY_HOLD_FRAMES + 2)  # A few more frames, so any late second restart would show up
	_check_lights_on(_changes[1], restarts)  # Assertion 4
	await _check_pause()  # Assertion 5
	await _check_hide()  # Assertion 6
	_check_amount(amount_at_load)  # Assertion 7, over every frame recorded since load
	_finish()


## Called by _run() first. Loads base.tscn into the tree, finds the player, the switch, the keeper, light 1 and the dust,
## then (after one frame, once every _ready() has run) listens to lights_changed and adds the sampler. Returns false if something is missing.
func _build_scene() -> bool:
	var base: Node = load(BASE_SCENE).instantiate()  # We build the real main scene
	root.add_child(base)  # And put it in the tree, so the brain, the body, the switch, the keeper and the listener all run as in the game
	_player = base.get_node_or_null("Player") as Humanoid
	_switch = base.get_node_or_null("LightSwitch") as Node3D
	_ceiling_lights = base.get_node_or_null("CeilingLights") as CeilingLights
	_light_1 = base.get_node_or_null("ceiling_light_1") as Light3D
	_dust = base.get_node_or_null("LightDust") as GPUParticles3D
	if not _check("base.tscn has Player, LightSwitch, CeilingLights, ceiling_light_1 and LightDust (GPUParticles3D)",
			_player != null and _switch != null and _ceiling_lights != null and _light_1 != null and _dust != null):
		return false
	_check("LightDust.ceiling_lights is wired to CeilingLights", _dust.get("ceiling_lights") == _ceiling_lights)  # The listener must follow the real keeper
	_sampler = Sampler.new()
	_sampler.process_priority = 1000  # Higher numbers run later: it reads the values after all of this frame's code
	_sampler.process_mode = Node.PROCESS_MODE_ALWAYS  # It keeps recording while the tree is paused
	_sampler.dust = _dust
	root.add_child(_sampler)
	await process_frame  # The nodes' _ready() (and so the listener's connect) runs on this first frame, not inside _initialize()
	# Only now is the scene inside the tree, so global_position can be read
	_check("LightDust stands at %s (got %s)" % [DUST_POSITION, _dust.global_position], _dust.global_position.distance_to(DUST_POSITION) <= POSITION_EPS)  # Under ceiling light 1
	var listeners := _ceiling_lights.lights_changed.get_connections().map(func(c: Dictionary) -> Object: return c["callable"].get_object())
	_check("LightDust listens to CeilingLights.lights_changed", listeners.has(_dust))  # The listener connected in its _ready()
	_ceiling_lights.lights_changed.connect(_on_lights_changed)  # We listen too, only to know when changes happen; the listener connected first, so it runs first
	return true


## Called by CeilingLights.lights_changed, after the listener has already handled the same signal.
## We write down the frame, the state, light 1, and the dust exactly as the listener left it.
func _on_lights_changed(lights_on: bool) -> void:
	_changes.append({
		"frame": Engine.get_process_frames(),  # Which frame the change came on
		"lights_on": lights_on,  # What the keeper announced
		"light_1_visible": _light_1.visible,  # Whether light 1 really followed
		"visible": _dust.visible,  # The dust as the listener left it on this frame
		"emitting": _dust.emitting,
		"restarts": _restart_count(),
	})


## Called by _run(). Assertion 1: the lights start on (start_on), so the dust is shown and emitting, after exactly one restart() from the start-up query.
func _check_scene_load() -> void:
	_check("1 after load: lights are on (got %s)" % _ceiling_lights.is_lights_on(), _ceiling_lights.is_lights_on())  # The game's start state
	_check("1 after load: no lights_changed while standing (got %d)" % _changes.size(), _changes.is_empty())  # Nothing pressed, nothing announced
	_check("1 after load: dust is visible", _dust.is_visible_in_tree())  # Shown from the first frame, not empty
	_check("1 after load: dust is emitting", _dust.emitting)  # And making specks
	_check("1 after load: exactly 1 restart (got %d)" % _restart_count(), _restart_count() == 1)  # The one start-up restart(), which runs preprocess


## Called by _run() before the first F. Holds the real S key (move_back, +Z: the switch is behind the start point) until the switch's
## InteractArea overlaps the player, then releases it and lets the player stop. We only read the area; the brain and the body move the player.
func _walk_to_switch() -> bool:
	var area := _switch.get_node("InteractArea") as Area3D  # The space in front of the switch where F works
	_key(KEY_S, true)  # Press S
	var frames := 0
	while not area.overlaps_body(_player) and frames < WALK_TIMEOUT_FRAMES:  # Until the player is inside the area, or we give up
		await process_frame
		frames += 1
	_key(KEY_S, false)  # Release S
	await _wait_frames(SETTLE_FRAMES)  # The player slows down and stops (it can only drift further toward the wall, deeper into the area)
	return _check("walked to the switch with S in %d frames; player inside InteractArea" % frames, area.overlaps_body(_player))


## Called by _run(). Presses and releases the real F key and waits until the expected number of lights_changed have arrived.
func _press_f_and_wait(expected_changes: int) -> bool:
	_key(KEY_F, true)  # Press F; the brain turns "just pressed" into interact on the next physics frame
	await _wait_frames(KEY_HOLD_FRAMES)
	_key(KEY_F, false)  # Release F
	var frames := 0
	while _changes.size() < expected_changes and frames < SIGNAL_TIMEOUT_FRAMES:  # Until the change arrives, or we give up
		await process_frame
		frames += 1
	return _check("F press %d: lights_changed arrived (%d so far)" % [expected_changes, _changes.size()], _changes.size() == expected_changes)


## Called by _run(). Assertion 2: on the frame the lights go off, the dust is invisible and not emitting, and was not restarted.
func _check_lights_off(change: Dictionary, restarts_before: int) -> void:
	_check("2 F turned the lights off (announced %s, keeper %s, light 1 visible %s)" % [change.lights_on, _ceiling_lights.is_lights_on(), change.light_1_visible],
		not change.lights_on and not _ceiling_lights.is_lights_on() and not change.light_1_visible)
	_check("2 on that frame: dust invisible", not change.visible)  # Invisible at once
	_check("2 on that frame: dust not emitting", not change.emitting)  # And no new births
	_check("2 no restart on lights off (restarts %d -> %d)" % [restarts_before, change.restarts], change.restarts == restarts_before)


## Called by _run(). Assertion 3: after 1 s with the lights off, the dust is still invisible, not emitting, not restarted, with no extra announcement.
func _check_stays_off(restarts_before: int) -> void:
	_check("3 1 s later: dust still invisible", not _dust.is_visible_in_tree())
	_check("3 1 s later: dust still not emitting", not _dust.emitting)
	_check("3 1 s later: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)
	_check("3 1 s later: still one lights_changed (got %d)" % _changes.size(), _changes.size() == 1)


## Called by _run(). Assertion 4: on the frame the lights come on, the dust is shown and emitting, after exactly one restart();
## showing fires visibility_changed too, and that must not add a second restart(). One press, one announcement.
func _check_lights_on(change: Dictionary, restarts_before: int) -> void:
	_check("4 F turned the lights on (announced %s, keeper %s, light 1 visible %s)" % [change.lights_on, _ceiling_lights.is_lights_on(), change.light_1_visible],
		change.lights_on and _ceiling_lights.is_lights_on() and change.light_1_visible)
	_check("4 on that frame: dust visible", change.visible)  # Shown on the same frame
	_check("4 on that frame: dust emitting", change.emitting)  # And making specks
	_check("4 on that frame: exactly 1 restart (restarts %d -> %d)" % [restarts_before, change.restarts], change.restarts == restarts_before + 1)  # Not 0 (emitting = true only), not 2 (visibility_changed again)
	_check("4 a few frames later: still exactly 1 restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before + 1)  # No late second restart
	_check("4 two presses, two lights_changed (got %d)" % _changes.size(), _changes.size() == 2)


## Called by _run(). Assertion 5: while the tree is paused, the dust (PAUSABLE through Base) stops processing and nothing about it changes;
## unpaused, it processes again. Whether the specks really freeze on screen is for the frame strip.
func _check_pause() -> void:
	var restarts_before := _restart_count()
	_check("5 before pause: dust processes", _dust.can_process())
	paused = true  # This test is the SceneTree, so this is get_tree().paused = true
	await _wait_frames(PAUSE_FRAMES)  # The SceneTree still sends process_frame while paused, so we can keep counting
	_check("5 paused: dust does not process", not _dust.can_process())  # Its simulation time stands still
	_check("5 paused: dust still visible and emitting", _dust.is_visible_in_tree() and _dust.emitting)  # The pause hides nothing and stops nothing
	_check("5 paused: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)
	_check("5 paused: lights still on, no lights_changed (got %d)" % _changes.size(), _ceiling_lights.is_lights_on() and _changes.size() == 2)
	paused = false  # We let the tree run again
	await process_frame
	_check("5 unpaused: dust processes again", _dust.can_process())
	_check("5 unpaused: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)  # It carries on; a pause throws nothing away


## Called by _run(). Assertion 6: hidden by other code with the lights on, the dust stops emitting on that frame;
## shown again with the lights on, it restarts exactly once (so preprocess runs again). We stand in for that other code.
func _check_hide() -> void:
	var restarts_before := _restart_count()
	_dust.visible = false  # Hidden by "other code"; the listener hears visibility_changed at once
	_check("6 hidden: emitting stops on that frame", not _dust.emitting)
	_check("6 hidden: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)
	await _wait_frames(HIDE_FRAMES)
	_check("6 still hidden after 0.5 s: not emitting, no restart", not _dust.emitting and _restart_count() == restarts_before)
	_dust.visible = true  # Shown again, lights still on
	_check("6 shown again: emitting on that frame", _dust.emitting)
	_check("6 shown again: exactly 1 restart (restarts %d -> %d)" % [restarts_before, _restart_count()], _restart_count() == restarts_before + 1)
	await _wait_frames(KEY_HOLD_FRAMES)
	_check("6 a few frames later: still exactly 1 restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before + 1)


## Called by _run() last. Assertion 7: over every recorded frame, amount stayed what it loaded with and amount_ratio stayed 1.0.
func _check_amount(amount_at_load: int) -> void:
	var amounts := {}  # Every amount value seen
	var ratios := {}  # Every amount_ratio value seen
	for s in _sampler.samples:
		amounts[s.amount] = true
		ratios[s.amount_ratio] = true
	_check("7 amount never changed: %d frames, values %s (loaded %d)" % [_sampler.samples.size(), amounts.keys(), amount_at_load], amounts.keys() == [amount_at_load])
	_check("7 amount_ratio stayed 1.0: values %s" % [ratios.keys()], ratios.keys().size() == 1 and is_equal_approx(ratios.keys()[0], 1.0))


# ============================================================
# Helper functions: input, waiting, reading and printing
# ============================================================
## Simulates one real key, press or release. It goes through Input and the InputMap, so the player brain reads it as usual.
## The device is the one the InputMap stores for that key (interact's F is stored with device 16, the keyboard id the 4.7 editor writes),
## so the event matches the project's binding exactly as a real key press would.
func _key(physical_keycode: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = physical_keycode
	event.pressed = pressed
	event.device = _device_for(physical_keycode)
	Input.parse_input_event(event)


## Called by _key(). Returns the device id of the InputMap event bound to this physical key, or -1 (all devices) if none is bound.
func _device_for(physical_keycode: Key) -> int:
	for action in InputMap.get_actions():  # We look through every action the project defines
		for e in InputMap.action_get_events(action):
			if e is InputEventKey and (e as InputEventKey).physical_keycode == physical_keycode:  # The binding for this key
				return e.device
	return -1


## Waits this many rendered frames.
func _wait_frames(count: int) -> void:
	for i in count:
		await process_frame


## Reads the listener's restart counter (observation only).
func _restart_count() -> int:
	return int(_dust.get("restart_count"))


## Prints one PASS / FAIL line and counts it; returns ok, so callers can stop early.
func _check(label: String, ok: bool) -> bool:
	print(("  PASS  " if ok else "  FAIL  ") + label)  # One line per check, the same form as the other tests
	if ok:  # If it passed, we add it to the passes
		_passes += 1
	else:  # Otherwise we add it to the failures; _finish() turns them into the exit code
		_failures += 1
	return ok


## Called at the end. Prints the summary line and quits; the exit code is 1 when any check failed.
func _finish() -> void:
	print("== %d passed, %d failed ==" % [_passes, _failures])  # The real counts, so a failure is never reported as "all pass"
	quit(1 if _failures > 0 else 0)  # run-test.sh passes this exit code on
