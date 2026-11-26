extends SceneTree

const BASE_SCENE := "res://base.tscn"
const DUST_POSITION := Vector3(0.0, 1.45, -3.20)
const POSITION_EPS := 0.001
const IDLE_FRAMES := 30
const WALK_TIMEOUT_FRAMES := 300
const SETTLE_FRAMES := 20
const KEY_HOLD_FRAMES := 3
const SIGNAL_TIMEOUT_FRAMES := 30
const OFF_WAIT_FRAMES := 60
const PAUSE_FRAMES := 20
const HIDE_FRAMES := 30

var _failures := 0
var _passes := 0
var _player: Humanoid
var _switch: Node3D
var _ceiling_lights: CeilingLights
var _light_1: Light3D
var _dust: GPUParticles3D
var _sampler: Sampler
var _changes: Array[Dictionary] = []


class Sampler extends Node:
	var dust: GPUParticles3D
	var samples: Array[Dictionary] = []

	func _process(_delta: float) -> void:
		samples.append({"amount": dust.amount, "amount_ratio": dust.amount_ratio})


func _initialize() -> void:
	_run()


func _run() -> void:
	if not await _build_scene():
		_finish()
		return
	await _wait_frames(IDLE_FRAMES)
	var amount_at_load := _dust.amount
	_check_scene_load()
	if not await _walk_to_switch():
		_finish()
		return
	var restarts := _restart_count()
	if not await _press_f_and_wait(1):
		_finish()
		return
	_check_lights_off(_changes[0], restarts)
	await _wait_frames(OFF_WAIT_FRAMES)
	_check_stays_off(restarts)
	if not await _press_f_and_wait(2):
		_finish()
		return
	await _wait_frames(KEY_HOLD_FRAMES + 2)
	_check_lights_on(_changes[1], restarts)
	await _check_pause()
	await _check_hide()
	_check_amount(amount_at_load)
	_finish()


func _build_scene() -> bool:
	var base: Node = load(BASE_SCENE).instantiate()
	root.add_child(base)
	_player = base.get_node_or_null("Player") as Humanoid
	_switch = base.get_node_or_null("LightSwitch") as Node3D
	_ceiling_lights = base.get_node_or_null("CeilingLights") as CeilingLights
	_light_1 = base.get_node_or_null("ceiling_light_1") as Light3D
	_dust = base.get_node_or_null("LightDust") as GPUParticles3D
	if not _check("base.tscn has Player, LightSwitch, CeilingLights, ceiling_light_1 and LightDust (GPUParticles3D)",
			_player != null and _switch != null and _ceiling_lights != null and _light_1 != null and _dust != null):
		return false
	_check("LightDust.ceiling_lights is wired to CeilingLights", _dust.get("ceiling_lights") == _ceiling_lights)
	_sampler = Sampler.new()
	_sampler.process_priority = 1000
	_sampler.process_mode = Node.PROCESS_MODE_ALWAYS
	_sampler.dust = _dust
	root.add_child(_sampler)
	await process_frame
	_check("LightDust stands at %s (got %s)" % [DUST_POSITION, _dust.global_position], _dust.global_position.distance_to(DUST_POSITION) <= POSITION_EPS)
	var listeners := _ceiling_lights.lights_changed.get_connections().map(func(c: Dictionary) -> Object: return c["callable"].get_object())
	_check("LightDust listens to CeilingLights.lights_changed", listeners.has(_dust))
	_ceiling_lights.lights_changed.connect(_on_lights_changed)
	return true


func _on_lights_changed(lights_on: bool) -> void:
	_changes.append({
		"frame": Engine.get_process_frames(),
		"lights_on": lights_on,
		"light_1_visible": _light_1.visible,
		"visible": _dust.visible,
		"emitting": _dust.emitting,
		"restarts": _restart_count(),
	})


func _check_scene_load() -> void:
	_check("1 after load: lights are on (got %s)" % _ceiling_lights.is_lights_on(), _ceiling_lights.is_lights_on())
	_check("1 after load: no lights_changed while standing (got %d)" % _changes.size(), _changes.is_empty())
	_check("1 after load: dust is visible", _dust.is_visible_in_tree())
	_check("1 after load: dust is emitting", _dust.emitting)
	_check("1 after load: exactly 1 restart (got %d)" % _restart_count(), _restart_count() == 1)


func _walk_to_switch() -> bool:
	var area := _switch.get_node("InteractArea") as Area3D
	_key(KEY_S, true)
	var frames := 0
	while not area.overlaps_body(_player) and frames < WALK_TIMEOUT_FRAMES:
		await process_frame
		frames += 1
	_key(KEY_S, false)
	await _wait_frames(SETTLE_FRAMES)
	return _check("walked to the switch with S in %d frames; player inside InteractArea" % frames, area.overlaps_body(_player))


func _press_f_and_wait(expected_changes: int) -> bool:
	_key(KEY_F, true)
	await _wait_frames(KEY_HOLD_FRAMES)
	_key(KEY_F, false)
	var frames := 0
	while _changes.size() < expected_changes and frames < SIGNAL_TIMEOUT_FRAMES:
		await process_frame
		frames += 1
	return _check("F press %d: lights_changed arrived (%d so far)" % [expected_changes, _changes.size()], _changes.size() == expected_changes)


func _check_lights_off(change: Dictionary, restarts_before: int) -> void:
	_check("2 F turned the lights off (announced %s, keeper %s, light 1 visible %s)" % [change.lights_on, _ceiling_lights.is_lights_on(), change.light_1_visible],
		not change.lights_on and not _ceiling_lights.is_lights_on() and not change.light_1_visible)
	_check("2 on that frame: dust invisible", not change.visible)
	_check("2 on that frame: dust not emitting", not change.emitting)
	_check("2 no restart on lights off (restarts %d -> %d)" % [restarts_before, change.restarts], change.restarts == restarts_before)


func _check_stays_off(restarts_before: int) -> void:
	_check("3 1 s later: dust still invisible", not _dust.is_visible_in_tree())
	_check("3 1 s later: dust still not emitting", not _dust.emitting)
	_check("3 1 s later: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)
	_check("3 1 s later: still one lights_changed (got %d)" % _changes.size(), _changes.size() == 1)


func _check_lights_on(change: Dictionary, restarts_before: int) -> void:
	_check("4 F turned the lights on (announced %s, keeper %s, light 1 visible %s)" % [change.lights_on, _ceiling_lights.is_lights_on(), change.light_1_visible],
		change.lights_on and _ceiling_lights.is_lights_on() and change.light_1_visible)
	_check("4 on that frame: dust visible", change.visible)
	_check("4 on that frame: dust emitting", change.emitting)
	_check("4 on that frame: exactly 1 restart (restarts %d -> %d)" % [restarts_before, change.restarts], change.restarts == restarts_before + 1)
	_check("4 a few frames later: still exactly 1 restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before + 1)
	_check("4 two presses, two lights_changed (got %d)" % _changes.size(), _changes.size() == 2)


func _check_pause() -> void:
	var restarts_before := _restart_count()
	_check("5 before pause: dust processes", _dust.can_process())
	paused = true
	await _wait_frames(PAUSE_FRAMES)
	_check("5 paused: dust does not process", not _dust.can_process())
	_check("5 paused: dust still visible and emitting", _dust.is_visible_in_tree() and _dust.emitting)
	_check("5 paused: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)
	_check("5 paused: lights still on, no lights_changed (got %d)" % _changes.size(), _ceiling_lights.is_lights_on() and _changes.size() == 2)
	paused = false
	await process_frame
	_check("5 unpaused: dust processes again", _dust.can_process())
	_check("5 unpaused: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)


func _check_hide() -> void:
	var restarts_before := _restart_count()
	_dust.visible = false
	_check("6 hidden: emitting stops on that frame", not _dust.emitting)
	_check("6 hidden: no restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before)
	await _wait_frames(HIDE_FRAMES)
	_check("6 still hidden after 0.5 s: not emitting, no restart", not _dust.emitting and _restart_count() == restarts_before)
	_dust.visible = true
	_check("6 shown again: emitting on that frame", _dust.emitting)
	_check("6 shown again: exactly 1 restart (restarts %d -> %d)" % [restarts_before, _restart_count()], _restart_count() == restarts_before + 1)
	await _wait_frames(KEY_HOLD_FRAMES)
	_check("6 a few frames later: still exactly 1 restart (restarts %d)" % _restart_count(), _restart_count() == restarts_before + 1)


func _check_amount(amount_at_load: int) -> void:
	var amounts := {}
	var ratios := {}
	for s in _sampler.samples:
		amounts[s.amount] = true
		ratios[s.amount_ratio] = true
	_check("7 amount never changed: %d frames, values %s (loaded %d)" % [_sampler.samples.size(), amounts.keys(), amount_at_load], amounts.keys() == [amount_at_load])
	_check("7 amount_ratio stayed 1.0: values %s" % [ratios.keys()], ratios.keys().size() == 1 and is_equal_approx(ratios.keys()[0], 1.0))


func _key(physical_keycode: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = physical_keycode
	event.pressed = pressed
	event.device = _device_for(physical_keycode)
	Input.parse_input_event(event)


func _device_for(physical_keycode: Key) -> int:
	for action in InputMap.get_actions():
		for e in InputMap.action_get_events(action):
			if e is InputEventKey and (e as InputEventKey).physical_keycode == physical_keycode:
				return e.device
	return -1


func _wait_frames(count: int) -> void:
	for i in count:
		await process_frame


func _restart_count() -> int:
	return int(_dust.get("restart_count"))


func _check(label: String, ok: bool) -> bool:
	print(("  PASS  " if ok else "  FAIL  ") + label)
	if ok:
		_passes += 1
	else:
		_failures += 1
	return ok


func _finish() -> void:
	print("== %d passed, %d failed ==" % [_passes, _failures])
	quit(1 if _failures > 0 else 0)
