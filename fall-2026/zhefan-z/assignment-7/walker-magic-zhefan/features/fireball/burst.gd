extends Sprite2D
## FX-BURST: shown for a moment where a fireball ends, then removed.

const DURATION := 0.15


func _ready() -> void:
	await get_tree().create_timer(DURATION, false).timeout
	queue_free()
