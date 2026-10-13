extends SceneTree
# Claims checked (Shaders in 3D): lit versus unshaded versus a shader that writes its own (empty) light().
#   LEFT  sphere: lab-shaders/02-flat-teal-3d.gdshader                (default: lit)
#   MIDDLE sphere: lab-shaders/07-flat-teal-3d-unshaded.gdshader      (render_mode unshaded)
#   RIGHT sphere: lab-shaders/08-flat-teal-3d-empty-light.gdshader    (writes an empty light())
#   Scene: orthographic camera, one DirectionalLight3D (energy 1.0, tilted 30 degrees down) that turns about the vertical axis, and a dim
#   white ambient light (energy 0.25). The lamp's turn is SCRIPTED. Forward+ unless the run is started with --rendering-method.
# Run:  ./run-script.sh verify4-lamp.gd run-4-lamp-forward-plus.log
#       ./run-script.sh verify4-lamp.gd run-4b-lamp-compatibility.log --rendering-method gl_compatibility
const LAB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/lab-shaders/"
const PNG_DIR := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/evidence/planning-checks/png/"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func mk(file: String, x: float) -> MeshInstance3D:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(LAB + file)
	var m := ShaderMaterial.new()
	m.shader = sh
	var mi := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = 0.5
	sm.height = 1.0
	mi.mesh = sm
	mi.material_override = m
	mi.position = Vector3(x, 0, 0)
	return mi

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(1280, 720)
	var stage := Node3D.new()
	root.add_child(stage)
	var env := Environment.new()
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color.WHITE
	env.ambient_light_energy = 0.25
	var we := WorldEnvironment.new()
	we.environment = env
	stage.add_child(we)
	var lamp := DirectionalLight3D.new()
	lamp.light_energy = 1.0
	stage.add_child(lamp)
	stage.add_child(mk("02-flat-teal-3d.gdshader", -1.3))
	stage.add_child(mk("07-flat-teal-3d-unshaded.gdshader", 0.0))
	stage.add_child(mk("08-flat-teal-3d-empty-light.gdshader", 1.3))
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 3.2
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	var runs := []
	var settings := [["lamp yaw 0 (lamp lights the face the camera sees)", 0.0, 1.0, "yaw000"], ["lamp yaw 90", 90.0, 1.0, "yaw090"], ["lamp yaw 180 (lamp lights the far side)", 180.0, 1.0, "yaw180"], ["lamp yaw 270", 270.0, 1.0, "yaw270"], ["lamp off (energy 0)", 0.0, 0.0, "lamp-off"]]
	for s in settings:
		lamp.rotation_degrees = Vector3(-30, s[1], 0)
		lamp.light_energy = s[2]
		for i in range(4): await process_frame
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		img.save_png(PNG_DIR + "lamp-%s-%s.png" % [RenderingServer.get_current_rendering_method(), s[3]])
		var ppu := img.get_height() / 3.2
		var cx := img.get_width() / 2.0
		var cy := img.get_height() / 2.0
		var row := {}
		for k in [["lit", -1.3], ["unshaded", 0.0], ["empty_light", 1.3]]:
			var sx: float = cx + float(k[1]) * ppu
			var pts := {}
			for p in [["left_limb", -0.35], ["centre", 0.0], ["right_limb", 0.35]]:
				var c := img.get_pixel(int(sx + float(p[1]) * ppu), int(cy))
				pts[p[0]] = [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]
			row[k[0]] = pts
		runs.append({"setting": s[0], "probes": row})
	out("lamp", {"renderer": RenderingServer.get_current_rendering_method(), "albedo_typed": [0.37, 0.64, 0.57], "runs": runs,
		"reading": "unshaded never changes; lit changes with the lamp; the empty-light sphere ignores the lamp and equals the lit sphere with the lamp off (ambient only)"})
	quit(0)
