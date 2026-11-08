class_name Hearts
extends Control
## One heart for each of Rudy's hearts, full or empty (UI-HEART), side by side,
## drawn at half scale with mipmaps.

const FULL := preload("res://ui/art/UI-HEART-FULL.png")
const EMPTY := preload("res://ui/art/UI-HEART-EMPTY.png")
const DENSITY := 2.0 ## texture px per game px
const SPACING := 60.0

var max_hearts := 3:
	set(value):
		max_hearts = value
		queue_redraw()
var shown := 3: ## how many are full
	set(value):
		shown = value
		queue_redraw()


func _draw() -> void:
	for i in max_hearts:
		var heart := FULL if i < shown else EMPTY
		draw_texture_rect(heart, Rect2(Vector2(i * SPACING, 0.0), heart.get_size() / DENSITY), false)
