extends SceneTree

const OUT := "res://evidence/a5/use-it/"
var report := {}

func _initialize() -> void:
	call_deferred("run")

func frames(count: int = 12) -> void:
	for i in count: await process_frame

func image_now(path: String) -> Image:
	await frames(8)
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.convert(Image.FORMAT_RGB8)
	img.save_png(OUT + path + ".png")
	return img

func rgb(img: Image, pixel: Vector2i) -> Array:
	var c := img.get_pixelv(pixel)
	return [roundi(c.r * 255), roundi(c.g * 255), roundi(c.b * 255)]

func find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null: return found
	return null

func fire() -> void:
	root.borderless = true
	root.size = Vector2i(1280, 720)
	root.position = Vector2i(80, 80)
	root.always_on_top = true
	root.grab_focus()
	await frames(5)
	var rig: Node = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	root.add_child(rig)
	await frames()
	var game := find_game(rig)
	game.fixed_map_seed = 2026
	await game.start_contract("city")
	game.open_modal("capture")
	var at: Vector2 = game.world_map.main_path[0] + Vector2(0, 8)
	game.player.teleport(game.world_map.nearest_walkable(Vector3(at.x, 0.7, at.y)))
	game.camera.size = 24.0
	game.camera.global_position = game.player.global_position + GameManager.CAMERA_OFFSET
	game._hud.hide()
	game.player.hide()
	for hazard in get_nodes_in_group("ground_hazards"): hazard.hide()
	await frames(30)
	var controlled := game.world_environment.environment.duplicate() as Environment
	controlled.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	controlled.tonemap_exposure = 1.0
	controlled.glow_enabled = false
	controlled.fog_enabled = false
	controlled.volumetric_fog_enabled = false
	controlled.adjustment_enabled = false
	controlled.ssao_enabled = false
	controlled.ssil_enabled = false
	controlled.ssr_enabled = false
	game.world_environment.environment = controlled
	game.outline_pass.hide()
	await frames(30)
	var background := await image_now("fire-background")
	var samples := [Vector2i(640, 420), Vector2i(704, 420)]
	var prediction := {"r1": [[210, 210, 67], [186, 186, 67]], "r05": [[158, 121, 67], [142, 110, 67]], "r0": [[58, 58, 67], [59, 58, 67]], "r2": [[210, 255, 67]]}
	report.fire = {"background": [rgb(background, samples[0]), rgb(background, samples[1])], "predictions": prediction, "samples": {}, "uniform_readback": {}, "camera_transform": str(game.camera.global_transform), "camera_size": game.camera.size, "player_position": str(game.player.global_position), "tonemap_mode": controlled.tonemap_mode, "exposure": controlled.tonemap_exposure}
	var panel := MeshInstance3D.new()
	var mesh := QuadMesh.new()
	var cam := game.camera
	var center := Vector2(640.5, 420.5)
	mesh.size = Vector2(cam.project_position(center + Vector2(128, 0), 8).distance_to(cam.project_position(center - Vector2(128, 0), 8)), cam.project_position(center + Vector2(0, 128), 8).distance_to(cam.project_position(center - Vector2(0, 128), 8)))
	panel.mesh = mesh
	panel.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var material := ShaderMaterial.new()
	material.shader = load("res://shaders/burning_bottle_fire.gdshader")
	material.set_shader_parameter("flicker_amount", 0.0)
	panel.material_override = material
	rig.add_child(panel)
	panel.global_transform = Transform3D(cam.global_basis, cam.project_position(center, 8))
	for entry in [["r1", 1.0], ["r05", 0.5], ["r0", 0.0], ["r2", 2.0]]:
		material.set_shader_parameter("fire_remaining", entry[1])
		var img := await image_now("fire-" + entry[0])
		report.fire.samples[entry[0]] = [rgb(img, samples[0]), rgb(img, samples[1])]
		report.fire.uniform_readback[entry[0]] = material.get_shader_parameter("fire_remaining")
		if entry[0] == "r1":
			DisplayServer.window_set_title("Downfall A5 Fire Calibration")
			print("A5_OS_CAPTURE_READY")
			var hold_started := Time.get_ticks_usec()
			while Time.get_ticks_usec() - hold_started < 15000000: await process_frame
	rig.queue_free()
	await frames()

func materials() -> void:
	var scene: Node3D = load("res://tests/material_review.tscn").instantiate()
	root.add_child(scene)
	var a := scene.get_node("PanelA_Mild") as MeshInstance3D
	var b := scene.get_node("PanelB_Weathered") as MeshInstance3D
	var original_a := a.material_override as ShaderMaterial
	var original_b := b.material_override as ShaderMaterial
	var material := original_a.duplicate() as ShaderMaterial
	a.material_override = material
	report.material_sweep = []
	for name_and_values in [["uv_scale", [0.25, 1.0, 8.0]], ["tint_color", [Color.BLACK, Color.WHITE, Color.WHITE]], ["roughness_scale", [0.0, 1.0, 2.0]], ["normal_strength", [0.0, 1.0, 2.0]]]:
		var uniform_name: String = name_and_values[0]
		for light_name in ["review", "raking"]:
			scene.get_node("Sun").visible = light_name == "review"
			scene.get_node("RakingLight").visible = light_name == "raking"
			for index in 3:
				for reset_name in ["uv_scale", "roughness_scale", "normal_strength"]: material.set_shader_parameter(reset_name, 1.0)
				material.set_shader_parameter("tint_color", Color.WHITE)
				var value: Variant = name_and_values[1][index]
				material.set_shader_parameter(uniform_name, value)
				var tag: String = ["min", "default", "max"][index]
				var path := "sweep-%s-%s-%s" % [uniform_name, tag, light_name]
				await image_now(path)
				report.material_sweep.append({"uniform": uniform_name, "setting": tag, "value": str(value), "light": light_name, "image": path + ".png"})
	a.material_override = original_a
	b.material_override = original_b
	scene.get_node("Sun").show()
	scene.get_node("RakingLight").hide()
	await image_now("materials-baseline")
	var changed_a := original_a.duplicate() as ShaderMaterial
	changed_a.set_shader_parameter("tint_color", Color(0.25, 1, 1, 1))
	a.material_override = changed_a
	await image_now("materials-a-only")
	report.material_instances = {"same_shader": original_a.shader == original_b.shader, "different_materials": original_a != original_b, "changed_parameter": "A.tint_color=(0.25,1,1,1)", "B_original": original_b.get_shader_parameter("tint_color")}
	scene.queue_free()
	await frames()

func shader_time() -> void:
	var scene := Node3D.new()
	root.add_child(scene)
	var camera := Camera3D.new()
	camera.position.z = 2
	camera.current = true
	scene.add_child(camera)
	var environment := WorldEnvironment.new()
	environment.environment = Environment.new()
	environment.environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	scene.add_child(environment)
	var panel := MeshInstance3D.new()
	panel.mesh = QuadMesh.new()
	scene.add_child(panel)
	var shader := Shader.new()
	shader.code = "shader_type spatial; render_mode unshaded; void fragment() { float t = mod(floor(TIME * 1000.0), 16777216.0); vec3 bytes = vec3(mod(t,256.0), mod(floor(t/256.0),256.0), floor(t/65536.0))/255.0; ALBEDO = mix(bytes/12.92, pow((bytes+0.055)/1.055,vec3(2.4)), step(vec3(0.04045),bytes)); }"
	var material := ShaderMaterial.new()
	material.shader = shader
	panel.material_override = material
	await frames(30)
	report.shader_time = []
	for scale in [1.0, 0.5, 2.0, 0.0]:
		Engine.time_scale = scale
		await frames(10)
		await RenderingServer.frame_post_draw
		var first := rgb(root.get_texture().get_image(), Vector2i(640, 360))
		var started := Time.get_ticks_usec()
		await frames(120)
		await RenderingServer.frame_post_draw
		var last := rgb(root.get_texture().get_image(), Vector2i(640, 360))
		var duration := (Time.get_ticks_usec() - started) / 1000000.0
		var shader_delta: float = (last[0] + 256 * last[1] + 65536 * last[2] - first[0] - 256 * first[1] - 65536 * first[2]) / 1000.0
		report.shader_time.append({"time_scale": scale, "frames": 120, "wall_seconds": duration, "shader_seconds": shader_delta, "first_rgb8": first, "last_rgb8": last})
	Engine.time_scale = 1.0
	scene.queue_free()
	await frames()

func base() -> void:
	var game := GameManager.new()
	game.save_enabled = false
	game.fixed_map_seed = 1729
	root.add_child(game)
	await frames(60)
	game.open_modal("capture")
	var crates: Array[MeshInstance3D] = []
	var stack: Array[Node] = [game.base_map]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for child in node.get_children(): stack.append(child)
		if node is MeshInstance3D and node.has_meta("model") and str(node.get_meta("model")) == "crate_stack":
			var surface := (node as MeshInstance3D).get_surface_override_material(0)
			if surface is ShaderMaterial and surface.shader.resource_path == "res://shaders/cargo_panel.gdshader": crates.append(node)
	report.base = {"crate_count": crates.size(), "tonemap": game.world_environment.environment.tonemap_mode, "crates": []}
	var center := Vector3.ZERO
	for crate in crates:
		center += crate.global_position
		report.base.crates.append({"position": str(crate.global_position), "material": crate.get_surface_override_material(0).resource_path})
	if not crates.is_empty():
		center /= crates.size()
		game.player.teleport(center + Vector3(0, 0.7, 4))
		game.camera.size = 16
		game.camera.global_position = center + GameManager.CAMERA_OFFSET
		game._hud.hide()
		await image_now("base-crates-overview")
		for i in crates.size():
			game.camera.size = 7
			game.camera.global_position = crates[i].global_position + GameManager.CAMERA_OFFSET
			await image_now("base-crate-%d" % i)
	game.queue_free()
	await frames()

func run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	report = {"engine": Engine.get_version_info().string, "renderer": RenderingServer.get_current_rendering_method(), "driver": RenderingServer.get_current_rendering_driver_name(), "adapter": RenderingServer.get_video_adapter_name()}
	var phases := OS.get_cmdline_user_args()
	if not phases.is_empty() and FileAccess.file_exists(OUT + "measurement.json"):
		report = JSON.parse_string(FileAccess.get_file_as_string(OUT + "measurement.json"))
	if phases.is_empty() or "fire" in phases: await fire()
	if phases.is_empty() or "materials" in phases: await materials()
	if phases.is_empty() or "time" in phases: await shader_time()
	if phases.is_empty() or "base" in phases: await base()
	var file := FileAccess.open(OUT + "measurement.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t"))
	file.close()
	print("A5_USE_IT_COMPLETE ", JSON.stringify(report))
	quit()
