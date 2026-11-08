extends Node
## Scratch check, not part of the game: runs Main in a window, presses F9
## twice with injected key events, and reports the vsync mode and the FPS.

func _ready() -> void:
	add_child((load("res://app/main.tscn") as PackedScene).instantiate())
	_run.call_deferred()


func _mode() -> String:
	return "disabled" if DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED else "enabled (%d)" % DisplayServer.window_get_vsync_mode()


func _press_f9() -> void:
	var e := InputEventKey.new()
	e.keycode = KEY_F9
	e.pressed = true
	Input.parse_input_event(e)
	await get_tree().process_frame
	var r := InputEventKey.new()
	r.keycode = KEY_F9
	r.pressed = false
	Input.parse_input_event(r)
	await get_tree().process_frame


func _fps_over(seconds: float) -> float:
	var frames := 0
	var t0 := Time.get_ticks_usec()
	while Time.get_ticks_usec() - t0 < seconds * 1e6:
		await get_tree().process_frame
		frames += 1
	return frames / ((Time.get_ticks_usec() - t0) / 1e6)


func _run() -> void:
	await get_tree().create_timer(1.0).timeout
	print("CHECK screen refresh rate %.1f Hz; vsync %s; FPS %.1f" % [DisplayServer.screen_get_refresh_rate(), _mode(), await _fps_over(2.0)])
	await _press_f9()
	print("CHECK after one F9: vsync %s; FPS %.1f" % [_mode(), await _fps_over(2.0)])
	await _press_f9()
	print("CHECK after a second F9: vsync %s; FPS %.1f" % [_mode(), await _fps_over(2.0)])
	get_tree().quit()
