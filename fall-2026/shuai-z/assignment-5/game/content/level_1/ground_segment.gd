@tool
class_name GroundSegment
extends StaticBody2D
## A block of Level 1's ground. The node's position is its top-left corner, on
## the walk line; it sizes its own collision box from `size`, in the editor
## too. A gap between two segments is a cliff.
## It draws ENV-GROUND (content/level_1/art/env.json): the slab tile along it
## and, at an end marked as a cliff, the cliff piece, whose face is the end of
## the collision box. They are stored at 2 texture px per game px with their
## top 97 px above the walk line, so the grass, the tufts and the wheat stand
## above it and the soil runs to the bottom of the view.
## A cliff piece starts with the tile's first column, so the tiles meet it at
## the start of a period. Between two cliffs the run of tiles is a whole number
## of periods, squeezed or stretched a little to fit; next to one cliff the
## tiles start from it; with none, from the segment's left end. The tiles are
## drawn one by one rather than as one repeating texture, which would bleed the
## soil's bottom rows into the top edge.

const TILE := preload("res://content/level_1/art/ground_tile.png")
const CLIFF_LEFT := preload("res://content/level_1/art/ground_cliff_left.png")
const CLIFF_RIGHT := preload("res://content/level_1/art/ground_cliff_right.png")
const DENSITY := 2.0 ## texture px per game px
const ART_TOP := -97.0 ## the art's top, from the walk line (env.json: y 743, walk line 840)
const TILE_WIDTH := 220.0 ## one period of the tile, in game px
const CLIFF_WIDTH := 235.5 ## a cliff piece, in game px
const CLIFF_FACE := 200.0 ## from the right piece's left edge to its face (the left piece is its mirror)

@export var size := Vector2(1920, 240):
	set(value):
		size = value
		_fit_shape()
		queue_redraw()
@export var cliff_left := false:
	set(value):
		cliff_left = value
		queue_redraw()
@export var cliff_right := false:
	set(value):
		cliff_right = value
		queue_redraw()

var _shape: CollisionShape2D


func _ready() -> void:
	_shape = CollisionShape2D.new()
	add_child(_shape)
	_fit_shape()


## The run of tiles: where it starts, the width of one tile, and how many.
func tile_run() -> Dictionary:
	var from := CLIFF_FACE if cliff_left else 0.0
	var to := size.x - CLIFF_FACE if cliff_right else size.x
	var period := TILE_WIDTH
	var count := ceili((to - from) / TILE_WIDTH)
	if cliff_left and cliff_right:
		count = maxi(roundi((to - from) / TILE_WIDTH), 1)
		period = (to - from) / count
	elif cliff_right:
		from = to - count * TILE_WIDTH
	return {"from": from, "period": period, "count": count}


func _fit_shape() -> void:
	if _shape == null:
		return
	var box := RectangleShape2D.new()
	box.size = size
	_shape.shape = box
	_shape.position = size / 2.0


func _draw() -> void:
	var run := tile_run()
	var height := TILE.get_height() / DENSITY
	for i in int(run.count):
		draw_texture_rect(TILE, Rect2(run.from + i * run.period, ART_TOP, run.period, height), false)
	if cliff_left:
		draw_texture_rect(CLIFF_LEFT, Rect2(CLIFF_FACE - CLIFF_WIDTH, ART_TOP, CLIFF_WIDTH, height), false)
	if cliff_right:
		draw_texture_rect(CLIFF_RIGHT, Rect2(size.x - CLIFF_FACE, ART_TOP, CLIFF_WIDTH, height), false)
