extends Node
## Shared by the three capture scenes in this folder (tests/capture/capture_*.tscn). Real windowed runs only:
## open the scene in the editor, run it with F6, press the key. A headless run uses a dummy renderer and cannot
## capture. PNGs and JSON go to fall-2026/zhefan-z/assignment-5/captures/, outside the Godot project.
## Every parameter change is in memory only; no resource is ever saved.
## Process mode is left at the default, so the game under it still pauses with Esc (keys wait until unpaused).

var out_dir := (ProjectSettings.globalize_path("res://") + "/../captures").simplify_path()
var busy := false   # a capture sequence is running; keys are ignored until it ends


func _ready() -> void:
	print(JSON.stringify({"capture_scene": scene_file_path, "out_dir": out_dir, "keys": bindings()}))


## Overridden by each scene: key name -> what it does.
func bindings() -> Dictionary:
	return {}


## Overridden by each scene.
func on_key(_keycode: Key) -> void:
	pass


func _input(event: InputEvent) -> void:
	var key := event as InputEventKey
	if key == null or not key.pressed or key.echo:
		return
	if key.keycode in [KEY_F9, KEY_F10, KEY_F11, KEY_F12]:
		get_viewport().set_input_as_handled()
		if busy:
			print(JSON.stringify({"ignored": OS.get_keycode_string(key.keycode), "why": "a capture is running"}))
		else:
			on_key(key.keycode)


## Waits for the frame to be drawn, saves the viewport as out_dir/file, prints one JSON line, returns the image.
func capture(file: String, info := {}) -> Image:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	DirAccess.make_dir_recursive_absolute(out_dir)
	var path := out_dir.path_join(file)
	var err := img.save_png(path)
	var row := {"capture": file, "path": path, "size": [img.get_width(), img.get_height()], "save": error_string(err)}
	row.merge(info)
	print(JSON.stringify(row))
	return img


## The pixel under a viewport position (floor of the position), printed as one JSON line.
func sample(img: Image, label: String, file: String, pos: Vector2, info := {}) -> Dictionary:
	var px := Vector2i(floori(pos.x), floori(pos.y))
	var row := {"file": file, "label": label, "viewport_position": [pos.x, pos.y], "pixel": [px.x, px.y]}
	if Rect2i(Vector2i.ZERO, img.get_size()).has_point(px):
		var c := img.get_pixelv(px)
		row["rgb8"] = [c.r8, c.g8, c.b8]
	else:
		row["rgb8"] = null
		row["note"] = "outside the image"
	row.merge(info)
	print(JSON.stringify(row))
	return row


func write_json(file: String, data: Variant) -> void:
	DirAccess.make_dir_recursive_absolute(out_dir)
	var path := out_dir.path_join(file)
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		print(JSON.stringify({"json": file, "path": path, "save": error_string(FileAccess.get_open_error())}))
		return
	f.store_string(JSON.stringify(data, "  ") + "\n")
	f.close()
	print(JSON.stringify({"json": file, "path": path, "save": "OK"}))


func rgb8(c: Color) -> Array:
	return [c.r8, c.g8, c.b8]
