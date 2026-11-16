extends RefCounted
# cove_builder.gd: builds THE COVE, the scene every picture of the film comes from. Used by the capture harness (capture-scenes/water_scene.gd)
# and by tools/make_scene.gd, which saves the same cove as scenes/water.tscn. Units are metres; y is up.
#   water      a PlaneMesh 8 x 8 at y = 0 wearing the water ShaderMaterial (cut into a grid for the vertex stage)
#   sea floor  a flat sand plane (top at y = -0.9), and a sand beach plane rising from x = 0.8 to the edge (it crosses the water near x = 2.7)
#   rocks      two grey rocks, one poking through the surface
#   floaters   a teal buoy (sphere) and a cream crate (box)
#   light      one directional lamp from behind the cove; ambient and reflections from a plain sky whose horizon is the stage grey
# Camera views: "iso" (perspective, 3/4 view), "top" (orthographic, straight down), "side" (orthographic, from the front at the waterline),
# "low" (perspective, just above the waterline: the near edge of the water shows its silhouette), "under" (perspective, 1.2 m below the water looking up).

const STAGE_GREY := Color("#D9D5CA")
const SAND := Color("#B89D6E")
const ROCK := Color("#8E877B")
const TEAL := Color("#5FA391")
const CREAM := Color("#F4EFE3")

static func std(color: Color, rough := 0.85) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	m.roughness = rough
	return m

# A normal map made by Godot itself: FastNoiseLite -> NoiseTexture2D with Seamless and As Normal Map on.
static func normal_noise(seed_v: int, freq: float, bump := 6.0, size := 512) -> NoiseTexture2D:
	var fn := FastNoiseLite.new()
	fn.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	fn.seed = seed_v
	fn.frequency = freq
	fn.fractal_octaves = 3
	var t := NoiseTexture2D.new()
	t.width = size
	t.height = size
	t.seamless = true
	t.as_normal_map = true
	t.bump_strength = bump
	t.noise = fn
	return t

# A baked cellular texture: FastNoiseLite set to Cellular, returning the second distance minus the first (the cell borders).
static func cell_noise(freq := 0.02, seed_v := 5) -> NoiseTexture2D:
	var fn := FastNoiseLite.new()
	fn.noise_type = FastNoiseLite.TYPE_CELLULAR
	fn.cellular_return_type = FastNoiseLite.RETURN_DISTANCE2_SUB
	fn.cellular_jitter = 1.0
	fn.fractal_type = FastNoiseLite.FRACTAL_NONE      # the default (FBM, five octaves) smears cellular noise into mush
	fn.frequency = freq
	fn.seed = seed_v
	var t := NoiseTexture2D.new()
	t.width = 512
	t.height = 512
	t.seamless = true
	t.noise = fn
	return t

# Give a material the textures its shader asks for (by uniform name). Returns the textures made, by name.
static func feed_textures(mat: ShaderMaterial, all := false) -> Dictionary:
	var made := {}
	var names := []
	for u in mat.shader.get_shader_uniform_list():
		names.append(String(u["name"]))
	if all:      # the capture harness may swap shaders mid-clip: have every texture ready (parameters a shader does not declare are simply kept)
		names = ["cell_tex", "normal_a", "normal_b"]
	if names.has("cell_tex"):
		made["cell_tex"] = cell_noise()
		mat.set_shader_parameter("cell_tex", made["cell_tex"])
	if names.has("normal_a"):
		made["normal_a"] = normal_noise(1, 0.006)
		mat.set_shader_parameter("normal_a", made["normal_a"])
	if names.has("normal_b"):
		made["normal_b"] = normal_noise(2, 0.009)
		mat.set_shader_parameter("normal_b", made["normal_b"])
	return made

static func add_environment(world: Node3D, ambient := 0.55) -> Dictionary:
	var env := Environment.new()
	env.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var psm := ProceduralSkyMaterial.new()
	psm.sky_top_color = Color("#BFD0DC")
	psm.sky_horizon_color = STAGE_GREY
	psm.ground_horizon_color = STAGE_GREY
	psm.ground_bottom_color = STAGE_GREY
	psm.sky_curve = 0.25
	psm.sun_angle_max = 0.0
	sky.sky_material = psm
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	env.ambient_light_energy = ambient
	env.reflected_light_source = Environment.REFLECTION_SOURCE_SKY
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	var we := WorldEnvironment.new()
	we.name = "WorldEnvironment"
	we.environment = env
	world.add_child(we)
	var lamp := DirectionalLight3D.new()
	lamp.name = "Lamp"
	lamp.light_energy = 1.0
	lamp.rotation_degrees = Vector3(-38.0, 200.0, 0.0)
	world.add_child(lamp)
	return {"env": env, "lamp": lamp}

# Returns {"water": MeshInstance3D, "buoy": ..., "crate": ...} (buoy and crate only when floaters is true; nothing but the water when bare is true).
static func add_cove(world: Node3D, water_mat: Material, plane_cuts := 0, bare := false, floaters := true) -> Dictionary:
	var out := {}
	var pm := PlaneMesh.new()
	pm.size = Vector2(8.0, 8.0)
	pm.subdivide_width = plane_cuts
	pm.subdivide_depth = plane_cuts
	var water := MeshInstance3D.new()
	water.name = "Water"
	water.mesh = pm
	water.material_override = water_mat
	world.add_child(water)
	out["water"] = water
	if bare:
		return out
	var floor_mi := MeshInstance3D.new()
	floor_mi.name = "SeaFloor"
	var fm := PlaneMesh.new()
	fm.size = Vector2(4.8, 8.0)
	floor_mi.mesh = fm
	floor_mi.position = Vector3(-1.6, -0.9, 0.0)
	floor_mi.material_override = std(SAND)
	world.add_child(floor_mi)
	var beach := MeshInstance3D.new()
	beach.name = "Beach"
	var bm := PlaneMesh.new()
	bm.size = Vector2(Vector2(3.2, 1.5).length(), 8.0)
	beach.mesh = bm
	beach.position = Vector3(2.4, -0.15, 0.0)
	beach.rotation_degrees = Vector3(0, 0, rad_to_deg(atan2(1.5, 3.2)))
	beach.material_override = std(SAND)
	world.add_child(beach)
	var rock1 := MeshInstance3D.new()
	rock1.name = "Rock1"
	var sm := SphereMesh.new()
	sm.radius = 0.55
	sm.height = 1.1
	rock1.mesh = sm
	rock1.position = Vector3(1.0, -0.25, -1.4)
	rock1.scale = Vector3(1.0, 0.8, 0.9)
	rock1.material_override = std(ROCK, 0.95)
	world.add_child(rock1)
	var rock2 := MeshInstance3D.new()
	rock2.name = "Rock2"
	var bx := BoxMesh.new()
	bx.size = Vector3(0.9, 0.7, 0.8)
	rock2.mesh = bx
	rock2.position = Vector3(-0.1, -0.55, 1.9)
	rock2.rotation_degrees = Vector3(0, 28, 0)
	rock2.material_override = std(ROCK, 0.95)
	world.add_child(rock2)
	if floaters:
		var buoy := MeshInstance3D.new()
		buoy.name = "Buoy"
		var bs := SphereMesh.new()
		bs.radius = 0.3
		bs.height = 0.6
		buoy.mesh = bs
		buoy.position = Vector3(-1.5, 0.0, 0.6)
		buoy.material_override = std(TEAL, 0.55)
		world.add_child(buoy)
		out["buoy"] = buoy
		var crate := MeshInstance3D.new()
		crate.name = "Crate"
		var cb := BoxMesh.new()
		cb.size = Vector3(0.5, 0.5, 0.5)
		crate.mesh = cb
		crate.position = Vector3(-0.2, 0.0, -0.6)
		crate.rotation_degrees = Vector3(0, 20, 0)
		crate.material_override = std(CREAM, 0.7)
		world.add_child(crate)
		out["crate"] = crate
	return out

static func add_camera(world: Node3D, view := "iso", top_size := 9.0, side_size := 4.0) -> Camera3D:
	var cam := Camera3D.new()
	cam.name = "Camera"
	world.add_child(cam)
	cam.current = true
	if view == "top":
		cam.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam.size = top_size
		cam.position = Vector3(0, 10, 0)
		cam.rotation_degrees = Vector3(-90, 0, 0)
	elif view == "side":
		cam.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam.size = side_size
		cam.position = Vector3(0, 0.0, 10)
		cam.rotation_degrees = Vector3(0, 0, 0)
	elif view == "under":
		cam.fov = 40.0
		cam.look_at_from_position(Vector3(0.0, -1.2, 6.0), Vector3(0.0, 0.0, 0.0))
	elif view == "low":
		cam.fov = 30.0
		cam.look_at_from_position(Vector3(0.0, 1.1, 9.0), Vector3(0.0, 0.0, 0.0))
	else:
		cam.fov = 38.0
		cam.look_at_from_position(Vector3(0.0, 5.0, 7.6), Vector3(0.2, -0.35, 0.0))
	return cam

# A second see-through plane (red, alpha 0.6) UNDER the water but with its node origin nearer the camera than the water's: Godot sorts transparent
# objects by node position, so it is drawn after the water. Used by the sorting and depth_draw tests (evidence/planning-checks, E16).
static func add_sorting_plane(world: Node3D) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = "RedPlane"
	var pm := PlaneMesh.new()
	pm.size = Vector2(2.0, 2.0)
	mi.mesh = pm
	mi.position = Vector3(0.0, -0.4, 3.0)
	var m := StandardMaterial3D.new()
	m.albedo_color = Color(0.9, 0.1, 0.1, 0.6)
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mi.material_override = m
	world.add_child(mi)
	return mi
