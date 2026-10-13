extends Node
## Act 5 edge probe (scratch copy only). Real keyboard events via Input.parse_input_event: Enter to start, Left held.
var frame := 0
var out := ""
var game: Node = null
func _ready() -> void:
	process_priority = -100
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--out="): out = a.substr(6)
func key(code: Key, down: bool, label: String) -> void:
	var e := InputEventKey.new()
	e.keycode = code
	e.physical_keycode = code
	e.pressed = down
	Input.parse_input_event(e)
	print("INPUT f=%d %s %s" % [frame, label, "DOWN" if down else "UP"])
func shot(label: String) -> void:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(out + "/" + label + ".png")
	var p = game.player
	print("SHOT f=%d %s player.x=%.1f y=%.1f" % [frame, label, p.position.x, p.position.y])
func _process(_d: float) -> void:
	frame += 1
	if game == null:
		game = get_tree().current_scene
		if game and "test_mode" in game: game.test_mode = true
	if frame == 36: key(KEY_ENTER, true, "Enter")
	if frame == 38: key(KEY_ENTER, false, "Enter")
	if frame == 42: key(KEY_LEFT, true, "Left (held)")
	if frame >= 44 and frame <= 110 and frame % 3 == 0: shot("edge-%03d" % frame)
	if frame == 130: get_tree().quit()
