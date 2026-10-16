extends "res://tests/harness.gd"
## A3-R3: the room's orbit camera can look behind and below the props.
## Drives the real input actions frame by frame; it proves where the camera
## goes and what is hidden, not that a person finds the view useful.

const RoomScene = preload("res://a3/lantern_gate_room.tscn")
const TARGET := Vector3(0.0, 1.15, 0.0)

func _hold(action: String, frames: int) -> void:
	Input.action_press(action)
	for i in frames:
		await process_frame
	Input.action_release(action)
	await process_frame

func _aims_at_target(cam: Camera3D) -> bool:
	var forward := -cam.global_transform.basis.z
	return forward.dot((TARGET - cam.global_position).normalized()) > 0.999

func _floor_hit(room: Node3D) -> String:
	var query := PhysicsRayQueryParameters3D.create(Vector3(3.0, 2.0, 3.0), Vector3(3.0, -2.0, 3.0), 1)
	var hit: Dictionary = room.get_world_3d().direct_space_state.intersect_ray(query)
	return "none" if hit.is_empty() else String(hit.collider.name)

func _hidden_below(cam: Camera3D, floor_mesh: MeshInstance3D) -> bool:
	return cam.global_position.y < 0.0 and not floor_mesh.visible

func run() -> void:
	suite = "a3-camera"
	var room = RoomScene.instantiate()
	root.add_child(room)
	await process_frame
	await physics_frame
	var cam: Camera3D = room.get_node("Camera3D")
	var floor_mesh: MeshInstance3D = room.get_node("Floor/Mesh")
	var floor_shape: CollisionShape3D = room.get_node("Floor/CollisionShape3D")

	check("start-view-unchanged", cam.position.distance_to(Vector3(5.8, 3.8, 7.6)) <= 0.01 and _aims_at_target(cam) and floor_mesh.visible, {"position": str(cam.position)})

	# Held E for 118 frames at 1.6 rad/s turns about 180 degrees.
	await _hold("a3_orbit_right", 118)
	check("half-orbit-reaches-behind", cam.position.z < -1.0 and _aims_at_target(cam) and floor_mesh.visible, {"position": str(cam.position)})

	# Held F long enough to reach the -50 degree limit.
	await _hold("a3_tilt_down", 90)
	await physics_frame
	var pitch_deg := rad_to_deg(asin((cam.position.y - TARGET.y) / cam.position.distance_to(TARGET)))
	check("tilt-goes-below-floor-and-clamps", _hidden_below(cam, floor_mesh) and absf(pitch_deg + 50.0) <= 0.1 and _aims_at_target(cam), {"position": str(cam.position), "pitch_deg": pitch_deg, "floor_mesh_visible": floor_mesh.visible})
	check("floor-collider-stays-while-hidden", not floor_shape.disabled and _floor_hit(room) == "Floor", {"ray_hit": _floor_hit(room)})

	# Mutation: a floor drawn while the camera is below must fail the predicate.
	floor_mesh.visible = true
	check("mutation-floor-shown-below-caught", not _hidden_below(cam, floor_mesh))
	room.orbit(0.0, 0.0)
	check("mutation-floor-shown-below-restored", _hidden_below(cam, floor_mesh))

	await _hold("a3_tilt_up", 150)
	pitch_deg = rad_to_deg(asin((cam.position.y - TARGET.y) / cam.position.distance_to(TARGET)))
	check("tilt-up-clamps-and-floor-returns", absf(pitch_deg - 80.0) <= 0.1 and floor_mesh.visible, {"pitch_deg": pitch_deg})

	await _hold("a3_zoom_out", 200)
	var far := cam.position.distance_to(TARGET)
	await _hold("a3_zoom_in", 200)
	var near := cam.position.distance_to(TARGET)
	check("zoom-clamps-3-to-14-m", absf(far - 14.0) <= 0.01 and absf(near - 3.0) <= 0.01, {"far": far, "near": near})

	# Right-drag: 100 viewport pixels to the right turns the orbit by -0.8 rad
	# (pushed in local coordinates, so the 2D stretch factor does not apply).
	var before: float = room.yaw
	var press := InputEventMouseButton.new()
	press.button_index = MOUSE_BUTTON_RIGHT
	press.pressed = true
	root.push_input(press, true)
	var motion := InputEventMouseMotion.new()
	motion.relative = Vector2(100, 0)
	root.push_input(motion, true)
	var release := InputEventMouseButton.new()
	release.button_index = MOUSE_BUTTON_RIGHT
	release.pressed = false
	root.push_input(release, true)
	await process_frame
	check("right-drag-orbits", absf(angle_difference(before, room.yaw) + 0.8) <= 0.001 and not room.dragging, {"yaw_before": before, "yaw_after": room.yaw})

	room.queue_free()
	await process_frame
	completed = true
