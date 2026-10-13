extends "res://rts_scene.gd"
# C02 (beat B03): a plain teal rectangle on the meadow. At u = 0.58 the smallest screen reader (01-window) is switched on and the
# rectangle vanishes: it now shows only what is behind it. The ShaderLab ring around [0.37, 0.21, 0.69, 0.53] marks where it still is.
const SWITCH_ON := 0.58
var rect_node: ColorRect
var reader: ShaderMaterial

func build() -> void:
	world = L.build_world(self, canvas_size)
	rect_node = L.rect(pct(0.38, 0.22), pct(0.30, 0.30), L.TEAL, "Window")
	add_child(rect_node)
	frame_of(rect_node)
	reader = L.mat_file("01-window.gdshader")

func set_time(t: float) -> void:
	rect_node.material = reader if u_of(t) >= SWITCH_ON else null
