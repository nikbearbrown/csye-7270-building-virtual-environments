extends SceneTree
# scene_frames.gd: renders every capture scene at u = 0.10, 0.50 and 0.85 of its beat (the Gate V sample points are 0.50 and 0.85) and saves
# PNGs (1280 x 720, root window) into the folder given after --out. Durations are the beats' estimated audio lengths.
#   godot --path <project> --script res://scene_frames.gd -- --out /abs/dir
const L = preload("res://rts_lib.gd")
const SCENES := [
	["c01_pool", 13.6], ["c02_window", 12.2], ["c03_addresses", 12.9], ["c04_invert", 11.9], ["c05_gray", 12.2], ["c06_spot_oval", 10.5],
	["c07_spot_swap", 13.3], ["c08_spot_game", 11.2], ["c09_shift", 11.9], ["c10_ripple_still", 12.2], ["c11_ripple_time", 8.8], ["c12_amount", 9.9],
	["c13_blur", 11.6], ["c14_ride_glued", 12.6], ["c15_pool_tint", 11.9], ["c16_pan", 11.6], ["c17_xray", 12.9], ["c18_overlap", 12.9],
	["c19_overlap_fix", 13.3], ["c20_fresh_layer", 11.9], ["c21_hud", 9.2], ["c22_edge", 12.2], ["c23_finale", 12.6]]
const US := [0.10, 0.50, 0.85]

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func run() -> void:
	var out_dir := "/private/tmp/claude-501/rts-checks/frames"
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		if a[i] == "--out":
			out_dir = a[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	var holder: Node2D = null
	for entry in SCENES:
		if holder != null:
			holder.queue_free()
			await frames(2)
		holder = Node2D.new()
		root.add_child(holder)
		var sc: Node2D = (load("res://scene_%s.gd" % entry[0]) as GDScript).new()
		sc.set("auto", false)
		sc.set("duration", float(entry[1]))
		holder.add_child(sc)
		await frames(3)
		for u in US:
			sc.call("set_time", u * float(entry[1]))
			await frames(4)
			var img := L.grab(root)
			var path := "%s/%s-u%02d.png" % [out_dir, entry[0], int(round(u * 100.0))]
			img.save_png(path)
		L.note("rendered " + String(entry[0]))
	quit(0)
