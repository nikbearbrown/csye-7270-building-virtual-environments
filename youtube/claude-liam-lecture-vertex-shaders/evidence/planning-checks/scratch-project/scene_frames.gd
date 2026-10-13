extends SceneTree
# Runs one capture scene from capture_scenes.gd and saves frames at the requested times (real time: planning evidence only, not the offline capture).
#   godot --path <proj> --script res://scene_frames.gd -- --scene pair --times 0.5,1.5,3.0 --out /abs/dir [--shaders /abs/shader/dir] [--duration D]
const V = preload("res://vscene.gd")
const CS = preload("res://capture_scenes.gd")

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var a := OS.get_cmdline_user_args()
	var scene := "pair"
	var times: Array = [1.5]
	var out_dir := V.png_dir()
	var shaders := V.film_dir().path_join("lab-shaders")
	var size := "1280x720"
	var duration := 12.0
	var i := 0
	while i < a.size():
		match a[i]:
			"--scene": scene = a[i + 1]
			"--times":
				times = []
				for s in String(a[i + 1]).split(","):
					times.append(float(s))
			"--out": out_dir = a[i + 1]
			"--shaders": shaders = a[i + 1]
			"--size": size = a[i + 1]
			"--duration": duration = float(a[i + 1])
		i += 2
	var wh := size.split("x")
	V.setup(root, int(wh[0]), int(wh[1]))
	DirAccess.make_dir_recursive_absolute(out_dir)
	var holder := Node2D.new()
	root.add_child(holder)
	var ctx := CS.build(scene, holder, shaders, duration)
	root.size = ctx["canvas"]                                    # each scene declares its own logical canvas
	var t := 0.0
	var next := 0
	var start_ms := Time.get_ticks_msec()
	await process_frame
	while next < times.size():
		t = (Time.get_ticks_msec() - start_ms) / 1000.0
		CS.tick(ctx, t)
		await process_frame
		if t >= times[next]:
			RenderingServer.force_draw(false)
			var img := root.get_texture().get_image()
			var path := "%s/scene-%s-t%.2f.png" % [out_dir, scene, times[next]]
			img.save_png(path)
			V.out("scene-frame", {"scene": scene, "requested_t": times[next], "actual_t": snappedf(t, 0.001), "png": path})
			next += 1
	quit(0)
