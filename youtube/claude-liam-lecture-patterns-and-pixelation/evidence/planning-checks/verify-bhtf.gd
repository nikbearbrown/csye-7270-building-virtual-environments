extends SceneTree
# Does the "Your turn" prompt of the film (a grid of round dots from a Sprite2D's texture; cells = dots along the SHORTER side; the
# dot takes the texture's colour at the middle of its cell; round even on a wide texture) have an answer that passes both checks,
# and do the two plausible wrong answers fail the check that is meant to catch them?
#   reference  (reference-shaders/bhtf-reference.gdshader)  floor + 0.5 lookup, cells counted along the shorter side
#   rounded    (reference-shaders/bhtf-rounded.gdshader)    cell number rounded: dots centred on grid lines -> edge dots cut in half
#   no-aspect  (reference-shaders/bhtf-no-aspect.gdshader)  same count both ways -> ovals on a wide texture
# Textures: square 128x128, wide 256x128 (2:1), and 200x128 (not a whole ratio: the far edge cannot hold whole cells, a limit
# of any answer, noted in FACTCHECK).
# Method: render at scale 1.0 (one picture pixel = one screen pixel), label the connected blobs of non-stage pixels (each whole dot
# is one blob; a dot cut by the picture's edge is a smaller blob), and report the blob count, their areas and their shapes.
# Run: godot --path <scratch project that contains reference-shaders/ and this file> --script res://verify-bhtf.gd

const STAGE := Color("#D9D5CA")

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func make_tex(w: int, h: int) -> ImageTexture:
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	for y in h:
		for x in w:
			img.set_pixel(x, y, Color(0.37 + 0.55 * x / float(w - 1), 0.64 - 0.15 * y / float(h - 1), 0.57, 1.0))
	return ImageTexture.create_from_image(img)

func render(tex: ImageTexture, shader_file: String, cells: float) -> Image:
	for c in root.get_children():
		c.queue_free()
	await frames(2)
	var sp := Sprite2D.new()
	sp.texture = tex
	sp.position = Vector2(320, 180)
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string("res://reference-shaders/" + shader_file)
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("cells", cells)
	sp.material = mat
	root.add_child(sp)
	await frames(3)
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func is_stage(c: Color) -> bool:
	return absf(c.r - STAGE.r) + absf(c.g - STAGE.g) + absf(c.b - STAGE.b) < 0.03

# connected blobs (4-neighbour) of non-stage pixels: returns an Array of [area, width, height]
func blobs(img: Image) -> Array:
	var w := img.get_width()
	var h := img.get_height()
	var seen := PackedByteArray()
	seen.resize(w * h)
	var found: Array = []
	for y0 in h:
		for x0 in w:
			if seen[y0 * w + x0] == 1 or is_stage(img.get_pixel(x0, y0)):
				continue
			var stack: Array[Vector2i] = [Vector2i(x0, y0)]
			seen[y0 * w + x0] = 1
			var area := 0
			var minx := x0
			var maxx := x0
			var miny := y0
			var maxy := y0
			while stack.size() > 0:
				var p: Vector2i = stack.pop_back()
				area += 1
				minx = mini(minx, p.x)
				maxx = maxi(maxx, p.x)
				miny = mini(miny, p.y)
				maxy = maxi(maxy, p.y)
				for d: Vector2i in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
					var q := p + d
					if q.x < 0 or q.y < 0 or q.x >= w or q.y >= h:
						continue
					if seen[q.y * w + q.x] == 1 or is_stage(img.get_pixel(q.x, q.y)):
						continue
					seen[q.y * w + q.x] = 1
					stack.append(q)
			found.append([area, maxx - minx + 1, maxy - miny + 1])
	return found

func summarize(found: Array) -> Dictionary:
	var areas: Array = []
	for b in found:
		areas.append(b[0])
	areas.sort()
	var median: int = areas[areas.size() / 2]
	var cut := 0
	var worst_ratio := 1.0
	for b in found:
		if b[0] < 0.8 * median:
			cut += 1
		elif b[2] > 0:
			worst_ratio = maxf(worst_ratio, maxf(float(b[1]) / b[2], float(b[2]) / b[1]))
	return {"blobs": found.size(), "area_min": areas[0], "area_median": median, "area_max": areas[areas.size() - 1],
		"blobs_smaller_than_80pct_of_median": cut, "worst_width_to_height_of_whole_dots": snappedf(worst_ratio, 0.01)}

func run() -> void:
	RenderingServer.set_default_clear_color(STAGE)
	root.size = Vector2i(640, 360)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name()})
	var variants: Array[String] = ["bhtf-reference.gdshader", "bhtf-rounded.gdshader", "bhtf-no-aspect.gdshader"]
	var textures: Array[Vector2i] = [Vector2i(128, 128), Vector2i(256, 128), Vector2i(200, 128)]
	for t: Vector2i in textures:
		var tex := make_tex(t.x, t.y)
		for v: String in variants:
			var img := await render(tex, v, 8.0)
			var s := summarize(blobs(img))
			s["texture"] = [t.x, t.y]
			s["cells_param"] = 8
			out("%dx%d-%s" % [t.x, t.y, v.replace(".gdshader", "")], s)
			DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://bhtf-out"))
			img.save_png(ProjectSettings.globalize_path("res://bhtf-out/%dx%d-%s.png" % [t.x, t.y, v.replace(".gdshader", "")]))
	quit(0)
