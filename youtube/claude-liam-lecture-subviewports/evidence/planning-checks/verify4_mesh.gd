extends SceneTree
# SubViewports film, check 4: the picture on a mesh, with the film's own shader 08-wobble.gdshader.
#  M2  vertex counts of a QuadMesh: subdivide 0, 1, 7, 15, 31
#  M1  a QuadMesh in a MeshInstance2D lands the picture UPSIDE DOWN; M4: with a negative height it lands upright
#  M3  the same wobble on a plain quad (four corners) and on the 31 x 31 grid: top-edge profile against the formula (TIME read in the same draw)
#  M5  the same wobble on a plain Sprite2D (four corners) only leans it
# Run: godot --path <project> --fixed-fps 30 --script res://verify4_mesh.gd

const STAGE := Common.STAGE
const AMPLITUDE := 16.0
const FREQUENCY := 10.0
const SPEED := 3.0

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per step: a covered window is not drawn on every frame (RESULTS.md, run X)

func main_img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func top_edge(img: Image, x: int) -> int:
	for y in range(20, img.get_height()):
		if Common.diff(img.get_pixel(x, y), STAGE) > 0.05:
			return y
	return -1

func quad(size: Vector2, n: int) -> QuadMesh:
	var q := QuadMesh.new()
	q.size = size
	q.subdivide_width = n
	q.subdivide_depth = n
	return q

func second_differences(ys: Array) -> Array:
	var sd: Array = []
	for i in range(1, ys.size() - 1):
		sd.append(ys[i - 1] - 2 * ys[i] + ys[i + 1])
	return sd

func run() -> void:
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var stage_rect := ColorRect.new()
	stage_rect.color = STAGE
	stage_rect.size = Vector2(1280, 720)
	root.add_child(stage_rect)
	var tprobe := ColorRect.new()
	tprobe.size = Vector2(12, 12)
	tprobe.material = Common.material_from_code(Common.TIME_PROBE_CODE)
	root.add_child(tprobe)
	var sub := SubViewport.new()
	sub.size = Vector2i(512, 512)
	sub.transparent_bg = true
	root.add_child(sub)
	var fill := ColorRect.new()        # opaque white over the whole picture, a red marker at its TOP-left, a blue marker at its BOTTOM-left
	fill.color = Color.WHITE
	fill.size = Vector2(512, 512)
	sub.add_child(fill)
	var red := ColorRect.new()
	red.color = Color(1, 0, 0, 1)
	red.size = Vector2(48, 48)
	sub.add_child(red)
	var blue := ColorRect.new()
	blue.color = Color(0, 0, 1, 1)
	blue.position = Vector2(0, 464)
	blue.size = Vector2(48, 48)
	sub.add_child(blue)

	# ---------------------------------------------------------------- M2
	var counts: Dictionary = {}
	for n: int in [0, 1, 7, 15, 31]:
		counts[str(n)] = (quad(Vector2(512, 512), n).get_mesh_arrays()[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()
	Common.out("M2-vertex-counts", {"subdivide_width_and_depth_to_vertices": counts, "reading": "0 is a plain quad with its four corners; n cuts give (n + 2) x (n + 2) corners, so 31 gives 1,089"})

	# ---------------------------------------------------------------- M6: why the picture lands upside down: the vertex that gets UV (0, 0) (the picture's top-left)
	var layout: Dictionary = {}
	for sz: Vector2 in [Vector2(2, 2), Vector2(2, -2)]:
		var qm := quad(sz, 0)
		var arr := qm.get_mesh_arrays()
		var vv: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		var uu: PackedVector2Array = arr[Mesh.ARRAY_TEX_UV]
		for i in vv.size():
			if uu[i].is_equal_approx(Vector2(0, 0)):
				layout["size (%d, %d)" % [sz.x, sz.y]] = "UV (0, 0), the picture's top-left, sits on the vertex at (%d, %d)" % [vv[i].x, vv[i].y]
	Common.out("M6-quadmesh-layout", {"where_the_pictures_top_left_goes": layout, "reading": "with a positive height the picture's top-left is on the vertex with y = +1 (up in 3D, but DOWN on a 2D screen), so the picture lands upside down; with a negative height it is on y = -1, the top of the screen"})

	# ---------------------------------------------------------------- M1, M4
	var mi := MeshInstance2D.new()
	mi.mesh = quad(Vector2(512, 512), 0)
	mi.texture = sub.get_texture()
	mi.position = Vector2(640, 360)
	root.add_child(mi)
	await frames(4)
	var img := main_img()
	var r1 := {"screen_top_left": Common.rgb(img.get_pixel(640 - 256 + 20, 360 - 256 + 20)), "screen_bottom_left": Common.rgb(img.get_pixel(640 - 256 + 20, 360 + 256 - 20))}
	Common.out("M1-quadmesh-default-size-lands-the-picture-upside-down", {"mesh_size": [512, 512], "result": r1, "reading": "the picture's TOP-left marker is red: red at the screen's top-left would be upright; blue there means the picture is upside down"})
	mi.mesh = quad(Vector2(512, -512), 0)
	await frames(4)
	img = main_img()
	var r4 := {"screen_top_left": Common.rgb(img.get_pixel(640 - 256 + 20, 360 - 256 + 20)), "screen_bottom_left": Common.rgb(img.get_pixel(640 - 256 + 20, 360 + 256 - 20))}
	Common.out("M4-negative-height-lands-it-upright", {"mesh_size": [512, -512], "result": r4, "reading": "red at the top-left: upright"})
	mi.queue_free()
	await frames(2)

	# ---------------------------------------------------------------- M3: plain quad and grid under the wobble
	var xs := [10, 60, 110, 160, 210, 260, 310, 360, 410, 460, 500]
	for n: int in [0, 31]:
		var m := MeshInstance2D.new()
		m.mesh = quad(Vector2(512, -512), n)
		m.texture = sub.get_texture()
		m.position = Vector2(640, 360)
		m.material = Common.material_from_file("08-wobble.gdshader")
		m.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(m)
		await frames(6)
		img = main_img()
		var T := Common.time_of(img)
		var ys: Array = []
		var exp: Array = []
		for dx: int in xs:
			ys.append(top_edge(img, 640 - 256 + dx))
			var u := (dx + 0.5) / 512.0
			exp.append(snappedf(104.0 + sin(u * FREQUENCY + T * SPEED) * AMPLITUDE, 0.1))
		var rms := 0.0
		if n == 31:
			for i in xs.size():
				rms += pow(float(ys[i]) - float(exp[i]), 2.0)
			rms = sqrt(rms / xs.size())
		Common.out("M3-top-edge-subdivide-%d" % n, {"subdivide": n, "TIME_read": snappedf(T, 0.001), "x_offsets": xs, "top_edge_y_measured": ys, "top_edge_y_by_formula": exp if n == 31 else "n/a (a plain quad has only the four corners)", "second_differences": second_differences(ys), "span_px": (ys.max() - ys.min()), "rms_error_px_against_the_formula": snappedf(rms, 0.01) if n == 31 else "n/a",
			"reading": "plain quad: second differences are 0 or 1 (a straight edge, at most a lean). grid: the edge follows 104 + sin(UV.x * 10 + TIME * 3) * 16 to within a pixel or two, a span near twice the amplitude"})
		m.queue_free()
		await frames(2)

	# ---------------------------------------------------------------- M5: Sprite2D under the same shader
	var spr := Sprite2D.new()
	spr.texture = sub.get_texture()
	spr.position = Vector2(640, 360)
	spr.material = Common.material_from_file("08-wobble.gdshader")
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(spr)
	await frames(6)
	img = main_img()
	var ys5: Array = []
	for dx: int in xs:
		ys5.append(top_edge(img, 640 - 256 + dx))
	Common.out("M5-sprite2d-has-four-corners", {"top_edge_y_measured": ys5, "second_differences": second_differences(ys5), "reading": "a plain Sprite2D under the wobble: a straight (leaning) edge; only its four corners move"})
	quit(0)
