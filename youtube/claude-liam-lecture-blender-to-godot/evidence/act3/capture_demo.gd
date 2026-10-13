# ACT III capture (B21): Godot's official 3D platformer demo, windowed, with Debug > Visible Collision Shapes on,
# seen from the side through an ORTHOGONAL camera (3.6 m tall view) so the player's capsule has a known scale.
#   godot --path <copy of walker-3d-platformer/godot> --script res://capture_demo.gd --resolution 1600x900 -- <out.png>
extends SceneTree
var frames := 0
var game: Node
var cam: Camera3D
var out := "capture_demo.png"
var CAM_SIDE := 1.0    # camera on the +X side of the player (the -X side looks into a wall)
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	if a.size() > 0: out = a[0]
	game = (load("res://game.tscn") as PackedScene).instantiate()
	root.add_child(game)
	game.get_node("TouchScreenUI").queue_free()
	# Debug > Visible Collision Shapes, for the PLAYER only: switch the hint on, then re-enter the player so its shape draws.
	debug_collisions_hint = true
	var pl: Node = game.get_node("Player")
	game.remove_child(pl)
	game.add_child(pl)
	pl.get_node("%CoinCount").hide()
	# a daylight key light, so the floor reads as grass and not as near-black (the demo's own scene is a night scene)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-35.0, 70.0, 0.0)
	sun.light_energy = 1.4
	root.add_child(sun)
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 3.6
	root.add_child(cam)
	cam.current = true
func _process(_delta: float) -> bool:
	frames += 1
	var p: Node3D = game.get_node("Player")
	var capsule: CollisionShape3D = p.get_node("CollisionCapsule")
	cam.global_position = p.global_position + Vector3(CAM_SIDE * 10.0, 1.05, 0.0)
	cam.look_at(p.global_position + Vector3(0.0, 1.05, 0.0), Vector3.UP)
	if frames == 90:
		var shape: CapsuleShape3D = capsule.shape
		print("player capsule: height ", shape.height, " radius ", shape.radius, "  gravity ", ProjectSettings.get_setting("physics/3d/default_gravity"),
			"  ticks/s ", ProjectSettings.get_setting("physics/common/physics_ticks_per_second"), "  player y ", snappedf(p.global_position.y, 0.001))
		var img := root.get_texture().get_image()
		img.save_png(out)
		print("saved ", out, " ", img.get_size())
		quit()
	return false
