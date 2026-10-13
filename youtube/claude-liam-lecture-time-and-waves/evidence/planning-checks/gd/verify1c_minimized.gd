extends SceneTree
# Time and Waves, planning check 1c: does TIME advance while the window is minimized (not drawn)?
# The window is minimized at 2 s and restored at 4 s. Printed: wall seconds, TIME read from a pixel, frames drawn, process frames.
# Side finding for the notes: this explains why the first TIME run of an earlier plan was inconclusive (a window that stops being drawn stops TIME).
# Run: godot --path <scratch> --always-on-top --script res://verify1c.gd
const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
var rect: ColorRect
func _initialize() -> void: call_deferred("run")
func read_time() -> float:
	RenderingServer.force_draw(false)
	var c := root.get_texture().get_image().get_pixel(20, 20)
	return roundf(c.r * 255.0) + (roundf(c.g * 255.0) + c.b) / 255.0
func run() -> void:
	root.size = Vector2i(320, 180)
	rect = ColorRect.new()
	rect.position = Vector2(10, 10); rect.size = Vector2(20, 20)
	var sh := Shader.new(); sh.code = ENCODER
	var mat := ShaderMaterial.new(); mat.shader = sh
	rect.material = mat
	root.add_child(rect)
	var t_start := Time.get_ticks_usec()
	var pf0 := Engine.get_process_frames()
	var minimized := false
	var restored := false
	for i in range(14):
		var t_next := Time.get_ticks_usec() + 500000
		while Time.get_ticks_usec() < t_next:
			await process_frame
		var k := (Time.get_ticks_usec() - t_start) / 1000000.0
		if k > 2.0 and not minimized:
			minimized = true
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_MINIMIZED)
			print("-- window minimized at about %.1f s" % k)
		if k > 4.0 and not restored:
			restored = true
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
			print("-- window restored at about %.1f s" % k)
		print("t_real=%.3f  TIME=%.3f  ticks=%.3f  drawn=%d  process_frames=%d  mode=%d" % [k, read_time(), Time.get_ticks_usec() / 1000000.0, Engine.get_frames_drawn(), Engine.get_process_frames() - pf0, DisplayServer.window_get_mode()])
	quit(0)
