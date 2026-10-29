extends SceneTree
## Compares one in-engine capture with an OS screenshot of the same frame, which
## the assignment's Use It asks for once. It renders hint_experiment.tscn, saves
## the frame the engine drew, then has macOS's screencapture take the window's
## client area only, and prints both images' values at the six band centres.
## Not headless. Run from assignment-5/:
##   godot --path godot --resolution 1920x1080 --always-on-top --script res://tests/capture_hint_vs_os.gd
## Both PNGs go to evidence/use-it/os-compare/.

const SCENE := "res://scenes/hint_experiment.tscn"
const PREDICTED := {"QuadA": [64, 128, 192], "QuadB": [137, 188, 225]} ## CHANGE-BRIEF.md section 4
const BAND_WIDTH := 0.5 ## m, a third of the 1.5 m quad


func _initialize() -> void:
	if DisplayServer.get_name() == "headless":
		printerr("STOP this needs a window: a headless run draws no frame to read")
		quit(1)
		return
	var out := ProjectSettings.globalize_path("res://").path_join("../evidence/use-it/os-compare").simplify_path()
	DirAccess.make_dir_recursive_absolute(out)
	var scene := (load(SCENE) as PackedScene).instantiate() as Node3D
	root.add_child(scene)
	# screencapture's coordinates start at the primary display's top-left corner,
	# so put the window on that display first.
	var primary := DisplayServer.get_primary_screen()
	var origin := DisplayServer.screen_get_position(primary)
	DisplayServer.window_set_current_screen(primary)
	DisplayServer.window_set_position(origin + Vector2i(64, 128))
	for i in 30:
		await process_frame
	await RenderingServer.frame_post_draw
	var engine := root.get_texture().get_image()
	engine.save_png(out.path_join("engine.png"))

	# The window's client area: Godot gives pixels from its own origin; screencapture takes points.
	var scale := DisplayServer.screen_get_scale(primary)
	var pos := Vector2(DisplayServer.window_get_position() - origin) / scale
	var size := Vector2(DisplayServer.window_get_size()) / scale
	var rect := "%d,%d,%d,%d" % [roundi(pos.x), roundi(pos.y), roundi(size.x), roundi(size.y)]
	print("WINDOW screen %d of %d (primary %d at %s, %s px, scale %s); window at %s px, %s px" % [
		DisplayServer.window_get_current_screen(), DisplayServer.get_screen_count(), primary, origin,
		DisplayServer.screen_get_size(primary), scale, DisplayServer.window_get_position(), DisplayServer.window_get_size()])
	var os_path := out.path_join("os-screenshot.png")
	var output := []
	var code := OS.execute("screencapture", ["-x", "-t", "png", "-R", rect, os_path], output, true)
	print("SCREENCAPTURE exit %d, region %s in points %s" % [code, rect, "".join(output).strip_edges()])
	var shot := Image.load_from_file(os_path) if FileAccess.file_exists(os_path) else null
	if shot == null:
		printerr("STOP no OS screenshot was written")
		quit(1)
		return
	shot.convert(Image.FORMAT_RGB8)
	print("SIZES engine %s, OS screenshot %s" % [engine.get_size(), shot.get_size()])
	# If the region missed the window, the file holds someone else's screen: remove it unread.
	var corner := shot.get_pixel(shot.get_width() / 20, shot.get_height() / 20)
	var background := engine.get_pixel(engine.get_width() / 20, engine.get_height() / 20)
	if shot.get_size() != engine.get_size() or absi(corner.r8 - background.r8) > 24 or absi(corner.b8 - background.b8) > 24:
		DirAccess.remove_absolute(os_path)
		printerr("STOP the OS screenshot did not show this window (corner %s, expected near %s); it was removed" % [corner.to_html(false), background.to_html(false)])
		quit(1)
		return

	var camera := scene.get_node("Camera") as Camera3D
	var ratio := Vector2(shot.get_size()) / Vector2(engine.get_size())
	for quad: String in ["QuadA", "QuadB"]:
		var node := scene.get_node(quad) as Node3D
		for band in 3:
			var at := camera.unproject_position(node.global_position + Vector3((band - 1) * BAND_WIDTH, 0.0, 0.0))
			var e := engine.get_pixelv(Vector2i(at.round()))
			var o := shot.get_pixelv(Vector2i((at * ratio).round()))
			print("BAND %s %d: predicted %d; engine %d, %d, %d; OS screenshot %d, %d, %d" % [
				quad, band + 1, PREDICTED[quad][band], e.r8, e.g8, e.b8, o.r8, o.g8, o.b8])
	quit(0)
