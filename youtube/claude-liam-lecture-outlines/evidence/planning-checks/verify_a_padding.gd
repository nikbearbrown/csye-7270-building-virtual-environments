extends SceneTree
# A: the padding trap. A sprite trimmed to its opaque bounding box leaves the outline no pixels to live on; padding fixes it.
# Uses the film's final shader (lab-shaders/08-loop.gdshader) at thickness 4 and the exact add_padding() text shown on screen (padding_snippet.gd).
# Run: godot --path <scratch project with ol_lib.gd, padding_snippet.gd and the shader copied in> --script res://verify_a_padding.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func render(tex: Texture2D, params: Dictionary, name: String, centered := true) -> void:
	var sp := Sprite2D.new()
	sp.texture = tex
	sp.centered = false     # integer top-left so every texel lands on one screen pixel (an odd-sized image centred on a pixel corner would straddle pixels)
	sp.position = Vector2(int(320 - tex.get_width() / 2.0), int(180 - tex.get_height() / 2.0))
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp.material = Lib.material("08-loop.gdshader", params)
	root.add_child(sp)
	await frames(3)
	Lib.save(Lib.snap(root), OUT + "/" + name + ".png")
	sp.queue_free()
	await frames(1)

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--out": OUT = a[i + 1]
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = Vector2i(640, 360)
	var pad = load("res://padding_snippet.gd").new()
	var line := Color(0.25, 0.25, 0.75, 1.0)

	var full := Lib.blob(128)
	var tight_img := Lib.crop_to_content(full)
	var tight := ImageTexture.create_from_image(tight_img)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"full_size": [full.get_width(), full.get_height()], "tight_size": [tight_img.get_width(), tight_img.get_height()],
		"opaque_rect_in_full": str(Lib.opaque_rect(full))})

	# does create_empty() start transparent? (so is fill() needed? kept for clarity, not claimed)
	var e := Image.create_empty(4, 4, false, Image.FORMAT_RGBA8)
	out("create_empty_pixel", {"rgba": [e.get_pixel(0, 0).r, e.get_pixel(0, 0).g, e.get_pixel(0, 0).b, e.get_pixel(0, 0).a]})

	await render(tight, {"thickness": 4.0, "line_color": line}, "pad-tight-t4")
	var p4: ImageTexture = pad.add_padding(tight, 4)
	out("padded4", {"size": [p4.get_width(), p4.get_height()]})
	await render(p4, {"thickness": 4.0, "line_color": line}, "pad-padded4-t4")
	var p2: ImageTexture = pad.add_padding(tight, 2)
	await render(p2, {"thickness": 4.0, "line_color": line}, "pad-padded2-t4")
	var p6: ImageTexture = pad.add_padding(tight, 6)
	await render(p6, {"thickness": 4.0, "line_color": line}, "pad-padded6-t4")
	# the original art with its generous padding, for reference
	await render(ImageTexture.create_from_image(full), {"thickness": 4.0, "line_color": line}, "pad-original-t4")
	# slide (look-right shader) clipped by the rectangle: the picture cannot leave its own rectangle
	var sp := Sprite2D.new()
	sp.texture = ImageTexture.create_from_image(full)
	sp.centered = false
	sp.position = Vector2(256, 116)
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp.material = Lib.material("01-look-right.gdshader", {"look": 0.25})
	root.add_child(sp)
	await frames(3)
	Lib.save(Lib.snap(root), OUT + "/pad-slide-clipped-look0.25.png")
	sp.queue_free()
	await frames(1)

	# a non-centered Sprite2D moves when padding is added (its top-left corner is the origin): check by how much
	var s1 := Sprite2D.new(); s1.texture = tight; s1.centered = false; s1.position = Vector2(100, 100)
	var s2 := Sprite2D.new(); s2.texture = p4; s2.centered = false; s2.position = Vector2(100, 100)
	s1.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST; s2.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(s1)
	await frames(3)
	var i1 := Lib.snap(root)
	s1.queue_free()
	root.add_child(s2)
	await frames(3)
	var i2 := Lib.snap(root)
	var r1 := _first_solid(i1); var r2 := _first_solid(i2)
	out("non_centered_shift", {"first_solid_pixel_unpadded": r1, "first_solid_pixel_padded4": r2, "note": "the picture moves by the padding when the node is not centered"})
	quit(0)

func _first_solid(img: Image) -> Array:
	for y in img.get_height():
		for x in img.get_width():
			var c := img.get_pixel(x, y)
			if c.is_equal_approx(Lib.TEAL):
				return [x, y]
	return [-1, -1]
