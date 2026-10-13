extends SceneTree
# Claim checked (Shaders in 3D): in a spatial shader, light() runs once for every light that touches a pixel, and the results add.
# A shader whose light() adds the same constant (DIFFUSE_LIGHT += vec3(0.1)) is drawn on a white quad with no ambient light, under
# zero, one, two and three identical directional lamps. If light() runs once per lamp and the results add, the pixel's LINEAR value
# should be 0, 1x, 2x and 3x the one-lamp value (Forward+ encodes linear light for the screen; the script decodes it before comparing).
# Scripted: the lamps are added one by one by the script. This is a planning check, not a shot in the film.
# Run:  ./run-script.sh verify7-light-count.gd run-7-light-count.log
const CODE := "shader_type spatial;\nvoid fragment() { ALBEDO = vec3(1.0); }\nvoid light() { DIFFUSE_LIGHT += vec3(0.1); }\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func centre_linear() -> float:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	if RenderingServer.get_current_rendering_method() != "gl_compatibility":
		c = c.srgb_to_linear()
	return snappedf(c.r, 0.0001)

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(320, 180)
	var stage := Node3D.new()
	root.add_child(stage)
	var env := Environment.new()
	env.ambient_light_source = Environment.AMBIENT_SOURCE_DISABLED
	var we := WorldEnvironment.new()
	we.environment = env
	stage.add_child(we)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.0
	cam.position = Vector3(0, 0, 3)
	stage.add_child(cam)
	cam.current = true
	var sh := Shader.new()
	sh.code = CODE
	var m := ShaderMaterial.new()
	m.shader = sh
	var mi := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(1.8, 1.8)
	mi.mesh = q
	mi.material_override = m
	stage.add_child(mi)
	var rows := []
	for n in range(0, 4):
		if n > 0:
			var lamp := DirectionalLight3D.new()
			lamp.rotation_degrees = Vector3(0, 20.0 * n, 0)    # all point at the front of the quad (their -Z axis goes into the scene)
			lamp.shadow_enabled = false
			stage.add_child(lamp)
		for i in range(4): await process_frame
		rows.append({"lamps": n, "centre_linear_red": centre_linear()})
	var one: float = rows[1]["centre_linear_red"]
	for r in rows:
		r["ratio_to_one_lamp"] = snappedf(float(r["centre_linear_red"]) / one, 0.01) if one > 0.0 else 0.0
	out("light-count", {"renderer": RenderingServer.get_current_rendering_method(), "rows": rows, "expected_ratios": [0, 1, 2, 3]})
	quit(0)
