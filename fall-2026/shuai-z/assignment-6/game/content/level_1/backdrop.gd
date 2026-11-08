@tool
class_name Backdrop
extends Node2D
## Level 1's two painted layers behind the play (content/level_1/art/env.json):
## - the far layer, ENV-SKY-CASTLE: sky, hills and the castle, on a canvas
##   layer behind the world. It does not repeat: it scrolls at FAR_MOTION of
##   the camera, so the one image covers the whole level, and it keeps its
##   screen size when the camera zooms, so the pull-back on the teleport circle
##   never shows its edges;
## - the fields, ENV-FIELDS: wheat meeting meadow, drawn by this node in the
##   world, repeated sideways and scrolling at FIELDS_MOTION of the camera.
## The copies of the fields are drawn side by side rather than as one
## repeating texture, which would bleed the bottom rows into the top edge.
## It runs after the camera (process_priority), so the layers move in the same
## frame as the view and do not lag behind it.

const FIELDS := preload("res://content/level_1/art/fields.png")
const FIELDS_Y := 243.0 ## the top of the fields image, in game px (env.json)
const FIELDS_COPIES := 9 ## from one copy left of the level's start, enough for the view at the end, zoomed out
const FIELDS_MOTION := 0.4 ## of the camera's motion
const FAR_MOTION := 0.0218 ## of the camera's motion; env.json's max_motion_scale for a 7700 px level
const VIEW_WIDTH := 1920.0

@onready var _sky: Sprite2D = $Far/Sky


func _ready() -> void:
	process_priority = 10


func _process(_delta: float) -> void:
	if Engine.is_editor_hint():
		return
	var view_left := view_left_x()
	position.x = view_left * (1.0 - FIELDS_MOTION)
	var spare := _sky.texture.get_width() - VIEW_WIDTH
	_sky.position.x = -clampf(view_left * FAR_MOTION, 0.0, spare)


## The level x at the left edge of the screen.
func view_left_x() -> float:
	return (get_viewport().get_canvas_transform().affine_inverse() * Vector2.ZERO).x


## The fields' drawing, in level px: from its left edge to its right edge.
func fields_span() -> Vector2:
	var width := FIELDS.get_width()
	return Vector2(position.x - width, position.x + (FIELDS_COPIES - 1) * width)


func _draw() -> void:
	var width := FIELDS.get_width()
	for i in FIELDS_COPIES:
		draw_texture(FIELDS, Vector2((i - 1) * width, FIELDS_Y))
