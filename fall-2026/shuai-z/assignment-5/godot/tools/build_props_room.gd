extends SceneTree
## Builds res://scenes/props_room.tscn: a floor, one light, a camera, and the
## three walker-rudy props side by side on the floor at game scale (1 unit = 1 m).
##
## Run from the repository's assignment-3 folder:
##   /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tools/build_props_room.gd

const OUT := "res://scenes/props_room.tscn"

## name, scene, X position (m). Each origin is the centre of the prop's
## underside, so Y = 0 puts it on the floor.
const PROPS := [
	["Spikes", "res://assets/props/spikes.glb", -2.0],
	["Waystone", "res://assets/props/waystone.glb", -0.8],
	["TeleportCircle", "res://assets/props/teleport_circle.glb", 1.2],
]

const RUDY_HEIGHT := 1.2 ## m, CHANGE-BRIEF.md: Rudy = 160 px = 1.2 m


func _init() -> void:
	var root := Node3D.new()
	root.name = "PropsRoom"

	var env := WorldEnvironment.new()
	env.name = "WorldEnvironment"
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color("#9DB8CF") # a pale afternoon sky
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color("#FFF4E0")
	e.ambient_light_energy = 0.45
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.environment = e
	_add(root, env)

	var floor_mesh := PlaneMesh.new()
	floor_mesh.size = Vector2(8, 5)
	var floor_mat := StandardMaterial3D.new()
	floor_mat.albedo_color = Color("#8E9A5B") # field green
	floor_mat.roughness = 1.0
	floor_mesh.material = floor_mat
	var floor := MeshInstance3D.new()
	floor.name = "Floor"
	floor.mesh = floor_mesh
	_add(root, floor)

	var sun := DirectionalLight3D.new()
	sun.name = "Sun"
	sun.light_energy = 1.1
	sun.shadow_enabled = true
	_add(root, sun)
	sun.look_at_from_position(Vector3(3, 6, 4), Vector3.ZERO, Vector3.UP)

	for p in PROPS:
		var prop: Node3D = load(p[1]).instantiate()
		prop.name = p[0]
		prop.position = Vector3(p[2], 0, 0)
		_add(root, prop)

	# Not a prop: a 1.2 m post where Rudy would stand, so the props can be
	# judged against his height. Rudy himself is a 2D sprite.
	var marker_mesh := CylinderMesh.new()
	marker_mesh.top_radius = 0.04
	marker_mesh.bottom_radius = 0.04
	marker_mesh.height = RUDY_HEIGHT
	marker_mesh.radial_segments = 8
	var marker_mat := StandardMaterial3D.new()
	marker_mat.albedo_color = Color("#E0E0E0")
	marker_mesh.material = marker_mat
	var marker := MeshInstance3D.new()
	marker.name = "RudyHeightMarker"
	marker.mesh = marker_mesh
	marker.position = Vector3(-2.9, RUDY_HEIGHT / 2, 0)
	_add(root, marker)

	var cam := Camera3D.new()
	cam.name = "Camera"
	cam.fov = 50
	cam.current = true
	_add(root, cam)
	cam.look_at_from_position(Vector3(-0.3, 2.2, 4.6), Vector3(-0.3, 0.25, 0), Vector3.UP)

	var packed := PackedScene.new()
	var err := packed.pack(root)
	if err == OK:
		err = ResourceSaver.save(packed, OUT)
	print("saved %s: %s" % [OUT, error_string(err)])
	root.free()
	quit(0 if err == OK else 1)


func _add(parent: Node, child: Node) -> void:
	parent.add_child(child)
	child.owner = parent
