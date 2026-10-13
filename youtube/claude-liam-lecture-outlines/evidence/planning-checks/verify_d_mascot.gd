extends SceneTree
# D: thin parts. A sprite with a three-pixel antenna and a small ball on top, outlined with 4 reads, 8 reads, a ring of 16 and a ring of 32,
# at thickness 2, 4 and 8. The PNGs are measured against the true outline (every empty pixel within that distance of a solid one) by analyze_mascot.py.
# Run: godot --path <scratch project> --script res://verify_d_mascot.gd -- --out <png dir>
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
	if shader != "":
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
	var m := Lib.mascot(128)
	Lib.save(m, OUT + "/mascot-texture.png")          # the raw texture, for the analysis' ideal outline
	var tex := ImageTexture.create_from_image(m)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "opaque_rect": str(Lib.opaque_rect(m))})
	await shoot(tex, "", {}, "mascot-plain")
	for t in [2.0, 4.0, 6.0, 8.0]:
		var ti := int(t)
		await shoot(tex, "06-pixel-steps.gdshader", {"thickness": t, "line_color": line}, "mascot-4-t%d" % ti)
		await shoot(tex, "07-eight-reads.gdshader", {"thickness": t, "line_color": line}, "mascot-8-t%d" % ti)
		await shoot(tex, "10-ring.gdshader", {"thickness": t, "line_color": line}, "mascot-16-t%d" % ti)
		await shoot(tex, "ring-n.gdshader", {"thickness": t, "line_color": line, "samples": 32}, "mascot-32-t%d" % ti)
		await shoot(tex, "ring-n.gdshader", {"thickness": t, "line_color": line, "samples": 64}, "mascot-64-t%d" % ti)
	quit(0)
