extends "res://rts_scene.gd"
# C19 (beat B33): the same two windows, both visible from the start, and a BackBufferCopy (copy mode Viewport) between them.
# The BackBufferCopy is switched on at u = 0.76 (its visible flag): before it the overlap is flipped once, after it the overlap shows the original colours.
const FIX_AT := 0.76
var bbc: BackBufferCopy

func build() -> void:
	world = L.build_world(self, canvas_size)
	win(0.16, 0.12, 0.34, 0.46, "03-invert.gdshader", "A")
	bbc = BackBufferCopy.new()
	bbc.name = "BackBufferCopy"
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	add_child(bbc)
	win(0.38, 0.30, 0.34, 0.46, "03-invert.gdshader", "B")

func set_time(t: float) -> void:
	bbc.visible = u_of(t) >= FIX_AT
