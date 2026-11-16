extends SceneTree
var viewport: SubViewport
var world: Node3D
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var output := OS.get_cmdline_user_args()[0]
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
	var texture_image := Image.create(3, 1, false, Image.FORMAT_RGB8)
	for i in range(3): texture_image.set_pixel(i, 0, Color(float([64, 128, 192][i]) / 255.0, float([64, 128, 192][i]) / 255.0, float([64, 128, 192][i]) / 255.0))
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
	RenderingServer.force_draw(false)
	var image := viewport.get_texture().get_image()
	image.save_png(output + "/hint-native-3840.png")
	var samples := []
	for row in range(2):
		for col in range(3):
			var world_point := Vector3(float(col - 1), 0.65 if row == 0 else -0.65, 0)
			var pixel := camera.unproject_position(world_point)
			var color := image.get_pixel(int(pixel.x), int(pixel.y))
			samples.append({"hint": "source_color" if row == 0 else "data", "input_byte": [64, 128, 192][col], "pixel": [pixel.x, pixel.y], "rgb": [color.r, color.g, color.b]})
	var file := FileAccess.open(output + "/hint-samples.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info(), "renderer": RenderingServer.get_video_adapter_name(), "rendering_method": "gl_compatibility", "width": image.get_width(), "height": image.get_height(), "samples": samples}, "\t"))
	file.close()
	print("FIXTURE," + JSON.stringify(samples))
	for node in world.get_children():
		if node is MeshInstance3D: node.material_override.set_shader_parameter("show_screen_grid", true)
	for i in range(4): await process_frame
	RenderingServer.force_draw(false)
	viewport.get_texture().get_image().save_png(output + "/hint-screen-grid-native-3840.png")
	viewport.queue_free()
	await process_frame
	quit()
