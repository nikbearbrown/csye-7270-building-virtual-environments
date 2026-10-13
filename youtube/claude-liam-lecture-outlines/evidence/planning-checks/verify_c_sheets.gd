extends SceneTree
# C: sprite sheets and animation. What does UV cover on a Sprite2D that shows one frame of a sheet (hframes) or a region, and does the outline bleed
# across the frame border? Does an AnimatedSprite2D (separate frame textures, or atlas frames) keep its outline?
# Run: godot --path <scratch project> --script res://verify_c_sheets.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func px(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

# a 128x64 sheet: frame 0 (left) is solid teal edge to edge; frame 1 (right) is a small disc with transparent surroundings
func make_sheet() -> Image:
	var img := Image.create_empty(128, 64, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in 64:
		for x in 64:
			img.set_pixel(x, y, Lib.TEAL)
	var c := Vector2(96, 32)
	for y in 64:
		for x in range(64, 128):
			if Vector2(x, y).distance_to(c) < 14.0:
				img.set_pixel(x, y, Lib.CREAM)
	return img

func snap_to(name: String) -> Image:
	var im := Lib.snap(root)
	Lib.save(im, OUT + "/" + name + ".png")
	return im

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--out": OUT = a[i + 1]
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = Vector2i(640, 360)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var sheet := ImageTexture.create_from_image(make_sheet())

	# C1: hframes sheet, frame 1 shown at scale 4 (64x64 frame -> 256x256 on screen), UV painted
	var sp := Sprite2D.new()
	sp.texture = sheet
	sp.hframes = 2
	sp.frame = 1
	sp.centered = false
	sp.position = Vector2(192, 52)
	sp.scale = Vector2(4, 4)
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp.material = Lib.material("show-uv.gdshader")
	root.add_child(sp)
	await frames(3)
	var im := snap_to("sheet-hframes-uv")
	# frame occupies x 192..448, y 52..308 on screen
	out("C1-hframes-uv", {"uv_at_frame_left_edge_top": px(im, 194, 54), "uv_at_frame_right_edge_bottom": px(im, 445, 305), "uv_at_frame_centre": px(im, 320, 180),
		"reading": "red = UV.x, green = UV.y. If UV covered only the frame, red would run 0 to 1 across it; the docs say the whole texture space is covered, so red runs about 0.5 to 1"})
	sp.material = Lib.material("show-pixel-size.gdshader")
	await frames(3)
	im = snap_to("sheet-hframes-pixelsize")
	out("C1b-hframes-pixel-size", {"centre": px(im, 320, 180), "reading": "red 0.5 = 1/128 (the whole sheet is 128 wide), green 1.0 = 1/64 (64 tall)"})

	# C1c: the outline on that frame: does the solid neighbouring frame bleed a line into the left edge of frame 1?
	sp.material = Lib.material("08-loop.gdshader", {"thickness": 4.0, "line_color": Color(0.25, 0.25, 0.75, 1.0)})
	await frames(3)
	im = snap_to("sheet-hframes-outline-t4")
	var line_cols: Array = []
	for x in range(192, 215):
		var c := im.get_pixel(x, 180)
		line_cols.append(1 if c.is_equal_approx(Color(0.251, 0.251, 0.749)) or (absf(c.r - 0.25) < 0.02 and absf(c.b - 0.75) < 0.02) else 0)
	out("C1c-hframes-outline", {"line_pixels_along_row_y180_from_frame_left": line_cols, "reading": "1 = outline colour. A run of 1s at the very left edge of frame 1 is a line drawn from frame 0's pixels"})

	# C2: region_enabled with the same pixels
	sp.hframes = 1
	sp.frame = 0
	sp.region_enabled = true
	sp.region_rect = Rect2(64, 0, 64, 64)
	await frames(3)
	im = snap_to("sheet-region-outline-t4")
	var line_cols2: Array = []
	for x in range(192, 215):
		var c2 := im.get_pixel(x, 180)
		line_cols2.append(1 if (absf(c2.r - 0.25) < 0.02 and absf(c2.b - 0.75) < 0.02) else 0)
	out("C2-region-outline", {"line_pixels_along_row_y180_from_frame_left": line_cols2})
	sp.region_filter_clip_enabled = true
	await frames(3)
	im = snap_to("sheet-region-clip-outline-t4")
	var line_cols3: Array = []
	for x in range(192, 215):
		var c3 := im.get_pixel(x, 180)
		line_cols3.append(1 if (absf(c3.r - 0.25) < 0.02 and absf(c3.b - 0.75) < 0.02) else 0)
	out("C2b-region-filter-clip", {"line_pixels_along_row_y180_from_frame_left": line_cols3, "note": "region_filter_clip_enabled = true"})
	sp.queue_free()
	await frames(2)

	# C3: AnimatedSprite2D, two separate padded textures (a disc, and a wide pill), same shader
	var f0 := ImageTexture.create_from_image(Lib.blob(128))
	var wide := Image.create_empty(128, 128, false, Image.FORMAT_RGBA8)
	wide.fill(Color(0, 0, 0, 0))
	for y in range(48, 80):
		for x in range(20, 108):
			wide.set_pixel(x, y, Lib.TEAL)
	var f1 := ImageTexture.create_from_image(wide)
	var sf := SpriteFrames.new()
	sf.add_frame("default", f0)
	sf.add_frame("default", f1)
	var an := AnimatedSprite2D.new()
	an.sprite_frames = sf
	an.centered = false
	an.position = Vector2(256, 116)
	an.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	an.material = Lib.material("08-loop.gdshader", {"thickness": 3.0, "line_color": Color(0.25, 0.25, 0.75, 1.0)})
	root.add_child(an)
	an.frame = 0
	await frames(3)
	snap_to("anim-separate-frame0")
	an.frame = 1
	await frames(3)
	snap_to("anim-separate-frame1")
	an.queue_free()
	await frames(2)

	# C4: AnimatedSprite2D using AtlasTexture frames cut from one sheet (what 'add frames from sprite sheet' creates)
	var atlas0 := AtlasTexture.new(); atlas0.atlas = sheet; atlas0.region = Rect2(0, 0, 64, 64)
	var atlas1 := AtlasTexture.new(); atlas1.atlas = sheet; atlas1.region = Rect2(64, 0, 64, 64)
	var sf2 := SpriteFrames.new()
	sf2.add_frame("default", atlas0)
	sf2.add_frame("default", atlas1)
	var an2 := AnimatedSprite2D.new()
	an2.sprite_frames = sf2
	an2.centered = false
	an2.position = Vector2(192, 52)
	an2.scale = Vector2(4, 4)
	an2.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	an2.material = Lib.material("show-uv.gdshader")
	root.add_child(an2)
	an2.frame = 1
	await frames(3)
	im = snap_to("anim-atlas-uv")
	out("C4-atlas-frame-uv", {"uv_at_frame_left_edge_top": px(im, 194, 54), "uv_at_frame_right_edge_bottom": px(im, 445, 305), "uv_at_frame_centre": px(im, 320, 180)})
	an2.material = Lib.material("08-loop.gdshader", {"thickness": 4.0, "line_color": Color(0.25, 0.25, 0.75, 1.0)})
	await frames(3)
	im = snap_to("anim-atlas-outline-t4")
	var line_cols4: Array = []
	for x in range(192, 215):
		var c4 := im.get_pixel(x, 180)
		line_cols4.append(1 if (absf(c4.r - 0.25) < 0.02 and absf(c4.b - 0.75) < 0.02) else 0)
	out("C4b-atlas-outline", {"line_pixels_along_row_y180_from_frame_left": line_cols4})
	quit(0)
