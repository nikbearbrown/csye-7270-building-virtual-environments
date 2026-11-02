# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: runs directly with --script, no scene needed
## Texture-writing script for the A5 hint experiment: writes a 3×1 PNG whose three pixels are the greys 64, 128 and 192 in order (R = G = B).
## Run: godot --headless --path godot --script res://tools/make_hint_greys.gd
## After writing, it reads the file back and checks each pixel; if any is wrong it exits with code 1.

# ============================================================
# Constants: the texture path and the three grey values (CHANGE-BRIEF 2026-11-01 revision, Part 2)
# ============================================================
const OUT_PATH := "res://experiments/hint/hint_greys_3x1.png"  # The output PNG
const GREYS: Array[int] = [64, 128, 192]  # 8-bit grey of the three pixels, left to right
const MAX_BYTE := 255.0  # Maximum of an 8-bit channel, used to turn 0–255 into 0–1

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points)
# ============================================================
## When Godot calls it: once, when the script is loaded with --script and the scene tree is created. Writes the texture, checks it, then quits.
func _init() -> void:
	var img := _make_image()
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT_PATH.get_base_dir()))
	var err := img.save_png(OUT_PATH)
	print("save ", OUT_PATH, " -> ", error_string(err))
	quit(0 if err == OK and _check_saved() else 1)

# ============================================================
# Feature functions: writing and checking the texture
# ============================================================
## Builds a 3×1 RGB8 image; pixel i has R, G and B all equal to GREYS[i].
## Called by _init().
func _make_image() -> Image:
	var img := Image.create_empty(GREYS.size(), 1, false, Image.FORMAT_RGB8)
	for i in GREYS.size():
		var v := GREYS[i] / MAX_BYTE
		img.set_pixel(i, 0, Color(v, v, v))
	return img


## Reads the PNG source file straight back from disk (not through the importer) and checks that each pixel is the expected grey. Returns true if all are right.
## Called by _init() after saving.
func _check_saved() -> bool:
	var img := Image.load_from_file(ProjectSettings.globalize_path(OUT_PATH))
	var ok := img != null and img.get_width() == GREYS.size() and img.get_height() == 1
	for i in GREYS.size():
		if not ok:
			break
		var c := img.get_pixel(i, 0)
		var got := [roundi(c.r * MAX_BYTE), roundi(c.g * MAX_BYTE), roundi(c.b * MAX_BYTE)]
		print("pixel ", i, ": ", got, " expected ", GREYS[i])
		ok = got == [GREYS[i], GREYS[i], GREYS[i]]
	print("check -> ", "PASS" if ok else "FAIL")
	return ok
