extends SceneTree
# Claim checked (Shaders in 3D, on-screen definition): ALPHA is how visible a surface is: 0 is invisible, 1 is solid.
# One unshaded spatial quad on the stage colour, centre pixel read for: no ALPHA written (control), ALPHA 1.0, ALPHA 0.5 and ALPHA 0.0.
# If 0 is invisible the centre reads the stage colour; if 1 is solid it reads the control's colour. No lamp, no ambient light needed (unshaded).
# Run:  ./run-script.sh verify11-alpha-ends.gd run-11-alpha-ends.log
const HEAD := "shader_type spatial;\nrender_mode unshaded;\nvoid fragment() {\n\tALBEDO = vec3(0.60, 0.25, 0.15);\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func px(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(320, 180)
	var stage := Node3D.new()
	root.add_child(stage)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.0
	cam.position = Vector3(0, 0, 3)
	stage.add_child(cam)
	cam.current = true
	var mi := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(1.2, 1.2)
	mi.mesh = q
	stage.add_child(mi)
	var rows := []
	for c in [["control (ALPHA not written)", ""], ["ALPHA = 1.0", "\tALPHA = 1.0;\n"], ["ALPHA = 0.5", "\tALPHA = 0.5;\n"], ["ALPHA = 0.0", "\tALPHA = 0.0;\n"]]:
		var sh := Shader.new()
		sh.code = HEAD + c[1] + "}\n"
		var m := ShaderMaterial.new()
		m.shader = sh
		mi.material_override = m
		for i in range(4): await process_frame
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		rows.append({"case": c[0], "centre": px(img, img.get_width() / 2, img.get_height() / 2), "stage_corner": px(img, 4, 4)})
	out("alpha-ends", {"renderer": RenderingServer.get_current_rendering_method(), "rows": rows})
	quit(0)
