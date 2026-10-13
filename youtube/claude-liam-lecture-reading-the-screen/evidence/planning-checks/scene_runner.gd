extends SceneTree
# scene_runner.gd: loads one capture scene, steps it to chosen times, saves a PNG per time and prints named probes.
#   godot --path <project> --script res://scene_runner.gd -- --scene res://scene_c02_window.gd --duration 8 --times 0.2,0.5,0.9
#         [--route sub4k|native1080] [--prefix c02] [--probe name=fx,fy ...] [--shots <dir>]
# Without --route the scene is added to the root window (1280 x 720). With --route sub4k it is drawn by a 3840 x 2160 SubViewport over a
# 1280 x 720 canvas (size_2d_override), the route most captures use; PNGs are then saved at 1920 x 1080 to keep the folder small.
# With --route native1080 it is drawn by a 1920 x 1080 SubViewport at scale 1 and the scene is built for a 1920 x 1080 canvas: the route for shaders
# whose result depends on texel counts (C13, the mip-level blur; see verify10.gd). PNGs are saved at 1920 x 1080 as they are.
const L = preload("res://rts_lib.gd")

var A := {"scene": "", "duration": 8.0, "times": [], "utimes": [], "route": "", "prefix": "", "probe": [], "shots": "/private/tmp/claude-501/rts-checks/shots", "frames": 3}

func _initialize() -> void: call_deferred("run")

func parse() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		var k: String = a[i]
		if k == "--scene": A["scene"] = a[i + 1]; i += 2
		elif k == "--duration": A["duration"] = float(a[i + 1]); i += 2
		elif k == "--times":
			for s in String(a[i + 1]).split(","):
				A["times"].append(float(s))
			i += 2
		elif k == "--utimes":
			for s in String(a[i + 1]).split(","):
				A["utimes"].append(float(s))
			i += 2
		elif k == "--route": A["route"] = a[i + 1]; i += 2
		elif k == "--prefix": A["prefix"] = a[i + 1]; i += 2
		elif k == "--probe": A["probe"].append(a[i + 1]); i += 2
		elif k == "--shots": A["shots"] = a[i + 1]; i += 2
		elif k == "--frames": A["frames"] = int(a[i + 1]); i += 2
		else: i += 1

func frames(n: int) -> void:
	for i in range(n): await process_frame

func run() -> void:
	parse()
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	var scene_script: GDScript = load(A["scene"])
	var scene: Node2D = scene_script.new()
	scene.set("auto", false)
	scene.set("duration", float(A["duration"]))
	var sub: SubViewport = null
	if A["route"] == "sub4k":
		sub = SubViewport.new()
		sub.size = Vector2i(3840, 2160)
		sub.size_2d_override = Vector2i(1280, 720)
		sub.size_2d_override_stretch = true
		sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sub)
		sub.add_child(scene)
	elif A["route"] == "native1080":
		sub = SubViewport.new()
		sub.size = Vector2i(1920, 1080)
		scene.set("canvas_size", Vector2(1920, 1080))
		sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sub)
		sub.add_child(scene)
	else:
		root.add_child(scene)
	await frames(3)
	var prefix: String = A["prefix"] if A["prefix"] != "" else String(A["scene"]).get_file().get_basename()
	DirAccess.make_dir_recursive_absolute(A["shots"])
	var steps: Array = []
	for t in A["times"]:
		steps.append([t, "t%05.2f" % t])
	for uu in A["utimes"]:
		steps.append([uu * float(A["duration"]), "u%0.2f" % uu])
	for step in steps:
		var t: float = step[0]
		scene.call("set_time", t)
		await frames(int(A["frames"]))
		var img: Image
		if sub != null:
			img = sub.get_texture().get_image()
			if img.get_width() != 1920:
				img.resize(1920, 1080, Image.INTERPOLATE_BILINEAR)
		else:
			img = L.grab(root)
		var path := "%s/%s-%s.png" % [A["shots"], prefix, step[1]]
		img.save_png(path)
		var probes := {}
		for p in A["probe"]:
			var kv := String(p).split("=", true, 1)
			var xy := kv[1].split(",")
			probes[kv[0]] = L.px(img, float(xy[0]), float(xy[1]))
		L.out("frame", {"scene": A["scene"], "route": A["route"] if A["route"] != "" else "root", "t": t, "duration": A["duration"], "png": path, "probes": probes,
			"renderer": RenderingServer.get_current_rendering_method()})
	quit(0)
