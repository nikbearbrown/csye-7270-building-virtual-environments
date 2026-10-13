extends SceneTree
# scene_capture.gd: the reference capture driver for the film's Godot captures (C01 to C23). It renders ONE capture scene, frame by frame, to PNGs.
# Run it with a fixed tick so TIME-driven shaders (ripples, the pool) repeat exactly:
#   godot --path <project> --fixed-fps 30 --script res://scene_capture.gd -- --scene res://scene_c01_pool.gd --duration 13.6 --out /abs/dir [--fps 30] [--width 3840 --height 2160] [--frames N] [--native]
# The scene is drawn by a SubViewport of --width x --height over a 1280 x 720 canvas (size_2d_override), the route used for most captures. With --native
# there is no override: the SubViewport is --width x --height (use 1920 x 1080) at scale 1 and the scene is built for a canvas of that size. That is the
# route for a shader whose result depends on texel counts (C13, the mip-level blur; see verify10.gd). Frame i is scene.set_time(i / fps).
# Then: ffmpeg -framerate 30 -i <out>/f%05d.png -c:v libx264 -pix_fmt yuv420p <name>.mp4  (the build session does that step; capture_all.py does it for all 23).
# Offline and fixed-tick: it says nothing about real-time frame rate. Scripted input in a scene is labelled in the lane's videoLabel.
const L = preload("res://rts_lib.gd")

var A := {"scene": "", "duration": 8.0, "fps": 30, "out": "", "width": 3840, "height": 2160, "frames": 0, "native": false}

func _initialize() -> void: call_deferred("run")

func parse() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		var k: String = a[i]
		if k == "--scene": A["scene"] = a[i + 1]; i += 2
		elif k == "--duration": A["duration"] = float(a[i + 1]); i += 2
		elif k == "--fps": A["fps"] = int(a[i + 1]); i += 2
		elif k == "--out": A["out"] = a[i + 1]; i += 2
		elif k == "--width": A["width"] = int(a[i + 1]); i += 2
		elif k == "--height": A["height"] = int(a[i + 1]); i += 2
		elif k == "--frames": A["frames"] = int(a[i + 1]); i += 2
		elif k == "--native": A["native"] = true; i += 1
		else: i += 1

func run() -> void:
	parse()
	if A["out"] == "" or A["scene"] == "":
		print("usage: --scene res://scene_cNN_name.gd --duration SECONDS --out /abs/dir")
		quit(2)
		return
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	DirAccess.make_dir_recursive_absolute(A["out"])
	var sub := SubViewport.new()
	sub.size = Vector2i(int(A["width"]), int(A["height"]))
	var scene: Node2D = (load(A["scene"]) as GDScript).new()
	if A["native"]:
		scene.set("canvas_size", Vector2(float(A["width"]), float(A["height"])))
	else:
		sub.size_2d_override = Vector2i(1280, 720)
		sub.size_2d_override_stretch = true
	sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sub)
	scene.set("auto", false)
	scene.set("duration", float(A["duration"]))
	sub.add_child(scene)
	await process_frame
	await process_frame
	var n: int = int(A["frames"]) if int(A["frames"]) > 0 else int(ceil(float(A["duration"]) * float(A["fps"])))
	var changed := 0
	var prev: PackedByteArray = PackedByteArray()
	for i in n:
		scene.call("set_time", float(i) / float(A["fps"]))
		await process_frame
		RenderingServer.force_draw(false)
		var img := sub.get_texture().get_image()
		img.save_png("%s/f%05d.png" % [A["out"], i])
		var d := img.get_data()
		if prev.size() > 0 and d != prev:
			changed += 1
		prev = d
	L.out("capture", {"scene": A["scene"], "frames": n, "fps": A["fps"], "size": [int(A["width"]), int(A["height"])], "route": "native" if A["native"] else "sub-viewport over 1280 x 720", "frames_that_differ_from_the_previous": changed, "out": A["out"], "renderer": RenderingServer.get_current_rendering_method()})
	quit(0)
