extends SceneTree
# Evidence-run copy of render-hint-fixture.gd, edited for the film (original untouched).
# Differences from the example's fixture, all deliberate:
#   1. an explicit WorldEnvironment: Linear tonemap, exposure 1.0, glow/fog/adjustments off, flat background.
#      (The example has no WorldEnvironment node; the engine default applied.)
#   2. the true renderer is read from the engine (RenderingServer.get_current_rendering_method()),
#      not hard-coded as the example's JSON does.
#   3. RGB8 integers, round(c * 255), for the centre pixel of each of the 6 bands.
#   4. the output dir is the first user arg (as in the example); a second user arg names the files.
# Run: godot --path godot --rendering-method <forward_plus|gl_compatibility> --script res://course-series/tests/ev-hint-fixture.gd -- <outdir> <tag>
var viewport: SubViewport
var world: Node3D
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var args := OS.get_cmdline_user_args()
	var output: String = args[0]
	var tag: String = args[1] if args.size() > 1 else "hint"
	viewport = SubViewport.new()
	viewport.size = Vector2i(3840, 2160)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	world = Node3D.new()
	viewport.add_child(world)
	var camera := Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 4.0
	camera.position = Vector3(0, 0, 5)
	world.add_child(camera)
	camera.make_current()
	var environment := Environment.new()
	environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color(0.965, 0.953, 0.925)
	environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	environment.tonemap_exposure = 1.0
	environment.glow_enabled = false
	environment.fog_enabled = false
	environment.adjustment_enabled = false
	var sky := WorldEnvironment.new()
	sky.environment = environment
	world.add_child(sky)
	var texture_image := Image.create(3, 1, false, Image.FORMAT_RGB8)
	for i in range(3):
		var g := float([64, 128, 192][i]) / 255.0
		texture_image.set_pixel(i, 0, Color(g, g, g))
	texture_image.save_png(output + "/gray-three-band.png")
	var texture := ImageTexture.create_from_image(texture_image)
	for row in range(2):
		var node := MeshInstance3D.new()
		var quad := QuadMesh.new()
		quad.size = Vector2(3.0, 0.75)
		node.mesh = quad
		node.position.y = 0.65 if row == 0 else -0.65
		var material := ShaderMaterial.new()
		material.shader = load("res://course-series/shaders/hint.gdshader")
		material.set_shader_parameter("as_color", texture)
		material.set_shader_parameter("as_data", texture)
		material.set_shader_parameter("use_color", row == 0)
		node.material_override = material
		world.add_child(node)
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	image.save_png(output + "/hint_" + tag + ".png")
	var samples := []
	for row in range(2):
		for col in range(3):
			var world_point := Vector3(float(col - 1), 0.65 if row == 0 else -0.65, 0)
			var pixel := camera.unproject_position(world_point)
			var color := image.get_pixel(int(pixel.x), int(pixel.y))
			samples.append({
				"quad": "source_color" if row == 0 else "no_hint (data)",
				"input_byte": [64, 128, 192][col],
				"pixel": [int(pixel.x), int(pixel.y)],
				"rgb8": [roundi(color.r * 255.0), roundi(color.g * 255.0), roundi(color.b * 255.0)],
			})
	var method := RenderingServer.get_current_rendering_method()
	var report := {
		"engine": Engine.get_version_info().string,
		"rendering_method": method,
		"adapter": RenderingServer.get_video_adapter_name(),
		"adapter_vendor": RenderingServer.get_video_adapter_vendor(),
		"adapter_api_version": RenderingServer.get_video_adapter_api_version(),
		"rendering_driver": RenderingServer.get_current_rendering_driver_name(),
		"image_format": image.get_format(),
		"width": image.get_width(),
		"height": image.get_height(),
		"environment": {"tonemap": "Linear", "exposure": 1.0, "glow": false, "fog": false, "adjustments": false},
		"samples": samples,
	}
	var file := FileAccess.open(output + "/hint_" + tag + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t"))
	file.close()
	print("RENDERER ", method, " / ", RenderingServer.get_video_adapter_name(), " / driver ", RenderingServer.get_current_rendering_driver_name())
	print("HINT_SAMPLES ", JSON.stringify(samples))
	viewport.queue_free()
	await process_frame
	quit()
