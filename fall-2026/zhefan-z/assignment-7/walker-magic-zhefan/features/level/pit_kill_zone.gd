extends Area2D
## Under the pit gap. Any body that can fail (the player) fails when it enters.

const REASON := "Fell into the dark"


func _ready() -> void:
	collision_layer = 1 << 4   # hazard
	collision_mask = 1 << 1    # player
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node) -> void:
	if body.has_method("fail"):
		body.fail(REASON, true)
