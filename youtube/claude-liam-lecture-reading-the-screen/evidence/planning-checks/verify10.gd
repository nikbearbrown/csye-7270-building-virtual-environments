extends SceneTree
# verify10: does the CAPTURE ROUTE change what a shader shows?  Three routes are compared:
#   root        the scene in a plain 1280 x 720 window (what a small game window shows; the route of verify1 to verify8 and of frames/)
#   sub4k       a 3840 x 2160 SubViewport over a 1280 x 720 canvas (size_2d_override): the route the first plan used for every capture
#   native1080  a 1920 x 1080 SubViewport at scale 1, the scene built for a 1920 x 1080 canvas: the route the series now asks for shaders that read pixels
# A shader that works in fractions (SCREEN_UV, a ratio of SCREEN_PIXEL_SIZE) must look the same in all three; a shader that counts texels (a mip-level blur,
# textureLod on a screen texture with mipmaps) cannot, because the screen texture has as many texels as the SubViewport has pixels.
# Part A: the blur window of C13 at levels 0, 4.0, 4.5 and 5.0 in each route: how far a level-N picture differs from the sharp one (mean over the window's
#         inside, all three channels, 0 to 1) and the largest step between neighbouring pixels.
# Part B: the spotlight scenes (C06, C07, C08) in root and sub4k: lit width and height in CANVAS pixels (image pixels x 1280 / image width) and the
#         lit centroid against the player's place on the screen.
# Run: ./run-checks.sh verify10 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")

var holder: Node
var sub: SubViewport = null

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

# route: "root", "sub4k" or "native1080"
func load_scene(route: String, path: String, duration: float) -> Node2D:
	if holder != null:
		holder.queue_free()
		holder = null
		sub = null
		await frames(2)
	var sc: Node2D = (load(path) as GDScript).new()
	sc.set("auto", false)
	sc.set("duration", duration)
	if route == "root":
		holder = Node2D.new()
		root.add_child(holder)
		holder.add_child(sc)
	else:
		sub = SubViewport.new()
		if route == "sub4k":
			sub.size = Vector2i(3840, 2160)
			sub.size_2d_override = Vector2i(1280, 720)
			sub.size_2d_override_stretch = true
		else:
			sub.size = Vector2i(1920, 1080)
			sc.set("canvas_size", Vector2(1920, 1080))
		sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sub)
		sub.add_child(sc)
		holder = sub
	await frames(3)
	return sc

func shot() -> Image:
	await frames(3)
	RenderingServer.force_draw(false)
	if sub != null:
		return sub.get_texture().get_image()
	return root.get_texture().get_image()

func region_mean_diff(a: Image, b: Image, r: Rect2) -> float:
	var w := a.get_width()
	var h := a.get_height()
	var x0 := int(r.position.x * w)
	var x1 := int((r.position.x + r.size.x) * w)
	var y0 := int(r.position.y * h)
	var y1 := int((r.position.y + r.size.y) * h)
	var step := maxi(1, int(round(w / 1280.0)))
	var tot := 0.0
	var n := 0
	for y in range(y0, y1, step):
		for x in range(x0, x1, step):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			tot += (absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b)) / 3.0
			n += 1
	return tot / float(maxi(n, 1))

func region_largest_step(a: Image, r: Rect2) -> float:
	var w := a.get_width()
	var h := a.get_height()
	var x0 := int(r.position.x * w)
	var x1 := int((r.position.x + r.size.x) * w)
	var y0 := int(r.position.y * h)
	var y1 := int((r.position.y + r.size.y) * h)
	var best := 0.0
	var ystep := maxi(1, int(round(w / 1280.0)) * 2)
	for y in range(y0, y1, ystep):
		var prev := a.get_pixel(x0, y)
		for x in range(x0 + 1, x1):
			var c := a.get_pixel(x, y)
			best = maxf(best, maxf(absf(c.r - prev.r), maxf(absf(c.g - prev.g), absf(c.b - prev.b))))
			prev = c
	return best

func is_gray(c: Color) -> bool:
	return maxf(absf(c.r - c.g), maxf(absf(c.g - c.b), absf(c.r - c.b))) < 0.012

# lit (non-gray) extent in CANVAS pixels, and the centroid in canvas pixels
func lit_stats(im: Image) -> Dictionary:
	var w := im.get_width()
	var h := im.get_height()
	var k := 1280.0 / float(w)
	var stride := maxi(1, int(round(w / 1280.0)) * 3)
	var minx := 99999
	var maxx := -1
	var miny := 99999
	var maxy := -1
	var sx := 0.0
	var sy := 0.0
	var n := 0
	for y in range(0, h, stride):
		for x in range(0, w, stride):
			if not is_gray(im.get_pixel(x, y)):
				minx = mini(minx, x)
				maxx = maxi(maxx, x)
				miny = mini(miny, y)
				maxy = maxi(maxy, y)
				sx += x
				sy += y
				n += 1
	return {"width_canvas_px": snappedf((maxx - minx) * k, 1.0), "height_canvas_px": snappedf((maxy - miny) * k, 1.0), "centroid_canvas_px": [snappedf(sx / n * k, 1.0), snappedf(sy / n * k, 1.0)]}

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	var inner := Rect2(0.2224, 0.1624, 0.5152, 0.5152)    # inside the 0.56 x 0.56 window at (0.20, 0.14), clear of its frame
	# ---- Part A: the blur ----
	for route: String in ["root", "sub4k", "native1080"]:
		var sc := await load_scene(route, "res://scene_c13_blur.gd", 11.6)
		var w: ColorRect = sc.get("w")
		var sharp: Image
		var rows: Array = []
		for level: float in [0.0, 4.0, 4.5, 5.0]:
			sc.call("set_time", 0.30 * 11.6)    # the scene's own blur is 0 here; the level is then set by hand
			(w.material as ShaderMaterial).set_shader_parameter("blur", level)
			var im := await shot()
			if level == 0.0:
				sharp = im
			rows.append({"level": level, "mean_difference_from_sharp": snappedf(region_mean_diff(im, sharp, inner), 0.0001), "largest_step_between_neighbour_pixels": snappedf(region_largest_step(im, inner), 0.0001)})
		L.out("A-blur-" + route, {"route": route, "image_px": [sharp.get_width(), sharp.get_height()], "rows": rows})
	# ---- Part B: the spotlight ----
	for route: String in ["root", "sub4k"]:
		var sc := await load_scene(route, "res://scene_c06_spot_oval.gd", 14.0)
		sc.call("set_time", 0.50 * 14.0)
		var im := await shot()
		L.out("B-C06-oval-" + route, {"route": route, "u": 0.5, "lit": lit_stats(im)})
		sc = await load_scene(route, "res://scene_c07_spot_swap.gd", 10.0)
		var rows7: Array = []
		for u: float in [0.50, 0.85]:
			sc.call("set_time", u * 10.0)
			im = await shot()
			rows7.append({"u": u, "lit": lit_stats(im)})
		L.out("B-C07-swap-" + route, {"route": route, "rows": rows7})
		sc = await load_scene(route, "res://scene_c08_spot_game.gd", 14.0)
		var u8 := 0.20
		sc.call("set_time", u8 * 14.0)
		im = await shot()
		var ang := TAU * u8 + PI
		L.out("B-C08-game-" + route, {"route": route, "u": u8, "player_canvas_px": [snappedf(1280.0 * (0.50 + 0.20 * cos(ang)), 1.0), snappedf(720.0 * (0.50 + 0.12 * sin(ang)), 1.0)], "lit": lit_stats(im)})
	quit(0)
