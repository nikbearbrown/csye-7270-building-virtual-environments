extends SceneTree
# make_sky.gd: writes the procedural sky as PNGs so the captures' texture can be looked at and re-made.
# Run: godot --headless --path <project dir> --script res://make_sky.gd -- <out dir>
const SkyLib := preload("res://sky_lib.gd")


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir: String = args[0] if args.size() > 0 else "/tmp"
	DirAccess.make_dir_recursive_absolute(out_dir)
	var t0 := Time.get_ticks_msec()
	var s512 := SkyLib.make_sky(512)
	s512.save_png(out_dir + "/sky-512.png")
	var t1 := Time.get_ticks_msec()
	var s1536 := SkyLib.make_sky(1536)
	s1536.save_png(out_dir + "/sky-1536.png")
	var t2 := Time.get_ticks_msec()
	# tiling check: put four copies side by side and save a 1024 crop around the seam
	var tile := Image.create(1024, 1024, false, Image.FORMAT_RGBA8)
	for ty in 2:
		for tx in 2:
			tile.blit_rect(s512, Rect2i(0, 0, 512, 512), Vector2i(tx * 512, ty * 512))
	tile.save_png(out_dir + "/sky-512-tiled-2x2.png")
	print("RESULT " + JSON.stringify({"id": "make_sky", "ms_512": t1 - t0, "ms_1536": t2 - t1, "out": out_dir}))
	quit(0)
