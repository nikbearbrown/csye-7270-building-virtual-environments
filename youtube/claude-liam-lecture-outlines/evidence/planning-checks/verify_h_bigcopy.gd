extends SceneTree
# H: the "bigger copy behind the sprite" outline. A plus-shaped sprite, a copy of it scaled up by a fifth about its centre, tinted and drawn behind.
# How thick is the border at the tip of an arm compared with the side of an arm?  (arms: half-length 24, half-width 8 image pixels)
# Run: godot --path <scratch project> --script res://verify_h_bigcopy.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func plus() -> Image:
	var img := Image.create_empty(64, 64, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in range(24, 40):
		for x in range(8, 56):
			img.set_pixel(x, y, Lib.TEAL)
	for y in range(8, 56):
		for x in range(24, 40):
			img.set_pixel(x, y, Lib.TEAL)
	return img

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--out": OUT = a[i + 1]
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = Vector2i(640, 360)
	var tex := ImageTexture.create_from_image(plus())
	var back := Sprite2D.new()
	back.texture = tex
	back.position = Vector2(320, 180)
	back.scale = Vector2(2.4, 2.4)                      # 2.0 x 1.2
	back.modulate = Color(0.25, 0.25, 0.75)
	back.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(back)
	var front := Sprite2D.new()
	front.texture = tex
	front.position = Vector2(320, 180)
	front.scale = Vector2(2.0, 2.0)
	front.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(front)
	await frames(3)
	Lib.save(Lib.snap(root), OUT + "/bigcopy-plus.png")
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	quit(0)
