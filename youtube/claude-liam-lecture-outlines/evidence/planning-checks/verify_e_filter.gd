extends SceneTree
# E: texture filtering. The outline reads the texture's alpha at offsets; with nearest filtering each read is one image pixel, with linear filtering it is
# a blend of the four nearest. Same sprite, same shader (lab-shaders/08-loop.gdshader), thickness 1, drawn at 4x (a whole number) and 2.25x (not a whole number),
# each on black and white (to solve the alpha) with the filter set on the node.
# Run: godot --path <scratch project> --script res://verify_e_filter.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func shoot(tex: Texture2D, filter: int, scale: float, name: String, thickness: float) -> void:
	var sp := Sprite2D.new()
	sp.texture = tex
	sp.centered = true
	sp.position = Vector2(320, 180)
	sp.scale = Vector2(scale, scale)
	sp.texture_filter = filter
	sp.material = Lib.material("08-loop.gdshader", {"thickness": thickness, "line_color": Color(0.25, 0.25, 0.75, 1.0)})
	root.add_child(sp)
	for bg in [["black", Color(0, 0, 0)], ["white", Color(1, 1, 1)], ["stage", Lib.STAGE]]:
		RenderingServer.set_default_clear_color(bg[1])
		await frames(3)
		Lib.save(Lib.snap(root), OUT + "/" + name + "-on-" + bg[0] + ".png")
	sp.queue_free()
	await frames(1)

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--out": OUT = a[i + 1]
	root.size = Vector2i(640, 360)
	var tex := ImageTexture.create_from_image(Lib.blob(128))
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	await shoot(tex, CanvasItem.TEXTURE_FILTER_PARENT_NODE, 2.0, "filter-default-x2-t1", 1.0)   # no filter set anywhere: the project default (this scratch project changes nothing)
	await shoot(tex, CanvasItem.TEXTURE_FILTER_NEAREST, 2.0, "filter-nearest-x2-t1", 1.0)
	await shoot(tex, CanvasItem.TEXTURE_FILTER_LINEAR, 2.0, "filter-linear-x2-t1", 1.0)
	await shoot(tex, CanvasItem.TEXTURE_FILTER_NEAREST, 2.25, "filter-nearest-x2.25-t1", 1.0)
	await shoot(tex, CanvasItem.TEXTURE_FILTER_LINEAR, 2.25, "filter-linear-x2.25-t1", 1.0)
	await shoot(tex, CanvasItem.TEXTURE_FILTER_NEAREST, 2.25, "filter-nearest-x2.25-t0", 0.0)
	await shoot(tex, CanvasItem.TEXTURE_FILTER_LINEAR, 2.25, "filter-linear-x2.25-t0", 0.0)
	quit(0)
