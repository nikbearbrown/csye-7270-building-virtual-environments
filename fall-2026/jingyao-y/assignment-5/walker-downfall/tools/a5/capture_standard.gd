extends SceneTree

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var shader := load("res://shaders/standard_generated.gdshader") as Shader
	if shader == null:
		quit(1)
		return
	var names := []
	for entry in shader.get_shader_uniform_list():
		names.append(str(entry.name))
	for name in ["albedo", "normal_scale", "texture_albedo", "texture_roughness", "texture_normal"]:
		if not names.has(name):
			push_error("Missing generated uniform: " + name)
			quit(1)
			return
	var fixture := Node3D.new()
	root.add_child(fixture)
	var box := MeshInstance3D.new()
	box.mesh = BoxMesh.new()
	fixture.add_child(box)
	var material := ShaderMaterial.new()
	material.shader = shader
	material.set_shader_parameter("albedo", Color.WHITE)
	material.set_shader_parameter("roughness", 1.0)
	material.set_shader_parameter("metallic", 0.0)
	material.set_shader_parameter("specular", 0.5)
	material.set_shader_parameter("normal_scale", 1.0)
	material.set_shader_parameter("uv1_scale", Vector3.ONE)
	material.set_shader_parameter("uv1_offset", Vector3.ZERO)
	material.set_shader_parameter("texture_albedo", load("res://textures/cargo_panel/rusty_metal_sheet_diff_1k.png"))
	material.set_shader_parameter("texture_roughness", load("res://textures/cargo_panel/rusty_metal_sheet_rough_1k.png"))
	material.set_shader_parameter("texture_normal", load("res://textures/cargo_panel/rusty_metal_sheet_nor_gl_1k.png"))
	box.material_override = material
	var camera := Camera3D.new()
	fixture.add_child(camera)
	camera.position.z = 3.0
	camera.make_current()
	var light := DirectionalLight3D.new()
	fixture.add_child(light)
	light.rotation_degrees = Vector3(-35, -30, 0)
	for i in range(10):
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://evidence/a5/use-it/standard-generated.png")
	print("STANDARD_SHADER_RENDER_PROBE_OK renderer=", RenderingServer.get_current_rendering_method(), " uniforms=", names)
	fixture.queue_free()
	for i in range(3):
		await process_frame
	quit()

