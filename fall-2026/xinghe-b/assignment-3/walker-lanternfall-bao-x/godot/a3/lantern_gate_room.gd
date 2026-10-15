extends Node3D

# A3-R3: an orbit camera, so the human check can look behind and below the props.
const ORBIT_TARGET := Vector3(0.0, 1.15, 0.0)
const TURN_SPEED := 1.6  # radians per second while Q/E or R/F is held
const ZOOM_SPEED := 6.0  # metres per second while Z/X is held
const PITCH_MIN := deg_to_rad(-50.0)
const PITCH_MAX := deg_to_rad(80.0)
const DISTANCE_MIN := 3.0
const DISTANCE_MAX := 14.0
const DRAG_RADIANS_PER_PIXEL := 0.008
const WHEEL_STEP := 0.5

@onready var stand_in: CharacterBody3D = $StandIn
@onready var camera: Camera3D = $Camera3D
@onready var floor_mesh: MeshInstance3D = $Floor/Mesh

var yaw := 0.0
var pitch := 0.0
var distance := 0.0
var dragging := false

func _ready() -> void:
	_ensure_inputs()
	# Start the orbit from the camera position saved in the scene, so the opening view is unchanged.
	var offset := camera.position - ORBIT_TARGET
	distance = offset.length()
	pitch = asin(offset.y / distance)
	yaw = atan2(offset.x, offset.z)
	_place_camera()

func _process(delta: float) -> void:
	var turn := Input.get_axis("a3_orbit_left", "a3_orbit_right")
	var tilt := Input.get_axis("a3_tilt_down", "a3_tilt_up")
	var zoom := Input.get_axis("a3_zoom_in", "a3_zoom_out")
	if turn != 0.0 or tilt != 0.0 or zoom != 0.0:
		orbit(turn * TURN_SPEED * delta, tilt * TURN_SPEED * delta, zoom * ZOOM_SPEED * delta)

func _physics_process(_delta: float) -> void:
	var axis := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	stand_in.velocity = Vector3(axis.x, 0.0, axis.y) * 2.0
	stand_in.move_and_slide()

func orbit(d_yaw: float, d_pitch: float, d_distance := 0.0) -> void:
	yaw = wrapf(yaw + d_yaw, -PI, PI)
	pitch = clampf(pitch + d_pitch, PITCH_MIN, PITCH_MAX)
	distance = clampf(distance + d_distance, DISTANCE_MIN, DISTANCE_MAX)
	_place_camera()

func _place_camera() -> void:
	camera.position = ORBIT_TARGET + Vector3(sin(yaw) * cos(pitch), sin(pitch), cos(yaw) * cos(pitch)) * distance
	camera.look_at(ORBIT_TARGET)
	# Below the floor's top only its picture is hidden; the floor collider stays.
	floor_mesh.visible = camera.position.y >= 0.0

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_RIGHT:
			dragging = event.pressed
		elif event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_UP:
			orbit(0.0, 0.0, -WHEEL_STEP)
		elif event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			orbit(0.0, 0.0, WHEEL_STEP)
	elif event is InputEventMouseMotion and dragging:
		orbit(-event.relative.x * DRAG_RADIANS_PER_PIXEL, event.relative.y * DRAG_RADIANS_PER_PIXEL)
	elif event.is_action_pressed("debug_collision"):
		get_tree().debug_collisions_hint = not get_tree().debug_collisions_hint
	elif event.is_action_pressed("ui_cancel"):
		get_tree().change_scene_to_file("res://game/main.tscn")

func _ensure_inputs() -> void:
	var keys := {
		"move_left": [KEY_A, KEY_LEFT],
		"move_right": [KEY_D, KEY_RIGHT],
		"move_up": [KEY_W, KEY_UP],
		"move_down": [KEY_S, KEY_DOWN],
		"debug_collision": [KEY_F3],
		"a3_orbit_left": [KEY_Q],
		"a3_orbit_right": [KEY_E],
		"a3_tilt_up": [KEY_R],
		"a3_tilt_down": [KEY_F],
		"a3_zoom_in": [KEY_Z],
		"a3_zoom_out": [KEY_X],
	}
	for action in keys:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for code in keys[action]:
			var key := InputEventKey.new()
			key.physical_keycode = code
			InputMap.action_add_event(action, key)
