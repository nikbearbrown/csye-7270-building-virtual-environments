extends SceneTree
# tools/smoke.gd: loads scenes/water.tscn exactly as the editor would, runs it for 3 seconds of real time in a window, saves one frame and prints a few numbers.
#   godot --path . --script tools/smoke.gd -- /absolute/path/frame.png
# This is a real-time run: its picture depends on the clock when it ends (the film's captures use a fixed clock instead).
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)
	root.size = Vector2i(1280, 720)
	var scene: PackedScene = load("res://scenes/water.tscn")
	var cove := scene.instantiate()
	root.add_child(cove)
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 3000:
		await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		img.save_png(args[0])
	var water: MeshInstance3D = cove.get_node("Water")
	var mesh := water.mesh as PlaneMesh
	var driver = cove.get_node("WaterDriver")
	print("SMOKE renderer=", RenderingServer.get_current_rendering_method(), " nodes=", cove.get_child_count(), " water cuts=", mesh.subdivide_width, "x", mesh.subdivide_depth,
		" vertices=", (mesh.subdivide_width + 2) * (mesh.subdivide_depth + 2), " wave_clock=", snappedf(driver.clock, 0.01), " buoy_y=", snappedf(cove.get_node("Buoy").position.y, 0.001),
		" centre pixel=", img.get_pixel(640, 360))
	quit()
