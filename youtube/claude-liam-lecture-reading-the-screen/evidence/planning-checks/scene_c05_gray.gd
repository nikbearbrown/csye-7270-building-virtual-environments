extends "res://rts_scene.gd"
# C05 (beat B15): the gray filter (05-gray) on a full-screen ColorRect in a CanvasLayer (layer 1); the player stands in the meadow.
# The `amount` uniform is driven by the "game" (this script): colour drains out of the whole picture between u = 0.62 and 0.95.
const DRAIN_FROM := 0.62
const DRAIN_TO := 0.95
var filter_rect: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	add_child(L.make_player(pct(0.50, 0.56)))
	filter_rect = add_filter_layer("05-gray.gdshader")

func set_time(t: float) -> void:
	uni(filter_rect, "amount", ramp(u_of(t), DRAIN_FROM, DRAIN_TO))
