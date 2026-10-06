extends SceneTree

# AC-01 checkpoint-pad acceptance test.
# Drives the player exclusively via Input.action_press / action_release.
# Criterion 5 is the only exception: it writes player.position directly and is
# labelled as a constructed fixture throughout.
# Prints one JSON line per criterion; exits 1 if any criterion fails.

var _game: Node3D
var _player: Player
var _pad: Node        # CheckpointPad (Area3D); accessed via get() to avoid type dependency
var _camera: Camera3D
var _all_pass := true

func _initialize() -> void:
	call_deferred("run_tests")

func run_tests() -> void:
	_game = load("res://game.tscn").instantiate()
	root.add_child(_game)
	current_scene = _game
	_player = _game.get_node("Player") as Player
	_pad    = _game.get_node("CheckpointPad")
	_camera = _player.get_node("Target/Camera3D") as Camera3D

	# Let physics settle before any checks
	await physics_frame
	await physics_frame
	await physics_frame

	var r1 := _check_c1()
	_emit(r1)

	var r2 := await _check_c2()
	_emit(r2)

	# C3 drives the player to the pad, so C4/C5 run after activation
	var r3 := await _check_c3()
	_emit(r3)

	var r4 := await _check_c4()
	_emit(r4)

	var r5 := await _check_c5()
	_emit(r5)

	# C6 uses a fresh game instance so the pad is not yet activated
	_teardown()
	await process_frame

	_game = load("res://game.tscn").instantiate()
	root.add_child(_game)
	current_scene = _game
	_player = _game.get_node("Player") as Player
	await physics_frame
	await physics_frame

	var r6 := await _check_c6()
	_emit(r6)

	_teardown()
	await process_frame
	quit(0 if _all_pass else 1)


# ── helpers ──────────────────────────────────────────────────────────────────

func _emit(result: Dictionary) -> void:
	print(JSON.stringify(result))
	if not result.get("pass", false):
		_all_pass = false

func _teardown() -> void:
	_game.process_mode = Node.PROCESS_MODE_DISABLED
	_stop_audio(_game)
	current_scene = null
	_game.queue_free()

func _stop_audio(node: Node) -> void:
	if node is AudioStreamPlayer or node is AudioStreamPlayer2D or node is AudioStreamPlayer3D:
		node.stop()
	for child in node.get_children():
		_stop_audio(child)

# Navigate player toward target_world XZ using camera-relative input actions.
# Returns true while player is more than close_dist from target.
func _navigate_toward(target: Vector3, close_dist: float) -> bool:
	var delta := Vector3(target.x - _player.global_position.x,
	                     0.0,
	                     target.z - _player.global_position.z)
	var dist := delta.length()
	if dist < close_dist:
		for a in [&"move_forward", &"move_back", &"move_left", &"move_right"]:
			Input.action_release(a)
		return false
	delta = delta.normalized()
	var cam_r := _camera.global_basis.x
	cam_r.y = 0.0
	cam_r = cam_r.normalized()
	var cam_f := -_camera.global_basis.z
	cam_f.y = 0.0
	cam_f = cam_f.normalized()
	var mr := delta.dot(cam_r)
	var mf := delta.dot(cam_f)
	for a in [&"move_forward", &"move_back", &"move_left", &"move_right"]:
		Input.action_release(a)
	if mf >  0.15: Input.action_press(&"move_forward")
	elif mf < -0.15: Input.action_press(&"move_back")
	if mr >  0.15: Input.action_press(&"move_right")
	elif mr < -0.15: Input.action_press(&"move_left")
	return true


# ── criteria ─────────────────────────────────────────────────────────────────

func _check_c1() -> Dictionary:
	# C1: pad is an Area3D on walkable floor, 3–6 m from start, not on probe path,
	#     collision footprint >= 1.5 m x 1.5 m.
	var cshape := _pad.get_node("CollisionShape3D") as CollisionShape3D
	var box    := cshape.shape as BoxShape3D
	var fprint_ok := box.size.x >= 1.5 and box.size.z >= 1.5

	var pad_pos: Vector3 = _pad.get("global_position")
	var start   := _player.initial_position
	var horiz   := Vector2(pad_pos.x - start.x, pad_pos.z - start.z).length()
	var dist_ok := horiz >= 3.0 and horiz <= 6.0

	# Not on the probe path (Z ≈ 3.93, X in [-9.5, -4.7])
	var z_close    := absf(pad_pos.z - 3.933) < 0.5
	var x_in_range := pad_pos.x > -9.5 and pad_pos.x < -4.7
	var off_path   := not (z_close and x_in_range)

	# Walkable floor below pad
	var space := root.get_world_3d().direct_space_state
	var qry   := PhysicsRayQueryParameters3D.create(
		pad_pos + Vector3(0, 1.0, 0),
		pad_pos + Vector3(0, -3.0, 0))
	var hit    := space.intersect_ray(qry)
	var on_floor := not hit.is_empty()

	var pass_val := fprint_ok and dist_ok and off_path and on_floor
	return {
		"criterion": 1, "pass": pass_val,
		"footprint_ge_1p5": fprint_ok, "footprint_xz": [box.size.x, box.size.z],
		"dist_from_start_m": snappedf(horiz, 0.001), "dist_in_range": dist_ok,
		"off_probe_path": off_path, "on_walkable_floor": on_floor,
		"pad_pos": [snappedf(pad_pos.x,0.001), snappedf(pad_pos.y,0.001), snappedf(pad_pos.z,0.001)]
	}


func _check_c2() -> Dictionary:
	# C2: before activation, holding reset_position 5 frames → within 0.2 m of level start.
	for _i in range(5):
		Input.action_press(&"reset_position")
		await physics_frame
		await process_frame
	Input.action_release(&"reset_position")

	var dist := _player.global_position.distance_to(_player.initial_position)
	return {
		"criterion": 2, "pass": dist < 0.2,
		"dist_from_start_m": snappedf(dist, 0.0001), "threshold_m": 0.2
	}


func _check_c3() -> Dictionary:
	# C3: player reaches pad (input only) within 600 frames; activation fires exactly once;
	#     re-entering does not fire a second time.
	var pad_pos: Vector3 = _pad.get("global_position")
	var reached_frame := -1
	var nav_actions := [&"move_forward", &"move_back", &"move_left", &"move_right"]

	for frame in range(600):
		await physics_frame
		if (_pad.get("activation_count") as int) > 0:
			reached_frame = frame
			for a in nav_actions:
				Input.action_release(a)
			break
		_navigate_toward(pad_pos, 0.3)
		await process_frame

	if reached_frame < 0:
		for a in nav_actions:
			Input.action_release(a)
		return {
			"criterion": 3, "pass": false,
			"reason": "did_not_reach_pad_within_600_frames",
			"activation_count": _pad.get("activation_count")
		}

	# Walk away so body_exited fires, then walk back to trigger body_entered again
	for _i in range(180):
		await physics_frame
		_navigate_toward(_player.initial_position, 2.0)
		await process_frame
	for a in nav_actions:
		Input.action_release(a)

	# Brief pause so area detects the exit
	for _i in range(10):
		await physics_frame
		await process_frame

	# Walk back into the pad
	for _i in range(200):
		await physics_frame
		_navigate_toward(pad_pos, 0.3)
		await process_frame
	for a in nav_actions:
		Input.action_release(a)

	var count_final := _pad.get("activation_count") as int
	var once_only   := count_final == 1

	return {
		"criterion": 3, "pass": reached_frame >= 0 and once_only,
		"reached_in_frames": reached_frame,
		"activation_count_after_reentry": count_final,
		"once_only": once_only
	}


func _check_c4() -> Dictionary:
	# C4: after activation, holding reset_position 5 frames → within 0.2 m of pad's respawn_point.
	var pad_rs: Vector3 = _pad.get("respawn_point")

	for _i in range(5):
		Input.action_press(&"reset_position")
		await physics_frame
		await process_frame
	Input.action_release(&"reset_position")

	var dist := _player.global_position.distance_to(pad_rs)
	return {
		"criterion": 4, "pass": dist < 0.2,
		"dist_from_pad_respawn_m": snappedf(dist, 0.0001), "threshold_m": 0.2,
		"pad_respawn_point": [snappedf(pad_rs.x,0.001), snappedf(pad_rs.y,0.001), snappedf(pad_rs.z,0.001)]
	}


func _check_c5() -> Dictionary:
	# C5 — CONSTRUCTED FIXTURE (labelled): writes player.position directly to test the
	# fall branch (global_position.y < -12) of the same reset code path.
	# This is not a fall a player would make; it tests the code, not a gameplay scenario.
	var pad_rs: Vector3 = _pad.get("respawn_point")

	# Constructed fixture: teleport player below fall threshold
	_player.position = Vector3(_player.position.x, -13.0, _player.position.z)

	# Wait 2 physics frames; fall branch should trigger in frame 1
	await physics_frame
	await process_frame
	await physics_frame
	await process_frame

	var dist := _player.global_position.distance_to(pad_rs)
	return {
		"criterion": 5, "pass": dist < 0.2,
		"label": "constructed_fixture_fall_branch",
		"note": "player.position written directly; tests code path, not gameplay",
		"dist_from_pad_respawn_m": snappedf(dist, 0.0001), "threshold_m": 0.2
	}


func _check_c6() -> Dictionary:
	# C6: regression — with pad present but NOT activated, reset still returns to level start.
	# (Full regression for input_probe.gd and feature_route.gd: run those scripts separately.)
	var start := _player.initial_position

	# Move player away from start
	for _i in range(80):
		Input.action_press(&"move_forward")
		await physics_frame
		await process_frame
	Input.action_release(&"move_forward")

	var pos_before := _player.global_position
	var moved_ok := pos_before.distance_to(start) > 0.5

	# Hold reset — pad not activated, so respawn_point == initial_position
	for _i in range(5):
		Input.action_press(&"reset_position")
		await physics_frame
		await process_frame
	Input.action_release(&"reset_position")

	var dist := _player.global_position.distance_to(start)
	var reset_ok := dist < 0.2

	return {
		"criterion": 6, "pass": moved_ok and reset_ok,
		"label": "regression_reset_before_pad_activation",
		"moved_before_reset": moved_ok,
		"dist_from_start_after_reset_m": snappedf(dist, 0.0001),
		"note": "full regression: also run input_probe.gd and feature_route.gd"
	}
