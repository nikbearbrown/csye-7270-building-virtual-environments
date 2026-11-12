extends SceneTree
## Writes the mage run sheet (CHANGE-BRIEF Clip 1): res://assets/sprites/mage/mage_run_sheet.png, 124x69, the two
## Assignment 2 run frames side by side, cell 62x69: cell 0 (x 0-61) = mage_run_contact.png, cell 1 (x 62-123) =
## mage_run_passing.png. Both originals are only read. Pixels are copied unchanged (blit, no filtering), so both cells
## keep the A2 canvas and the feet anchor at (31, 67). Its import settings are in mage_run_sheet.png.import, written by
## hand to match the other mage PNGs; import it once afterwards (--import).
## From fall-2026/zhefan-z/assignment-7/, run once:
##   Godot_v4.7.2-stable_win64_console.exe --headless --path walker-magic-zhefan --script res://tools/pack_run_sheet.gd
## Image.load_from_file prints an engine WARNING ("will not work on export") per source; it is expected here.

const CELLS := ["res://assets/sprites/mage/mage_run_contact.png", "res://assets/sprites/mage/mage_run_passing.png"]
const SHEET := "res://assets/sprites/mage/mage_run_sheet.png"
const CELL := Vector2i(62, 69)


func _initialize() -> void:
	var sheet := Image.create(CELL.x * CELLS.size(), CELL.y, false, Image.FORMAT_RGBA8)
	var sources: Array[Image] = []
	for i in CELLS.size():
		var src := Image.load_from_file(ProjectSettings.globalize_path(CELLS[i]))
		if src == null or src.get_size() != CELL:
			printerr("bad source %s: %s" % [CELLS[i], src.get_size() if src else "null"])
			quit(1)
			return
		src.convert(Image.FORMAT_RGBA8)
		sources.append(src)
		sheet.blit_rect(src, Rect2i(Vector2i.ZERO, CELL), Vector2i(CELL.x * i, 0))
	var err := sheet.save_png(ProjectSettings.globalize_path(SHEET))

	# Read back and compare every pixel of each cell with its source.
	var back := Image.load_from_file(ProjectSettings.globalize_path(SHEET))
	back.convert(Image.FORMAT_RGBA8)
	var mismatches := 0
	for i in CELLS.size():
		for y in CELL.y:
			for x in CELL.x:
				if back.get_pixel(CELL.x * i + x, y) != sources[i].get_pixel(x, y):
					mismatches += 1
	print("wrote %s: save %s; read back %dx%d, pixel mismatches against the sources: %d" % [SHEET, error_string(err),
		back.get_width(), back.get_height(), mismatches])
	quit(0 if err == OK and mismatches == 0 and back.get_size() == Vector2i(124, 69) else 1)
