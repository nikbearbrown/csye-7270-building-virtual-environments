class_name LightSwitch
extends Node3D

@export var ceiling_lights: CeilingLights

@onready var _interact_area: Area3D = $InteractArea

func _ready() -> void:
	add_to_group(Humanoid.INTERACTABLE_GROUP)

func can_interact(actor: Node3D) -> bool:
	if ceiling_lights == null:
		return false
	return _interact_area.overlaps_body(actor)

func interact(_actor: Node3D) -> void:
	ceiling_lights.toggle()
