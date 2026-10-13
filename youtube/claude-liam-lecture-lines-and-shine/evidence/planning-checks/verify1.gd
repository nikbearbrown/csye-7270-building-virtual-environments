extends SceneTree
# Lines and Shine: GDScript-side checks the Shader Lab cannot do. Prints one RESULT line per check.
#  T1: the tween code shown in the film (set the start, tween the uniform) sweeps the highlight across the sprite:
#      the centre pixel of the blob is white only while the band is over it (expected: |offset| <= thickness 0.1).
#  T2: before any set_shader_parameter, get_shader_parameter("offset") is null; a tween on the uniform then fails ("does not exist").
#  T3: with the start set first, the same tween works and ends at the final value.
# Run (windowed, as the Lab does):  godot --path <scratch project> --script res://verify1.gd

const SHINE_FILE := "res://10-shine.gdshader"
# The film's on-screen code, verbatim (attached to the root node of the scene):
const FILM_SCRIPT := "extends Node2D\nfunc shine():\n\tvar mat: ShaderMaterial = $Sprite.material\n\tmat.set_shader_parameter(\"offset\", -1.5)\n\tcreate_tween().tween_property(mat, \"shader_parameter/offset\", 1.5, 0.8)\n"
const NO_SET_SCRIPT := "extends Node2D\nfunc shine_without_start():\n\tvar mat: ShaderMaterial = $Sprite.material\n\tcreate_tween().tween_property(mat, \"shader_parameter/offset\", 1.5, 0.8)\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func blob_texture(n: int = 128) -> ImageTexture:
	# the same teal blob with two cream eyes and transparent padding as the Lab's "sprite"
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	for y in n:
		for x in n:
			if Vector2(x, y).distance_to(c) < n * 0.30:
				img.set_pixel(x, y, Color("#5FA391"))
	return ImageTexture.create_from_image(img)

func centre_rgb() -> Array:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var p := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	return [snappedf(p.r, 0.001), snappedf(p.g, 0.001), snappedf(p.b, 0.001)]

func make_scene(script_source: String) -> Node2D:
	var holder := Node2D.new()
	var scr := GDScript.new()
	scr.source_code = script_source
	var err := scr.reload()
	if err != OK:
		out("script-error", {"error": err})
	holder.set_script(scr)
	var spr := Sprite2D.new()
	spr.name = "Sprite"
	spr.texture = blob_texture()
	spr.position = Vector2(320, 180)
	spr.scale = Vector2(2.25, 2.25)
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(SHINE_FILE)
	var mat := ShaderMaterial.new()
	mat.shader = sh
	spr.material = mat
	holder.add_child(spr)
	return holder

func run() -> void:
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))

	# ---- T1: the film's tween code
	var scene := make_scene(FILM_SCRIPT)
	root.add_child(scene)
	await frames(3)
	var mat: ShaderMaterial = scene.get_node("Sprite").material
	var before_any_set = mat.get_shader_parameter("offset")
	var resting := centre_rgb()
	scene.call("shine")
	var t := 0.0
	var white_times: Array = []
	var samples: Array = []
	var guard := 0
	while t < 1.0 and guard < 400:
		await process_frame
		guard += 1
		t += root.get_process_delta_time()
		var c := centre_rgb()
		var off = mat.get_shader_parameter("offset")
		samples.append([snappedf(t, 0.001), snappedf(float(off), 0.001), c[0]])
		if c[0] > 0.99 and c[1] > 0.99 and c[2] > 0.99:
			white_times.append(snappedf(t, 0.001))
	var first_white = white_times[0] if white_times.size() > 0 else -1.0
	var last_white = white_times[white_times.size() - 1] if white_times.size() > 0 else -1.0
	out("T1-tween-sweeps-the-highlight", {
		"offset_before_any_set": str(before_any_set),
		"centre_before_call": resting,
		"white_frames": white_times.size(),
		"first_white_s": first_white,
		"last_white_s": last_white,
		"expected_white_window_s": [0.373, 0.427],
		"offset_at_end": snappedf(float(mat.get_shader_parameter("offset")), 0.001),
		"frames_sampled": samples.size()})
	scene.queue_free()
	await frames(3)

	# ---- T2: tween without the start value
	var scene2 := make_scene(NO_SET_SCRIPT)
	root.add_child(scene2)
	await frames(3)
	var mat2: ShaderMaterial = scene2.get_node("Sprite").material
	var before_set = mat2.get_shader_parameter("offset")
	scene2.call("shine_without_start")
	await create_timer(0.5).timeout
	await frames(2)
	out("T2-tween-without-start-value", {
		"get_shader_parameter_before_any_set": str(before_set),
		"centre_after_0.5s": centre_rgb(),
		"reading": "if the engine logged 'The tweened property ... does not exist' above this line, the tween never ran; the centre stays at its resting value"})
	scene2.queue_free()
	quit(0)
