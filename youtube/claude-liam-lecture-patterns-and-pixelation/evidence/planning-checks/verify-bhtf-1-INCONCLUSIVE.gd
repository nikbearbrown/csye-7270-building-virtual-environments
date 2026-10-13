extends SceneTree
# FIRST VERSION of verify-bhtf.gd, kept because its result was inconclusive (see run-bhtf-1-INCONCLUSIVE-window-metric.log).
# Flaw: it measured the bounding box and pixel count of the non-stage pixels inside ONE CELL-SIZED WINDOW at the middle and at the
# corners. A dot grid has one dot's worth of area in ANY window one cell wide, even when the grid is shifted half a cell (the
# window then holds four quarter-dots), so the "rounded" answer (dots centred on grid lines) looked the same as the reference.
# Fixed in verify-bhtf.gd, which labels connected blobs and counts them instead.
# (Only the measuring part is reproduced here; render(), make_tex() and the shader files are the same as in verify-bhtf.gd.)

func dot_box(img: Image, x0: int, y0: int, w: int, h: int) -> Array:
	var minx := 99999
	var maxx := -1
	var miny := 99999
	var maxy := -1
	var n := 0
	for y in range(y0, y0 + h):
		for x in range(x0, x0 + w):
			if not is_stage(img.get_pixel(x, y)):
				n += 1
				minx = mini(minx, x)
				maxx = maxi(maxx, x)
				miny = mini(miny, y)
				maxy = maxi(maxy, y)
	if n == 0:
		return [0, 0, 0]
	return [maxx - minx + 1, maxy - miny + 1, n]

# per variant and texture it printed: dot_middle_w_h_px / dot_top_left / dot_bottom_right / dot_top_right = dot_box(...) of the cell
# window at the middle and at three corners, then "round_in_middle" and "edge_dots_whole" computed from those boxes.
func is_stage(c: Color) -> bool:
	return absf(c.r - 0.851) + absf(c.g - 0.835) + absf(c.b - 0.792) < 0.03
