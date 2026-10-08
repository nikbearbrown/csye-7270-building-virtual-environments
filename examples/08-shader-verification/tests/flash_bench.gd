@tool
extends Node2D
## Static visual bench: no gameplay, input, animation, or timers.

const Art = preload("res://features/player/clawd_art.gd")
@export var draw_clawd := false


func _draw() -> void:
	if draw_clawd:
		Art.paint(self, "idle", 0.5, Vector2.ZERO, 1.0)
	else:
		draw_rect(Rect2(0, 0, 640, 360), Color("f6f3ec"))


func _ready() -> void:
	queue_redraw()
