extends SceneTree
# Reference for capture C02 (CAPTURE-PLAN scene S2, beat B08): the UV-colors shader (lab-shaders/06-uv-colors-3d.gdshader) on a flat square,
# a box and a sphere in a row, each tilted -20 degrees about X and turned about Y. Saves PNG frames at three turn angles so the picture the
# film asks for exists as evidence, and reads the centre pixel of each mesh to show that every mesh draws its OWN colors.
# The motion in the film is a scripted SWING about Y, plus or minus 50 degrees (one swing in 8 s), not a full turn: with default culling a flat
# square vanishes while its back faces the camera (the first attempt, a full turn, lost the square at 168 degrees: see the first run kept in
# run-9a-three-meshes-full-turn-square-vanishes.log). Swinging keeps every face the film talks about in view.
# Run:  ./run-script.sh verify9-three-meshes-picture.gd run-9-three-meshes-picture.log
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
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(LAB + "06-uv-colors-3d.gdshader")
	var mat := ShaderMaterial.new()
	mat.shader = sh
	var q := QuadMesh.new()
	q.size = Vector2(1.0, 1.0)
	var b := BoxMesh.new()
	b.size = Vector3(1.0, 1.0, 1.0)
	var s := SphereMesh.new()
	var meshes := [q, b, s]
	var xs := [-1.6, 0.0, 1.6]
	var nodes := []
	for i in range(3):
		var mi := MeshInstance3D.new()
		mi.mesh = meshes[i]
		mi.material_override = mat
		mi.position = Vector3(xs[i], 0, 0)
		stage.add_child(mi)
		nodes.append(mi)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 3.2
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	var frames_saved := []
	for yaw in [-50, 0, 50]:
		for n in nodes:
			n.rotation_degrees = Vector3(-20, yaw, 0)
		for i in range(4): await process_frame
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		img.save_png(PNG_DIR + "three-meshes-swing%+d.png" % yaw)
		var ppu := img.get_height() / 3.2
		var row := []
		for x in xs:
			var c := img.get_pixel(int(img.get_width() / 2.0 + x * ppu), img.get_height() / 2)
			row.append([snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)])
		frames_saved.append({"yaw_deg": yaw, "centre_pixel_of_square_box_sphere": row})
	out("three-meshes", {"renderer": RenderingServer.get_current_rendering_method(), "frames": frames_saved, "saved": ["three-meshes-swing-50.png", "three-meshes-swing+0.png", "three-meshes-swing+50.png"],
		"reading": "the three meshes show different colors at the same screen position because each supplies its own UV map"})
	quit(0)
