extends "res://rts_scene.gd"
# C06 (beats B16 and B17): the spotlight with the naive distance (06-spotlight-oval). The player walks one lap of a flat ellipse
# around the middle of the screen; every frame the game sends the player's position, as a screen address, to the filter.
# The lit area is an OVAL: measured on a 1280 x 720 canvas at radius 0.25 it reaches 320 px sideways and 180 px up and down.
const CENTER := Vector2(0.50, 0.50)
const LAP := Vector2(0.20, 0.12)         # half width, half height of the player's path, as fractions of the canvas
var player: Sprite2D
var filter_rect: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	player = L.make_player(pct(CENTER.x, CENTER.y))
	player.name = "Player"
	add_child(player)
	filter_rect = add_filter_layer(shader_name())
	uni(filter_rect, "radius", 0.25)

func shader_name() -> String:
	return "06-spotlight-oval.gdshader"

func set_time(t: float) -> void:
	var a := TAU * u_of(t) + PI          # one lap per beat, starting on the left
	player.position = pct(CENTER.x + LAP.x * cos(a), CENTER.y + LAP.y * sin(a))

func _process(_delta: float) -> void:
	var size := get_viewport_rect().size
	uni(filter_rect, "player", player.get_global_transform_with_canvas().origin / size)
