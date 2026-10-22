extends Node2D
## UI-CROSSHAIR, code-drawn (not generated): a 9x9 px pale cross with a dark 1 px edge, drawn in
## viewport pixels at the mouse. Neutral colours, because the fire is the only warm thing on screen.

const PALE := Color("e8e6f0")   # hair base: reads on the dark cave
const EDGE := Color("1a1420")   # outline colour


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_HIDDEN


func _exit_tree() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE


func _process(_delta: float) -> void:
	position = get_viewport().get_mouse_position().floor()
	queue_redraw()


func _draw() -> void:
	for c: Color in [EDGE, PALE]:
		var w := 3.0 if c == EDGE else 1.0
		for seg: Array in [[Vector2(-4, 0), Vector2(-1, 0)], [Vector2(2, 0), Vector2(5, 0)],
				[Vector2(0, -4), Vector2(0, -1)], [Vector2(0, 2), Vector2(0, 5)]]:
			draw_line(seg[0] + Vector2(0.5, 0.5), seg[1] + Vector2(0.5, 0.5), c, w)
	draw_rect(Rect2(0, 0, 1, 1), PALE)
