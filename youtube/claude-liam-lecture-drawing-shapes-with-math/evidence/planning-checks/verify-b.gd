extends SceneTree
# Scratch verification B for "Drawing Shapes with Math" (not shown in the film).
# Run: godot --path <scratch project> --script res://verify-b.gd -- <absolute path to the film folder>
#   3b. the odd-size edge case again, this time in a SubViewport (verify-a could not resize the window: see run-a-verify-a.log)
#   4.  compile the failing shader (UV inside your own function) and keep the engine's complete message, line numbers included

var film := ""

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func count_teal_row(img: Image, y: int) -> int:
	var n := 0
	for x in range(img.get_width()):
		var c := img.get_pixel(x, y)
		if abs(c.r - 0.3686) < 0.02 and abs(c.g - 0.6392) < 0.02 and abs(c.b - 0.5686) < 0.02: n += 1
	return n

func count_teal_col(img: Image, x: int) -> int:
	var n := 0
	for y in range(img.get_height()):
		var c := img.get_pixel(x, y)
		if abs(c.r - 0.3686) < 0.02 and abs(c.g - 0.6392) < 0.02 and abs(c.b - 0.5686) < 0.02: n += 1
	return n

func sub_render(size: int) -> Image:
	var sub := SubViewport.new()
	sub.size = Vector2i(size, size)
	sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sub)
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(film + "/lab-shaders/17-crosshair.gdshader")
	var m := ShaderMaterial.new()
	m.shader = sh
	for n in ["dot_size", "ring_distance", "ring_width", "arm_gap", "arm_width"]:
		m.set_shader_parameter(n, 0.0)
	m.set_shader_parameter("arm_length", 1.0)
	var r := ColorRect.new()
	r.size = Vector2(size, size)
	r.material = m
	sub.add_child(r)
	await frames(4)
	var img := sub.get_texture().get_image()
	sub.queue_free()
	await frames(2)
	return img

func run() -> void:
	var args := OS.get_cmdline_user_args()
	film = args[0] if args.size() > 0 else ""
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	# 3b: arm_width 0, arm_length 1, all else 0, in an even and an odd SubViewport
	for size: int in [480, 481]:
		var img: Image = await sub_render(size)
		var mid: int = int(size / 2.0)
		out("3b-zero-width-arms", {"view": [img.get_width(), img.get_height()], "middle_row_index": mid,
			"teal_on_middle_row": count_teal_row(img, mid), "teal_on_row_100": count_teal_row(img, 100),
			"teal_on_middle_column": count_teal_col(img, mid)})
	# 4: the failing shader, compiled by drawing it once
	var bad := Shader.new()
	bad.code = FileAccess.get_file_as_string(film + "/lab-shaders/16-uv-inside-function-FAILS.gdshader")
	var rect := ColorRect.new()
	rect.size = Vector2(100, 100)
	var bm := ShaderMaterial.new()
	bm.shader = bad
	rect.material = bm
	root.add_child(rect)
	await frames(3)
	out("4-failing-shader-drawn", {"note": "the engine's messages for this compile are above this line in the log"})
	quit(0)
