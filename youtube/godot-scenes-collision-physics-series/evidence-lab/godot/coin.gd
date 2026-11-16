extends Area2D
signal collected(value: int)
@export var value := 1
var claimed := false
func _ready() -> void:
    body_entered.connect(_on_body_entered)
func _on_body_entered(body: Node2D) -> void:
    if claimed or not body is CharacterBody2D:
        return
    claimed = true # synchronous guard before the deferred change
    set_deferred("monitoring", false)
    collected.emit(value)
    # This lab keeps the object visible for inspection; a game can animate then queue_free.
