extends Node2D
signal approach_requested(actor: Node2D)
@export var locked := true
var is_open := false
var occupants: Dictionary = {}
@onready var sensor: Area2D = $Approach
@onready var solid: CollisionShape2D = $Solid/CollisionShape2D
func _ready() -> void:
    sensor.body_entered.connect(_entered)
    sensor.body_exited.connect(_exited)
func _entered(actor: Node2D) -> void:
    occupants[actor.get_instance_id()] = weakref(actor)
    approach_requested.emit(actor)
func _exited(actor: Node2D) -> void:
    occupants.erase(actor.get_instance_id())
func open() -> void:
    if locked or is_open:
        return
    is_open = true
    solid.set_deferred("disabled", true)
    $Panel.modulate.a = 0.15
func close_when_clear() -> bool:
    for id in occupants.keys():
        if occupants[id].get_ref() == null:
            occupants.erase(id)
    if not occupants.is_empty():
        return false
    is_open = false
    solid.set_deferred("disabled", false)
    $Panel.modulate.a = 1.0
    return true
