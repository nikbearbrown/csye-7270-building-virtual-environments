extends SceneTree
# render_captures.gd: builds capture scenes from captures.json in a 1920x1080 SubViewport (scale 1), steps the capture clock at 30 steps per second
# and writes PNG stills at the requested times. This is a planning check (stills only), not the film's recording.
# Run: godot --path <project dir> --script res://render_captures.gd -- <shader dir> <captures.json> <out dir> <id>:<t1>,<t2>,... [<id>:...]
const LS := preload("res://light_scene.gd")

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame

func run() -> void:
	var a := OS.get_cmdline_user_args()
	var shaders := a[0]
	var caps := a[1]
	var outdir := a[2]
	DirAccess.make_dir_recursive_absolute(outdir)
	for k in range(3, a.size()):
		var parts := a[k].split(":")
		var id := parts[0]
		var times: PackedFloat64Array = PackedFloat64Array()
		for tt in parts[1].split(","):
			times.append(float(tt))
		var sv := SubViewport.new()
		sv.size = Vector2i(1920, 1080)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var s: Node2D = LS.new()
		s.manual = true
		s.setup(id, shaders, caps)
		sv.add_child(s)
		await frames(3)
		for T in times:
			while s.t < T - 0.0001:
				s.step(1.0 / 30.0)
				await process_frame
			await frames(2)
			RenderingServer.force_draw(false)
			var im := sv.get_texture().get_image()
			var path := "%s/%s-t%.2f.png" % [outdir, id, T]
			im.save_png(path)
			print("RESULT " + JSON.stringify({"id": id, "t": T, "png": path, "size": [im.get_width(), im.get_height()], "state": s.state()}))
		sv.queue_free()
		await frames(3)
	quit(0)
