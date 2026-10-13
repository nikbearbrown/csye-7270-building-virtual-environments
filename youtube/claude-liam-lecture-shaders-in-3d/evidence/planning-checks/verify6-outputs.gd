extends SceneTree
# Claims checked (Shaders in 3D): a spatial fragment() sets surface properties, and each of the five outputs the film names changes the
# picture. One sphere per setting, lab-shaders/16-all-outputs.gdshader, one lamp and a dim ambient light, Forward+ by default.
#   ROUGHNESS 0.1 vs 0.9 : the shine tightens or spreads      METALLIC 0 vs 1 : the sphere darkens (nothing around it to reflect)
#   EMISSION  0 vs 1     : the sphere glows by itself          ALPHA 1 vs 0.35 : the stage shows through
# METALLIC = 1 reading near-black is the reason the film shows these five as a table of names and not as spheres (SHOTLIST B12).
# Run:  ./run-script.sh verify6-outputs.gd run-6-outputs.log
const LAB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/lab-shaders/"
const PNG_DIR := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/evidence/planning-checks/png/"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func sphere(params: Dictionary) -> MeshInstance3D:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(LAB + "16-all-outputs.gdshader")
	var m := ShaderMaterial.new()
	m.shader = sh
	for k in params: m.set_shader_parameter(k, params[k])
	var mi := MeshInstance3D.new()
	mi.mesh = SphereMesh.new()
	mi.material_override = m
	return mi

# brightest green value and mean green value inside the sphere's disc (radius 0.5 world units, centred)
func stats(img: Image) -> Dictionary:
	var ppu := img.get_height() / 3.4
	var cx := img.get_width() / 2.0
	var cy := img.get_height() / 2.0
	var r := 0.5 * ppu - 3.0
	var mx := 0.0
	var sum := 0.0
	var n := 0
	for y in range(int(cy - r), int(cy + r)):
		for x in range(int(cx - r), int(cx + r)):
			if Vector2(x - cx, y - cy).length() < r:
				var g := img.get_pixel(x, y).g
				mx = maxf(mx, g)
				sum += g
				n += 1
	var c := img.get_pixel(int(cx), int(cy))
	return {"brightest_green": snappedf(mx, 0.001), "mean_green": snappedf(sum / n, 0.001), "centre": [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]}

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
	lamp.rotation_degrees = Vector3(-35, -30, 0)
	stage.add_child(lamp)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 3.4
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	var rows := []
	var cases := [["roughness 0.1", {"roughness": 0.1}], ["roughness 0.9", {"roughness": 0.9}], ["metallic 0", {"metallic": 0.0}], ["metallic 1 (roughness 0.35)", {"metallic": 1.0, "roughness": 0.35}],
		["emission 0", {"glow": 0.0}], ["emission 1 (orange)", {"glow": 1.0}], ["alpha 1", {"alpha": 1.0}], ["alpha 0.35", {"alpha": 0.35}]]
	for c in cases:
		var mi := sphere(c[1])
		stage.add_child(mi)
		for i in range(4): await process_frame
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		var s := stats(img)
		s["case"] = c[0]
		rows.append(s)
		mi.queue_free()
		await process_frame
	out("outputs", {"renderer": RenderingServer.get_current_rendering_method(), "stage_colour": [0.851, 0.835, 0.792], "cases": rows})
	quit(0)
