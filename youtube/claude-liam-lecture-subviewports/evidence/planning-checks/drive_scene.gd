extends SceneTree
# Drives one CaptureScene: builds it into a 1280 x 720 canvas, steps t by 1/30 per frame, saves PNG frames at the requested times.
# godot --path <dir> --fixed-fps 30 --script res://drive_scene.gd -- <scene id> <out dir> <t1> <t2> ...
var args: PackedStringArray

func _initialize() -> void: call_deferred("run")

func run() -> void:
	args = OS.get_cmdline_user_args()
	var id := args[0]
	var out_dir := args[1]
	var times: Array = []
	for i in range(2, args.size()):
		times.append(float(args[i]))
	DirAccess.make_dir_recursive_absolute(out_dir)
	root.size = Vector2i(1280, 720)
	var canvas := Node2D.new()
	root.add_child(canvas)
	var sc := CaptureScene.new(id)
	sc.build(canvas)
	var t := 0.0
	var idx := 0
	var step := 1.0 / 30.0
	sc.update(0.0)
	await process_frame
	var guard := 0
	while idx < times.size() and guard < 3000:
		sc.update(t)
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per logical frame (a covered window is not drawn on every frame)
		if t + 1e-6 >= times[idx]:
			var img := root.get_texture().get_image()
			img.save_png("%s/%s_t%05.2f.png" % [out_dir, id, times[idx]])
			idx += 1
		t += step
		guard += 1
	print("RESULT " + JSON.stringify({"scene": id, "saved": times, "frames_stepped": guard}))
	quit(0)
