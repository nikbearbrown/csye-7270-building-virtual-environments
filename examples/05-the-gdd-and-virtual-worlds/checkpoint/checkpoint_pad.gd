class_name CheckpointPad
extends Area3D

var activation_count: int = 0
var respawn_point: Vector3 = Vector3.ZERO

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node3D) -> void:
	if activation_count > 0:
		return
	if not body is Player:
		return
	activation_count += 1
	# Snap XZ to pad centre; use player's Y (floor level when walking in)
	respawn_point = Vector3(global_position.x, body.global_position.y, global_position.z)
	body.respawn_point = respawn_point
