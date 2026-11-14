extends Node
## Presentation only (Assignment 7 visual upgrade): during LUNGE, on the first LUNGE tick and every `interval_ticks`
## ticks after it, leaves a ghost of the wolf's current rig pose: a copy of the Rear and Front parts at their global
## transforms, tinted, at `ghost_alpha`, fading to 0 over `ghost_life` seconds and then freed. No ghost in any other
## state. Reads the wolf (its state and its parts) and never writes it; the ghosts are its own nodes, added to the wolf's
## parent just before the wolf so they draw behind it and stay where they were left. Settings live in wolf.tscn.
## This node comes after the wolf's AnimationPlayer in the scene, so it reads the pose the clip set on the same tick.

@export var interval_ticks := 3
@export_range(0.0, 1.0) var ghost_alpha := 0.4
@export var ghost_life := 0.15
@export var tint := Color(0.55, 0.85, 1.0)

var _lunge_tick := -1   # ticks since LUNGE began; -1 outside LUNGE

@onready var wolf: Wolf = get_parent()
@onready var parts: Array[Sprite2D] = [
	get_node("../Facing/Rig/RearPivot/Rear") as Sprite2D, get_node("../Facing/Rig/FrontPivot/Front") as Sprite2D]


func _physics_process(_delta: float) -> void:
	if wolf.state != Wolf.State.LUNGE:
		_lunge_tick = -1
		return
	_lunge_tick += 1
	if _lunge_tick % interval_ticks == 0:
		_leave_ghost()


func _leave_ghost() -> void:
	var host := wolf.get_parent()
	var ghost := Node2D.new()
	ghost.name = "LungeGhost"
	ghost.modulate = Color(tint, ghost_alpha)
	host.add_child(ghost, true)   # readable names (LungeGhost, LungeGhost2, ...) while several are alive
	host.move_child(ghost, wolf.get_index())
	for part in parts:
		var copy := Sprite2D.new()
		copy.texture = part.texture
		copy.region_enabled = part.region_enabled
		copy.region_rect = part.region_rect
		copy.centered = part.centered
		copy.offset = part.offset
		ghost.add_child(copy)
		copy.global_transform = part.global_transform
	var fade := ghost.create_tween()
	fade.tween_property(ghost, "modulate:a", 0.0, ghost_life)
	fade.tween_callback(ghost.queue_free)
