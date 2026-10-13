extends "res://rts_scene.gd"
# C03 (beat B08): two 16:9 rectangles slide to the right together.
#  top    02-miniature: texture(screen_texture, UV)        -> a tiny copy of the whole screen that does not move with the picture
#  bottom 01-window:    texture(screen_texture, SCREEN_UV) -> a window: the meadow behind it, wherever it is
# Both read the same copy of the screen (the meadow), so neither shows the other.
const SLIDE_FROM := 0.15
const SLIDE_TO := 0.90
var top: ColorRect
var bottom: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	top = win(0.04, 0.07, 0.28, 0.28, "02-miniature.gdshader", "UvMiniature")
	bottom = win(0.04, 0.60, 0.28, 0.28, "01-window.gdshader", "ScreenUvWindow")

func set_time(t: float) -> void:
	var x := lerpf(0.04, 0.56, ramp(u_of(t), SLIDE_FROM, SLIDE_TO)) * canvas_size.x
	top.position.x = x
	bottom.position.x = x
