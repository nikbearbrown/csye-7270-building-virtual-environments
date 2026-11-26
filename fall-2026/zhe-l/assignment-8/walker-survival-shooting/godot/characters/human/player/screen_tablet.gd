class_name ScreenTablet
extends Node3D

const TABLET_MOVE_START := 0.0
const TABLET_MOVE_DONE := 1.0

@export var moving_time : float = 0.35

var _screen_allowed := false
var _screen_want_show := false
var _slide_start_transform:= Transform3D.IDENTITY
var _slide_progress := TABLET_MOVE_DONE

@onready var _tablet : TabletDevice = $TabletDevice
@onready var _tablet_shown_place : Marker3D = $ShownSlot
@onready var _tablet_hidden_place : Marker3D = $HiddenSlot

func _ready() -> void:
	_tablet.transform = _tablet_hidden_place.transform


func _process(delta: float) -> void:
	if moving_time <= 0.0:
		_slide_progress = TABLET_MOVE_DONE
	else:
		_slide_progress = move_toward(_slide_progress,TABLET_MOVE_DONE,delta/moving_time)
	var eased := smoothstep(TABLET_MOVE_START,TABLET_MOVE_DONE,_slide_progress)
	var target_place: Marker3D = _tablet_shown_place if _screen_want_show else _tablet_hidden_place
	_tablet.transform = _slide_start_transform.interpolate_with(target_place.transform,eased)
	_update_screen()


func set_shown(shown: bool) -> void:
	if shown == _screen_want_show: return
	_screen_want_show = shown
	_slide_start_transform = _tablet.transform
	_slide_progress = TABLET_MOVE_START


func set_screen_allowed(allowed: bool) -> void:
	_screen_allowed = allowed


func set_screen_image(image: Texture2D) -> void:
	_tablet.set_screen_image(image)


func get_screen_uv(ray_origin: Vector3, ray_direction: Vector3) -> Vector2:
	return _tablet.get_screen_uv(ray_origin, ray_direction)


func _update_screen() -> void:
	var arrived := _slide_progress == TABLET_MOVE_DONE
	var screen_on := _screen_want_show and arrived and _screen_allowed
	_tablet.set_screen_lit(screen_on)
