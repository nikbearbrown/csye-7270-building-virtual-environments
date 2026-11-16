extends AnimatableBody2D
@export var speed := 60.0
func _ready() -> void:
    sync_to_physics = false # this script already runs on physics ticks
func _physics_process(delta: float) -> void:
    position.x += speed * delta
