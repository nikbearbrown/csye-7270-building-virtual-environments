extends SceneTree
## Renders the main scene in a real window and saves 1x frames (headless uses a dummy renderer).
## Usage (from the project folder):
##   Godot_v4.7.2-stable_win64_console.exe --path . -s res://tests/capture_scene.gd -- <out_dir> [collisions]
## With "collisions", collision shapes are drawn as in Debug > Visible Collision Shapes.
## Each line of the optional plan file <out_dir>/plan.txt is either
##   name x y state facing(1|-1)            show one state's image at (x, y)
##   name fire aim_x aim_y wait_frames      cast at the aim point (mouse moved there), save after n frames
##   name wolf x image(run|lunge|down) facing flash(0|1)   pose the wolf (its AI stopped)
##   name hud hp N | fail Text_with_underscores | paused | cleared | none    set the HUD, then save
## Without it, one frame of the starting view is saved as start.png.

var out_dir := ""


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	out_dir = args[0] if args.size() > 0 else "user://captures"
	debug_collisions_hint = "collisions" in args
	call_deferred("run")


func frames(n: int) -> void:
	for i in n:
		await process_frame


func save(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.save_png(out_dir.path_join(name + ".png"))
	print("saved ", out_dir.path_join(name + ".png"), " ", img.get_size())


func run() -> void:
	DirAccess.make_dir_recursive_absolute(out_dir)
	var main: Node = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	await frames(10)
	var plan := out_dir.path_join("plan.txt")
	if not FileAccess.file_exists(plan) or main.player == null:
		await save("start")
		quit()
		return
	for line in FileAccess.get_file_as_string(plan).split("\n", false):
		var p := line.split(" ", false)
		var player: CharacterBody2D = main.player
		if p[1] == "hud":
			var hud: Control = main.hud
			match p[2]:
				"hp": hud.set_hp(int(p[3]), 5)
				"fail": hud.show_fail(p[3].replace("_", " "))
				"paused": hud.show_paused(true)
				"cleared": hud.show_cleared()
				_: hud.hide_message()
			await frames(3)
			await save(p[0])
			continue
		if p[1] == "wolf":
			var wolf: Node = main.get_node("Level/Wolf")
			wolf.set_physics_process(false)
			wolf.global_position = Vector2(float(p[2]), 327)
			wolf.sprite.texture = {"run": wolf.TEX_RUN, "lunge": wolf.TEX_LUNGE, "down": wolf.TEX_DOWN}[p[3]]
			wolf.facing = int(p[4])
			wolf._apply_facing()
			(wolf.sprite.material as ShaderMaterial).set_shader_parameter("flash", float(p[5]))
			# Main centres the camera on the player, so place her 150 px left of the wolf (also shows scale).
			player.capture_pose(Vector2(float(p[2]) - 150, 327), "idle", 1)
			await frames(3)
			await save(p[0])
			continue
		if p[1] == "fire":
			var aim := Vector2(float(p[2]), float(p[3]))
			player.set_physics_process(true)
			player.use_scripted = true
			# The crosshair is drawn in screen pixels: convert the world aim point through the camera.
			root.warp_mouse(aim - Vector2(main.camera.get_screen_center_position().x - 320.0, 0.0))
			player.scripted.aim = aim
			player.scripted.cast_pressed = true
			for i in int(p[4]):
				await physics_frame
			await save(p[0])
			continue
		player.capture_pose(Vector2(float(p[1]), float(p[2])), p[3], int(p[4]))
		for i in 6:   # let areas (pit, exit) see the new position before the frame is saved
			await physics_frame
		await frames(3)
		await save(p[0])
	quit()
