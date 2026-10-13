extends SceneTree
# Diagnostic: does TIME stop advancing when the window is not being drawn? Print ticks, TIME (decoded), frames drawn and process frames.
const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
var rect: ColorRect
func _initialize() -> void: call_deferred("run")
func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()
func read_time() -> float:
	var c := grab().get_pixel(20, 20)
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
	for i in range(24):
		var t_next := Time.get_ticks_usec() + 500000
		while Time.get_ticks_usec() < t_next:
			await process_frame
		var k := (Time.get_ticks_usec() - t_start) / 1000000.0
		print("t_real=%.3f  TIME=%.3f  ticks=%.3f  drawn=%d  process_frames=%d  focused=%s  mode=%d" % [k, read_time(), Time.get_ticks_usec() / 1000000.0, Engine.get_frames_drawn(), Engine.get_process_frames() - pf0, str(DisplayServer.window_is_focused()), DisplayServer.window_get_mode()])
	quit(0)
