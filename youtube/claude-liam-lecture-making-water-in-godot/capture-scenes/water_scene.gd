extends Node
# water_scene.gd: the capture harness adapter of "Making Water in Godot" (lab/capture.gd --scene). It builds THE COVE with water-project/scripts/cove_builder.gd
# (the same builder that writes the project's scene) and applies what the capture's environment variables ask for. All variables are set by captures.py:
#   W_SHADER   the shader file in lab-shaders/ (or a path relative to it)             W_ID    the capture id (logged)
#   W_VIEW     iso (default) | top | side     W_TOPSIZE / W_SIDESIZE  orthographic size (metres)
#   W_CUTS     PlaneMesh cuts each way (default 0; 127 for the vertex stages)       W_BARE=1  the water plane alone      W_NOFLOAT=1  no buoy or crate
#   W_SET      "name=value;name=value"  uniforms at t = 0 (cast by the shader's own declared type)
#   W_FOLLOW=1 drive wave_clock from the capture clock and put the buoy and crate on the surface with water_driver.gd      W_CLOCK0  clock at t = 0 (s)
#   W_LAMP     "pitch,yaw" of the lamp in degrees     W_AMBIENT  ambient energy       W_FOV  perspective field of view
#   W_EXTRA=sort  adds a second see-through plane under the water whose node origin is nearer the camera (sorting test E16)
#   W_LATE=1   the water has no material until apply_material() is called (--call-at T:apply_material): a plain plane first, then the shader
#   W_SHADER2  a second shader file; swap_shader() (--call-at T:swap_shader) assigns it to the SAME material, so the uniform values and textures carry over
#   CLIP_L     the clip's length in seconds (set by captures.py; the scene's own events are fractions of it)
const ROOT := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/"
const SHADERS := ROOT + "lab-shaders/"
const CB := ROOT + "water-project/scripts/cove_builder.gd"
const DRV := ROOT + "water-project/scripts/water_driver.gd"

var water_mat: ShaderMaterial
var nodes: Dictionary
var driver: Node
var clock0 := 0.0
var textures: Dictionary
var clip_len := 1.0

func harness_setup(ctx: Dictionary) -> void:
	if OS.get_environment("CLIP_L") != "":
		clip_len = float(OS.get_environment("CLIP_L"))
	var builder = load(CB)
	var shader_file := OS.get_environment("W_SHADER")
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(SHADERS + shader_file)
	water_mat = ShaderMaterial.new()
	water_mat.shader = sh
	textures = builder.feed_textures(water_mat, true)
	ctx["materials"]["water"] = water_mat
	var world := Node3D.new()
	add_child(world)
	var amb := float(OS.get_environment("W_AMBIENT")) if OS.get_environment("W_AMBIENT") != "" else 0.55
	var le: Dictionary = builder.add_environment(world, amb)
	if OS.get_environment("W_LAMP") != "":
		var pr := OS.get_environment("W_LAMP").split(",")
		(le["lamp"] as DirectionalLight3D).rotation_degrees = Vector3(float(pr[0]), float(pr[1]), 0.0)
	var cuts := int(OS.get_environment("W_CUTS")) if OS.get_environment("W_CUTS") != "" else 0
	nodes = builder.add_cove(world, water_mat, cuts, OS.get_environment("W_BARE") == "1", OS.get_environment("W_NOFLOAT") != "1")
	if OS.get_environment("W_LATE") == "1":
		(nodes["water"] as MeshInstance3D).material_override = null
	var view := OS.get_environment("W_VIEW") if OS.get_environment("W_VIEW") != "" else "iso"
	var top := float(OS.get_environment("W_TOPSIZE")) if OS.get_environment("W_TOPSIZE") != "" else 9.0
	var side := float(OS.get_environment("W_SIDESIZE")) if OS.get_environment("W_SIDESIZE") != "" else 4.0
	var cam: Camera3D = builder.add_camera(world, view, top, side)
	if OS.get_environment("W_FOV") != "":
		cam.fov = float(OS.get_environment("W_FOV"))
	if OS.get_environment("W_EXTRA") == "sort":
		builder.add_sorting_plane(world)
	for kv in OS.get_environment("W_SET").split(";", false):
		var p := kv.split("=", true, 1)
		if p.size() == 2:
			set_param_text(p[0], p[1])
	if OS.get_environment("W_FOLLOW") == "1":
		clock0 = float(OS.get_environment("W_CLOCK0")) if OS.get_environment("W_CLOCK0") != "" else 0.0
		driver = Node.new()
		driver.set_script(load(DRV))
		driver.water = nodes["water"]
		var fl: Array[Node3D] = []
		for k in ["buoy", "crate"]:
			if nodes.has(k):
				fl.append(nodes[k])
		driver.floaters = fl
		world.add_child(driver)
		for kv in OS.get_environment("W_SET").split(";", false):      # the three wave numbers belong to the driver while it runs
			var p := kv.split("=", true, 1)
			if p.size() == 2 and ["wave_height", "wave_length", "wave_speed"].has(p[0]):
				driver.set(p[0], float(p[1]))
		driver.set_clock(clock0)

func apply_material() -> void:
	(nodes["water"] as MeshInstance3D).material_override = water_mat

func swap_shader() -> void:
	var sh2 := Shader.new()
	sh2.code = FileAccess.get_file_as_string(SHADERS + OS.get_environment("W_SHADER2"))
	water_mat.shader = sh2

func set_param_text(name: String, value: String) -> void:
	for u in water_mat.shader.get_shader_uniform_list():
		if String(u["name"]) == name:
			var t := int(u["type"])
			var parts := value.split(",")
			var v: Variant
			if t == TYPE_FLOAT: v = float(value)
			elif t == TYPE_INT: v = int(value)
			elif t == TYPE_BOOL: v = value == "true"
			elif t == TYPE_COLOR: v = Color(value) if value.begins_with("#") else Color(float(parts[0]), float(parts[1]), float(parts[2]), 1.0)
			elif t == TYPE_VECTOR2: v = Vector2(float(parts[0]), float(parts[1]))
			elif t == TYPE_VECTOR3: v = Vector3(float(parts[0]), float(parts[1]), float(parts[2]))
			else: v = value
			water_mat.set_shader_parameter(name, v)

func harness_frame(t: float) -> void:
	if driver != null:
		for sw in OS.get_environment("W_DRIVE").split(";", false):   # "wave_height:0:0.04,1f:0.25": piecewise-linear sweeps of the driver's numbers (f = fraction of CLIP_L)
			var nm := sw.get_slice(":", 0)
			var pts: Array = []
			for pair in sw.substr(nm.length() + 1).split(","):
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
			driver.set(nm, v)
		driver.set_clock(clock0 + t)
