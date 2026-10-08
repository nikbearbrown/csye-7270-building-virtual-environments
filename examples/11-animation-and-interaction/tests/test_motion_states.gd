extends SceneTree

# Worst-case xfade is 0.1 s = 6 frames; +2 buffer.
const XFADE_FRAMES := 8
const SETTLE_FRAMES := 40

var _player: CharacterBody3D
var _anim: AnimationTree
var _pb: AnimationNodeStateMachinePlayback
var _all_pass := true


func _initialize() -> void:
	var game: Node = (load("res://game.tscn") as PackedScene).instantiate()
	get_root().add_child(game)
	await process_frame
	_player = game.get_node("Player") as CharacterBody3D
	_anim = _player.get_node("AnimationTree") as AnimationTree
	await _step(SETTLE_FRAMES)
	_pb = _anim.get("parameters/motion/playback") as AnimationNodeStateMachinePlayback
	if _pb == null:
		print("FAIL: could not obtain state machine playback")
		quit(1)
		return
	await _check1()
	await _reset(); await _check2(0)
	await _reset(); await _check2(1)
	await _reset(); await _check3()
	await _reset(); await _check4()
	await _reset(); await _check5()
	print("RESULT: %s" % ("PASS" if _all_pass else "FAIL"))
	quit(0 if _all_pass else 1)


func _step(n: int = 1) -> void:
	for _i in n:
		await physics_frame


func _state() -> StringName:
	return _pb.get_current_node()


func _ok(label: String, passed: bool) -> void:
	print("%s %s" % [("PASS" if passed else "FAIL"), label])
	if not passed:
		_all_pass = false


func _reset() -> void:
	for a: StringName in [&"move_forward", &"move_back", &"move_left", &"move_right", &"jump", &"shoot"]:
		Input.action_release(a)
	Input.action_press(&"reset_position")
	await _step(3)
	Input.action_release(&"reset_position")
	await _step(SETTLE_FRAMES)


# ---------------------------------------------------------------------------
# Check 1: standing → ground; run + jump → jump, fall, ground in order.
# ---------------------------------------------------------------------------
func _check1() -> void:
	_ok("1a: standing is ground", _state() == &"ground")

	# Short run (5 frames) so the player builds a little speed without leaving
	# the starting platform, then jump. Track state from the first loop frame
	# to avoid capturing any pre-jump state that could skew the order check.
	Input.action_press(&"move_forward")
	await _step(5)
	Input.action_press(&"jump")

	var visit: Array[StringName] = []
	for _i in 220:
		await physics_frame
		var s := _state()
		if visit.is_empty() or visit.back() != s:
			visit.append(s)
		if s == &"ground" and visit.has(&"fall") and visit.has(&"jump"):
			break

	Input.action_release(&"jump")
	Input.action_release(&"move_forward")

	var ji := visit.find(&"jump")
	var fi := visit.find(&"fall")
	var gi := visit.rfind(&"ground")
	_ok("1b: jump→fall→ground order", ji >= 0 and fi > ji and gi > fi)


# ---------------------------------------------------------------------------
# Check 2: three consecutive hops; enter jump each hop; no fall while rising;
#          no jump/fall on floor beyond cross-fade + 2 frames.
# ---------------------------------------------------------------------------
func _check2(physics_tick_offset: int) -> void:
	await _step(physics_tick_offset)
	Input.action_press(&"jump")

	var hops_with_jump := 0
	var bad_fall_while_rising := false
	var bad_air_on_floor := false

	var in_air := false
	var entered_jump := false
	var floor_entry_frame := -1

	for frame in 600:
		await physics_frame
		var s := _state()
		var on_floor := _player.is_on_floor()
		var vy := _player.velocity.y

		if not on_floor and vy > 0.0 and s == &"fall":
			bad_fall_while_rising = true

		if on_floor and (s == &"jump" or s == &"fall"):
			if floor_entry_frame < 0:
				floor_entry_frame = frame
			elif frame - floor_entry_frame > XFADE_FRAMES:
				bad_air_on_floor = true
		else:
			floor_entry_frame = -1

		if not on_floor:
			in_air = true
			if s == &"jump":
				entered_jump = true
		elif in_air:
			if entered_jump:
				hops_with_jump += 1
			in_air = false
			entered_jump = false
			if hops_with_jump >= 3:
				break

	Input.action_release(&"jump")
	var offset_label := " (offset %d)" % physics_tick_offset
	_ok("2a: enters jump on each of 3 hops%s" % offset_label, hops_with_jump >= 3)
	_ok("2b: no fall state while velocity.y > 0%s" % offset_label, not bad_fall_while_rising)
	_ok("2c: no jump/fall on floor past cross-fade%s" % offset_label, not bad_air_on_floor)


# ---------------------------------------------------------------------------
# Check 3: direction reversal at full speed stays in ground; run blend
#          falls then rises.
# ---------------------------------------------------------------------------
func _check3() -> void:
	Input.action_press(&"move_forward")
	await _step(60)

	var always_ground := true
	var blend_fell := false
	var blend_rose := false
	var prev_b := float(_anim[&"parameters/motion/ground/run/blend_amount"])
	var min_b := prev_b

	Input.action_release(&"move_forward")
	Input.action_press(&"move_back")

	for _i in 120:
		await physics_frame
		if _state() != &"ground":
			always_ground = false
		var b := float(_anim[&"parameters/motion/ground/run/blend_amount"])
		if b < prev_b - 0.01:
			blend_fell = true
			min_b = minf(min_b, b)
		if blend_fell and b > min_b + 0.05:
			blend_rose = true
		prev_b = b

	Input.action_release(&"move_back")
	_ok("3a: stays in ground during direction reversal", always_ground)
	_ok("3b: ground run blend falls then rises", blend_fell and blend_rose)


# ---------------------------------------------------------------------------
# Check 4: reset while rising leaves jump within cross-fade + 2 frames,
#          then reaches ground.
# ---------------------------------------------------------------------------
func _check4() -> void:
	Input.action_press(&"jump")
	for _i in 90:
		await physics_frame
		if _state() == &"jump" and _player.velocity.y > 2.0:
			break

	Input.action_press(&"reset_position")
	await physics_frame
	Input.action_release(&"reset_position")
	Input.action_release(&"jump")

	var left_jump := false
	for _i in XFADE_FRAMES + 2:
		await physics_frame
		if _state() != &"jump":
			left_jump = true
			break

	var reached_ground := false
	for _i in 60:
		await physics_frame
		if _state() == &"ground":
			reached_ground = true
			break

	_ok("4a: leaves jump within cross-fade after reset", left_jump)
	_ok("4b: reaches ground after reset", reached_ground)


# ---------------------------------------------------------------------------
# Check 5: shooting during a jump keeps gun blend > 0 in air; order unchanged.
# ---------------------------------------------------------------------------
func _check5() -> void:
	Input.action_press(&"shoot")
	await physics_frame
	Input.action_release(&"shoot")
	Input.action_press(&"jump")

	var gun_ok_in_air := false
	var visit: Array[StringName] = [_state()]

	for _i in 200:
		await physics_frame
		var s := _state()
		if visit.back() != s:
			visit.append(s)
		var gun := float(_anim[&"parameters/gun/blend_amount"])
		if (s == &"jump" or s == &"fall") and gun > 0.0:
			gun_ok_in_air = true
		if s == &"ground" and visit.has(&"fall"):
			break

	Input.action_release(&"jump")

	var ji := visit.find(&"jump")
	var fi := visit.find(&"fall")
	var gi := visit.rfind(&"ground")
	_ok("5a: gun blend > 0 while in jump or fall", gun_ok_in_air)
	_ok("5b: jump→fall→ground order preserved with shoot", ji >= 0 and fi > ji and gi > fi)
