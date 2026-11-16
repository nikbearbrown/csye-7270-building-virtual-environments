extends Node
# gap_scene.gd: the depth-gap test as a capture. A perspective camera looks straight down from 6 m. A plate (wearing the shader on the command line)
# lies at y = 0, 6.0 m from the camera. A flat floor lies under its LEFT half; its height runs from G_FLOOR0 to G_FLOOR1 (metres, negative) over the clip.
# Over the floor, the gap along the view axis equals -floor_y. Env: G_FLOOR0, G_FLOOR1, CLIP_L.
const ROOT := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/"
var floor_mi: MeshInstance3D
var y0 := -0.2
var y1 := -1.0
var clip_len := 1.0
func harness_setup(ctx: Dictionary) -> void:
	if OS.get_environment("CLIP_L") != "": clip_len = float(OS.get_environment("CLIP_L"))
	if OS.get_environment("G_FLOOR0") != "": y0 = float(OS.get_environment("G_FLOOR0"))
	if OS.get_environment("G_FLOOR1") != "": y1 = float(OS.get_environment("G_FLOOR1"))
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(ROOT + "lab-shaders/" + OS.get_environment("W_SHADER"))
	var mat := ShaderMaterial.new()
	mat.shader = sh
	ctx["materials"]["water"] = mat
	var world := Node3D.new()
	add_child(world)
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color("#D9D5CA")
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color.WHITE
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	var we := WorldEnvironment.new()
	we.environment = env
	world.add_child(we)
	floor_mi = MeshInstance3D.new()
	var fm := PlaneMesh.new()
	fm.size = Vector2(4.0, 6.0)
	floor_mi.mesh = fm
	floor_mi.position = Vector3(-2.0, y0, 0.0)
	var fmat := StandardMaterial3D.new()
	fmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	fmat.albedo_color = Color("#B89D6E")
	floor_mi.material_override = fmat
	world.add_child(floor_mi)
	var plate := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(6.0, 6.0)
	plate.mesh = pm
	plate.material_override = mat
	world.add_child(plate)
	var cam := Camera3D.new()
	cam.fov = 40.0
	world.add_child(cam)
	cam.global_position = Vector3(0, 6, 0)
	cam.rotation_degrees = Vector3(-90, 0, 0)
	cam.current = true
func harness_frame(t: float) -> void:
	var steps := OS.get_environment("G_STEPS")          # "0:-0.2,0.3f:-0.2,...": piecewise-linear floor height (f = fraction of CLIP_L)
	if steps == "":
		floor_mi.position.y = lerpf(y0, y1, clampf(t / maxf(clip_len, 0.001), 0.0, 1.0))
		return
	var pts: Array = []
	for pair in steps.split(","):
		var tv := pair.split(":")
		var tt := float(tv[0].substr(0, tv[0].length() - 1)) * clip_len if tv[0].ends_with("f") else float(tv[0])
		pts.append([tt, float(tv[1])])
	var v: float = pts[0][1]
	for i in range(1, pts.size()):
		if t >= pts[i][0]:
			v = pts[i][1]
		elif t > pts[i - 1][0]:
			v = lerpf(pts[i - 1][1], pts[i][1], (t - pts[i - 1][0]) / (pts[i][0] - pts[i - 1][0]))
			break
		else:
			break
	floor_mi.position.y = v
