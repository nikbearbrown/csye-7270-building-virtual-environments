extends Node
# E8: depth gap. A perspective camera looks straight down from 6 m. A transparent plate lies at y = 0 (6.0 m from the camera). A flat floor at y = -0.5
# (6.5 m away) lies under the left half of it. Over the floor the gap along the view axis must be 0.5 m everywhere; over nothing the depth texture reads the far plane.
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
	fm.size = Vector2(4.0, 6.0)
	floor_mi.mesh = fm
	floor_mi.position = Vector3(-2.0, -0.5, 0.0)
	var fmat := StandardMaterial3D.new()
	fmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	fmat.albedo_color = Color("#B89D6E")
	floor_mi.material_override = fmat
	world.add_child(floor_mi)
	var plate := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(6.0, 6.0)
	plate.mesh = pm
	plate.position = Vector3(0.0, 0.0, 0.0)
	plate.material_override = ctx["materials"]["main"]
	world.add_child(plate)
	var cam := Camera3D.new()
	cam.fov = 40.0
	cam.position = Vector3(0, 6, 0)
	cam.rotation_degrees = Vector3(-90, 0, 0)
	world.add_child(cam)
	cam.current = true
