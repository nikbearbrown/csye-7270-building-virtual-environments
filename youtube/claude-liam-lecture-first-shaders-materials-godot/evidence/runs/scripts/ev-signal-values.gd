extends SceneTree
# Evidence-run copy of the `signal` part of render-material-evidence.gd (original untouched).
# Same fixed orthographic camera, Linear tonemap, exposure 1.0, directional light, ambient 0.35 white,
# one 3 x 2 quad with signal.gdshader at activation 0, 0.5, 1, 2 (2 is outside hint_range, set from code),
# two sample pixels (UV.x 0.15625 dark stripe, 0.21875 light stripe), RGB8 readback = round(c * 255).
# Only changes: the true renderer is read from the engine; file names carry a tag; JSON also keeps the float readback.
# Run: godot --path godot --rendering-method <forward_plus|gl_compatibility> --script res://course-series/tests/ev-signal-values.gd -- <outdir> <tag> <png_prefix>
var viewport: SubViewport
var camera: Camera3D
var world: Node3D
var output: String
func _initialize() -> void: call_deferred("run")
func snapshot(file_name: String) -> Image:
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	assert(image.get_size() == Vector2i(3840, 2160))
	assert(image.save_png(output + "/" + file_name + ".png") == OK)
	return image
func run() -> void:
	var args := OS.get_cmdline_user_args()
	output = args[0]
	var tag: String = args[1]
	var prefix: String = args[2]
	viewport = SubViewport.new(); viewport.size = Vector2i(3840, 2160)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport); world = Node3D.new(); viewport.add_child(world)
	camera = Camera3D.new(); camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 4.0; camera.position = Vector3(0, 0, 5); world.add_child(camera); camera.make_current()
	var environment := Environment.new(); environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color("14262d"); environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	environment.tonemap_exposure = 1.0; environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color.WHITE; environment.ambient_light_energy = 0.35
	var sky := WorldEnvironment.new(); sky.environment = environment; world.add_child(sky)
	var light := DirectionalLight3D.new(); light.rotation_degrees = Vector3(-30, -30, 0); world.add_child(light)
	var quad := MeshInstance3D.new(); var mesh := QuadMesh.new(); mesh.size = Vector2(3, 2); quad.mesh = mesh
	var signal_material := ShaderMaterial.new(); signal_material.shader = load("res://course-series/shaders/signal.gdshader")
	quad.material_override = signal_material; world.add_child(quad)
	var rows := []
	for value in [0.0, 0.5, 1.0, 2.0]:
		signal_material.set_shader_parameter("activation", value)
		var image: Image = await snapshot(prefix + "_" + str(value))
		var pixels := []
		for u in [0.15625, 0.21875]:
			var pos := camera.unproject_position(Vector3((u - 0.5) * 3.0, 0, 0))
			var color := image.get_pixel(int(pos.x), int(pos.y))
			pixels.append({"uv_x": u, "pixel": [int(pos.x), int(pos.y)], "rgb8": [roundi(color.r * 255), roundi(color.g * 255), roundi(color.b * 255)], "float": [color.r, color.g, color.b]})
		rows.append({"set_value": value, "readback": signal_material.get_shader_parameter("activation"), "samples": pixels})
	var report := {
		"engine": Engine.get_version_info().string,
		"rendering_method": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"rendering_driver": RenderingServer.get_current_rendering_driver_name(),
		"tag": tag, "tonemap": "Linear", "exposure": 1.0, "size": [3840, 2160], "rows": rows,
	}
	var file := FileAccess.open(output + "/signal_values_" + tag + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t")); file.close()
	print("RENDERER ", report.rendering_method, " / ", report.adapter, " / driver ", report.rendering_driver)
	for row in rows:
		print("SIGNAL ", row.set_value, " ", JSON.stringify(row.samples.map(func(s): return s.rgb8)))
	viewport.queue_free(); await process_frame; quit()
