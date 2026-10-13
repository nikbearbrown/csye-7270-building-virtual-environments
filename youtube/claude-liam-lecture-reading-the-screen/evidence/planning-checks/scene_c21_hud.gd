extends "res://rts_scene.gd"
# C21 (beat B35): the gray filter is on canvas layer 1 at full strength from the first frame (the previous beat ended gray). The health bar sits in its
# own CanvasLayer, first at index 0 (below the filter: it is gray too), then at u = 0.58 the layer index is set to 2 (above the filter: it keeps its colour).
const RAISE_AT := 0.58
var filter_rect: ColorRect
var hud_layer: CanvasLayer

func build() -> void:
	world = L.build_world(self, canvas_size)
	add_child(L.make_player(pct(0.50, 0.56)))
	filter_rect = add_filter_layer("05-gray.gdshader")
	hud_layer = CanvasLayer.new()
	hud_layer.name = "HudLayer"
	hud_layer.layer = 0
	add_child(hud_layer)
	hud_layer.add_child(L.make_hud(canvas_size))

func set_time(t: float) -> void:
	var u := u_of(t)
	uni(filter_rect, "amount", 1.0)
	hud_layer.layer = 2 if u >= RAISE_AT else 0
