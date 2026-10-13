extends SceneTree
# Claims checked (Shaders in 3D): a three-D surface is drawn from its front side only unless the render mode says otherwise.
#   LEFT  quad: lab-shaders/07-flat-teal-3d-unshaded.gdshader   (default culling: back faces are not drawn)
#   RIGHT quad: lab-shaders/09-two-sided.gdshader               (render_mode unshaded, cull_disabled)
#   Both turn about the vertical axis; the camera looks at them from the front. Turning is SCRIPTED. Probes read the centre of each quad.
# Run:  ./run-script.sh verify5-cull-turnaround.gd run-5-cull-turnaround.log
const LAB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/lab-shaders/"

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
	var q := QuadMesh.new()
	q.size = Vector2(1.2, 1.2)
	mi.mesh = q
	mi.material_override = m
	mi.position = Vector3(x, 0, 0)
	return mi

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(1280, 720)
	var stage := Node3D.new()
	root.add_child(stage)
	var left := mk("07-flat-teal-3d-unshaded.gdshader", -1.0)
	var right := mk("09-two-sided.gdshader", 1.0)
	stage.add_child(left)
	stage.add_child(right)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 3.0
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	var rows := []
	for yaw in [0, 60, 120, 180, 240, 300]:
		left.rotation_degrees = Vector3(0, yaw, 0)
		right.rotation_degrees = Vector3(0, yaw, 0)
		for i in range(4): await process_frame
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		var ppu := img.get_height() / 3.0
		var cy := img.get_height() / 2
		var cx := img.get_width() / 2.0
		var l := img.get_pixel(int(cx - 1.0 * ppu), cy)
		var r := img.get_pixel(int(cx + 1.0 * ppu), cy)
		rows.append({"yaw_deg": yaw, "default_culling": [snappedf(l.r, 0.001), snappedf(l.g, 0.001), snappedf(l.b, 0.001)], "cull_disabled": [snappedf(r.r, 0.001), snappedf(r.g, 0.001), snappedf(r.b, 0.001)]})
	out("cull", {"renderer": RenderingServer.get_current_rendering_method(), "stage_colour_where_nothing_is_drawn": [0.851, 0.835, 0.792], "runs": rows,
		"reading": "default: the quad shows its colour at yaw 0, 60 and 300 (front toward the camera) and shows the stage colour at 120, 180 and 240 (its back toward the camera); cull_disabled shows the colour at every angle"})
	quit(0)
