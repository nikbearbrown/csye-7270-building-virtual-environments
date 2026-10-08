extends SceneTree

var checks := 0
var failures := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func key(code: Key) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.pressed = true
	root.push_input(event)
	await process_frame
	event = InputEventKey.new()
	event.keycode = code
	root.push_input(event)
	await process_frame

func run() -> void:
	root.size = Vector2i(1280, 720)
	var scene: Node = load("res://control.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	for entry in [["QualitySlider", "scale"], ["FOVSlider", "fov"], ["BrightnessSlider", "adjustment_brightness"], ["ContrastSlider", "adjustment_contrast"], ["SaturationSlider", "adjustment_saturation"]]:
		var slider: HSlider = scene.find_child(entry[0], true, false)
		slider.grab_focus()
		await key(KEY_END)
		check(is_equal_approx(slider.value, slider.max_value), entry[0] + " keyboard maximum")
		var actual: float
		if entry[1] == "scale":
			actual = root.scaling_3d_scale
		elif entry[1] == "fov":
			actual = scene.camera.fov
		else:
			actual = scene.world_environment.environment.get(entry[1])
		check(is_equal_approx(actual, slider.value), entry[0] + " connected state")
		await key(KEY_HOME)
		check(is_equal_approx(slider.value, slider.min_value), entry[0] + " keyboard minimum")
	var button: Button = scene.get_node("HideShowButton")
	await click(button)
	check(not scene.get_node("SettingsMenu").visible and button.text == "Show settings", "hide via mouse")
	await click(button)
	check(scene.get_node("SettingsMenu").visible and button.text == "Hide settings", "show via mouse")
	print("RESULT ", checks, " checks, ", failures, " failures; headless state only, no pixel/performance proof")
	scene.queue_free()
	await process_frame
	quit(1 if failures else 0)

func click(button: Button) -> void:
	var event := InputEventMouseButton.new()
	event.position = button.get_global_rect().get_center()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = true
	root.push_input(event)
	await process_frame
	event = InputEventMouseButton.new()
	event.position = button.get_global_rect().get_center()
	event.button_index = MOUSE_BUTTON_LEFT
	root.push_input(event)
	await process_frame
