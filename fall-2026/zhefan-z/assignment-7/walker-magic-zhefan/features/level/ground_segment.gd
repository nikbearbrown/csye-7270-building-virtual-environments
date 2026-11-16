@tool
extends StaticBody2D
## A strip of ground: the 37x33 rock tile repeated across `width`, with an optional end cap
## where the strip meets a pit. The node's position is the top-left corner; the top edge is the
## walkable surface (the tile is opaque from its first row).

const TILE := preload("res://assets/sprites/env/cave_ground_tile.png")
const CAP_LEFT := preload("res://assets/sprites/env/cave_ground_cap_left.png")    # rounded left side
const CAP_RIGHT := preload("res://assets/sprites/env/cave_ground_cap_right.png")  # rounded right side
const HEIGHT := 33

@export var width: int = 320:
	set(value):
		width = maxi(value, 16)
		_build()
@export var cap_at_left := false:
	set(value):
		cap_at_left = value
		_build()
@export var cap_at_right := false:
	set(value):
		cap_at_right = value
		_build()


func _ready() -> void:
	collision_layer = 1
	collision_mask = 0
	_build()


func _build() -> void:
	if not is_inside_tree():
		return
	for child in get_children():
		if child.name.begins_with("_Gen"):
			child.free()
	var left := CAP_LEFT.get_width() if cap_at_left else 0
	var right := CAP_RIGHT.get_width() if cap_at_right else 0
	var fill := Sprite2D.new()
	fill.name = "_GenTiles"
	fill.texture = TILE
	fill.centered = false
	fill.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	fill.region_enabled = true
	fill.region_rect = Rect2(0, 0, width - left - right, HEIGHT)
	fill.position = Vector2(left, 0)
	add_child(fill)
	if cap_at_left:
		_add_cap("_GenCapLeft", CAP_LEFT, 0)
	if cap_at_right:
		_add_cap("_GenCapRight", CAP_RIGHT, width - right)
	var shape := CollisionShape2D.new()
	shape.name = "_GenShape"
	var rect := RectangleShape2D.new()
	rect.size = Vector2(width, HEIGHT)
	shape.shape = rect
	shape.position = Vector2(width / 2.0, HEIGHT / 2.0)
	add_child(shape)


func _add_cap(node_name: String, tex: Texture2D, x: int) -> void:
	var cap := Sprite2D.new()
	cap.name = node_name
	cap.texture = tex
	cap.centered = false
	cap.position = Vector2(x, 0)
	add_child(cap)
