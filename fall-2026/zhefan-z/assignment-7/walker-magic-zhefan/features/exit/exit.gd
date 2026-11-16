@tool
extends Area2D
## ENV-EXIT, code-drawn placeholder (the optional generated exit was not made): a tall opening of
## pale daylight at the end of the cave, the first light that is not hers (storyboard P7).
## The node's position is the bottom centre, on the ground surface.

const WIDTH := 26.0
const HEIGHT := 78.0
const DAY := Color("dce6ee")


func _ready() -> void:
	collision_layer = 1 << 4   # hazard/trigger layer
	collision_mask = 1 << 1    # player
	if not Engine.is_editor_hint():
		body_entered.connect(_on_body_entered)
	queue_redraw()


func _draw() -> void:
	# Soft bands from the edge (faint) to the centre (bright), plus a little light spilling on the floor.
	for i in 5:
		var inset := i * 2.0
		var a := 0.12 + 0.17 * i
		draw_rect(Rect2(-WIDTH / 2 + inset, -HEIGHT + inset, WIDTH - 2 * inset, HEIGHT - inset), Color(DAY, a))
	draw_rect(Rect2(-WIDTH, -1, WIDTH * 2, 1), Color(DAY, 0.35))
	draw_rect(Rect2(-WIDTH * 0.75, 0, WIDTH * 1.5, 1), Color(DAY, 0.2))


func _on_body_entered(body: Node) -> void:
	if body.has_method("win"):
		body.win()
