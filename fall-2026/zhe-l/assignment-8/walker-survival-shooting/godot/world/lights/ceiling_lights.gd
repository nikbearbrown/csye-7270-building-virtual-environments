class_name CeilingLights
extends Node

const LIGHT_GROUP := &"ceiling_lights"

signal lights_changed(lights_on: bool)

@export var start_on: bool = true

var _lights_on: bool = true

func _ready() -> void:
	_lights_on = start_on
	_apply_to_lights()

func set_lights_on(on: bool) -> void:
	if on == _lights_on:
		return
	_lights_on = on
	_apply_to_lights()
	lights_changed.emit(_lights_on)

func toggle() -> void:
	set_lights_on(not _lights_on)

func is_lights_on() -> bool:
	return _lights_on

func _apply_to_lights() -> void:
	for light in get_tree().get_nodes_in_group(LIGHT_GROUP):
		(light as Light3D).visible = _lights_on
