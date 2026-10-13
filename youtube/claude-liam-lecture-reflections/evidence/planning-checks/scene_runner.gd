extends SceneTree
# scene_runner.gd: plays one capture scene from capture_scenes.gd (a stand-in for the build session's capture harness) and
# CHECKS it: at the requested times it prints what the picture contains, and it can dump a frame (downscaled to 1280 x 720).
#
#   godot --path <scratch project> --script res://scene_runner.gd -- --capture C08 [--route direct|sv] [--scale 1|3] [--times 2,10] [--out DIR]
#
#   --all-frames DIR write EVERY frame as DIR/f00000.png (30 fps, native size with --full; this is how the film's captures are rendered:
#                    see capture_scene.sh, which then runs ffmpeg). --limit N stops after N frames (for a short test).
#   --length SECONDS the clip length. The build plays every scene at the MEASURED length of its beat (audio first): all scripted events keep
#                    their place as a fraction of the clip (time is simply scaled by planned / length), so a 12.2 s beat and a 13.5 s scene
#                    line up. Default: the scene's planned length (the TABLE in capture_scenes.gd). "50%" and "85%" times follow the length.
#   --route direct   draw straight into the window's root viewport (needs --scale 1; the window is made 1280 x 720)
#   --route sv       the 4K route: a 3840 x 2160 SubViewport with size_2d_override 1280 x 720 and stretch on (use --scale 3)
# Run every capture in its own Godot process. Prints one RESULT line per requested time.
const CS = preload("res://capture_scenes.gd")
const P = preload("res://pond_common.gd")

var args := {"capture": "C01", "route": "direct", "scale": 1, "times": "", "out": "", "all_frames": "", "full": false, "limit": 0, "length": 0.0}
var cs
var sv: SubViewport
var parent_node: Node

func _initialize() -> void:
	call_deferred("run")

func parse() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		match a[i]:
			"--capture": args["capture"] = a[i + 1]; i += 2
			"--route": args["route"] = a[i + 1]; i += 2
			"--scale": args["scale"] = int(a[i + 1]); i += 2
			"--times": args["times"] = a[i + 1]; i += 2
			"--out": args["out"] = a[i + 1]; i += 2
			"--all-frames": args["all_frames"] = a[i + 1]; i += 2
			"--full": args["full"] = true; i += 1
			"--limit": args["limit"] = int(a[i + 1]); i += 2
			"--length": args["length"] = float(a[i + 1]); i += 2
			_: i += 1

func out(d: Dictionary) -> void:
	print("RESULT " + JSON.stringify(d))

func grab() -> Image:
	RenderingServer.force_draw(false)
	var img: Image = sv.get_texture().get_image() if sv != null else root.get_texture().get_image()
	if img.get_width() != 1280 and not args["full"]:
		img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
	return img

func classify_zone(c: Color, refs: Dictionary) -> String:
	var best := "other"
	var bd := 0.04
	for k in refs:
		var r: Color = refs[k]
		var d := Vector3(c.r - r.r, c.g - r.g, c.b - r.b).length()
		if d < bd:
			bd = d
			best = k
	return best

func check_three(t: float, img: Image) -> Dictionary:
	var refs := {"stage": CS.STAGE, "A": CS.COL_A, "B": CS.COL_B, "C": CS.COL_C, "black": Color(0, 0, 0)}
	var zones := {"A_only": Vector2(170, 340), "A_B": Vector2(275, 445), "B_only": Vector2(290, 550), "B_C": Vector2(395, 525), "C_only": Vector2(500, 565)}
	var d := {"main": {}}
	for k in zones:
		d["main"][k] = classify_zone(img.get_pixel(int(zones[k].x), int(zones[k].y)), refs)
	var windows := {"w1": Vector2(740, 56)}
	if cs.N.has("w2"):
		windows["w2"] = Vector2(740, 384)
	for w in windows:
		var o: Vector2 = windows[w]
		d[w] = {}
		for k in zones:
			var p: Vector2 = zones[k]
			d[w][k] = classify_zone(img.get_pixel(int(o.x + p.x * 0.375), int(o.y + p.y * 0.375)), refs)
	return d

func check_pond(t: float, img: Image) -> Dictionary:
	var player: Sprite2D = cs.N["player"]
	var refl: Sprite2D = cs.N["refl"]
	var x := int(round(player.position.x))
	var y := int(round(player.position.y + P.REFLECT_OFFSET))
	var with_c := img.get_pixel(clampi(x, 0, 1279), clampi(y, 0, 719))
	var was := refl.visible
	refl.visible = false
	await process_frame
	var none_img := grab()
	refl.visible = was
	await process_frame
	var n := 0
	var left := x - P.SPRITE_N / 2
	var top := y - P.SPRITE_N / 2
	for sy in range(maxi(top, 0), mini(top + P.SPRITE_N, 720)):
		for sx in range(maxi(left, 0), mini(left + P.SPRITE_N, 1280)):
			var a := img.get_pixel(sx, sy)
			var b := none_img.get_pixel(sx, sy)
			if absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.03:
				n += 1
	# mask leak in the final frame (mask colours: pure red, pure green, half red)
	var leak := 0
	for yy in range(0, 720, 4):
		for xx in range(0, 1280, 4):
			var c := img.get_pixel(xx, yy)
			if Vector3(c.r - 1.0, c.g, c.b).length() < 0.2 or Vector3(c.r, c.g - 1.0, c.b).length() < 0.2 or Vector3(c.r - 0.502, c.g, c.b).length() < 0.2:
				leak += 16
	var wp := img.get_pixel(100, 600)
	return {"player_x": player.position.x, "player_y": player.position.y, "reflection_pixels_changed": n, "pixel_at_reflection_centre": [snappedf(with_c.r, 0.001), snappedf(with_c.g, 0.001), snappedf(with_c.b, 0.001)],
		"mask_coloured_pixels": leak, "open_water_pixel_100_600": [snappedf(wp.r, 0.001), snappedf(wp.g, 0.001), snappedf(wp.b, 0.001)]}

func run() -> void:
	parse()
	RenderingServer.set_default_clear_color(CS.STAGE)
	var shaders := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"
	cs = CS.new()
	if not CS.TABLE.has(args["capture"]):
		out({"error": "unknown capture id " + String(args["capture"]), "known": CS.TABLE.keys()})
		quit(2)
		return
	var info: Dictionary = cs.setup(args["capture"], shaders, int(args["scale"]))
	var planned: float = info["duration"]
	var dur: float = float(args["length"]) if float(args["length"]) > 0.0 else planned
	var k: float = planned / dur          # scene seconds per clip second (1.0 unless --length is given)
	root.size = Vector2i(1280, 720)
	if args["route"] == "sv":
		sv = SubViewport.new()
		sv.size = Vector2i(3840, 2160)
		sv.size_2d_override = Vector2i(1280, 720)
		sv.size_2d_override_stretch = true
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		parent_node = sv
	else:
		parent_node = root
	await process_frame
	var t_build := Time.get_ticks_msec()
	cs.build(parent_node)
	var header := {"capture": args["capture"], "label": info["label"], "duration_s": dur, "planned_duration_s": planned, "time_scale": snappedf(k, 0.0001), "route": args["route"], "scale": args["scale"], "build_ms": Time.get_ticks_msec() - t_build,
		"renderer": RenderingServer.get_current_rendering_method(), "engine": Engine.get_version_info()["string"]}
	if k < 0.7 or k > 1.4:
		header["retime_warning"] = "the scene is played at %.2f x its planned speed (planned %.1f s, clip %.1f s): LOOK at the video; if it reads as slow motion or a rush, tell Bear" % [k, planned, dur]
	out(header)
	var times: Array = []
	for s in String(args["times"]).split(",", false):
		if s.ends_with("%"):
			times.append(float(s.trim_suffix("%")) / 100.0 * dur)      # "50%" and "85%" are the frames Gate V samples
		else:
			times.append(float(s))
	times.sort()
	var fps := 30
	var total := int(dur * fps)
	var ti := 0
	if args["limit"] > 0:
		total = mini(total, int(args["limit"]))
	var written := 0
	if args["all_frames"] != "":
		DirAccess.make_dir_recursive_absolute(args["all_frames"])
	for i in range(total + 1):
		var t := float(i) / fps
		cs.tick(t * k)
		await process_frame
		if args["all_frames"] != "" and i < total:
			var fimg := grab()
			fimg.save_png("%s/f%05d.png" % [args["all_frames"], i])
			written += 1
			continue
		if ti < times.size() and t >= times[ti] - 0.0001:
			await process_frame
			var img := grab()
			var d: Dictionary
			if info["family"] == "three":
				d = check_three(t, img)
			else:
				d = await check_pond(t, img)
			d["t"] = t
			d["capture"] = args["capture"]
			if args["out"] != "":
				DirAccess.make_dir_recursive_absolute(args["out"])
				var path: String = "%s/%s-t%05.2f.png" % [args["out"], args["capture"], t]
				img.save_png(path)
				d["png"] = path
			out(d)
			ti += 1
	if args["all_frames"] != "":
		out({"capture": args["capture"], "frames_written": written, "dir": args["all_frames"], "size": [3840 if args["full"] and args["route"] == "sv" else 1280, 2160 if args["full"] and args["route"] == "sv" else 720], "fps": fps})
	quit(0)
