extends SceneTree
# run_scene.gd: reference runner for the capture contract. Plays one scene spec (JSON) with scene_player.gd and saves a PNG at each requested time.
#   godot --path <scratch project> --script res://run_scene.gd -- --spec <abs path to scenes/NAME.json> --out <png dir> [--times 0,2.5,5] [--fractions 0,0.5,0.85] [--size 1280x720]
# --fractions are fractions of the spec's "duration" (the film checks the 50 % and 85 % frames). Output names: <spec id>-t<seconds>.png.
# This is planning evidence at 1280 x 720; the film's own captures are rendered by the build session's harness at 3840 x 2160 from the same specs.
const Lib := preload("res://ol_lib.gd")

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame

func run() -> void:
	var a := OS.get_cmdline_user_args()
	var spec_path := ""
	var out_dir := "/tmp"
	var times: Array = []
	var fracs: Array = []
	var size := Vector2i(1280, 720)
	var i := 0
	while i < a.size():
		var k: String = a[i]
		if k == "--spec":
			spec_path = a[i + 1]
		elif k == "--out":
			out_dir = a[i + 1]
		elif k == "--times":
			for p in a[i + 1].split(","):
				times.append(float(p))
		elif k == "--fractions":
			for p in a[i + 1].split(","):
				fracs.append(float(p))
		elif k == "--size":
			var wh: PackedStringArray = a[i + 1].split("x")
			size = Vector2i(int(wh[0]), int(wh[1]))
		i += 2
	var spec: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(spec_path))
	var dur := float(spec.get("duration", 6.0))
	for f in fracs: times.append(f * dur)
	if times.is_empty(): times = [0.0, dur * 0.5, dur * 0.85]
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = size
	var player_script = load("res://scene_player.gd")
	if player_script == null or not player_script.can_instantiate():
		print("RESULT " + JSON.stringify({"id": "run_scene", "ok": false, "error": "scene_player.gd did not load (see the parse error above)"}))
		quit(1)
		return
	var player = player_script.new()
	root.add_child(player)
	player.setup(spec)
	await frames(2)
	var order := times.duplicate()
	order.sort()
	for t in order:
		player.at(t)
		await frames(3)
		var img := Lib.snap(root)
		Lib.save(img, out_dir.path_join("%s-t%s.png" % [spec.get("id", "scene"), str(snappedf(t, 0.01))]))
	print("RESULT " + JSON.stringify({"id": "run_scene", "spec": spec.get("id", ""), "times": order, "engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()}))
	quit(0)
