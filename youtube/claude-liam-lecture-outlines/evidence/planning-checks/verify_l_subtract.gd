extends SceneTree
# L: the subtraction form against the product form. (a) one read with the subtraction form: what happens to the sprite's own pixels on its far side;
# (b) four reads, subtraction against the film's product, on the disc plus one isolated opaque pixel (a speck).
# Run: godot --path <scratch project> --script res://verify_l_subtract.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func shoot(tex: Texture2D, shader: String, params: Dictionary, name: String) -> void:
	var sp := Sprite2D.new()
	sp.texture = tex
	sp.centered = false
	sp.position = Vector2(256, 116)
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp.material = Lib.material(shader, params)
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
	var line := Color(0.25, 0.25, 0.75, 1.0)
	var disc := ImageTexture.create_from_image(Lib.blob(128))
	var speck := ImageTexture.create_from_image(Lib.blob_speck(128))
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	await shoot(disc, "subtract-one.gdshader", {"line_color": line}, "subtract-one")
	await shoot(speck, "subtract-four.gdshader", {"thickness": 1.0, "line_color": line}, "speck-subtract-four")
	await shoot(speck, "06-pixel-steps.gdshader", {"thickness": 1.0, "line_color": line}, "speck-product-four")
	quit(0)
