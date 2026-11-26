extends SceneTree

const BASE_SCENE := "res://base.tscn"
const FPS := 60
const DUST_LIFETIME_FRAMES := 96
const RING_LIFETIME_FRAMES := 27
const END_TOLERANCE_FRAMES := 2
const FLOOR_TOP := 0.25
const POSITION_EPS := 0.001
const FLOOR_EPS := 0.02
const MIN_JUMP_HEIGHT := 0.5
const MIN_RETRIGGER_DISTANCE := 0.3
const IDLE_FRAMES := 60
const JUMP_HOLD_FRAMES := 3
const GAP_FRAMES := 10
const MOVE_HOLD_FRAMES := 9
const LANDING_TIMEOUT_FRAMES := 180
const STAND_FRAMES := 120

var _failures := 0
var _passes := 0
var _player: Humanoid
var _effect: Node3D
var _dust: GPUParticles3D
var _ring: GPUParticles3D
var _sampler: Sampler
var _landings: Array[Dictionary] = []
var _dust_finished: Array[int] = []
var _ring_finished: Array[int] = []


class Sampler extends Node:
	var player: Humanoid
	var effect: Node3D
	var samples: Array[Dictionary] = []

	func _process(_delta: float) -> void:
		samples.append({
			"pf": Engine.get_physics_frames(),
			"effect_pos": effect.global_position,
			"player_y": player.global_position.y,
		})


func _initialize() -> void:
	_run()


func _run() -> void:
	if not await _build_scene():
		_finish()
		return
	await _wait_frames(IDLE_FRAMES)
	_check_scene_load()
	var load_landings := _landings.size()
	var jump1_start := _sampler.samples.size()
	await _jump(0)
	if not await _wait_for_landings(load_landings + 1):
		_finish()
		return
	_check_first_landing(_landings[load_landings], jump1_start)
	await _wait_frames(GAP_FRAMES)
	await _jump(MOVE_HOLD_FRAMES)
	if not await _wait_for_landings(load_landings + 2):
		_finish()
		return
	await _wait_frames(DUST_LIFETIME_FRAMES + 30)
	_check_retrigger(_landings[load_landings], _landings[load_landings + 1], load_landings)
	var landings_before_stand := _landings.size()
	var finishes_before_stand := _dust_finished.size() + _ring_finished.size()
	var stand_start := _sampler.samples.size()
	await _wait_frames(STAND_FRAMES)
	_check_standing(landings_before_stand, finishes_before_stand, stand_start)
	_check_never_otherwise()
	_finish()


func _build_scene() -> bool:
	var base: Node = load(BASE_SCENE).instantiate()
	root.add_child(base)
	_player = base.get_node_or_null("Player") as Humanoid
	_effect = base.get_node_or_null("LandingDust") as Node3D
	if not _check("base.tscn has Player (Humanoid) and LandingDust (Node3D)", _player != null and _effect != null):
		return false
	_dust = _effect.get_node_or_null("Dust") as GPUParticles3D
	_ring = _effect.get_node_or_null("GroundRing") as GPUParticles3D
	if not _check("LandingDust has Dust and GroundRing", _dust != null and _ring != null):
		return false
	_check("LandingDust.body is wired to Player", _effect.get("body") == _player)
	_sampler = Sampler.new()
	_sampler.process_priority = 1000
	_sampler.player = _player
	_sampler.effect = _effect
	root.add_child(_sampler)
	await process_frame
	var listeners := _player.landed.get_connections().map(func(c: Dictionary) -> Object: return c["callable"].get_object())
	_check("LandingDust listens to Player.landed", listeners.has(_effect))
	_player.landed.connect(_on_player_landed)
	_dust.finished.connect(func() -> void: _dust_finished.append(Engine.get_physics_frames()))
	_ring.finished.connect(func() -> void: _ring_finished.append(Engine.get_physics_frames()))
	return true


func _on_player_landed() -> void:
	_landings.append({
		"pf": Engine.get_physics_frames(),
		"feet": _player.global_position,
		"effect_pos": _effect.global_position,
		"dust": _dust.emitting,
		"ring": _ring.emitting,
	})


func _key(physical_keycode: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = physical_keycode
	event.pressed = pressed
	Input.parse_input_event(event)


func _jump(move_frames: int) -> void:
	if move_frames > 0:
		_key(KEY_D, true)
	_key(KEY_SPACE, true)
	for i in maxi(JUMP_HOLD_FRAMES, move_frames):
		await process_frame
		if i + 1 == JUMP_HOLD_FRAMES:
			_key(KEY_SPACE, false)
		if move_frames > 0 and i + 1 == move_frames:
			_key(KEY_D, false)


func _wait_for_landings(count: int) -> bool:
	for i in LANDING_TIMEOUT_FRAMES:
		if _landings.size() >= count:
			break
		await process_frame
	await process_frame
	return _check("landing %d arrives within %d frames" % [count, LANDING_TIMEOUT_FRAMES], _landings.size() >= count)


func _wait_frames(frames: int) -> void:
	for i in frames:
		await process_frame


func _check_scene_load() -> void:
	var load_frames: Array[int] = []
	for l in _landings:
		load_frames.append(l["pf"])
	_check("1 scene load: no landed signal in the first %d frames (got %d, at physics frames %s)" % [IDLE_FRAMES, _landings.size(), load_frames], _landings.is_empty())
	_check("1 scene load: no Dust or GroundRing burst finished during load (dust %s, ring %s)" % [_dust_finished, _ring_finished],
		_dust_finished.is_empty() and _ring_finished.is_empty())
	var first_pos: Vector3 = _sampler.samples[0]["effect_pos"]
	var last_pos: Vector3 = _sampler.samples[-1]["effect_pos"]
	_check("1 scene load: the effect did not move during load (%s -> %s)" % [first_pos, last_pos], first_pos.is_equal_approx(last_pos))


func _check_first_landing(first: Dictionary, jump_start: int) -> void:
	_check("2 first landing: Dust and GroundRing started by the trigger on the landing frame (dust %s, ring %s)" % [first["dust"], first["ring"]], first["dust"] and first["ring"])
	_check("2 first landing: effect at the feet (effect %s, feet %s)" % [first["effect_pos"], first["feet"]],
		(first["effect_pos"] as Vector3).distance_to(first["feet"]) < POSITION_EPS)
	_check("2 first landing: effect on the floor top y = %s (got %.4f)" % [FLOOR_TOP, first["effect_pos"].y], absf(first["effect_pos"].y - FLOOR_TOP) < FLOOR_EPS)
	var start_pos: Vector3 = _sampler.samples[jump_start]["effect_pos"]
	var start_pf: int = _sampler.samples[jump_start]["pf"]
	var highest := -INF
	var still := true
	for i in range(jump_start, _sampler.samples.size()):
		var s: Dictionary = _sampler.samples[i]
		if s["pf"] >= first["pf"]:
			break
		highest = maxf(highest, s["player_y"])
		still = still and (s["effect_pos"] as Vector3).is_equal_approx(start_pos)
	var flight_finishes := 0
	for pf in _dust_finished + _ring_finished:
		if pf > start_pf and pf < first["pf"]:
			flight_finishes += 1
	_check("3 take-off and flight: the feet rose above %.2f m (highest %.3f), so this was a real jump" % [FLOOR_TOP + MIN_JUMP_HEIGHT, highest], highest > FLOOR_TOP + MIN_JUMP_HEIGHT)
	_check("3 take-off and flight: the effect did not move before the landing frame", still)
	_check("3 take-off and flight: no burst finished during the flight (got %d)" % flight_finishes, flight_finishes == 0)


func _check_retrigger(first: Dictionary, second: Dictionary, load_landings: int) -> void:
	var gap: int = second["pf"] - first["pf"]
	_check("4 retrigger: second landing %d frames (%.3f s) after the first, inside the Dust lifetime of %d frames" % [gap, float(gap) / FPS, DUST_LIFETIME_FRAMES], gap < DUST_LIFETIME_FRAMES)
	_check("5 retrigger: exactly 2 landed signals from the two jumps (got %d)" % (_landings.size() - load_landings), _landings.size() - load_landings == 2)
	var moved := (second["feet"] as Vector3).distance_to(first["feet"])
	_check("5 retrigger: second landing %.3f m from the first (more than %.1f m)" % [moved, MIN_RETRIGGER_DISTANCE], moved > MIN_RETRIGGER_DISTANCE)
	_check("5 retrigger: effect at the new feet (effect %s, feet %s)" % [second["effect_pos"], second["feet"]],
		(second["effect_pos"] as Vector3).distance_to(second["feet"]) < POSITION_EPS)
	_check("5 retrigger: Dust and GroundRing started by the trigger on the second landing frame (dust %s, ring %s)" % [second["dust"], second["ring"]], second["dust"] and second["ring"])
	var dust_after := _finishes_after(_dust_finished, first["pf"])
	var ring_after := _finishes_after(_ring_finished, first["pf"])
	var want_dust: int = second["pf"] + DUST_LIFETIME_FRAMES
	var want_ring := [first["pf"] + RING_LIFETIME_FRAMES, second["pf"] + RING_LIFETIME_FRAMES]
	_check("6 restart: the first Dust burst was cleared: no Dust finish near physics frame %d (Dust finishes %s)" % [first["pf"] + DUST_LIFETIME_FRAMES, dust_after],
		not _has_near(dust_after, first["pf"] + DUST_LIFETIME_FRAMES))
	_check("6 restart: Dust finished exactly once, at physics frame %d +/- %d (Dust finishes %s)" % [want_dust, END_TOLERANCE_FRAMES, dust_after],
		dust_after.size() == 1 and _has_near(dust_after, want_dust))
	_check("6 restart: GroundRing finished once per landing, at %s +/- %d (GroundRing finishes %s)" % [want_ring, END_TOLERANCE_FRAMES, ring_after],
		ring_after.size() == 2 and _has_near(ring_after, want_ring[0]) and _has_near(ring_after, want_ring[1]))


func _check_standing(landings_before: int, finishes_before: int, stand_start: int) -> void:
	var finishes_now := _dust_finished.size() + _ring_finished.size()
	var start_pos: Vector3 = _sampler.samples[stand_start]["effect_pos"]
	var end_pos: Vector3 = _sampler.samples[-1]["effect_pos"]
	_check("7 standing: no landed signal in %d more frames (got %d)" % [STAND_FRAMES, _landings.size() - landings_before], _landings.size() == landings_before)
	_check("7 standing: no burst finished while standing (got %d)" % (finishes_now - finishes_before), finishes_now == finishes_before)
	_check("7 standing: the effect did not move while standing", start_pos.is_equal_approx(end_pos))


func _check_never_otherwise() -> void:
	var landing_frames := {}
	for l in _landings:
		landing_frames[l["pf"]] = true
	var stray: Array[int] = []
	for i in range(1, _sampler.samples.size()):
		var moved := not (_sampler.samples[i]["effect_pos"] as Vector3).is_equal_approx(_sampler.samples[i - 1]["effect_pos"])
		if moved and not landing_frames.has(_sampler.samples[i]["pf"]):
			stray.append(_sampler.samples[i]["pf"])
	_check("whole run: the effect moved only on landing frames (stray frames %s)" % [stray], stray.is_empty())


func _finishes_after(list: Array[int], from_pf: int) -> Array[int]:
	var out: Array[int] = []
	for pf in list:
		if pf > from_pf:
			out.append(pf)
	return out


func _has_near(list: Array[int], want: int) -> bool:
	for pf in list:
		if absi(pf - want) <= END_TOLERANCE_FRAMES:
			return true
	return false


func _check(what: String, ok: bool) -> bool:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if ok:
		_passes += 1
	else:
		_failures += 1
	return ok


func _finish() -> void:
	print("== %d passed, %d failed ==" % [_passes, _failures])
	quit(1 if _failures > 0 else 0)
