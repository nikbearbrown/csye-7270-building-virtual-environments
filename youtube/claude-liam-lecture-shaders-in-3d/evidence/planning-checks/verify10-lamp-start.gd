extends SceneTree
# Reference for capture C03 (CAPTURE-PLAN scene S3, one sphere, beat B10): which starting yaw of the lamp shows "one side bright and one side
# dim" at once? Reads the left, centre and right of the lit sphere (lab-shaders/02-flat-teal-3d.gdshader) at four yaws and saves one frame each.
# Result: at -75 and -60 degrees the left is bright and the right dim; at -40 the sphere is mostly bright. The capture starts at -65.
# Run:  ./run-script.sh verify10-lamp-start.gd run-10-lamp-start.log
const LAB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/lab-shaders/"
const PNG_DIR := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/evidence/planning-checks/png/"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

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
	stage.add_child(lamp)
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(LAB + "02-flat-teal-3d.gdshader")
	var m := ShaderMaterial.new()
	m.shader = sh
	var mi := MeshInstance3D.new()
	mi.mesh = SphereMesh.new()
	mi.material_override = m
	stage.add_child(mi)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.2
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	var rows := []
	for yaw in [-90, -75, -65, -60, -40]:
		lamp.rotation_degrees = Vector3(-30, yaw, 0)
		for i in range(4): await process_frame
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		img.save_png(PNG_DIR + "lamp-start-yaw%d.png" % yaw)
		var ppu := img.get_height() / 2.2
		var cx := img.get_width() / 2.0
		var cy := img.get_height() / 2.0
		var pts := {}
		for p in [["left", -0.35], ["centre", 0.0], ["right", 0.35]]:
			var c := img.get_pixel(int(cx + float(p[1]) * ppu), int(cy))
			pts[p[0]] = [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]
		rows.append({"lamp_yaw_deg": yaw, "probes": pts})
	out("lamp-start", {"renderer": RenderingServer.get_current_rendering_method(), "rows": rows})
	quit(0)
