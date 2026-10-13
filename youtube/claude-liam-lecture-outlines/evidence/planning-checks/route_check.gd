extends SceneTree
# N: the capture route. The planning evidence is rendered at 1280 x 720. The film's captures are rendered through a SubViewport of 3840 x 2160 over the same
# 1280 x 720 canvas (the series' native-size route, size_2d_override with stretch). No shader in this film reads window pixels (no FRAGCOORD, SCREEN_PIXEL_SIZE,
# LIGHT_POSITION), so the two routes should draw the same picture. This plays one scene spec through BOTH routes at the same times and saves both PNGs.
# analyze_route.py then samples the 3840 x 2160 image at the centre of every 3 x 3 block and compares it with the 1280 x 720 image, pixel by pixel.
# Run: godot --path <scratch project> --script res://route_check.gd -- --spec <spec.json> --out <png dir> [--fractions 0.5,0.85 | --times 0.05,3.36,6.08]
const Lib := preload("res://ol_lib.gd")

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame

func run() -> void:
	var a := OS.get_cmdline_user_args()
	var spec_path := ""
	var out_dir := "/tmp"
	var fracs: Array = [0.5, 0.85]
	var abs_times: Array = []
	var i := 0
	while i < a.size():
		if a[i] == "--spec": spec_path = a[i + 1]
		elif a[i] == "--out": out_dir = a[i + 1]
		elif a[i] == "--fractions":
			fracs = []
			for p in a[i + 1].split(","): fracs.append(float(p))
		elif a[i] == "--times":                          # absolute seconds, ascending (needed for scripted key input: events fire in order)
			for p in a[i + 1].split(","): abs_times.append(float(p))
		i += 2
	var spec: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(spec_path))
	var dur := float(spec.get("duration", 6.0))
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = Vector2i(1280, 720)
	var player_script = load("res://scene_player.gd")
	var native = player_script.new()
	root.add_child(native)
	native.setup(spec)
	var vp := SubViewport.new()
	vp.size = Vector2i(3840, 2160)
	vp.size_2d_override = Vector2i(1280, 720)
	vp.size_2d_override_stretch = true
	vp.transparent_bg = false
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var big = player_script.new()
	vp.add_child(big)
	big.input_viewport = vp          # scripted key events (scene C26) must be pushed into the SubViewport, not the root window
	big.setup(spec)
	await frames(2)
	var id: String = spec.get("id", "scene")
	var times: Array = abs_times.duplicate()
	if times.is_empty():
		for f in fracs: times.append(snappedf(float(f) * dur, 0.01))
	for t in times:
		native.at(t)
		big.at(t)
		await frames(3)
		RenderingServer.force_draw(false)
		Lib.save(root.get_texture().get_image(), out_dir.path_join("%s-native-t%s.png" % [id, str(t)]))
		Lib.save(vp.get_texture().get_image(), out_dir.path_join("%s-sub3-t%s.png" % [id, str(t)]))
	print("RESULT " + JSON.stringify({"id": "route", "spec": id, "times": times, "engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "subviewport": [vp.size.x, vp.size.y]}))
	quit(0)
