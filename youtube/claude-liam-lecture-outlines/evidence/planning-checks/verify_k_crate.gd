extends SceneTree
# K: corners. A square sprite outlined with four reads (06-pixel-steps) and eight reads (07-eight-reads) at thickness 1 to 4.
# analyze_crate.py counts the pixels the eight-read line has that the four-read line lacks (the corner squares).
# Run: godot --path <scratch project> --script res://verify_k_crate.gd -- --out <png dir>
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
	var tex := ImageTexture.create_from_image(Lib.crate(128))
	var line := Color(0.25, 0.25, 0.75, 1.0)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "crate_rect": str(Lib.opaque_rect(Lib.crate(128)))})
	for t in [1.0, 2.0, 3.0, 4.0]:
		var ti := int(t)
		await shoot(tex, "06-pixel-steps.gdshader", {"thickness": t, "line_color": line}, "crate-4-t%d" % ti)
		await shoot(tex, "07-eight-reads.gdshader", {"thickness": t, "line_color": line}, "crate-8-t%d" % ti)
	quit(0)
