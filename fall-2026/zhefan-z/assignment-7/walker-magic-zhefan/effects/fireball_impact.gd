extends Node2D
## Effect A, fireball impact (CHANGE-BRIEF rule A6): frees itself 0.9 s after it enters the tree.
## Every emitter setting is in fireball_impact.tscn; this script only removes the instance.

const LIFETIME := 0.9


func _ready() -> void:
	await get_tree().create_timer(LIFETIME, false).timeout
	queue_free()
