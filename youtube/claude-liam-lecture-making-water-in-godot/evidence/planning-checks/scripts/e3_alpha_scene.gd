extends Node
# E3: alpha arithmetic. Top-down orthographic view: a sand floor under the left part of a transparent plate; a flat background colour beyond.
# Layout (world x -4..4 across the frame): floor x -4..0, plate x -3..1. Probe x (normalized): floor alone 0.06, plate over floor 0.30, plate over background 0.56, background alone 0.85.
#   plate over floor (0.375,0.5)   plate over background (0.625,0.5)   floor alone (0.125,0.5)   background alone (0.875,0.5)
const SAND := Color("#B89D6E")
func harness_setup(ctx: Dictionary) -> void:
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
	var floor_mi := MeshInstance3D.new()
	var fm := PlaneMesh.new()
	fm.size = Vector2(4.0, 4.0)
	floor_mi.mesh = fm
	floor_mi.position = Vector3(-2.0, -0.5, 0.0)
	var fmat := StandardMaterial3D.new()
	fmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	fmat.albedo_color = SAND
	floor_mi.material_override = fmat
	world.add_child(floor_mi)
	var plate := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(4.0, 4.0)
	plate.mesh = pm
	plate.position = Vector3(-1.0, 0.0, 0.0)
	plate.material_override = ctx["materials"]["main"]
	world.add_child(plate)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 4.5   # vertical extent 4.5 m, so 8 m across a 16:9 frame (x -4..4)
	cam.position = Vector3(0, 8, 0)
	cam.rotation_degrees = Vector3(-90, 0, 0)
	world.add_child(cam)
	cam.current = true
