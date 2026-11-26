class_name PlayerController
extends Node3D

const PLAYER_GROUP := &"players"
const THIRD_PERSON_BLEND := 0.0
const FIRST_PERSON_BLEND := 1.0

@export var mouse_sensitivity: float = 0.0025
@export_range(-89.0, 0.0) var pitch_min_degrees: float = -70.0
@export_range(0.0, 89.0) var pitch_max_degrees: float = 60.0
@export var tablet_long_press_seconds: float = 0.4
@export var aim_transition_seconds: float = 0.15
@export var tablet_transition_seconds: float = 0.35
@export_range(0.0, 1.0) var hide_body_at_blend: float = 0.7
@export var normal_fov: float = 75.0
@export var tablet_view_fov: float = 40.0

var _look_delta := Vector2.ZERO
var _tablet_held_seconds := 0.0
var _view_blend := THIRD_PERSON_BLEND
var _view_target := THIRD_PERSON_BLEND
var _view_transition_seconds := 0.0
var _view_is_tablet := false

@onready var _body: Humanoid = get_parent() as Humanoid
@onready var _camera_pivot: Node3D = $CameraPivot
@onready var _shoulder_arm: SpringArm3D = $CameraPivot/ShoulderArm
@onready var _spring_arm: SpringArm3D = $CameraPivot/ShoulderArm/SpringArm3D
@onready var _third_person_position: Marker3D = $CameraPivot/ShoulderArm/SpringArm3D/ThirdPersonCameraPosition
@onready var _first_person_position: Marker3D = $CameraPivot/FirstPersonCameraPosition
@onready var _tablet_camera_position: Marker3D = $CameraPivot/TabletCameraPosition
@onready var _camera: Camera3D = $PlayerCamera
@onready var _screen_tablet: ScreenTablet = $ScreenTabletLayer/SubViewportContainer/SubViewport/ScreenTablet
@onready var _tablet_os_viewport: SubViewport = $TabletOSViewport
@onready var _screen_tablet_container: SubViewportContainer = $ScreenTabletLayer/SubViewportContainer
@onready var _screen_tablet_camera: Camera3D = $ScreenTabletLayer/SubViewportContainer/SubViewport/ScreenTabletCamera


func _ready() -> void:
	_body.add_to_group(PLAYER_GROUP)
	_shoulder_arm.add_excluded_object(_body.get_rid())
	_spring_arm.add_excluded_object(_body.get_rid())
	_camera.make_current()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	_body.tablet_hold_changed.connect(_on_tablet_hold_changed)
	if not _body.is_node_ready():
		await _body.ready
	var tablet_os_image := _tablet_os_viewport.get_texture()
	_body.get_tablet().set_screen_image(tablet_os_image)
	_screen_tablet.set_screen_image(tablet_os_image)


func _input(event: InputEvent) -> void:
	if event is InputEventKey and _body.get_tablet_hold() == Humanoid.TabletHold.TWO_HAND:
		_send_key_to_tablet_os(event)
		get_viewport().set_input_as_handled()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouse and _is_holding_tablet():
		_send_mouse_to_tablet_os(event)
		return
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		_look_delta += (event as InputEventMouseMotion).relative
	elif event.is_action_pressed(&"ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	elif event is InputEventMouseButton and event.pressed and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		if not _is_holding_tablet():
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


func _physics_process(delta: float) -> void:
	_rotate_camera()
	var intent := _read_intent(delta)
	_body.apply_intent(intent, delta)
	_screen_tablet.set_screen_allowed(_body.is_tablet_screen_lit())
	_update_view(intent.aim)


func _process(delta: float) -> void:
	_move_view_blend(delta)
	_update_camera()


func _rotate_camera() -> void:
	_camera_pivot.rotation.y -= _look_delta.x * mouse_sensitivity
	_camera_pivot.rotation.x = clampf(
		_camera_pivot.rotation.x - _look_delta.y * mouse_sensitivity,
		deg_to_rad(pitch_min_degrees), deg_to_rad(pitch_max_degrees))
	_look_delta = Vector2.ZERO


func _read_intent(delta: float) -> CharacterIntent:
	var intent := CharacterIntent.new()
	var hold := _body.get_tablet_hold()
	var raising := _body.is_raising_tablet()
	intent.look_yaw = _camera_pivot.global_rotation.y
	if hold != Humanoid.TabletHold.TWO_HAND and not raising:
		intent.move = Input.get_vector(&"move_left", &"move_right", &"move_back", &"move_forward")
	if hold == Humanoid.TabletHold.NONE and not raising:
		intent.sprint = Input.is_action_pressed(&"sprint")
		intent.jump = Input.is_action_just_pressed(&"jump")
		intent.aim = Input.is_action_pressed(&"aim")
		intent.interact = Input.is_action_just_pressed(&"interact")
	intent.tablet_press = _read_tablet_press(delta)
	return intent


func _read_tablet_press(delta: float) -> CharacterIntent.TabletPress:
	if Input.is_action_pressed(&"tablet"):
		var before := _tablet_held_seconds
		_tablet_held_seconds += delta
		if before < tablet_long_press_seconds and _tablet_held_seconds >= tablet_long_press_seconds:
			return CharacterIntent.TabletPress.LONG
		return CharacterIntent.TabletPress.NONE
	var is_short := _tablet_held_seconds > 0.0 and _tablet_held_seconds < tablet_long_press_seconds
	_tablet_held_seconds = 0.0
	return CharacterIntent.TabletPress.SHORT if is_short else CharacterIntent.TabletPress.NONE


func _send_key_to_tablet_os(event: InputEventKey) -> void:
	if event.is_action(&"tablet"):
		return
	_tablet_os_viewport.push_input(event)


func _send_mouse_to_tablet_os(event: InputEventMouse) -> void:
	var screen_uv := _get_mouse_screen_uv(event)
	if screen_uv == TabletDevice.NOT_ON_SCREEN:
		return
	var os_event := event.duplicate() as InputEventMouse
	os_event.position = screen_uv * Vector2(_tablet_os_viewport.size)
	os_event.global_position = os_event.position
	_tablet_os_viewport.push_input(os_event, true)
	if _body.get_tablet_hold() != Humanoid.TabletHold.TWO_HAND:
		_tablet_os_viewport.gui_release_focus()


func _get_mouse_screen_uv(event: InputEventMouse) -> Vector2:
	if _body.get_tablet_hold() == Humanoid.TabletHold.ONE_HAND:
		var event_in_box := _screen_tablet_container.make_input_local(event) as InputEventMouse
		var mouse_in_view := event_in_box.position / _screen_tablet_container.stretch_shrink
		var small_ray_origin := _screen_tablet_camera.project_ray_origin(mouse_in_view)
		var small_ray_direction := _screen_tablet_camera.project_ray_normal(mouse_in_view)
		return _screen_tablet.get_screen_uv(small_ray_origin, small_ray_direction)
	var ray_origin := _camera.project_ray_origin(event.position)
	var ray_direction := _camera.project_ray_normal(event.position)
	return _body.get_tablet().get_screen_uv(ray_origin, ray_direction)


func _is_holding_tablet() -> bool:
	return _body.get_tablet_hold() != Humanoid.TabletHold.NONE


func _on_tablet_hold_changed(_old_hold: Humanoid.TabletHold, new_hold: Humanoid.TabletHold) -> void:
	_look_delta = Vector2.ZERO
	if _is_holding_tablet():
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	else:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	_screen_tablet.set_shown(new_hold == Humanoid.TabletHold.ONE_HAND)
	if _is_holding_tablet():
		_tablet_os_viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	else:
		_tablet_os_viewport.render_target_update_mode = SubViewport.UPDATE_DISABLED
	if new_hold != Humanoid.TabletHold.TWO_HAND:
		_tablet_os_viewport.gui_release_focus()


func _update_view(aiming: bool) -> void:
	if _body.get_tablet_hold() == Humanoid.TabletHold.TWO_HAND:
		_view_target = FIRST_PERSON_BLEND
		_view_transition_seconds = tablet_transition_seconds
		_view_is_tablet = true
	elif aiming:
		_view_target = FIRST_PERSON_BLEND
		_view_transition_seconds = aim_transition_seconds
		_view_is_tablet = false
	else:
		_view_target = THIRD_PERSON_BLEND


func _move_view_blend(delta: float) -> void:
	if _view_transition_seconds <= 0.0:
		_view_blend = _view_target
	else:
		_view_blend = move_toward(_view_blend, _view_target, delta / _view_transition_seconds)
	_body.set_visual_visible(_view_blend < hide_body_at_blend)


func _update_camera() -> void:
	var eased := smoothstep(THIRD_PERSON_BLEND, FIRST_PERSON_BLEND, _view_blend)
	_camera.global_transform = _third_person_position.global_transform.interpolate_with(
		_get_first_person_transform(), eased)
	_camera.fov = lerpf(normal_fov, tablet_view_fov, eased) if _view_is_tablet else normal_fov


func _get_first_person_transform() -> Transform3D:
	if not _view_is_tablet:
		return _first_person_position.global_transform
	var yaw := _camera_pivot.global_rotation.y
	var level_pivot := Transform3D(Basis.from_euler(Vector3(0.0, yaw, 0.0)), _camera_pivot.global_position)
	return level_pivot * _tablet_camera_position.transform

