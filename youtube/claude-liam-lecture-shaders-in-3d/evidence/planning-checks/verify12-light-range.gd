extends SceneTree
# Claim checked (Shaders in 3D, on-screen definition from the series GLOSSARY): light() runs once per pixel for each light that touches it.
# A spatial shader whose light() adds a constant (DIFFUSE_LIGHT += vec3(0.1)) is drawn on a white quad with no ambient light. If light() runs
# for a lamp only when the lamp reaches the pixel, the (linear) centre value is 0 for a lamp too far away to reach it and about 0.1 for a
# lamp in range. Cases: no lamp; an omni lamp 1.5 units in front of the quad with range 6; the same lamp 12 units away with range 2.
# Scripted lamp placement. A planning check, not a shot in the film.
# Run:  ./run-script.sh verify12-light-range.gd run-12-light-range.log
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
	for i in range(4): await process_frame
	rows.append({"case": "no lamp", "centre_linear_red": centre_linear()})
	var lamp := OmniLight3D.new()
	lamp.shadow_enabled = false
	lamp.omni_range = 6.0
	lamp.position = Vector3(0, 0, 1.5)
	stage.add_child(lamp)
	for i in range(4): await process_frame
	rows.append({"case": "omni lamp 1.5 in front, range 6 (reaches the quad)", "centre_linear_red": centre_linear()})
	lamp.omni_range = 2.0
	lamp.position = Vector3(0, 0, 12.0)
	for i in range(4): await process_frame
	rows.append({"case": "omni lamp 12 away, range 2 (does not reach the quad)", "centre_linear_red": centre_linear()})
	out("light-range", {"renderer": RenderingServer.get_current_rendering_method(), "rows": rows})
	quit(0)
