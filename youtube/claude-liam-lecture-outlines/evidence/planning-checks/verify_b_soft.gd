extends SceneTree
# B: antialiased (half-transparent) rim. What alpha does the outline shader really write at the seam, and does thickness 0 leave the sprite alone?
# Each scene is rendered on black, white and the stage colour so the shader's own alpha can be solved from the screen:  alpha = 1 - (white - black) / 255.
# Run: godot --path <scratch project> --script res://verify_b_soft.gd -- --out <png dir>
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
	var soft := ImageTexture.create_from_image(Lib.blob_soft(128))
	var hard := ImageTexture.create_from_image(Lib.blob(128))
	var line := Color(0.25, 0.25, 0.75, 1.0)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	await shoot(soft, "", {}, "soft-plain")
	await shoot(soft, "06-pixel-steps.gdshader", {"thickness": 1.0, "line_color": line}, "soft-four-t1")      # classic mix, four reads
	await shoot(soft, "06-pixel-steps.gdshader", {"thickness": 0.0, "line_color": line}, "soft-four-t0")
	await shoot(soft, "08-loop.gdshader", {"thickness": 1.0, "line_color": line}, "soft-loop-t1")
	await shoot(soft, "08-loop.gdshader", {"thickness": 0.0, "line_color": line}, "soft-loop-t0")
	await shoot(soft, "11-soft-edges.gdshader", {"thickness": 1.0, "line_color": line}, "soft-fix-t1")
	await shoot(soft, "11-soft-edges.gdshader", {"thickness": 0.0, "line_color": line}, "soft-fix-t0")
	await shoot(soft, "09-guard.gdshader", {"thickness": 0.0, "line_color": line}, "soft-guard-t0")
	await shoot(soft, "09-guard.gdshader", {"thickness": 1.0, "line_color": line}, "soft-guard-t1")
	await shoot(hard, "", {}, "hard-plain")
	await shoot(hard, "08-loop.gdshader", {"thickness": 0.0, "line_color": line}, "hard-loop-t0")
	quit(0)
