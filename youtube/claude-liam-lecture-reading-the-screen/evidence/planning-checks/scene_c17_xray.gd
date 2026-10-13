extends "res://rts_scene.gd"
# C17 (beat B31): what is in the copy? A miniature lens (02-miniature) shows the copy itself.
# Tree order: World, X (mustard block), Lens, Y (violet block). X is drawn before the lens, Y after it: the lens shows X and not Y.
# At u = 0.76 the lens is moved to the END of the tree: now the copy is taken after Y was drawn, and Y appears in the lens.
const MOVE_AT := 0.76
var lens: ColorRect
var moved := false

func build() -> void:
	world = L.build_world(self, canvas_size)
	add_child(L.rect(pct(0.08, 0.60), pct(0.16, 0.26), L.MUSTARD, "X"))
	lens = win(0.60, 0.06, 0.30, 0.30, "02-miniature.gdshader", "Lens")
	add_child(L.rect(pct(0.52, 0.58), pct(0.16, 0.26), L.VIOLET, "Y"))

func set_time(t: float) -> void:
	var late := u_of(t) >= MOVE_AT
	if late and not moved:
		move_child(lens, get_child_count() - 1)
		moved = true
	elif not late and moved:
		move_child(lens, get_child_count() - 2)       # back in front of Y
		moved = false
