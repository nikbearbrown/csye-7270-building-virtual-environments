extends SceneTree
# O: does the ring with its sixteen directions written as constants (shaders/ring-const.gdshader, used for the cost timing) draw the same picture as the film's
# ring (lab-shaders/10-ring.gdshader, sine and cosine per read)?  Disc and thin-stem sprites, thickness 1, 2, 3, 4 and 8, scale 1, nearest filter.
# analyze_ringconst.py counts the pixels that differ.
# Run: godot --path <scratch project> --script res://verify_o_ringconst.gd -- --out <png dir>
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
	var stem := ImageTexture.create_from_image(Lib.mascot(128))
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	for kind in [["disc", disc], ["stem", stem]]:
		for t in [1, 2, 3, 4, 8]:
			await shoot(kind[1], "10-ring.gdshader", {"thickness": float(t), "line_color": line}, "ringconst-%s-sincos-t%d" % [kind[0], t])
			await shoot(kind[1], "ring-const.gdshader", {"thickness": float(t), "line_color": line}, "ringconst-%s-const-t%d" % [kind[0], t])
	quit(0)
