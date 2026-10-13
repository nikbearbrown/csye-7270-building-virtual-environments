extends "res://rts_scene.gd"
# C18 (beat B32): two windows that each flip the colours (03-invert), A first, B drawn after A and overlapping it.
# B appears at u = 0.30. Flipping twice should give the original colours in the overlap; it stays flipped once, because B reads the same
# copy A read (taken before A was drawn). Overlap region as fractions of the canvas: x 0.38..0.50, y 0.30..0.58.
const B_AT := 0.30
var a: ColorRect
var b: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	a = win(0.16, 0.12, 0.34, 0.46, "03-invert.gdshader", "A")
	b = win(0.38, 0.30, 0.34, 0.46, "03-invert.gdshader", "B")

func set_time(t: float) -> void:
	b.visible = u_of(t) >= B_AT
