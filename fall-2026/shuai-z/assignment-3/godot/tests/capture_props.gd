extends SceneTree
## Renders res://scenes/props_room.tscn in a real window and saves screenshots:
## the scene's own camera, then from behind, from low down, from above and from below the floor.
## Not headless: the headless renderer draws nothing.
##
## Run from the repository's assignment-3 folder:
##   timeout 120 /Applications/Godot.app/Contents/MacOS/Godot --path godot --script res://tests/capture_props.gd -- ../evidence/godot

const VIEWS := [
	["1-camera", Vector3.ZERO, Vector3.ZERO], # the scene's own camera
	["2-behind", Vector3(-0.3, 1.6, -4.2), Vector3(-0.3, 0.25, 0)],
	["3-low", Vector3(-0.3, 0.12, 3.6), Vector3(-0.3, 0.3, 0)],
	["4-above", Vector3(-0.3, 6.5, 0.01), Vector3(-0.3, 0, 0)],
	["5-below", Vector3(-0.3, -2.5, 2.0), Vector3(-0.3, 0, 0)], # the floor plane is one-sided, so the undersides show
]


func _initialize() -> void:
	var out_dir := "../evidence/godot"
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		out_dir = args[0]
	out_dir = ProjectSettings.globalize_path("res://").path_join(out_dir).simplify_path()
	DirAccess.make_dir_recursive_absolute(out_dir)

	var scene: Node3D = load("res://scenes/props_room.tscn").instantiate()
	root.add_child(scene)
	await process_frame # the scene is in the tree only from here; before it, global_transform is the identity
	var cam := scene.get_node("Camera") as Camera3D
	var home := cam.global_transform

	for v in VIEWS:
		if v[0] == "1-camera":
			cam.global_transform = home
		else:
			cam.look_at_from_position(v[1], v[2], Vector3.UP)
		for i in 10:
			await process_frame
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		var path := out_dir.path_join("props_room-%s.png" % v[0])
		print("%s %s (%dx%d)" % [path, error_string(img.save_png(path)), img.get_width(), img.get_height()])
	quit(0)
